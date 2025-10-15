from datetime import datetime, time, timedelta

from django.core.management.base import BaseCommand
from django.db.models import Count
from django.utils import timezone

from competition.models import Submission, User, Vote


class Command(BaseCommand):
    help = 'Aggregate weekly AI vs Human competition results and allocate points.'

    CREATOR_BONUS = 100
    GUESSER_BONUS = 10
    TEAM_BONUS = 50

    def handle(self, *args, **options):
        now = timezone.now()
        period_end = self._last_friday_midnight(now)
        period_start = period_end - timedelta(days=7)

        self.stdout.write(self.style.NOTICE(f'Computing results for {period_start} to {period_end}'))

        weekly_submissions = Submission.objects.filter(created_at__gte=period_start, created_at__lt=period_end)
        weekly_votes = Vote.objects.filter(created_at__gte=period_start, created_at__lt=period_end).select_related('voter', 'submission')

        if not weekly_submissions.exists():
            self.stdout.write(self.style.WARNING('No submissions found for the target week.'))
            return

        category_winners = []
        for category_value, _ in Submission.CATEGORY_CHOICES:
            top_submission = (
                weekly_submissions.filter(category=category_value)
                .annotate(vote_total=Count('votes'))
                .order_by('-vote_total', '-created_at')
                .first()
            )
            if top_submission:
                category_winners.append(top_submission)
                top_submission.author.points += self.CREATOR_BONUS
                top_submission.author.save(update_fields=['points'])

        # Award correct guessers.
        correct_votes = [vote for vote in weekly_votes if vote.guess == vote.submission.true_identity]
        for vote in correct_votes:
            vote.voter.points += self.GUESSER_BONUS
            vote.voter.save(update_fields=['points'])

        # Compute team accuracy.
        team_results = {}
        for team in [User.TEAM_AI, User.TEAM_HUMAN]:
            team_votes = [vote for vote in weekly_votes if vote.voter.team == team]
            if team_votes:
                accurate = sum(1 for vote in team_votes if vote.guess == vote.submission.true_identity)
                team_results[team] = accurate / len(team_votes)
            else:
                team_results[team] = 0

        # Determine overall winning submission for the week.
        top_submission = (
            weekly_submissions.annotate(vote_total=Count('votes'))
            .order_by('-vote_total', '-created_at')
            .first()
        )

        winning_team = None
        if top_submission:
            winning_team = top_submission.true_identity

        # Determine prediction winner team.
        prediction_winner = None
        if team_results[User.TEAM_AI] > team_results[User.TEAM_HUMAN]:
            prediction_winner = User.TEAM_AI
        elif team_results[User.TEAM_HUMAN] > team_results[User.TEAM_AI]:
            prediction_winner = User.TEAM_HUMAN

        # Award team bonus to weekly winning team based on combined metrics.
        team_scores = {team: team_results[team] for team in team_results}
        if winning_team:
            team_scores[winning_team] += 1
        winning_side = max(team_scores, key=team_scores.get)

        winning_members = User.objects.filter(team=winning_side)
        for member in winning_members:
            member.points += self.TEAM_BONUS
            member.save(update_fields=['points'])

        # Output summary.
        self.stdout.write(self.style.SUCCESS('Weekly results computed successfully.'))
        self.stdout.write(f'Category winners: {[submission.title for submission in category_winners]}')
        self.stdout.write(f'Prediction accuracy: {team_results}')
        self.stdout.write(f'Result winning team: {winning_team}')
        self.stdout.write(f'Overall victorious team: {winning_side}')

    def _last_friday_midnight(self, dt):
        dt_utc = dt.astimezone(timezone.utc)
        weekday = dt_utc.weekday()
        days_since_friday = (weekday - 4) % 7
        last_friday_date = dt_utc.date() - timedelta(days=days_since_friday)
        return timezone.make_aware(datetime.combine(last_friday_date, time.min), timezone.utc)
