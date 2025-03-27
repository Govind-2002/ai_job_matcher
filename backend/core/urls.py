# core/urls.py
from django.urls import path, include
from rest_framework import routers
from . import views  # Only this import remains

router = routers.DefaultRouter()
router.register(r'candidates', views.CandidateViewSet)
router.register(r'jobs', views.JobPostingViewSet)
router.register(r'matches', views.MatchViewSet, basename='matches')

urlpatterns = [
    path('', include(router.urls)),
    # Remove any other path() entries referencing deleted functions
]