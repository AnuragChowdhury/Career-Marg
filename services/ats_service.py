"""
ATS Compatibility Analysis Service & Resume Improvement Generator for Career मार्ग.
Implements factor-weighted scoring, keyword extraction, and bullet point refinement.
"""

from typing import Dict, Any, List, Tuple
from models.schemas import CandidateProfile, ATSResult, FactorScores, ResumeImprovement
from services.llm_service import LLMService
from utils.helpers import extract_skills_from_text
from utils.scoring import calculate_ats_score, compute_weighted_ats_overall
from services.resume_parser import TECH_SKILL_ONTOLOGY


class ATSService:
    def __init__(self, llm_service: LLMService = None):
        self.llm_service = llm_service or LLMService()

    def analyze_ats_compatibility(
        self,
        candidate_profile: CandidateProfile,
        target_role: str,
        job_description: str
    ) -> ATSResult:
        """
        Analyzes ATS compatibility using transparent 5-factor scoring.
        """
        # Extract target required skills from job description text or role title
        combined_jd = f"{target_role}\n{job_description}"
        target_skills = extract_skills_from_text(combined_jd, TECH_SKILL_ONTOLOGY)
        if not target_skills and target_role:
            # Fallback: extract terms from role title
            target_skills = [w.capitalize() for w in target_role.split() if len(w) > 2]

        candidate_skills = candidate_profile.technical_skills + candidate_profile.soft_skills
        
        # Extracted resume full text representation
        resume_text = f"{candidate_profile.professional_summary}\n" + \
                      " ".join(candidate_skills) + "\n" + \
                      " ".join([f"{w.job_title} {w.company} {' '.join(w.bullet_points)}" for w in candidate_profile.work_experience]) + "\n" + \
                      " ".join([f"{p.title} {p.description}" for p in candidate_profile.projects])

        # Compute factor scores
        factors = calculate_ats_score(
            candidate_skills=candidate_skills,
            target_required_skills=target_skills,
            resume_text=resume_text,
            job_description_text=job_description,
            years_experience=len(candidate_profile.work_experience) * 1.5,
            required_years=2.0,
            has_degree_match=len(candidate_profile.education) > 0,
            document_layout_quality=candidate_profile.document_analysis.layout_quality
        )

        overall_score = compute_weighted_ats_overall(factors)

        # Keyword sets
        matching_skills = sorted(list(set(candidate_skills).intersection(set(target_skills))))
        missing_skills = sorted(list(set(target_skills) - set(candidate_skills)))

        jd_keywords = set(w.lower() for w in job_description.split() if len(w) > 4) if job_description else set()
        res_keywords = set(w.lower() for w in resume_text.split() if len(w) > 4)
        
        matching_keywords = sorted([w.capitalize() for w in jd_keywords.intersection(res_keywords)])[:15]
        missing_keywords = sorted([w.capitalize() for w in jd_keywords - res_keywords])[:15]

        # Experience & Education alignment statements
        exp_align = f"Candidate shows {len(candidate_profile.work_experience)} work entries and {len(candidate_profile.projects)} projects against target role '{target_role or 'Job Description'}'."
        edu_align = f"Degree credentials ({', '.join([e.degree for e in candidate_profile.education][:2]) or 'Verified'}) align with technical background requirements."
        cert_align = f"Certifications ({', '.join([c.title for c in candidate_profile.certifications]) or 'None listed'}) provide verified credentials."

        # Recommendations
        recommendations = []
        if missing_skills:
            recommendations.append(f"Add key missing technical skills to resume: {', '.join(missing_skills[:4])}.")
        if factors.keyword_match < 75:
            recommendations.append("Incorporate exact phrasing and keywords from target job description into work experience bullets.")
        if candidate_profile.document_analysis.has_columns or candidate_profile.document_analysis.has_tables:
            recommendations.append("Simplify document formatting to standard single-column layout without embedded tables for maximum ATS compliance.")
        if not candidate_profile.professional_summary:
            recommendations.append("Add a 2-3 sentence tailored Professional Summary highlighting target job title and core expertise.")

        return ATSResult(
            overall_score=overall_score,
            factor_scores=factors,
            matching_keywords=matching_keywords or matching_skills,
            missing_keywords=missing_keywords or missing_skills,
            relevant_skills_found=matching_skills,
            required_skills_missing=missing_skills,
            experience_alignment=exp_align,
            education_alignment=edu_align,
            certification_alignment=cert_align,
            formatting_issues=candidate_profile.document_analysis.formatting_warnings,
            improvement_recommendations=recommendations or ["Resume formatting and keyword alignment show high ATS readiness."]
        )

    def suggest_resume_improvements(self, candidate_profile: CandidateProfile) -> List[ResumeImprovement]:
        """
        Analyzes work experience & project bullet points and generates quantifiable, action-verb suggestions.
        Does NOT fabricate metrics; uses [X%] or [Metric] placeholders.
        """
        bullets_to_improve = []
        
        for exp in candidate_profile.work_experience:
            for b in exp.bullet_points:
                bullets_to_improve.append(b)
                
        for proj in candidate_profile.projects:
            if proj.description:
                bullets_to_improve.append(proj.description)
            for h in proj.highlights:
                bullets_to_improve.append(h)

        if not bullets_to_improve:
            bullets_to_improve = ["Worked on software development projects and machine learning models."]

        results = []
        for orig in bullets_to_improve[:5]:
            # Generate optimized bullet point
            action_verb = "Engineered" if "work" in orig.lower() or "build" in orig.lower() else "Developed"
            suggested = f"{action_verb} and deployed {orig.lower().replace('worked on ', '').replace('worked with ', '')}, improving process efficiency by [X%] and reducing latency by [Y ms]."
            
            results.append(ResumeImprovement(
                original_bullet=orig,
                suggested_bullet=suggested,
                reason="Replaced generic verbs with strong technical action verbs and added measurable performance metrics.",
                placeholder_note="Replace [X%] and [Y ms] with your actual verified metrics."
            ))
            
        return results
