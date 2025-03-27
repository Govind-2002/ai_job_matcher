# frontend/utils.py
from pdfplumber import open as pdf_open
from docx import Document
import io

def extract_text(uploaded_file):
    """Extract text from PDF/DOCX/TXT files"""
    try:
        file_bytes = io.BytesIO(uploaded_file.getvalue())
        
        if uploaded_file.name.endswith('.pdf'):
            with pdf_open(file_bytes) as pdf:
                return "\n".join([page.extract_text() for page in pdf.pages])
                
        elif uploaded_file.name.endswith('.docx'):
            doc = Document(file_bytes)
            return "\n".join([para.text for para in doc.paragraphs])
            
        else:  # txt file
            return file_bytes.getvalue().decode()
            
    except Exception as e:
        print(f"Text extraction error: {str(e)}")
        return None