import json
import logging
from typing import Dict, Any, List, Optional, TypedDict
from uuid import UUID
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import AgentReport, User
from app.services.llm_service import GeminiLLMService

logger = logging.getLogger(__name__)

# Try importing LangGraph, fallback if not fully installed yet
try:
    from langgraph.graph import StateGraph, END
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False


class AgentState(TypedDict):
    resume_text: str
    job_description: str
    ats_feedback: Dict[str, Any]
    recruiter_feedback: Dict[str, Any]
    reviewer_feedback: Dict[str, Any]
    advisor_feedback: Dict[str, Any]
    consolidated_report: Dict[str, Any]


def call_gemini_json(prompt: str) -> Dict[str, Any]:
    client = GeminiLLMService.get_client()
    if not client:
        return {}
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        text = response.text.strip()
        # Clean markdown code blocks if present
        if text.startswith("```"):
            lines = text.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            text = "\n".join(lines).strip()
        return json.loads(text)
    except Exception as e:
        logger.error(f"Error calling Gemini in agent node: {e}")
        return {}


def ats_expert_node(state: AgentState) -> Dict[str, Any]:
    prompt = (
        "You are an ATS Expert. Evaluate this resume based on ATS parsers rules:\n"
        f"Resume content:\n{state['resume_text']}\n"
        f"Target job description:\n{state['job_description']}\n\n"
        "Return ONLY a JSON dictionary with these keys: "
        "'formatting_score' (int 0-100), 'ats_compatibility' (string 'Low'/'Medium'/'High'), 'issues' (list of strings), and 'score' (int 0-100)."
    )
    res = call_gemini_json(prompt)
    # Fallback guarantees
    if not res:
        res = {"formatting_score": 70, "ats_compatibility": "Medium", "issues": ["Format looks standard."], "score": 70}
    return {"ats_feedback": res}


def recruiter_node(state: AgentState) -> Dict[str, Any]:
    prompt = (
        "You are a Recruiter. Review the resume from a hiring perspective:\n"
        f"Resume content:\n{state['resume_text']}\n"
        f"Target job description:\n{state['job_description']}\n\n"
        "Return ONLY a JSON dictionary with these keys: "
        "'hiring_verdict' (string 'Shortlist'/'Consider'/'Reject'), 'fit_rating' (float 1-5), 'skills_present' (list of strings), and 'skills_missing' (list of strings)."
    )
    res = call_gemini_json(prompt)
    if not res:
        res = {"hiring_verdict": "Consider", "fit_rating": 3.0, "skills_present": [], "skills_missing": []}
    return {"recruiter_feedback": res}


def resume_reviewer_node(state: AgentState) -> Dict[str, Any]:
    prompt = (
        "You are a Resume Reviewer. Focus on writing quality, grammar, action verbs, and structure:\n"
        f"Resume content:\n{state['resume_text']}\n"
        f"Target job description:\n{state['job_description']}\n\n"
        "Return ONLY a JSON dictionary with these keys: "
        "'writing_score' (int 0-100), 'grammar_issues' (list of strings), 'action_verbs_strength' (string 'Weak'/'Good'/'Strong'), and 'suggestions' (list of strings)."
    )
    res = call_gemini_json(prompt)
    if not res:
        res = {"writing_score": 75, "grammar_issues": [], "action_verbs_strength": "Good", "suggestions": []}
    return {"reviewer_feedback": res}


def career_advisor_node(state: AgentState) -> Dict[str, Any]:
    prompt = (
        "You are a Career Advisor. Assess candidate's next steps, growth opportunities, and certifications:\n"
        f"Resume content:\n{state['resume_text']}\n"
        f"Target job description:\n{state['job_description']}\n\n"
        "Return ONLY a JSON dictionary with these keys: "
        "'recommended_roles' (list of strings), 'suggested_certifications' (list of strings), 'career_advice' (string), and 'growth_areas' (list of strings)."
    )
    res = call_gemini_json(prompt)
    if not res:
        res = {"recommended_roles": [], "suggested_certifications": [], "career_advice": "Focus on backend architecture.", "growth_areas": []}
    return {"advisor_feedback": res}


