# Building Career मार्ग: How I Built an Executive Multimodal AI Career Preparation & Intelligence Suite

**By Anurag Chowdhury**  
*Published on [Medium](https://medium.com/@anuragchowdhury19official)*  

---

> **Tagline:** *Apne Career ko do Raasta* (Give Your Career a Clear Path)  
> 🚀 **Live Web Application:** [career-marg.streamlit.app](https://career-marg.streamlit.app/)  
> 💻 **GitHub Repository:** [github.com/AnuragChowdhury/Career-Marg](https://github.com/AnuragChowdhury/Career-Marg)  
> 👤 **Author Medium Profile:** [@anuragchowdhury19official](https://medium.com/@anuragchowdhury19official)

---

## 📖 The Spark Behind Career मार्ग

Every job seeker has faced the frustration of the **"Black Box" Hiring Barrier**. 

You spend days tailoring your resume, applying for roles you are qualified for, only to receive instant automated rejection emails from Applicant Tracking Systems (ATS). When you ask traditional AI tools for help, you get generic resume advice or hallucinated experience summaries that sound impressive but fall apart during technical interviews.

Traditional job preparation tools suffer from three fundamental flaws:
1. **Opaque Black-Box Scoring**: Opaque ATS scanners give arbitrary match scores without explaining *why* or *how* the score was calculated.
2. **Generic AI Wrapper Responses**: Generic chatbots produce cookie-cutter interview questions and fake resume accomplishments.
3. **Fragmented Workflows**: Candidates must jump between separate tools for ATS checking, skill mapping, mock interviewing, and portfolio planning.

I set out to solve this problem by building **Career मार्ग** — an executive, end-to-end multimodal AI career intelligence suite designed to bridge the gap between candidate preparation and industry expectations.

---

## 🌟 What is Career मार्ग?

**Career मार्ग** is an executive-grade multimodal AI career preparation platform. Powered by **Mistral OCR 3**, fine-tuned LLM reasoning engines, and custom analytics, it provides candidates with a transparent, data-driven roadmap to job readiness.

Whether you upload a digital PDF, a scanned document, a Microsoft Word (`.docx`) file, a `.txt` file, an image resume, or paste raw text directly, Career मार्ग transforms unstructured resume data into actionable career intelligence.

![Executive Landing Page](https://raw.githubusercontent.com/AnuragChowdhury/Career-Marg/main/assets/screenshots/00_home.png)
*Figure 1: Executive Landing Page & Platform Blueprint of Career मार्ग*

---

## 🚀 Deep Dive: The 10 Core Capabilities of Career मार्ग

Let's walk through the full suite of engineering features that power Career मार्ग.

---

### 1. Multimodal Document Understanding & Mistral OCR 3

The first challenge in resume analysis is document layout extraction. Resumes come in various formats: multi-column PDFs, scanned images, table-heavy Word documents, and unformatted plain text.

Career मार्ग integrates **Mistral OCR 3** with PyMuPDF/PIL local fallback engines to extract structured Markdown, columns, and visual layout hierarchy. A custom Pydantic v2 schema parser extracts verified facts (Education, Work Experience, Technical Skills, Projects) while strictly separating candidate facts from AI suggestions.

![Resume Analysis](https://raw.githubusercontent.com/AnuragChowdhury/Career-Marg/main/assets/screenshots/01_resume_analysis.png)
*Figure 2: Multimodal Resume Upload & Document Layout Understanding*

---

### 2. Transparent 5-Factor ATS Compatibility Optimization

Instead of giving candidates a random black-box percentage score, Career मार्ग implements a **Transparent 5-Factor Scoring Algorithm**:

- **Required Technical Skills Overlap** (40% Weight)
- **Keyword Match Density** (25% Weight)
- **Work Experience Relevance** (15% Weight)
- **Education Alignment** (10% Weight)
- **Document Layout & Structure Quality** (10% Weight)

The engine details exact matching keywords, missing high-priority skills, formatting warnings (e.g., table cells or multi-column layout risks for legacy ATS), and provides action-verb bullet point rewrites with quantifiable placeholders.

![ATS Compatibility Auditor](https://raw.githubusercontent.com/AnuragChowdhury/Career-Marg/main/assets/screenshots/02_ats_analysis.png)
*Figure 3: ATS Compatibility Auditor with Transparent Sub-Factor Breakdown*

---

### 3. Competency Gap Analysis & 30-Day Learning Roadmap

Knowing what skills you lack is only half the battle — knowing how to acquire them is what gets you hired.

Career मार्ग categorizes candidate skills against target job descriptions into:
- ✅ **Strong Match**: Fully covered skills.
- ⚡ **Partial Match**: Related or foundational skills needing upgrade.
- ❌ **Missing Skills**: Critical role requirements absent from candidate profile.
- ➕ **Additional Skills**: Unique candidate strengths.

From this breakdown, the system generates a **Structured Executive 30-Day Action Plan** divided into 10-day sprints (Days 1–10: High-Priority Skill Foundation, Days 11–20: Specialized Topics, Days 21–30: Portfolio Integration & Job Readiness).

![Skill Gap Analysis](https://raw.githubusercontent.com/AnuragChowdhury/Career-Marg/main/assets/screenshots/03_skill_gap.png)
*Figure 4: Skill Gap Categorization & Executive 30-Day Skill Gap Action Plan*

---

### 4. Personalized Interview Question Generator

Generic interview prep questions like *"Tell me about yourself"* don't prepare candidates for modern technical evaluations.

Career मार्ग synthesizes non-generic, highly tailored questions across **6 Core Categories**:
1. **Technical Questions**: Tailored to candidate's exact tech stack.
2. **Project-Based Questions**: Deep-dives into specific candidate projects.
3. **Resume-Based Questions**: Inquiries on specific work experience accomplishments.
4. **Behavioral Questions**: Scenario-based evaluation grounded in the target role.
5. **HR & Cultural Fit Questions**: Role expectations and alignment.
6. **Skill-Gap Questions**: Testing candidate awareness of missing competency areas.

![Interview Preparation](https://raw.githubusercontent.com/AnuragChowdhury/Career-Marg/main/assets/screenshots/04_interview_prep.png)
*Figure 5: Personalized Interview Question Generator across 6 Categories*

---

### 5. Text-Based Interactive Mock Interview Simulator

The centerpiece of Career मार्ग's interview preparation is an interactive, one-question-at-a-time simulator. Candidates submit text answers to generated questions and receive real-time evaluation.

The scoring model evaluates responses across 4 weighted metrics:
- **Relevance** (25%)
- **Technical Depth** (35%)
- **Completeness** (20%)
- **Clarity & Communication** (20%)

![Mock Interview Simulator](https://raw.githubusercontent.com/AnuragChowdhury/Career-Marg/main/assets/screenshots/05_mock_interview.png)
*Figure 6: Interactive Text-Based Mock Interview Engine in Action*

---

### 6. Turn-by-Turn Feedback & Executive Interview Report

Upon completing mock interview sessions, candidates receive an **Executive End-of-Session Interview Report** featuring an overall readiness score (e.g., *Interview Ready — High Confidence*), key strengths, actionable recommendations, and turn-by-turn question breakdowns complete with dynamic follow-up questions.

![Mock Interview Report](https://raw.githubusercontent.com/AnuragChowdhury/Career-Marg/main/assets/screenshots/06_mock_report.png)
*Figure 7: Executive End-of-Session Interview Report & Turn-by-Turn Feedback*

---

### 7. Career Role Matching & Industry Readiness Score

Not sure which job title fits your background best? 

Career मार्ग evaluates candidate credentials against industry benchmark roles (e.g., *Machine Learning Engineer*, *Data Scientist*, *Full Stack AI Developer*) and computes an overall **Industry Readiness Score (0-100)** across 6 core weighted dimensions: Technical Skills, Project Quality, Work Experience, Resume Quality, Target Role Alignment, and Interview Readiness.

![Career Role Match](https://raw.githubusercontent.com/AnuragChowdhury/Career-Marg/main/assets/screenshots/07_career_recommendations.png)
*Figure 8: Career Role Match Recommendations & Industry Readiness Score Breakdown*

---

### 8. Targeted Portfolio Project Recommendation Engine

To close identified skill gaps, candidates need proof of capability. Career मार्ग suggests targeted, portfolio-ready project architectures designed specifically to cover missing skills.

Each recommendation includes:
- **Project Problem Statement**
- **Skills Covered from Identified Gap**
- **Employability Justification**
- **Complete Recommended Technology Stack**

![Portfolio Project Recommendations](https://raw.githubusercontent.com/AnuragChowdhury/Career-Marg/main/assets/screenshots/08_project_recommendations.png)
*Figure 9: Portfolio Project Recommendation Engine for Targeted Skill Gaps*

---

### 9. Grounded Professional Profile & Branding Generator

Recruiters evaluate candidates across multiple touchpoints. Career मार्ग generates grounded professional content tailored for:
- Resume Professional Summaries
- LinkedIn Headlines
- LinkedIn About Sections
- Portfolio Bios
- GitHub Profile READMEs

**Strict Grounding Guarantee**: All generated content is strictly derived from verified facts in the candidate profile — ensuring zero hallucinated experience or unearned credentials.

![Professional Profile Generator](https://raw.githubusercontent.com/AnuragChowdhury/Career-Marg/main/assets/screenshots/09_profile_generator.png)
*Figure 10: Grounded Professional Profile & Branding Generator*

---

### 10. Multi-Graph Executive SaaS Analytics Dashboard

To track progress over time, Career मार्ग features a multi-graph executive analytics dashboard equipped with:
- **Candidate Competency Radar Chart** (Experience, Technical Skills, Soft Skills, Domain Fit, Education, ATS Optimization)
- **Skill Match Ratio Breakdown Donut Chart**
- Overall ATS Score, Industry Readiness, and Verified Skills Metrics Grid

![Executive SaaS Dashboard](https://raw.githubusercontent.com/AnuragChowdhury/Career-Marg/main/assets/screenshots/10_saas_dashboard.png)
*Figure 11: Multi-Graph Executive Analytics SaaS Dashboard*

---

## 🛠️ Under the Hood: System Architecture & Tech Stack

Building Career मार्ग required a modular, decoupled software architecture designed for performance, reliability, and local state persistence.

![Technical Architecture](https://raw.githubusercontent.com/AnuragChowdhury/Career-Marg/main/assets/screenshots/11_technical_architecture.png)
*Figure 12: Technical Architecture & Core System Mechanics of Career मार्ग*

### Core Technology Stack:
- **UI Framework**: Streamlit with custom executive CSS design system, Plotly charts, and client-side single page navigation.
- **Service Business Logic Layer**: Decoupled Python services (`mistral_ocr_service`, `document_service`, `resume_parser`, `llm_service`, `ats_service`, `skill_gap_service`, `interview_service`, `career_service`, `recommendation_service`, `profile_service`).
- **Document OCR**: Mistral OCR 3 REST API with PyMuPDF (`fitz`), PIL, and `python-docx` fallback parsing engines.
- **Data Validation & Schemas**: Pydantic v2 schemas (`CandidateProfile`, `DocumentAnalysis`, `ATSResult`, `SkillGapResult`).
- **Persistence Layer**: SQLite database via SQLAlchemy ORM (`careermarg.db`) with automatic database session recovery.

---

## 💡 Key Lessons Learned & Engineering Takeaways

1. **Multimodal Fallbacks are Essential**: Never rely solely on a single cloud API. Building PyMuPDF, PIL, and `python-docx` local fallbacks ensured Career मार्ग runs smoothly even when cloud OCR APIs timeout or reach rate limits.
2. **State Persistence Across Page Navigation**: Single-page application state management in multi-page frameworks like Streamlit requires database fallback auto-loading to prevent state loss during browser refreshes or GET navigations.
3. **Fact Grounding Matters**: In career tools, hallucination is unacceptable. Enforcing strict Pydantic schemas and prompt grounding rules prevents AI models from inventing fake job titles or credentials.

---

## 🌍 Try Career मार्ग Today!

Career मार्ग is fully open-source and live for anyone to explore:

- 🚀 **Experience the Live Web App:** [career-marg.streamlit.app](https://career-marg.streamlit.app/)
- 💻 **Explore the Source Code on GitHub:** [github.com/AnuragChowdhury/Career-Marg](https://github.com/AnuragChowdhury/Career-Marg)
- 📬 **Connect with me on Medium:** [@anuragchowdhury19official](https://medium.com/@anuragchowdhury19official)

If you find this project helpful or inspiring for your own AI applications, feel free to star the GitHub repository or reach out!

---
*Apne Career ko do Raasta — Give your career the direction it deserves.*
