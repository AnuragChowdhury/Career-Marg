"""
Skill Gap Analysis Service & Learning Roadmap Generator for Career मार्ग.
Categorizes candidate competencies into Strong, Partial, Missing, and Additional skills,
and generates structured, prioritized learning roadmaps.
"""

from typing import Dict, Any, List
from models.schemas import CandidateProfile, SkillGapResult, RoadmapItem
from services.llm_service import LLMService
from utils.helpers import extract_skills_from_text
from services.resume_parser import TECH_SKILL_ONTOLOGY


class SkillGapService:
    def __init__(self, llm_service: LLMService = None):
        self.llm_service = llm_service or LLMService()

    def analyze_skill_gaps(
        self,
        candidate_profile: CandidateProfile,
        target_role: str,
        job_description: str
    ) -> SkillGapResult:
        """
        Categorizes skills into Strong Match, Partial Match, Missing Skills, and Additional Skills.
        Generates personalized learning roadmap items.
        """
        candidate_skills = set(s.strip() for s in candidate_profile.technical_skills + candidate_profile.soft_skills)
        
        combined_jd = f"{target_role}\n{job_description}"
        jd_skills = set(extract_skills_from_text(combined_jd, TECH_SKILL_ONTOLOGY))
        
        if not jd_skills and target_role:
            jd_skills = set(w.capitalize() for w in target_role.split() if len(w) > 3)

        # Categorization logic
        strong_match = sorted(list(candidate_skills.intersection(jd_skills)))
        
        # Partial match heuristics (e.g., Deep Learning if ML is present, Docker if Linux present)
        partial_match = []
        if "Machine Learning" in candidate_skills and "Deep Learning" in jd_skills and "Deep Learning" not in candidate_skills:
            partial_match.append("Deep Learning")
        if "Python" in candidate_skills and "FastAPI" in jd_skills and "FastAPI" not in candidate_skills:
            partial_match.append("FastAPI")
        if "SQL" in candidate_skills and "PostgreSQL" in jd_skills and "PostgreSQL" not in candidate_skills:
            partial_match.append("PostgreSQL")

        missing_skills = sorted(list(jd_skills - candidate_skills - set(partial_match)))
        additional_skills = sorted(list(candidate_skills - jd_skills))[:8]

        # Ensure at least some default gap structure if no JD provided
        if not missing_skills and not strong_match:
            missing_skills = ["Docker", "Kubernetes", "MLOps", "CI/CD"]
            strong_match = list(candidate_skills)[:4] or ["Python", "Git"]

        # Learning Roadmap Generation
        roadmap = []
        priority_levels = ["High", "High", "Medium", "Medium", "Low"]
        
        for idx, skill in enumerate(missing_skills[:5]):
            prio = priority_levels[min(idx, len(priority_levels) - 1)]
            roadmap.append(RoadmapItem(
                skill=skill,
                priority=prio,
                importance="Critical requirement in target job description.",
                reason=f"{skill} is frequently requested for candidate evaluation in {target_role or 'this role'}.",
                topics=[f"Core {skill} Architecture", f"{skill} Best Practices", f"Integration with Web/API Ecosystem"],
                suggested_resources=[f"Official {skill} Documentation", f"Interactive {skill} Bootcamp"],
                suggested_project=f"Build and deploy an end-to-end application incorporating {skill}."
            ))

        for skill in partial_match:
            roadmap.append(RoadmapItem(
                skill=skill,
                priority="Medium",
                importance="Partial knowledge detected; upgrade to production readiness.",
                reason=f"Foundational background exists, but specialized competence in {skill} is needed.",
                topics=[f"Advanced {skill} Concepts", "Performance Optimization"],
                suggested_resources=[f"Hands-on {skill} Tutorials"],
                suggested_project=f"Enhance existing portfolio project using {skill}."
            ))

        return SkillGapResult(
            strong_match=strong_match,
            partial_match=partial_match,
            missing_skills=missing_skills,
            additional_skills=additional_skills,
            roadmap=roadmap
        )

    def generate_30_day_action_plan(self, skill_gap_result: SkillGapResult, target_role: str = "") -> Dict[str, Any]:
        """
        Generates a concise 30-Day Skill Gap Action Plan divided into 3 10-day phases.
        """
        missing = skill_gap_result.missing_skills or ["Docker", "MLOps", "Kubernetes"]
        partial = skill_gap_result.partial_match or ["FastAPI"]
        role = target_role or "Target Career Role"

        phase1_skills = missing[:2] if missing else ["Core Technical Requirement"]
        phase2_skills = (missing[2:4] if len(missing) >= 4 else missing[1:]) + partial[:1]
        phase3_skills = missing[:2] + partial[:1]

        summary_digest = (
            f"30-Day Strategy for {role}: Focus Days 1–10 on critical missing skills ({', '.join(phase1_skills)}), "
            f"Days 11–20 on specialized topics ({', '.join(phase2_skills[:2])}), and Days 21–30 on deploying a full portfolio project."
        )

        return {
            "summary_digest": summary_digest,
            "phase1": {
                "title": "Days 1–10: High Priority Skill Foundation",
                "focus_skills": phase1_skills,
                "action": f"Master core fundamentals and syntax of {', '.join(phase1_skills)}. Complete interactive tutorials and build mini-cli utilities."
            },
            "phase2": {
                "title": "Days 11–20: Deep Dive & Partial Skill Upgrade",
                "focus_skills": phase2_skills,
                "action": f"Upgrade foundational skills ({', '.join(phase2_skills[:2])}) to production readiness. Practice integration with web APIs and databases."
            },
            "phase3": {
                "title": "Days 21–30: Portfolio Integration & Job Readiness",
                "focus_skills": phase3_skills,
                "action": f"Build and deploy 1 end-to-end portfolio project incorporating {', '.join(phase3_skills[:2])}. Add quantified bullets to your resume."
            }
        }

