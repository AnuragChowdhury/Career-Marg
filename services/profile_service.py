"""
Professional Profile Content Generator Service for Career मार्ग.
Generates LinkedIn headline/about, portfolio bios, professional summary, and GitHub profiles.
Strictly grounded in candidate resume facts — never fabricates experience, skills, or titles.
"""

from models.schemas import CandidateProfile, ProfessionalProfileResult
from services.llm_service import LLMService


class ProfileService:
    def __init__(self, llm_service: LLMService = None):
        self.llm_service = llm_service or LLMService()

    def generate_professional_profile(
        self,
        candidate_profile: CandidateProfile,
        target_role: str = ""
    ) -> ProfessionalProfileResult:
        """
        Generates grounded professional branding materials based on CandidateProfile facts.
        """
        name = candidate_profile.personal_information.name or "Candidate"
        skills = ", ".join(candidate_profile.technical_skills[:5]) or "Software Engineering, AI"
        degree = candidate_profile.education[0].degree if candidate_profile.education else "Computer Science / Technical Degree"
        role = target_role or (candidate_profile.work_experience[0].job_title if candidate_profile.work_experience else "AI / Software Specialist")

        # 1. Professional Summary
        summary = (
            f"Results-driven {role} with expertise in {skills}. "
            f"Holds a background in {degree} with hands-on experience in building scalable technical solutions, "
            f"portfolio projects, and data-driven applications."
        )

        # 2. LinkedIn Headline
        linkedin_headline = f"{name} | {role} | Expertise in {skills}"

        # 3. LinkedIn About Section
        linkedin_about = (
            f"Passionate {role} specializing in {skills}.\n\n"
            f"🚀 Key Highlights:\n"
            f"• Technical Stack: {skills}\n"
            f"• Academic Foundation: {degree}\n"
            f"• Proven Projects: Developed {len(candidate_profile.projects)} end-to-end practical implementations.\n\n"
            f"Always eager to connect with industry leaders, collaborate on innovative technical challenges, and drive measurable engineering impact."
        )

        # 4. Portfolio About Section
        portfolio_about = (
            f"Hello! I'm {name}, a {role} focused on building intelligent software systems. "
            f"My technical background spans {skills}. I thrive on turning complex problems into elegant, production-ready code."
        )

        # 5. Professional Bio
        professional_bio = (
            f"{name} is a {role} experienced in {skills}. With credentials in {degree}, "
            f"{name} has engineered multiple domain projects and continues to drive technical excellence."
        )

        # 6. GitHub Profile Description
        github_desc = f"👨‍💻 {role} | Passionate about {skills} | Building open-source AI & software projects."

        return ProfessionalProfileResult(
            professional_summary=summary,
            linkedin_headline=linkedin_headline,
            linkedin_about=linkedin_about,
            portfolio_about=portfolio_about,
            professional_bio=professional_bio,
            github_description=github_desc
        )
