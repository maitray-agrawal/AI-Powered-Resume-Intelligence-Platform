import json
import logging
from typing import List, Dict, Any, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

# Try importing the GenAI SDK, fallback to None
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


class GeminiLLMService:
    @classmethod
    def get_client(cls) -> Optional[Any]:
        """Initializes and returns the Gemini client if credentials are configured."""
        if not GENAI_AVAILABLE:
            logger.warning("google-genai SDK is not installed. Running in mock mode.")
            return None
        if not settings.GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY is not set. Running in mock mode.")
            return None
        try:
            return genai.Client(api_key=settings.GEMINI_API_KEY)
        except Exception as e:
            logger.error(f"Failed to initialize Gemini Client: {e}")
            return None

    @classmethod
    def resume_improvement(cls, resume_text: str, job_description: Optional[str] = None) -> List[str]:
        """Analyzes a resume and returns a structured list of key improvements."""
        client = cls.get_client()
        if not client:
            return [
                "Quantify achievements in your work history with concrete metrics (e.g. % increase in performance, project timeline savings).",
                "Highlight key tools like FastAPI, Docker, and React near the top of the resume for ATS readability.",
                "Align your project descriptions closely with target roles, highlighting database and orchestration skills."
            ]

        prompt = (
            "Analyze the candidate's resume and suggest 3 high-impact improvement recommendations.\n"
            f"Resume Text:\n{resume_text}\n"
        )
        if job_description:
            prompt += f"Job Description:\n{job_description}\n"
            
        prompt += (
            "\nRespond ONLY with a JSON array of strings containing the improvements. "
            "Do not include markdown tags or wrap the JSON in backticks."
        )

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            # Clean possible markdown wrap ```json
            cleaned_text = cls._clean_json_response(response.text)
            return json.loads(cleaned_text)
        except Exception as e:
            logger.error(f"Gemini API error during resume improvement: {e}")
            return ["Improve bullet point action verbs.", "Ensure skills match standard industry keyword phrases."]

    @classmethod
    def resume_rewrite(cls, resume_text: str, target_role: str, sections_to_rewrite: List[str]) -> Dict[str, str]:
        """Rewrites specific sections of a resume to better target a given role."""
        client = cls.get_client()
        if not client:
            return {
                sec: f"[Mock Rewritten {sec.title()} Section]\n- Spearheaded development of backend services as a {target_role}, optimizing database queries.\n- Deployed production code using CI/CD pipelines and container architectures."
                for sec in sections_to_rewrite
            }

        prompt = (
            f"Rewrite the following sections of the resume to align with the target role: '{target_role}'.\n"
            f"Sections to rewrite: {', '.join(sections_to_rewrite)}\n"
            f"Resume Content:\n{resume_text}\n\n"
            "Respond ONLY with a JSON object where keys are the section names and values are the rewritten text for that section."
        )

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            cleaned_text = cls._clean_json_response(response.text)
            return json.loads(cleaned_text)
        except Exception as e:
            logger.error(f"Gemini API error during resume rewrite: {e}")
            return {sec: f"Error rewriting section '{sec}'; please verify API configurations." for sec in sections_to_rewrite}

    @classmethod
    def interview_questions(cls, resume_text: str, job_description: str) -> List[Dict[str, Any]]:
        """Generates tailored mock interview questions with rationales and suggested answer structures."""
        client = cls.get_client()
        if not client:
            return [
                {
                    "question": "Can you describe a project where you implemented containerization?",
                    "rationale": "The JD highlights Kubernetes and Docker, and your resume lists container experience.",
                    "suggested_approach": "Structure your answer using the STAR method: describe a project challenge, explain why you chose Docker, and highlight the deployment outcome."
                },
                {
                    "question": "How do you manage schema migrations with SQL databases in your FastAPI applications?",
                    "rationale": "The job requires backend design and your resume references PostgreSQL and FastAPI.",
                    "suggested_approach": "Mention using migrations tools like Alembic, keeping model classes synchronized, and handling schema rollbacks safely."
                }
            ]

        prompt = (
            "Analyze the candidate's resume and target JD to generate 2 relevant interview questions.\n"
            f"Resume Text:\n{resume_text}\n"
            f"Job Description:\n{job_description}\n\n"
            "Format the response ONLY as a JSON array of objects. Each object must contain keys: "
            "'question', 'rationale', and 'suggested_approach'. Do not wrap in markdown syntax."
        )

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            cleaned_text = cls._clean_json_response(response.text)
            return json.loads(cleaned_text)
        except Exception as e:
            logger.error(f"Gemini API error during interview prep: {e}")
            return [
                {
                    "question": "Describe your technical contribution to your most recent project.",
                    "rationale": "Assesses project engagement.",
                    "suggested_approach": "Highlight metrics, technologies, and team collaboration."
                }
            ]

    @classmethod
    def cover_letter(cls, resume_text: str, job_description: str) -> str:
        """Generates a professional cover letter matching the candidate's history to the job details."""
        client = cls.get_client()
        if not client:
            return (
                "Dear Hiring Manager,\n\n"
                "I am writing to express my strong interest in the position open at your company. "
                "With a background in software development and technical expertise matching your requirements, "
                "I am confident in my ability to contribute value immediately.\n\n"
                "Thank you for your consideration.\n\n"
                "Best regards,\n[Candidate Name]"
            )

        prompt = (
            "Generate a tailored, professional cover letter based on the candidate's resume and job description.\n"
            f"Resume Text:\n{resume_text}\n"
            f"Job Description:\n{job_description}\n\n"
            "Respond ONLY with the cover letter text itself. Do not include markdown wraps or metadata."
        )

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini API error during cover letter generation: {e}")
            return "Failed to generate cover letter due to system configuration errors."

    @staticmethod
    def _clean_json_response(text: str) -> str:
        """Cleans JSON strings returned inside Markdown block quotes."""
        text = text.strip()
        if text.startswith("```"):
            # strip start ```json or ```
            lines = text.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            text = "\n".join(lines).strip()
        return text
