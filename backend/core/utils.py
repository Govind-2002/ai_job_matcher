# core/utils.py
from pdfplumber import open as pdf_open
from docx import Document
import io

def extract_text_from_file(uploaded_file):
    try:
        # Read the entire file content into memory first
        file_content = uploaded_file.read()
        file_bytes = io.BytesIO(file_content)
        
        if uploaded_file.name.endswith('.pdf'):
            with pdf_open(file_bytes) as pdf:
                return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        elif uploaded_file.name.endswith('.docx'):
            doc = Document(file_bytes)
            return "\n".join([para.text for para in doc.paragraphs if para.text])
        else:  # txt file
            return file_content.decode()
    except Exception as e:
        print(f"Text extraction error: {str(e)}")
        return None
    finally:
        # Reset the file pointer (optional but safe)
        if uploaded_file:
            uploaded_file.seek(0)