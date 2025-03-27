# core/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse
from .models import CandidateProfile, JobPosting, MatchResult
from .serializers import (
    CandidateProfileSerializer,
    JobPostingSerializer,
    MatchResultSerializer
)
from .utils import extract_text_from_file
from .services import parse_resume, match_candidate_to_job
import traceback

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = CandidateProfile.objects.all()
    serializer_class = CandidateProfileSerializer

    @action(detail=False, methods=['POST'], url_path='upload-resume')
    def upload_resume(self, request):
        """Handle resume upload and parsing"""
        try:
            file = request.FILES.get('resume')
            if not file:
                return Response({"error": "No file uploaded"}, 
                               status=status.HTTP_400_BAD_REQUEST)
            
            # Extract text and parse resume
            text = extract_text_from_file(file)
            parsed_data = parse_resume(text)
            
            # Create candidate profile
            candidate = CandidateProfile.objects.create(
                name=parsed_data.get('name', ''),
                skills=parsed_data.get('skills', []),
                education=parsed_data.get('education', []),
                work_experience=parsed_data.get('experience', []),
                resume_file=file
            )
            
            return Response(
                CandidateProfileSerializer(candidate).data,
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class JobPostingViewSet(viewsets.ModelViewSet):
    """CRUD operations for job postings"""
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer

class MatchViewSet(viewsets.ViewSet):
    """Handle candidate-job matching operations"""
    
    @action(detail=False, methods=['POST'], url_path='match')
    def match_candidate(self, request):
        """Match a candidate to a specific job"""
        try:
            candidate_id = request.data.get('candidate_id')
            job_id = request.data.get('job_id')
            
            if not candidate_id or not job_id:
                return Response({"error": "Missing candidate_id or job_id"},
                              status=status.HTTP_400_BAD_REQUEST)
            
            # Retrieve objects
            candidate = CandidateProfile.objects.get(pk=candidate_id)
            job = JobPosting.objects.get(pk=job_id)
            
            # Perform matching
            match_data = match_candidate_to_job(
                candidate_data={
                    "skills": candidate.skills,
                    "experience": candidate.work_experience,
                    "education": candidate.education
                },
                job_data={
                    "required_skills": job.required_skills,
                    "description": job.description,
                    "title": job.title
                }
            )
            
            # Store match result
            match_result = MatchResult.objects.create(
                candidate=candidate,
                job=job,
                match_score=match_data.get('match_score', 0),
                missing_skills=match_data.get('missing_skills', []),
                summary=match_data.get('summary', '')
            )
            
            return Response(
                MatchResultSerializer(match_result).data,
                status=status.HTTP_200_OK
            )
            
        except CandidateProfile.DoesNotExist:
            return Response({"error": "Candidate not found"},
                          status=status.HTTP_404_NOT_FOUND)
        except JobPosting.DoesNotExist:
            return Response({"error": "Job posting not found"},
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)},
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Error handlers
def bad_request(request, exception=None):
    return JsonResponse({"error": "Bad request"}, status=400)

def page_not_found(request, exception=None):
    return JsonResponse({"error": "Page not found"}, status=404)

def server_error(request, exception=None):
    return JsonResponse({"error": "Server error"}, status=500)