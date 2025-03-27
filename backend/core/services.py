import openai
import json
import logging
import os

from django.conf import settings

logger = logging.getLogger(__name__)


# ...
openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_resume(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f"Parse this resume into structured JSON:\n{text}"
            }],
            functions=[{
                "name": "parse_resume",
                "description": "Extract structured data from resume",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "skills": {"type": "array", "items": {"type": "string"}},
                        "education": {"type": "array", "items": {"type": "string"}},
                        "work_experience": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["name", "skills", "education", "work_experience"]
                }
            }],
            function_call={"name": "parse_resume"}
        )
        
        result = json.loads(response.choices[0].message.function_call.arguments)
        logger.info("LLM Response: %s", response.choices[0].message.function_call.arguments)

        return {
            "name": result.get("name", ""),
            "skills": result.get("skills", []),
            "education": result.get("education", []),
            "work_experience": result.get("work_experience", [])
        }
        
    except Exception as e:
        logger.error("Resume parsing failed: %s", str(e), exc_info=True)  # Log full traceback
        return None

def match_candidate_to_job(candidate_data, job_data):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f"Analyze this candidate-job match:\nCandidate Skills: {candidate_data['skills']}\nJob Requirements: {job_data['required_skills']}"
            }],
            functions=[{
                "name": "match_candidate_to_job",
                "description": "Calculate compatibility between candidate and job",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "match_score": {"type": "integer", "description": "0-100 compatibility score"},
                        "missing_skills": {"type": "array", "items": {"type": "string"}},
                        "summary": {"type": "string", "description": "Brief analysis of match"}
                    },
                    "required": ["match_score", "missing_skills", "summary"]
                }
            }],
            function_call={"name": "match_candidate_to_job"}
        )
        
        return json.loads(response.choices[0].message.function_call.arguments)
    except Exception as e:
       

        logger = logging.getLogger(__name__)   


        raise