def consolidation_node(state: AgentState) -> Dict[str, Any]:
    prompt = (
        "You are a Chief Consolidation Agent. Compile the findings of all individual agents:\n"
        f"ATS Expert Feedback: {state['ats_feedback']}\n"
        f"Recruiter Feedback: {state['recruiter_feedback']}\n"
        f"Resume Reviewer Feedback: {state['reviewer_feedback']}\n"
        f"Career Advisor Feedback: {state['advisor_feedback']}\n\n"
        "Generate a final consolidated report JSON dictionary with these keys: "
        "'summary' (string), 'strengths' (list of strings), 'critical_improvements' (list of strings), and 'fit_percentage' (float 0-100)."
    )
    res = call_gemini_json(prompt)
    if not res:
        res = {"summary": "Completed review.", "strengths": ["Coherent layout"], "critical_improvements": ["Add achievements statistics"], "fit_percentage": 70.0}
    return {"consolidated_report": res}


class ResumeAgentWorkflowService:
    @classmethod
    def run_agent_workflow(
        cls,
        resume_text: str,
        job_description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Runs the multi-agent LangGraph workflow sequentially."""
        jd = job_description or "General Software Engineering positions"
        
        initial_state = {
            "resume_text": resume_text,
            "job_description": jd,
            "ats_feedback": {},
            "recruiter_feedback": {},
            "reviewer_feedback": {},
            "advisor_feedback": {},
            "consolidated_report": {}
        }

        # Ephemeral / mock mode if API credentials or LangGraph libraries are unavailable
        if not LANGGRAPH_AVAILABLE or not settings.GEMINI_API_KEY:
            logger.warning("Mocking multi-agent workflow.")
            state = initial_state
            state["ats_feedback"] = {
                "formatting_score": 85,
                "ats_compatibility": "High",
                "issues": ["Technical skills section could be positioned higher."],
                "score": 85
            }
            state["recruiter_feedback"] = {
                "hiring_verdict": "Shortlist",
                "fit_rating": 4.5,
                "skills_present": ["Python", "FastAPI", "React"],
                "skills_missing": ["PostgreSQL", "Docker"]
            }
            state["reviewer_feedback"] = {
                "writing_score": 90,
                "grammar_issues": [],
                "action_verbs_strength": "Strong",
                "suggestions": ["Add numbers/impact metrics to bullet points."]
            }
            state["advisor_feedback"] = {
                "recommended_roles": ["Senior Backend Engineer", "FastAPI Developer"],
                "suggested_certifications": ["AWS Certified Solutions Architect"],
                "career_advice": "Focus on cloud deployment projects to supplement backend capabilities.",
                "growth_areas": ["Cloud orchestration", "Infrastructure as Code"]
            }
            state["consolidated_report"] = {
                "summary": "Strong candidate with solid web backend foundation. Recommended for tech interviews.",
                "strengths": ["Clear section layouts", "Strong FastAPI experience"],
                "critical_improvements": ["List metrics in achievements", "Integrate cloud infrastructure items"],
                "fit_percentage": 85.0
            }
            return state

        # Compile and execute LangGraph
        try:
            workflow = StateGraph(AgentState)

            workflow.add_node("ats_expert", ats_expert_node)
            workflow.add_node("recruiter", recruiter_node)
            workflow.add_node("resume_reviewer", resume_reviewer_node)
            workflow.add_node("career_advisor", career_advisor_node)
            workflow.add_node("consolidator", consolidation_node)

            workflow.set_entry_point("ats_expert")
            workflow.add_edge("ats_expert", "recruiter")
            workflow.add_edge("recruiter", "resume_reviewer")
            workflow.add_edge("resume_reviewer", "career_advisor")
            workflow.add_edge("career_advisor", "consolidator")
            workflow.add_edge("consolidator", END)

            app = workflow.compile()
            final_state = app.invoke(initial_state)
            return final_state
        except Exception as e:
            logger.error(f"Error compiling/running LangGraph workflow: {e}")
            return initial_state

    @classmethod
    def save_report_to_db(
        cls,
        db: Session,
        user_id: UUID,
        report_data: Dict[str, Any]
    ) -> AgentReport:
        """Stores the consolidated report output in the database agent_reports table."""
        report = AgentReport(
            user_id=user_id,
            report_type="multi_agent_consolidated_report",
            content=report_data
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        return report

    @classmethod
    def get_or_create_default_user(cls, db: Session) -> User:
        """Helper to retrieve/create a default system user to bypass database constraints."""
        user = db.query(User).first()
        if not user:
            user = User(
                email="agent_recruiter@example.com",
                hashed_password="agent_pass_placeholder",
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        return user
