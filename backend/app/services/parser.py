import os
from pypdf import PdfReader
from docx import Document


class ResumeParser:
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text.strip()
        except Exception as e:
            raise ValueError(f"Error parsing PDF: {str(e)}")

    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        try:
            doc = Document(file_path)
            text = []
            for para in doc.paragraphs:
                text.append(para.text)
            return "\n".join(text).strip()
        except Exception as e:
            raise ValueError(f"Error parsing DOCX: {str(e)}")

    @classmethod
    def extract_text(cls, file_path: str, content_type: str) -> str:
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        if ext == '.pdf' or 'pdf' in content_type:
            return cls.extract_text_from_pdf(file_path)
        elif ext in ['.docx', '.doc'] or 'officedocument' in content_type:
            return cls.extract_text_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type '{ext}'. Only PDF and DOCX are supported.")
