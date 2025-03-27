from django.urls import path
from .match_url import match_candidate_to_job

from .views import MatchView

urlpatterns = [
    path('match/', MatchView.as_view({'post': 'create'}), name='match'),
]
