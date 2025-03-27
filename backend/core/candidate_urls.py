from django.urls import path
from .views import CandidateViewSet

urlpatterns = [
    path('candidates/', CandidateViewSet.as_view({'post': 'create', 'get': 'list'}), name='candidates'),
]
