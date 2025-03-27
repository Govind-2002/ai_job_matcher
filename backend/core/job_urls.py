from django.urls import path
from .views import JobPostingViewSet

urlpatterns = [
    path('', JobPostingViewSet.as_view({'get': 'list'}), name='jobs'),
]
