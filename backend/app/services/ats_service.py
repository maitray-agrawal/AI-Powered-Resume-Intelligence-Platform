from typing import List, Dict, Any, Optional
from app.schemas.ats import ResumeDataInput


class ATSEngineService:
    @classmethod
    def calculate_ats_score(
        cls,
        resume: ResumeDataInput,
        job_keywords: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Calculates constituent and overall ATS scores based on:
        1. Keyword match density or total skills catalog.
        2. Content coverage of critical sections.
        3. Document word count length constraints.
        """
        # 1. Calculate constituent scores
        keyword_score, keyword_findings, keyword_suggestions = cls._calculate_keyword_score(
            resume.skills, job_keywords
        )
        section_score, section_findings, section_suggestions = cls._calculate_section_score(
            resume
        )
        length_score, length_findings, length_suggestions = cls._calculate_length_score(
            resume
        )

        # 2. Compute weighted overall score
        # Weight distribution: Keyword matches (40%), Section coverage (40%), Document length (20%)
        overall_score = round(
            (keyword_score * 0.4) + (section_score * 0.4) + (length_score * 0.2), 1
        )

        # 3. Aggregate findings and suggestions
        findings = keyword_findings + section_findings + length_findings
        suggestions = keyword_suggestions + section_suggestions + length_suggestions

        return {
            "keyword_score": round(keyword_score, 1),
            "section_score": round(section_score, 1),
            "length_score": round(length_score, 1),
            "overall_score": overall_score,
            "findings": findings,
            "suggestions": suggestions
        }

    @classmethod
    def _calculate_keyword_score(
        cls,
        resume_skills: List[str],
        job_keywords: Optional[List[str]] = None
    ) -> tuple[float, List[str], List[str]]:
        findings = []
        suggestions = []

        if not job_keywords:
            # If no target job keywords are provided, evaluate skills count relative to general industry standard (ideal: >=10 skills)
            count = len(resume_skills)
            score = min(count * 10.0, 100.0)
            findings.append(f"Identified {count} professional skills on the resume.")
            if count < 5:
                suggestions.append("Add more specific technical and professional skills to demonstrate expertise.")
            elif count < 10:
                suggestions.append("List supplementary skills, programming languages, or tools relevant to your domain.")
            else:
                findings.append("Excellent skill list size and keyword depth.")
            return score, findings, suggestions

        # Lowercase for case-insensitive matching
        resume_skills_lower = {s.lower() for s in resume_skills}
        job_keywords_clean = [k.strip() for k in job_keywords if k.strip()]
        
        if not job_keywords_clean:
            return 100.0, ["No valid job description keywords supplied; scored 100%."], []

        matched_keywords = []
        missing_keywords = []

        for kw in job_keywords_clean:
            if kw.lower() in resume_skills_lower:
                matched_keywords.append(kw)
            else:
                missing_keywords.append(kw)

        match_count = len(matched_keywords)
        total_count = len(job_keywords_clean)
        score = (match_count / total_count) * 100.0

        findings.append(
            f"Matched {match_count} out of {total_count} target job description keywords ({round(score, 1)}%)."
        )
        if matched_keywords:
            findings.append(f"Matched keywords: {', '.join(matched_keywords)}.")

        if missing_keywords:
            suggestions.append(
                f"Consider adding missing job-specific keywords: {', '.join(missing_keywords[:5])}."
            )
            if len(missing_keywords) > 5:
                suggestions.append(f"Also consider adding: {', '.join(missing_keywords[5:])}.")
        else:
            findings.append("Perfect match! Resume covers all targeted job requirements.")

        return score, findings, suggestions

    @classmethod
    def _calculate_section_score(cls, resume: ResumeDataInput) -> tuple[float, List[str], List[str]]:
        findings = []
        suggestions = []
        
        sections = {
            "Education": resume.education,
            "Experience": resume.experience,
            "Projects": resume.projects,
            "Skills": resume.skills
        }

        present = []
        missing = []

        for name, content in sections.items():
            if content:
                present.append(name)
            else:
                missing.append(name)

        score = (len(present) / len(sections)) * 100.0
        
        findings.append(f"Crucial sections present: {', '.join(present)}.")
        if missing:
            findings.append(f"Missing core sections: {', '.join(missing)}.")
            for item in missing:
                suggestions.append(f"Create a designated '{item}' section to organize your qualifications.")
        else:
            findings.append("Excellent layout structure; all standard resume sections are present.")

        return score, findings, suggestions

    @classmethod
    def _calculate_length_score(cls, resume: ResumeDataInput) -> tuple[float, List[str], List[str]]:
        findings = []
        suggestions = []

        # Count total words across descriptive text sections
        text_content = " ".join([
            resume.education or "",
            resume.experience or "",
            resume.projects or ""
        ])
        
        words = text_content.split()
        word_count = len(words)
        
        findings.append(f"Resume text sections contain approximately {word_count} words.")

        if 400 <= word_count <= 800:
            score = 100.0
            findings.append("Ideal resume length and content density.")
        elif 300 <= word_count < 400 or 800 < word_count <= 1000:
            score = 80.0
            if word_count < 400:
                suggestions.append("Slightly brief content. Add detail to your experience or projects to strengthen your profile.")
            else:
                suggestions.append("Slightly long. Ensure all points are concise and remove repetitive descriptors.")
        elif 150 <= word_count < 300 or 1000 < word_count <= 1500:
            score = 50.0
            if word_count < 300:
                suggestions.append("Insufficient detail. Expand bullet points under work history and projects with outcomes.")
            else:
                suggestions.append("Resume is verbose. Condense descriptions or trim older experience to fit within standard pages.")
        else:
            score = 20.0
            if word_count < 150:
                suggestions.append("Critically short. A standard professional resume needs substantive descriptions and dates.")
            else:
                suggestions.append("Critically long. Exceeds standard readability limits. Heavily condense text content.")

        return score, findings, suggestions
