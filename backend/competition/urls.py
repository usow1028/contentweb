from django.urls import path

from .views import (
    LoginView,
    LogoutView,
    MeView,
    PingView,
    RegisterView,
    SubmissionDetailView,
    SubmissionListCreateView,
    VoteCreateView,
    WeeklySummaryView,
)

urlpatterns = [
    path('ping/', PingView.as_view(), name='ping'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
    path('submissions/', SubmissionListCreateView.as_view(), name='submission-list'),
    path('submissions/<int:pk>/', SubmissionDetailView.as_view(), name='submission-detail'),
    path('submissions/<int:pk>/vote/', VoteCreateView.as_view(), name='submission-vote'),
    path('results/weekly/', WeeklySummaryView.as_view(), name='weekly-summary'),
]
