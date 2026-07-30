"""
Pydantic Data Schemas for Career मार्ग.
Clean, strictly typed data structures representing candidate profiles, OCR metadata,
ATS results, Skill Gap analysis, Interview questions, and recommendations.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class PersonalInfo(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    linkedin: str = ""
    github: str = ""
    portfolio: str = ""


class Education(BaseModel):
    degree: str = ""
    institution: str = ""
    start_date: str = ""
    end_date: str = ""
    gpa: str = ""
    details: List[str] = Field(default_factory=list)


class WorkExperience(BaseModel):
    job_title: str = ""
    company: str = ""
    location: str = ""
    start_date: str = ""
    end_date: str = ""
    bullet_points: List[str] = Field(default_factory=list)


class Internship(BaseModel):
    title: str = ""
    organization: str = ""
    duration: str = ""
    details: List[str] = Field(default_factory=list)


class Project(BaseModel):
    title: str = ""
    description: str = ""
    technologies_used: List[str] = Field(default_factory=list)
    link: str = ""
    highlights: List[str] = Field(default_factory=list)


class Certification(BaseModel):
    title: str = ""
    issuer: str = ""
    issue_date: str = ""
    credential_id: str = ""


class DocumentAnalysis(BaseModel):
    page_count: int = 1
    file_type: str = "Digital PDF"  # Digital PDF, Scanned PDF, Image (JPG/PNG)
    has_columns: bool = False
    has_tables: bool = False
    layout_quality: float = 85.0  # 0 to 100
    readability_score: float = 80.0  # 0 to 100
    formatting_warnings: List[str] = Field(default_factory=list)


class CandidateProfile(BaseModel):
    personal_information: PersonalInfo = Field(default_factory=PersonalInfo)
    professional_summary: str = ""
    education: List[Education] = Field(default_factory=list)
    technical_skills: List[str] = Field(default_factory=list)
    soft_skills: List[str] = Field(default_factory=list)
    work_experience: List[WorkExperience] = Field(default_factory=list)
    internships: List[Internship] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
    certifications: List[Certification] = Field(default_factory=list)
    achievements: List[str] = Field(default_factory=list)
    publications: List[str] = Field(default_factory=list)
    extracurricular_activities: List[str] = Field(default_factory=list)
    document_analysis: DocumentAnalysis = Field(default_factory=DocumentAnalysis)
    extracted_facts: List[str] = Field(default_factory=list)
    ai_recommendations: List[str] = Field(default_factory=list)


class FactorScores(BaseModel):
    required_skill_match: float = 0.0  # 40% weight
    keyword_match: float = 0.0         # 25% weight
    experience_relevance: float = 0.0  # 15% weight
    education_relevance: float = 0.0   # 10% weight
    structure_quality: float = 0.0     # 10% weight


class ATSResult(BaseModel):
    overall_score: float = 0.0
    factor_scores: FactorScores = Field(default_factory=FactorScores)
    matching_keywords: List[str] = Field(default_factory=list)
    missing_keywords: List[str] = Field(default_factory=list)
    relevant_skills_found: List[str] = Field(default_factory=list)
    required_skills_missing: List[str] = Field(default_factory=list)
    experience_alignment: str = ""
    education_alignment: str = ""
    certification_alignment: str = ""
    formatting_issues: List[str] = Field(default_factory=list)
    improvement_recommendations: List[str] = Field(default_factory=list)


class RoadmapItem(BaseModel):
    skill: str
    priority: str = "High"  # High, Medium, Low
    importance: str = ""
    reason: str = ""
    topics: List[str] = Field(default_factory=list)
    suggested_resources: List[str] = Field(default_factory=list)
    suggested_project: str = ""


class SkillGapResult(BaseModel):
    strong_match: List[str] = Field(default_factory=list)
    partial_match: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    additional_skills: List[str] = Field(default_factory=list)
    roadmap: List[RoadmapItem] = Field(default_factory=list)


class InterviewQuestion(BaseModel):
    id: str = ""
    category: str = "Technical"  # Technical, Project-Based, Resume-Based, Behavioral, HR, Skill-Gap
    question: str = ""
    rationale: str = ""
    ideal_answer_hints: List[str] = Field(default_factory=list)


class MockAnswerEvaluation(BaseModel):
    question_id: str = ""
    question_text: str = ""
    user_answer: str = ""
    relevance_score: float = 0.0
    technical_correctness_score: float = 0.0
    completeness_score: float = 0.0
    clarity_score: float = 0.0
    overall_answer_score: float = 0.0
    feedback: str = ""
    strengths: List[str] = Field(default_factory=list)
    missing_key_points: List[str] = Field(default_factory=list)
    follow_up_question: Optional[str] = None


class ResumeImprovement(BaseModel):
    original_bullet: str
    suggested_bullet: str
    reason: str
    placeholder_note: Optional[str] = None


class CareerRecommendation(BaseModel):
    role_name: str
    match_percentage: float
    matching_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    recommended_next_steps: List[str] = Field(default_factory=list)


class ProjectRecommendation(BaseModel):
    title: str
    problem_statement: str
    skills_developed: List[str] = Field(default_factory=list)
    tech_stack: List[str] = Field(default_factory=list)
    difficulty: str = "Intermediate"  # Beginner, Intermediate, Advanced
    employability_reason: str = ""
    gap_skills_covered: List[str] = Field(default_factory=list)


class CategoryScore(BaseModel):
    category_name: str
    score: float
    max_score: float = 100.0


class IndustryReadinessResult(BaseModel):
    overall_score: float = 0.0
    category_scores: Dict[str, float] = Field(default_factory=dict)
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    actionable_improvement_plan: List[str] = Field(default_factory=list)


class ProfessionalProfileResult(BaseModel):
    professional_summary: str = ""
    linkedin_headline: str = ""
    linkedin_about: str = ""
    portfolio_about: str = ""
    professional_bio: str = ""
    github_description: str = ""
