from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.db.models import Count
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Submission, Vote
from .serializers import (
    RegisterSerializer,
    SubmissionCreateSerializer,
    SubmissionSerializer,
    UserSerializer,
    VoteSerializer,
)

User = get_user_model()


class PingView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return Response({'ok': True})


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': UserSerializer(user).data})


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class SubmissionListCreateView(generics.ListCreateAPIView):
    queryset = Submission.objects.all().annotate(votes_count=Count('votes'))
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubmissionCreateSerializer
        return SubmissionSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def list(self, request, *args, **kwargs):
        self.serializer_class = SubmissionSerializer
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SubmissionDetailView(generics.RetrieveAPIView):
    queryset = Submission.objects.all().annotate(votes_count=Count('votes'))
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class VoteCreateView(APIView):
    def post(self, request, pk, *args, **kwargs):
        submission = generics.get_object_or_404(Submission, pk=pk)
        serializer = VoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vote, created = Vote.objects.get_or_create(
            voter=request.user,
            submission=submission,
            defaults={'guess': serializer.validated_data['guess']},
        )
        if not created:
            return Response({'detail': 'You have already voted on this submission.'}, status=status.HTTP_400_BAD_REQUEST)
        vote_serializer = VoteSerializer(vote, context={'request': request})
        return Response(vote_serializer.data, status=status.HTTP_201_CREATED)


class WeeklySummaryView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        current_time = timezone.now()
        start_of_week = (current_time - timedelta(days=current_time.weekday())).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        submissions = Submission.objects.filter(created_at__gte=start_of_week).annotate(votes_count=Count('votes'))
        ai_votes = Vote.objects.filter(
            created_at__gte=start_of_week,
            guess=Submission.IDENTITY_AI,
            submission__true_identity=Submission.IDENTITY_AI,
        ).count()
        human_votes = Vote.objects.filter(
            created_at__gte=start_of_week,
            guess=Submission.IDENTITY_HUMAN,
            submission__true_identity=Submission.IDENTITY_HUMAN,
        ).count()
        return Response({
            'current_week_start': start_of_week,
            'submissions': SubmissionSerializer(submissions, many=True, context={'request': request}).data,
            'accurate_ai_guesses': ai_votes,
            'accurate_human_guesses': human_votes,
        })
