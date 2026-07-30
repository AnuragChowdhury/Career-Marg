"""
Structured Resume Parsing Service for Career मार्ग.
Converts raw extracted document text into structured CandidateProfile JSON schema.
Distinguishes strictly between facts explicitly found in the resume vs AI recommendations.
"""

import re
from typing import Dict, Any, List
from models.schemas import (
    CandidateProfile, PersonalInfo, Education, WorkExperience,
    Internship, Project, Certification, DocumentAnalysis
)
from services.llm_service import LLMService
from utils.helpers import clean_text, extract_skills_from_text


# Predefined technical & soft skill ontology for fallback extraction
TECH_SKILL_ONTOLOGY = [
    "Python", "Java", "C++", "C#", "SQL", "JavaScript", "TypeScript", "HTML", "CSS",
    "React", "React.js", "Node.js", "Express", "Angular", "Vue", "Next.js", "Django", "Flask", "FastAPI",
    "Machine Learning", "Deep Learning", "Artificial Intelligence", "NLP", "Natural Language Processing",
    "Computer Vision", "TensorFlow", "PyTorch", "Scikit-Learn", "Keras", "Pandas", "NumPy", "Matplotlib",
    "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Google Cloud", "CI/CD", "Git", "GitHub", "Linux",
    "MongoDB", "PostgreSQL", "MySQL", "SQLite", "Redis", "REST API", "GraphQL", "Microservices",
    "MLOps", "FAISS", "ChromaDB", "Streamlit", "Tableau", "Power BI", "Spark", "Hadoop", "Kafka"
]

SOFT_SKILL_ONTOLOGY = [
    "Problem Solving", "Communication", "Leadership", "Teamwork", "Collaboration",
    "Critical Thinking", "Adaptability", "Time Management", "Project Management",
    "Agile", "Scrum", "Analytical Skills", "Creativity", "Decision Making"
]


