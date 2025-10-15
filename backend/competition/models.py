from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    TEAM_AI = 'AI'
    TEAM_HUMAN = 'HUMAN'
    TEAM_CHOICES = [
        (TEAM_AI, 'Team AI'),
        (TEAM_HUMAN, 'Team Human'),
    ]

    team = models.CharField(max_length=5, choices=TEAM_CHOICES)
    points = models.IntegerField(default=0)


class Submission(models.Model):
    CATEGORY_IMAGE = 'IMAGE'
    CATEGORY_NOVEL = 'NOVEL'
    CATEGORY_POETRY = 'POETRY'
    CATEGORY_VIDEO = 'VIDEO'
    CATEGORY_MUSIC = 'MUSIC'

    CATEGORY_CHOICES = [
        (CATEGORY_IMAGE, 'Image'),
        (CATEGORY_NOVEL, 'Novel'),
        (CATEGORY_POETRY, 'Poetry'),
        (CATEGORY_VIDEO, 'Video'),
        (CATEGORY_MUSIC, 'Music'),
    ]

    IDENTITY_AI = User.TEAM_AI
    IDENTITY_HUMAN = User.TEAM_HUMAN

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    content_text = models.TextField(blank=True)
    content_file = models.FileField(upload_to='submissions/', blank=True, null=True)
    true_identity = models.CharField(max_length=5, choices=[(IDENTITY_AI, 'AI'), (IDENTITY_HUMAN, 'Human')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class Vote(models.Model):
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='votes')
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='votes')
    guess = models.CharField(max_length=5, choices=[(Submission.IDENTITY_AI, 'AI'), (Submission.IDENTITY_HUMAN, 'Human')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter', 'submission')
        ordering = ['-created_at']
