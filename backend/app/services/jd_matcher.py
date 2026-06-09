import numpy as np
from sentence_transformers import SentenceTransformer
from typing import Dict, Any, List

# Lazy load model to avoid memory consumption at load time
model = None


def get_jd_model():
    global model
    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")
    return model


def calculate_cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    if norm_v1 == 0.0 or norm_v2 == 0.0:
        return 0.0
    return float(dot_product / (norm_v1 * norm_v2))


class JDMatcherService:
    @classmethod
    def calculate_semantic_match(
        cls,
        resume_text: str,
        resume_skills: List[str],
        job_description_text: str,
        job_description_skills: List[str]
    ) -> Dict[str, float]:
        """
        Calculates semantic match percentage between a candidate's resume and a JD.
        Computes cosine similarities on embeddings of full texts and skill lists.
        """
        transformer = get_jd_model()

        # 1. Compute Resume Similarity
        resume_embedding = transformer.encode(resume_text or " ")
        jd_embedding = transformer.encode(job_description_text or " ")
        resume_similarity = calculate_cosine_similarity(resume_embedding, jd_embedding)

        # 2. Compute Skill Similarity
        if not resume_skills and not job_description_skills:
            skill_similarity = 1.0
        elif not resume_skills or not job_description_skills:
            skill_similarity = 0.0
        else:
            resume_skills_str = ", ".join(resume_skills)
            jd_skills_str = ", ".join(job_description_skills)
            skills_emb = transformer.encode(resume_skills_str)
            jd_skills_emb = transformer.encode(jd_skills_str)
            skill_similarity = calculate_cosine_similarity(skills_emb, jd_skills_emb)

        # Ensure similarities stay in positive/normalized bounds
        resume_similarity = max(0.0, min(1.0, resume_similarity))
        skill_similarity = max(0.0, min(1.0, skill_similarity))

        # 3. Overall Match Percentage (Weighted average: 50% Resume Similarity, 50% Skill Similarity)
        match_percentage = ((resume_similarity * 0.5) + (skill_similarity * 0.5)) * 100.0
        match_percentage = max(0.0, min(100.0, match_percentage))

        # Determine matched and missing skills
        resume_skills_lower = {s.lower() for s in resume_skills}
        matched = [s for s in job_description_skills if s.lower() in resume_skills_lower]
        missing = [s for s in job_description_skills if s.lower() not in resume_skills_lower]

        # Trigger MLflow logging
        try:
            from app.services.mlflow_service import MLflowTrackingService
            MLflowTrackingService.log_jd_match(
                resume_skills_count=len(resume_skills),
                jd_skills_count=len(job_description_skills),
                overall_score=round(match_percentage, 2),
                metrics={
                    "resume_similarity": round(resume_similarity, 4),
                    "skill_similarity": round(skill_similarity, 4)
                },
                matched_skills=matched,
                missing_skills=missing
            )
        except Exception as mlflow_err:
            pass

        return {
            "resume_similarity": round(resume_similarity, 4),
            "skill_similarity": round(skill_similarity, 4),
            "match_percentage": round(match_percentage, 2)
        }