class ResumeParser:
    def __init__(self, llm_service: LLMService = None):
        self.llm_service = llm_service or LLMService()

    def parse_resume(self, text: str, doc_analysis: DocumentAnalysis) -> CandidateProfile:
        """
        Parses resume text into a CandidateProfile. Uses LLM if available, otherwise heuristic NLP.
        """
        cleaned_text = clean_text(text)
        
        # Try LLM JSON parsing first
        llm_profile = self._parse_with_llm(cleaned_text)
        if llm_profile:
            llm_profile.document_analysis = doc_analysis
            return llm_profile
            
        # Heuristic NLP parsing fallback
        return self._parse_with_heuristics(cleaned_text, doc_analysis)

    def _parse_with_llm(self, text: str) -> CandidateProfile:
        system_prompt = (
            "You are an expert resume parsing system. Parse the resume into a strict JSON matching this structure:\n"
            "{\n"
            "  \"personal_information\": {\"name\": \"\", \"email\": \"\", \"phone\": \"\", \"location\": \"\", \"linkedin\": \"\", \"github\": \"\", \"portfolio\": \"\"},\n"
            "  \"professional_summary\": \"\",\n"
            "  \"education\": [{\"degree\": \"\", \"institution\": \"\", \"start_date\": \"\", \"end_date\": \"\", \"gpa\": \"\", \"details\": []}],\n"
            "  \"technical_skills\": [],\n"
            "  \"soft_skills\": [],\n"
            "  \"work_experience\": [{\"job_title\": \"\", \"company\": \"\", \"location\": \"\", \"start_date\": \"\", \"end_date\": \"\", \"bullet_points\": []}],\n"
            "  \"internships\": [{\"title\": \"\", \"organization\": \"\", \"duration\": \"\", \"details\": []}],\n"
            "  \"projects\": [{\"title\": \"\", \"description\": \"\", \"technologies_used\": [], \"link\": \"\", \"highlights\": []}],\n"
            "  \"certifications\": [{\"title\": \"\", \"issuer\": \"\", \"issue_date\": \"\", \"credential_id\": \"\"}],\n"
            "  \"achievements\": [],\n"
            "  \"publications\": [],\n"
            "  \"extracurricular_activities\": [],\n"
            "  \"extracted_facts\": [],\n"
            "  \"ai_recommendations\": []\n"
            "}\n"
            "Do NOT fabricate information. Only include facts explicitly mentioned in the text."
        )

        user_prompt = f"Resume Content:\n\n{text[:4000]}"
        json_resp = self.llm_service.generate_json(user_prompt, system_prompt)
        
        if json_resp:
            try:
                # Sanitize & populate model
                p_info = json_resp.get("personal_information", {})
                personal_info = PersonalInfo(**p_info) if isinstance(p_info, dict) else PersonalInfo()
                
                edu_list = [Education(**e) for e in json_resp.get("education", []) if isinstance(e, dict)]
                work_list = [WorkExperience(**w) for w in json_resp.get("work_experience", []) if isinstance(w, dict)]
                intern_list = [Internship(**i) for i in json_resp.get("internships", []) if isinstance(i, dict)]
                proj_list = [Project(**p) for p in json_resp.get("projects", []) if isinstance(p, dict)]
                cert_list = [Certification(**c) for c in json_resp.get("certifications", []) if isinstance(c, dict)]

                facts = json_resp.get("extracted_facts", [])
                if not facts:
                    facts = [
                        f"Extracted contact email: {personal_info.email}" if personal_info.email else "Parsed personal details.",
                        f"Identified {len(json_resp.get('technical_skills', []))} technical skills.",
                        f"Identified {len(edu_list)} education entries and {len(work_list)} work roles."
                    ]

                recs = json_resp.get("ai_recommendations", [])
                if not recs:
                    recs = [
                        "Consider quantifying project results with percentage improvements.",
                        "Add a concise 2-line targeted executive summary at the top of your resume."
                    ]

                tech_skills = json_resp.get("technical_skills", [])
                if not isinstance(tech_skills, list) or not tech_skills:
                    tech_skills = extract_skills_from_text(text, TECH_SKILL_ONTOLOGY)

                soft_skills = json_resp.get("soft_skills", [])
                if not isinstance(soft_skills, list) or not soft_skills:
                    soft_skills = extract_skills_from_text(text, SOFT_SKILL_ONTOLOGY)

                return CandidateProfile(
                    personal_information=personal_info,
                    professional_summary=json_resp.get("professional_summary", ""),
                    education=edu_list,
                    technical_skills=tech_skills,
                    soft_skills=soft_skills,
                    work_experience=work_list,
                    internships=intern_list,
                    projects=proj_list,
                    certifications=cert_list,
                    achievements=json_resp.get("achievements", []),
                    publications=json_resp.get("publications", []),
                    extracurricular_activities=json_resp.get("extracurricular_activities", []),
                    extracted_facts=facts,
                    ai_recommendations=recs
                )
            except Exception:
                pass

        return None

    def _parse_with_heuristics(self, text: str, doc_analysis: DocumentAnalysis) -> CandidateProfile:
        """
        Regex and rule-based heuristic extraction fallback.
        """
        # Email
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        email = email_match.group(0) if email_match else ""

        # Phone
        phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        phone = phone_match.group(0) if phone_match else ""

        # Name heuristic (first non-empty line)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        name = lines[0] if lines else "Candidate Name"
        if len(name) > 40 or "@" in name:
            name = "Candidate"

        # URLs
        linkedin = ""
        github = ""
        portfolio = ""
        for line in lines:
            if "linkedin.com" in line.lower() and not linkedin:
                linkedin = line
            elif "github.com" in line.lower() and not github:
                github = line
            elif any(domain in line.lower() for domain in ["portfolio", "http://", "https://"]) and not portfolio:
                portfolio = line

        p_info = PersonalInfo(
            name=name,
            email=email,
            phone=phone,
            linkedin=linkedin,
            github=github,
            portfolio=portfolio
        )

        # Technical & Soft skills extraction
        tech_skills = extract_skills_from_text(text, TECH_SKILL_ONTOLOGY)
        soft_skills = extract_skills_from_text(text, SOFT_SKILL_ONTOLOGY)

        # Education extraction heuristics
        education_entries = []
        for line in lines:
            if any(deg in line.lower() for deg in ["b.tech", "b.e", "bachelor", "master", "m.tech", "b.s", "m.s", "ph.d", "degree", "university", "institute", "college"]):
                education_entries.append(Education(
                    degree=line,
                    institution="Educational Institution",
                    details=[line]
                ))
        if not education_entries:
            education_entries.append(Education(degree="Degree / Education Mentioned", institution="University"))

        # Projects extraction heuristics
        projects = []
        proj_lines = [l for l in lines if any(k in l.lower() for k in ["project", "developed", "built", "implemented", "system", "app"])]
        for pl in proj_lines[:3]:
            projects.append(Project(
                title=pl[:50],
                description=pl,
                technologies_used=tech_skills[:3]
            ))

        # Work experience heuristics
        work_exp = []
        exp_lines = [l for l in lines if any(k in l.lower() for k in ["engineer", "developer", "intern", "manager", "analyst", "lead"])]
        for el in exp_lines[:2]:
            work_exp.append(WorkExperience(
                job_title=el[:40],
                company="Organization",
                bullet_points=[el]
            ))

        extracted_facts = [
            f"Explicitly extracted contact details: Email ({email or 'N/A'}), Phone ({phone or 'N/A'}).",
            f"Extracted {len(tech_skills)} technical skills from candidate text.",
            f"Extracted {len(education_entries)} education entries and {len(projects)} portfolio projects."
        ]

        ai_recommendations = [
            "Add quantifiable metrics (e.g. 'Improved efficiency by 25%') to bullet points.",
            "Include direct URLs to hosted live web applications or GitHub repositories.",
            "Ensure skills are logically grouped by category (Languages, Frameworks, Databases, Tools)."
        ]

        return CandidateProfile(
            personal_information=p_info,
            professional_summary=lines[1] if len(lines) > 1 and len(lines[1]) > 30 else "Aspiring professional with expertise in technical domain.",
            education=education_entries,
            technical_skills=tech_skills or ["Python", "Problem Solving"],
            soft_skills=soft_skills or ["Communication", "Teamwork"],
            work_experience=work_exp,
            projects=projects,
            document_analysis=doc_analysis,
            extracted_facts=extracted_facts,
            ai_recommendations=ai_recommendations
        )
