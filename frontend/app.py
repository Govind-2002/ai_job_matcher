import streamlit as st
import requests
import time

# Configuration
BACKEND_URL = "http://localhost:8000/api"
MAX_FILE_SIZE_MB = 5

def main():
    st.set_page_config(page_title="AI Job Matcher", layout="wide")
    
    # Initialize session state
    if 'candidate' not in st.session_state:
        st.session_state.candidate = None
    
    # Header Section
    st.header("AI-Powered Job Matching Platform")
    
    # Main columns
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Upload Your Resume")
        with st.form("resume_upload"):
            # File uploader
            resume = st.file_uploader("Choose file", type=["pdf", "docx", "txt"],
                                      help=f"Max file size: {MAX_FILE_SIZE_MB}MB")
            submitted = st.form_submit_button("Upload & Parse")
            
            if submitted and resume:
                try:
                    with st.spinner("Analyzing..."):
                        # Create proper multipart form data
                        files = {
                            'resume': (resume.name, resume.getvalue(), 
                                      'application/pdf' if resume.name.endswith('.pdf') 
                                      else 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                        }
            
                        # Send request without manual Content-Type header
                        response = requests.post(
                            f"{BACKEND_URL}/parse-resume/",
                            files=files
                        )

                        # For resume parsing
                        response = requests.post(
                            f"{BACKEND_URL}/parse-resume/",
                            files={'resume': (resume.name, resume.getvalue())}
                        )

                            # For matching
                        response = requests.post(
                                f"{BACKEND_URL}/match/",
                                json={'candidate_id': candidate_id, 'job_id': job_id}
                            )
                                        
                        if response.status_code == 200:
                            st.success("Resume parsed successfully!")
                            st.session_state.candidate = response.json()
                        else:
                            st.error(f"Backend error (HTTP {response.status_code}): {response.text}")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")
                
    with col2:
        st.subheader("Available Positions")
        try:
            response = requests.get(f"{BACKEND_URL}/jobs/")
            
            if response.status_code != 200:
                st.error("Failed to load job listings")
                return
                
            jobs = response.json()
            
            if jobs:
                selected_job = st.selectbox(
                    "Select a job to analyze match",
                    jobs,
                    format_func=lambda x: f"{x['title']} - {x['company']}",
                    help="Select a job to see compatibility analysis"
                )
                
                if st.button("Check Compatibility", disabled=not st.session_state.candidate):
                    with st.spinner("Analyzing match..."):
                        try:
                            match_response = requests.post(
                                f"{BACKEND_URL}/match/",
                                json={
                                    "candidate": st.session_state.candidate,
                                    "job": selected_job
                                }
                            )
                            
                            if match_response.status_code == 200:
                                result = match_response.json()
                                display_match_results(result)
                            else:
                                st.error(f"Match analysis failed: {match_response.text}")
                        
                        except Exception as e:
                            st.error(f"Connection error: {str(e)}")
            else:
                st.info("No job postings available")
        except Exception as e:
            st.error(f"Failed to load jobs: {str(e)}")

def display_match_results(result):
    st.subheader(f"Match Score: {result.get('match_score', 0)}/100")
    st.progress(result.get('match_score', 0) / 100)
    
    with st.expander("Detailed Analysis"):
        if missing_skills := result.get('missing_skills'):
            st.markdown("**Skills to Improve:**")
            for skill in missing_skills:
                st.markdown(f"- {skill}")
        else:
            st.success("Perfect skill match!")
            
        if summary := result.get('summary'):
            st.markdown("**Summary:**")
            st.info(summary)
            
        if recommendations := result.get('recommendations'):
            st.markdown("**Recommendations:**")
            st.write(recommendations)

if __name__ == "__main__":
    main()
