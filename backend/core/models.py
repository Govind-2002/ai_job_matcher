from django.db import models

class CandidateProfile(models.Model):
    name = models.CharField(max_length=255)
    skills = models.JSONField()
    education = models.JSONField()
    work_experience = models.JSONField()
    resume_file = models.FileField(upload_to='resumes/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # ✅ Fixed __str__ method
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"


class JobPosting(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    required_skills = models.JSONField()
    description = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # ✅ Fixed __str__ method
        return f"{self.title} @ {self.company}"


class MatchResult(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    match_score = models.IntegerField()
    missing_skills = models.JSONField()
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("candidate", "job"),)  # ✅ Fixed tuple format

    def __str__(self):  # ✅ Added __str__ method
        return f"{self.candidate.name} - {self.job.title} ({self.match_score}%)"
