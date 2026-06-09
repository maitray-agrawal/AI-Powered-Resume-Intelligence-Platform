import logging
import json
import time
from typing import Dict, Any, List, Optional
import mlflow
from app.core.config import settings

logger = logging.getLogger(__name__)


class MLflowTrackingService:
    _initialized = False

    @classmethod
    def initialize(cls):
        """Initializes the MLflow tracking URI and experiment."""
        if cls._initialized:
            return True
        try:
            # Set the tracking URI
            mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
            # Set the active experiment
            mlflow.set_experiment(settings.MLFLOW_EXPERIMENT_NAME)
            cls._initialized = True
            logger.info(f"MLflow initialized successfully with URI: {settings.MLFLOW_TRACKING_URI}")
            return True
        except Exception as e:
            logger.warning(f"Failed to initialize MLflow: {e}. MLflow logging will be disabled.")
            return False

    @classmethod
    def log_ats_score(
        cls,
        resume_name: str,
        overall_score: float,
        metrics: Dict[str, float],
        params: Dict[str, Any],
        findings: List[str],
        suggestions: List[str]
    ):
        """Logs ATS evaluation metrics, configuration parameters, and suggestions."""
        if not cls.initialize():
            return

        try:
            with mlflow.start_run(run_name=f"ATS_Score_{int(time.time())}") as run:
                # Log tags
                mlflow.set_tag("eval_type", "ats_scoring")
                mlflow.set_tag("resume_name", resume_name)

                # Log parameters
                mlflow.log_params(params)

                # Log metrics
                mlflow.log_metric("overall_score", overall_score)
                for metric_name, val in metrics.items():
                    mlflow.log_metric(metric_name, val)

                # Log findings and suggestions as json artifacts
                report_data = {
                    "resume_name": resume_name,
                    "overall_score": overall_score,
                    "metrics": metrics,
                    "findings": findings,
                    "suggestions": suggestions
                }
                mlflow.log_text(json.dumps(report_data, indent=2), "ats_report.json")
                logger.info(f"MLflow logged ATS Score for {resume_name} (Score: {overall_score})")
        except Exception as e:
            logger.warning(f"MLflow logging error in log_ats_score: {e}")

    @classmethod
    def log_jd_match(
        cls,
        resume_skills_count: int,
        jd_skills_count: int,
        overall_score: float,
        metrics: Dict[str, float],
        matched_skills: List[str],
        missing_skills: List[str]
    ):
        """Logs semantic job description compatibility metrics."""
        if not cls.initialize():
            return

        try:
            with mlflow.start_run(run_name=f"JD_Match_{int(time.time())}") as run:
                mlflow.set_tag("eval_type", "jd_matcher")

                # Log parameters
                mlflow.log_param("resume_skills_count", resume_skills_count)
                mlflow.log_param("jd_skills_count", jd_skills_count)

                # Log metrics
                mlflow.log_metric("match_score", overall_score)
                for metric_name, val in metrics.items():
                    mlflow.log_metric(metric_name, val)

                # Log skills lists as artifacts
                skills_data = {
                    "overall_score": overall_score,
                    "matched_skills": matched_skills,
                    "missing_skills": missing_skills
                }
                mlflow.log_text(json.dumps(skills_data, indent=2), "jd_skills_match.json")
                logger.info(f"MLflow logged JD Match (Score: {overall_score})")
        except Exception as e:
            logger.warning(f"MLflow logging error in log_jd_match: {e}")

    @classmethod
    def log_rag_chat(
        cls,
        resume_id: str,
        query: str,
        answer: str,
        source_count: int
    ):
        """Logs RAG Chatbot queries, answers, and context metrics."""
        if not cls.initialize():
            return

        try:
            with mlflow.start_run(run_name=f"RAG_Chat_{int(time.time())}") as run:
                mlflow.set_tag("eval_type", "rag_chat")
                mlflow.set_tag("resume_id", resume_id)

                # Log parameters / query details
                mlflow.log_param("resume_id", resume_id)
                mlflow.log_param("query_preview", query[:100])

                # Log metrics
                mlflow.log_metric("sources_retrieved", source_count)

                # Log full conversation interaction
                chat_data = {
                    "query": query,
                    "answer": answer,
                    "sources_retrieved_count": source_count
                }
                mlflow.log_text(json.dumps(chat_data, indent=2), "rag_interaction.json")
                logger.info(f"MLflow logged RAG chat interaction for resume_id {resume_id}")
        except Exception as e:
            logger.warning(f"MLflow logging error in log_rag_chat: {e}")

    @classmethod
    def log_agent_workflow(
        cls,
        workflow_result: Dict[str, Any],
        job_description_length: int
    ):
        """Logs LangGraph multi-agent run outputs, consolidated score, and feedback."""
        if not cls.initialize():
            return

        try:
            with mlflow.start_run(run_name=f"Agent_Workflow_{int(time.time())}") as run:
                mlflow.set_tag("eval_type", "multi_agent_workflow")

                # Log parameters
                mlflow.log_param("job_desc_length_chars", job_description_length)

                # Extract and log metrics from consolidated report
                consolidated = workflow_result.get("consolidated_report", {})
                fit_percentage = consolidated.get("fit_percentage", 0.0)
                mlflow.log_metric("consolidated_fit_percentage", fit_percentage)

                # Log constituent scores from feedback dictionaries
                ats_feed = workflow_result.get("ats_feedback", {})
                if "score" in ats_feed:
                    mlflow.log_metric("agent_ats_score", ats_feed["score"])
                if "formatting_score" in ats_feed:
                    mlflow.log_metric("agent_formatting_score", ats_feed["formatting_score"])

                recruiter_feed = workflow_result.get("recruiter_feedback", {})
                if "fit_rating" in recruiter_feed:
                    mlflow.log_metric("agent_recruiter_fit_rating", recruiter_feed["fit_rating"])

                reviewer_feed = workflow_result.get("reviewer_feedback", {})
                if "writing_score" in reviewer_feed:
                    mlflow.log_metric("agent_reviewer_writing_score", reviewer_feed["writing_score"])

                # Log full workflow output dictionary as JSON artifact
                mlflow.log_text(json.dumps(workflow_result, indent=2), "workflow_result.json")
                logger.info(f"MLflow logged Multi-Agent Workflow run (Fit: {fit_percentage}%)")
        except Exception as e:
            logger.warning(f"MLflow logging error in log_agent_workflow: {e}")
