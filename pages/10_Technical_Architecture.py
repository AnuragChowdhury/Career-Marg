"""
Streamlit Page 10: System Architecture & Technical Specifications
Detailed technical breakdown of core engine pipelines, scoring algorithms, OCR fallbacks, LLM grounding, and Pydantic data schemas.
"""

import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
import os
import textwrap
from dotenv import load_dotenv

load_dotenv()

from utils.helpers import init_session_state, apply_custom_style

st.set_page_config(
    page_title="Technical Architecture - Career मार्ग",
    page_icon="🔬",
    layout="wide"
)

# Initialize Session State & Styling
init_session_state(st.session_state)
apply_custom_style(active_page="technical_architecture")

# Helper function to render HTML content cleanly
def render_html(html_str: str):
    if hasattr(st, "html"):
        st.html(textwrap.dedent(html_str))
    else:
        st.markdown(textwrap.dedent(html_str), unsafe_allow_html=True)

# Helper function to render SVG diagrams in an iframe container
def render_svg_card(svg_content: str, height: int = 560):
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            margin: 0;
            padding: 4px;
            background: transparent;
            font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
        .diagram-container {{
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: 1.2rem;
            box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03);
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        svg {{
            width: 100%;
            height: auto;
            max-height: {height - 40}px;
            display: block;
        }}
    </style>
    </head>
    <body>
    <div class="diagram-container">
        {textwrap.dedent(svg_content)}
    </div>
    </body>
    </html>
    """
    components.html(full_html, height=height, scrolling=False)

# ---------------------------------------------------------
# PAGE TITLE & HERO HEADER
# ---------------------------------------------------------
render_html("""
<div class="candidate-main-card">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
        <div>
            <div class="candidate-title" style="font-size: 1.6rem;">🔬 Technical Architecture & System Mechanics</div>
            <div style="color: #64748B; font-size: 0.95rem; font-weight: 500; margin-top: 0.2rem;">
                Comprehensive engineering documentation detailing multimodal OCR pipelines, fine-tuned Qwen2.5 LLM, 5-factor ATS algorithms, document layout analysis, and project recommendation mechanics.
            </div>
        </div>
        <div>
            <span class="badge-chip chip-purple" style="font-size: 0.9rem; padding: 0.4rem 0.9rem;">⚡ Visual Service Explainability Engine</span>
        </div>
    </div>
</div>
""")

# ---------------------------------------------------------
# TECHNICALITY NAVIGATION TABS
# ---------------------------------------------------------
tab_overview, tab_ocr, tab_ats, tab_skills, tab_llm = st.tabs([
    "🏗️ System Overview & Expanded Services",
    "📄 Document Understanding & Layout Engine",
    "🎯 ATS Audit & Scoring Formulas",
    "📊 Skill Gap & Project Recommendation Engine",
    "🤖 Fine-Tuned Qwen2.5 & LLM Mechanics"
])

# =========================================================
# TAB 1: SYSTEM OVERVIEW & ARCHITECTURE FLOW
# =========================================================
with tab_overview:
    render_html("""
    <h3 class='card-title'>📐 End-to-End System Architecture (Expanded Services Breakdown)</h3>
    <p style='color: #475569; font-size: 0.95rem;'>The Career मार्ग platform features an expanded core service layer depicting the internal sub-components of <code>document_service.py</code> and <code>recommendation_service.py</code>.</p>
    """)

    svg_architecture = """
<svg viewBox="0 0 1000 540" width="100%" height="auto">
<defs>
<linearGradient id="blueGrad" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#4F46E5" />
<stop offset="100%" stop-color="#3730A3" />
</linearGradient>
<linearGradient id="orangeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#FF5C00" />
<stop offset="100%" stop-color="#D43F00" />
</linearGradient>
<linearGradient id="emeraldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#10B981" />
<stop offset="100%" stop-color="#047857" />
</linearGradient>
<linearGradient id="purpleGrad" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#8B5CF6" />
<stop offset="100%" stop-color="#6D28D9" />
</linearGradient>
<linearGradient id="tealGrad" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#0E7490" />
<stop offset="100%" stop-color="#155E75" />
</linearGradient>
<filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
<feDropShadow dx="0" dy="4" stdDeviation="4" flood-opacity="0.08"/>
</filter>
</defs>

<!-- Layer Backgrounds -->
<rect x="20" y="15" width="960" height="65" rx="12" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="2" />
<rect x="20" y="95" width="960" height="85" rx="12" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="2" />
<rect x="20" y="195" width="960" height="245" rx="12" fill="#FAF5FF" stroke="#E9D5FF" stroke-width="2" />
<rect x="20" y="455" width="960" height="65" rx="12" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="2" />

<!-- Layer Titles -->
<text x="35" y="38" font-size="11" font-weight="bold" fill="#64748B">UI LAYER (Streamlit Multi-Page Framework)</text>
<text x="35" y="115" font-size="11" font-weight="bold" fill="#475569">INGESTION &amp; VALIDATION LAYER</text>
<text x="35" y="215" font-size="11" font-weight="bold" fill="#6B21A8">CORE SERVICE BUSINESS LOGIC LAYER (EXPANDED MECHANICS)</text>
<text x="35" y="475" font-size="11" font-weight="bold" fill="#15803D">PERSISTENCE &amp; REASONING LAYER</text>

<!-- UI Components -->
<rect x="35" y="42" width="130" height="28" rx="6" fill="#FFFFFF" stroke="#CBD5E1" filter="url(#shadow)"/>
<text x="100" y="60" font-size="10" font-weight="bold" text-anchor="middle" fill="#1E293B">Resume Upload</text>

<rect x="180" y="42" width="130" height="28" rx="6" fill="#FFFFFF" stroke="#CBD5E1" filter="url(#shadow)"/>
<text x="245" y="60" font-size="10" font-weight="bold" text-anchor="middle" fill="#1E293B">ATS Auditor</text>

<rect x="325" y="42" width="130" height="28" rx="6" fill="#FFFFFF" stroke="#CBD5E1" filter="url(#shadow)"/>
<text x="390" y="60" font-size="10" font-weight="bold" text-anchor="middle" fill="#1E293B">Skill Gap View</text>

<rect x="470" y="42" width="130" height="28" rx="6" fill="#FFFFFF" stroke="#CBD5E1" filter="url(#shadow)"/>
<text x="535" y="60" font-size="10" font-weight="bold" text-anchor="middle" fill="#1E293B">Interview Prep</text>

<rect x="615" y="42" width="130" height="28" rx="6" fill="#FFFFFF" stroke="#CBD5E1" filter="url(#shadow)"/>
<text x="680" y="60" font-size="10" font-weight="bold" text-anchor="middle" fill="#1E293B">Mock Simulator</text>

<rect x="760" y="42" width="205" height="28" rx="6" fill="url(#orangeGrad)" filter="url(#shadow)"/>
<text x="862" y="60" font-size="10" font-weight="bold" text-anchor="middle" fill="#FFFFFF">Executive Dashboard &amp; Tech Specs</text>

<!-- Ingestion Cards -->
<rect x="120" y="122" width="220" height="40" rx="8" fill="url(#blueGrad)" filter="url(#shadow)"/>
<text x="230" y="146" font-size="11" font-weight="bold" text-anchor="middle" fill="#FFFFFF">Mistral OCR 3 API / PyMuPDF</text>

<line x1="340" y1="142" x2="410" y2="142" stroke="#4F46E5" stroke-width="3" stroke-dasharray="5,5" />

<rect x="410" y="122" width="240" height="40" rx="8" fill="url(#orangeGrad)" filter="url(#shadow)"/>
<text x="530" y="146" font-size="11" font-weight="bold" text-anchor="middle" fill="#FFFFFF">Pydantic v2 (CandidateProfile)</text>

<!-- Standard Services Row -->
<rect x="40" y="230" width="160" height="36" rx="6" fill="#FFFFFF" stroke="#DDD6FE" stroke-width="2" filter="url(#shadow)"/>
<text x="120" y="252" font-size="11" font-weight="bold" text-anchor="middle" fill="#5B21B6">ats_service.py</text>

<rect x="220" y="230" width="160" height="36" rx="6" fill="#FFFFFF" stroke="#DDD6FE" stroke-width="2" filter="url(#shadow)"/>
<text x="300" y="252" font-size="11" font-weight="bold" text-anchor="middle" fill="#5B21B6">skill_gap_service.py</text>

<rect x="400" y="230" width="160" height="36" rx="6" fill="#FFFFFF" stroke="#DDD6FE" stroke-width="2" filter="url(#shadow)"/>
<text x="480" y="252" font-size="11" font-weight="bold" text-anchor="middle" fill="#5B21B6">interview_service.py</text>

<rect x="580" y="230" width="160" height="36" rx="6" fill="#FFFFFF" stroke="#DDD6FE" stroke-width="2" filter="url(#shadow)"/>
<text x="660" y="252" font-size="11" font-weight="bold" text-anchor="middle" fill="#5B21B6">career_service.py</text>

<rect x="760" y="230" width="180" height="36" rx="6" fill="#FFFFFF" stroke="#DDD6FE" stroke-width="2" filter="url(#shadow)"/>
<text x="850" y="252" font-size="11" font-weight="bold" text-anchor="middle" fill="#5B21B6">profile_service.py</text>

<!-- EXPANDED SERVICE BOX 1: document_service.py -->
<rect x="40" y="280" width="440" height="145" rx="10" fill="#F0FDFA" stroke="#0D9488" stroke-width="2" filter="url(#shadow)"/>
<text x="260" y="302" font-size="12" font-weight="bold" text-anchor="middle" fill="#0F766E">📄 document_service.py (Layout &amp; Readability Engine)</text>
<line x1="55" y1="310" x2="465" y2="310" stroke="#CCFBF1" stroke-width="1.5"/>

<!-- Internal Sub-modules of document_service -->
<rect x="55" y="320" width="125" height="40" rx="6" fill="#FFFFFF" stroke="#14B8A6"/>
<text x="117" y="337" font-size="9" font-weight="bold" text-anchor="middle" fill="#0F766E">1. File Classifier</text>
<text x="117" y="351" font-size="8" text-anchor="middle" fill="#64748B">PDF, Image, Scanned</text>

<rect x="195" y="320" width="130" height="40" rx="6" fill="#FFFFFF" stroke="#14B8A6"/>
<text x="260" y="337" font-size="9" font-weight="bold" text-anchor="middle" fill="#0F766E">2. PyMuPDF Inspector</text>
<text x="260" y="351" font-size="8" text-anchor="middle" fill="#64748B">X-Variance &amp; Blocks</text>

<rect x="340" y="320" width="125" height="40" rx="6" fill="#FFFFFF" stroke="#14B8A6"/>
<text x="402" y="337" font-size="9" font-weight="bold" text-anchor="middle" fill="#0F766E">3. Table Detector</text>
<text x="402" y="351" font-size="8" text-anchor="middle" fill="#64748B">Drawing Vectors &amp; Delims</text>

<rect x="55" y="370" width="410" height="42" rx="6" fill="#CCFBF1" stroke="#0D9488"/>
<text x="260" y="388" font-size="9" font-weight="bold" text-anchor="middle" fill="#115E59">4. Layout Quality (0-100) &amp; Readability Warning Metric</text>
<text x="260" y="401" font-size="8" text-anchor="middle" fill="#134E4A">Calculates column penalty, page overflow (-15), &amp; word-length readability</text>

<!-- EXPANDED SERVICE BOX 2: recommendation_service.py -->
<rect x="500" y="280" width="440" height="145" rx="10" fill="#FFF7ED" stroke="#EA580C" stroke-width="2" filter="url(#shadow)"/>
<text x="720" y="302" font-size="12" font-weight="bold" text-anchor="middle" fill="#C2410C">🎯 recommendation_service.py (Project Generator)</text>
<line x1="515" y1="310" x2="925" y2="310" stroke="#FFEDD5" stroke-width="1.5"/>

<!-- Internal Sub-modules of recommendation_service -->
<rect x="515" y="320" width="125" height="40" rx="6" fill="#FFFFFF" stroke="#F97316"/>
<text x="577" y="337" font-size="9" font-weight="bold" text-anchor="middle" fill="#C2410C">1. Skill Gap Slicing</text>
<text x="577" y="351" font-size="8" text-anchor="middle" fill="#64748B">Extract Missing Gaps</text>

<rect x="655" y="320" width="130" height="40" rx="6" fill="#FFFFFF" stroke="#F97316"/>
<text x="720" y="337" font-size="9" font-weight="bold" text-anchor="middle" fill="#C2410C">2. Pattern Templates</text>
<text x="720" y="351" font-size="8" text-anchor="middle" fill="#64748B">Microservices / MLOps</text>

<rect x="800" y="320" width="125" height="40" rx="6" fill="#FFFFFF" stroke="#F97316"/>
<text x="862" y="337" font-size="9" font-weight="bold" text-anchor="middle" fill="#C2410C">3. Employability Reason</text>
<text x="862" y="351" font-size="8" text-anchor="middle" fill="#64748B">Recruiter Justification</text>

<rect x="515" y="370" width="410" height="42" rx="6" fill="#FFEDD5" stroke="#EA580C"/>
<text x="720" y="388" font-size="9" font-weight="bold" text-anchor="middle" fill="#9A3412">4. 3-Tier Portfolio Project Schema Output</text>
<text x="720" y="401" font-size="8" text-anchor="middle" fill="#7C2D12">Generates Problem Statements, Tech Stack, &amp; Difficulty (Beginner to Advanced)</text>

<!-- Persistence & LLM Cards -->
<rect x="140" y="470" width="340" height="38" rx="8" fill="url(#purpleGrad)" filter="url(#shadow)"/>
<text x="310" y="493" font-size="11" font-weight="bold" text-anchor="middle" fill="#FFFFFF">Fine-Tuned Qwen2.5-0.5B (llm_service.py)</text>

<rect x="550" y="470" width="310" height="38" rx="8" fill="url(#emeraldGrad)" filter="url(#shadow)"/>
<text x="705" y="493" font-size="12" font-weight="bold" text-anchor="middle" fill="#FFFFFF">SQLite Database (data/database.py)</text>
</svg>
"""
    render_svg_card(svg_architecture, height=570)

    col1, col2, col3 = st.columns(3)
    with col1:
        render_html("""
        <div class="dashboard-card">
            <h4 style="color: #1E293B; margin-top:0;">⚡ Ingestion & OCR Stack</h4>
            <ul style="color: #475569; font-size: 0.9rem; line-height: 1.6; margin-bottom:0; padding-left: 1.2rem;">
                <li><b>Mistral OCR 3 API</b>: High-fidelity layout, markdown table & text extraction.</li>
                <li><b>PyMuPDF (fitz)</b>: Native digital PDF layout parser fallback.</li>
                <li><b>PIL / pdfplumber</b>: Image & scanned document pre-processing.</li>
            </ul>
        </div>
        """)

    with col2:
        render_html("""
        <div class="dashboard-card">
            <h4 style="color: #1E293B; margin-top:0;">🤖 Fine-Tuned Qwen2.5 Model</h4>
            <ul style="color: #475569; font-size: 0.9rem; line-height: 1.6; margin-bottom:0; padding-left: 1.2rem;">
                <li><b>Base Model</b>: Qwen2.5-0.5B-Instruct (4-bit GGUF).</li>
                <li><b>Fine-Tuning</b>: Unsloth LoRA on Google Colab (T4 GPU).</li>
                <li><b>Domain Tasks</b>: Bullet rewriting, roadmaps & grounded bios.</li>
            </ul>
        </div>
        """)

    with col3:
        render_html("""
        <div class="dashboard-card">
            <h4 style="color: #1E293B; margin-top:0;">💾 Storage & UI Presentation</h4>
            <ul style="color: #475569; font-size: 0.9rem; line-height: 1.6; margin-bottom:0; padding-left: 1.2rem;">
                <li><b>SQLAlchemy ORM</b>: SQLite database persistence (<code>data/careermarg.db</code>).</li>
                <li><b>Streamlit Framework</b>: Executive dashboard with custom CSS design tokens.</li>
                <li><b>Plotly & SVG</b>: Dynamic interactive gauge, radar, and trend charts.</li>
            </ul>
        </div>
        """)

# =========================================================
# TAB 2: MULTIMODAL OCR & RESUME PARSER
# =========================================================
with tab_ocr:
    render_html("""
    <h3 class='card-title'>📄 Document Service Layout Engine & Visual Flowchart</h3>
    <p style='color: #475569; font-size: 0.95rem;'>Visual step-by-step execution mechanics depicting how <code>document_service.py</code> classifies document formats, inspects layout coordinates, and calculates quality scores.</p>
    """)

    # Interactive Step-by-Step Flowchart SVG for document_service.py
    svg_document_flow = """
<svg viewBox="0 0 960 260" width="100%" height="auto">
<defs>
<marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M 0 0 L 10 5 L 0 10 z" fill="#0D9488"/>
</marker>
</defs>

<!-- Step 1: Input Stream -->
<rect x="20" y="70" width="140" height="70" rx="8" fill="#EFF6FF" stroke="#3B82F6" stroke-width="2"/>
<text x="90" y="95" font-size="11" font-weight="bold" text-anchor="middle" fill="#1E3A8A">1. Raw Bytes Input</text>
<text x="90" y="112" font-size="9" text-anchor="middle" fill="#2563EB">PDF, PNG, JPG Bytes</text>

<line x1="160" y1="105" x2="195" y2="105" stroke="#0D9488" stroke-width="2.5" marker-end="url(#arrow)"/>

<!-- Step 2: File Classifier -->
<rect x="200" y="70" width="150" height="70" rx="8" fill="#F0FDF4" stroke="#16A34A" stroke-width="2"/>
<text x="275" y="95" font-size="11" font-weight="bold" text-anchor="middle" fill="#14532D">2. File Classifier</text>
<text x="275" y="112" font-size="9" text-anchor="middle" fill="#15803D">Ext check & char count</text>
<text x="275" y="124" font-size="8" text-anchor="middle" fill="#166534">(<100 chars = Scanned)</text>

<line x1="350" y1="105" x2="385" y2="105" stroke="#0D9488" stroke-width="2.5" marker-end="url(#arrow)"/>

<!-- Step 3: PyMuPDF Block Inspector -->
<rect x="390" y="70" width="160" height="70" rx="8" fill="#FAF5FF" stroke="#9333EA" stroke-width="2"/>
<text x="470" y="95" font-size="11" font-weight="bold" text-anchor="middle" fill="#581C87">3. PyMuPDF Blocks</text>
<text x="470" y="112" font-size="9" text-anchor="middle" fill="#7E22CE">page.get_text("blocks")</text>
<text x="470" y="124" font-size="8" text-anchor="middle" fill="#6B21A8">X0 variance column check</text>

<line x1="550" y1="105" x2="585" y2="105" stroke="#0D9488" stroke-width="2.5" marker-end="url(#arrow)"/>

<!-- Step 4: Table Detector -->
<rect x="590" y="70" width="150" height="70" rx="8" fill="#FFF7ED" stroke="#EA580C" stroke-width="2"/>
<text x="665" y="95" font-size="11" font-weight="bold" text-anchor="middle" fill="#7C2D12">4. Vector Table Check</text>
<text x="665" y="112" font-size="9" text-anchor="middle" fill="#C2410C">get_drawings() > 15</text>
<text x="665" y="124" font-size="8" text-anchor="middle" fill="#9A3412">ASCII border regex</text>

<line x1="740" y1="105" x2="775" y2="105" stroke="#0D9488" stroke-width="2.5" marker-end="url(#arrow)"/>

<!-- Step 5: Output DocumentAnalysis -->
<rect x="780" y="70" width="160" height="70" rx="8" fill="#CCFBF1" stroke="#0D9488" stroke-width="2"/>
<text x="860" y="95" font-size="11" font-weight="bold" text-anchor="middle" fill="#115E59">5. DocumentAnalysis</text>
<text x="860" y="112" font-size="9" text-anchor="middle" fill="#0D9488">Quality (0-100), Warnings</text>
<text x="860" y="124" font-size="8" text-anchor="middle" fill="#134E4A">& Readability Score</text>
</svg>
"""
    render_svg_card(svg_document_flow, height=270)

    # Detailed Document Service Technical Specification Card
    render_html("""
    <div class="dashboard-card" style="border-left: 4px solid #0D9488;">
        <h4 style="color: #0F766E; margin-top: 0;">🔬 Mechanics of <code>document_service.py</code></h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; color: #334155; font-size: 0.88rem;">
            <div>
                <b>1. File Classification Engine:</b><br/>
                Detects whether file extension is PNG/JPG or PDF. For PDFs, it evaluates extracted character length relative to page count to differentiate digital PDFs from scanned image PDFs (<100 chars).
            </div>
            <div>
                <b>2. PyMuPDF Coordinate Inspector:</b><br/>
                Calls <code>page.get_text("blocks")</code> to extract bounding box coordinates $(X_0, Y_0, X_1, Y_1)$. Computes the variance of starting $X$ positions across text blocks to detect multi-column layouts.
            </div>
            <div>
                <b>3. Table & Vector Graphic Detector:</b><br/>
                Inspects <code>page.get_drawings()</code> for vector rectangles/lines (>15 paths) and searches raw text for ASCII table borders (<code>│</code>, <code>┌</code>, <code>|</code>).
            </div>
            <div>
                <b>4. Layout Quality Penalty Formula:</b><br/>
                Baseline 90.0 score with explicit deduction rules:
                Multi-column (-10), Tables (-10), Page Count > 2 (-15), Scanned Image PDF (-15). Includes average word-length readability metric.
            </div>
        </div>
    </div>
    """)

# =========================================================
# TAB 3: ATS AUDIT & SCORING FORMULAS
# =========================================================
with tab_ats:
    render_html("""
    <h3 class='card-title'>🎯 Transparent 5-Factor ATS Scoring & Qwen Bullet Rewriter</h3>
    <p style='color: #475569; font-size: 0.95rem;'>The ATS Auditor calculates compatibility using a transparent 5-factor weighted algorithm, paired with our fine-tuned Qwen model for quantifiable bullet rewriting.</p>
    <div class="dashboard-card" style="background: #FAF5FF !important; border-left: 5px solid #8B5CF6 !important;">
        <h4 style="color: #5B21B6; margin-top:0;">🧮 Overall ATS Compatibility Formula</h4>
        <div style="font-size: 1.15rem; font-weight: 700; color: #4C1D95; padding: 0.5rem 0; font-family: monospace;">
            ATS Score = (0.40 × S<sub>skills</sub>) + (0.25 × S<sub>keywords</sub>) + (0.15 × S<sub>experience</sub>) + (0.10 × S<sub>education</sub>) + (0.10 × S<sub>structure</sub>)
        </div>
    </div>
    """)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        render_html("""<div class="metric-card">
            <div class="metric-title">1. Required Skills</div>
            <div class="metric-value" style="color: #FF5C00;">40%</div>
            <p style="font-size: 0.78rem; color: #64748B; margin-top:0.4rem;">Direct set intersection of candidate skills vs JD required skills.</p>
        </div>""")
    with col2:
        render_html("""<div class="metric-card metric-card-2">
            <div class="metric-title">2. Keyword Overlap</div>
            <div class="metric-value" style="color: #10B981;">25%</div>
            <p style="font-size: 0.78rem; color: #64748B; margin-top:0.4rem;">TF-IDF word token match across entire job description body.</p>
        </div>""")
    with col3:
        render_html("""<div class="metric-card metric-card-3">
            <div class="metric-title">3. Experience Fit</div>
            <div class="metric-value" style="color: #F59E0B;">15%</div>
            <p style="font-size: 0.78rem; color: #64748B; margin-top:0.4rem;">Linear ratio of verified years vs required years of experience.</p>
        </div>""")
    with col4:
        render_html("""<div class="metric-card metric-card-4">
            <div class="metric-title">4. Education Match</div>
            <div class="metric-value" style="color: #8B5CF6;">10%</div>
            <p style="font-size: 0.78rem; color: #64748B; margin-top:0.4rem;">Degree qualification hierarchy matching (BS/MS/PhD).</p>
        </div>""")
    with col5:
        render_html("""<div class="metric-card">
            <div class="metric-title">5. Layout Quality</div>
            <div class="metric-value" style="color: #0284C7;">10%</div>
            <p style="font-size: 0.78rem; color: #64748B; margin-top:0.4rem;">Document structural cleanliness & OCR parser confidence score.</p>
        </div>""")

    render_html("""
    <br/>
    <div class="dashboard-card" style="border-left: 4px solid #FF5C00;">
        <h4 style="color: #D43F00; margin-top: 0;">🔥 Qwen Fine-Tuned Feature: Quantifiable Bullet Point Rewrite Engine</h4>
        <p style="color: #475569; font-size: 0.9rem;">
            The ATS service uses the fine-tuned <b>Qwen2.5-0.5B-Instruct</b> model to rewrite weak resume bullet points into high-impact, ATS-optimized action bullets with metric placeholders:
        </p>
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; padding: 0.9rem; border-radius: 8px; font-family: monospace; font-size: 0.85rem;">
            <span style="color: #DC2626;">❌ Original Weak Bullet:</span> "Worked on machine learning model for customer sentiment."<br/>
            <span style="color: #16A34A; font-weight: bold;">✅ Fine-Tuned Qwen Output:</span> "Engineered and deployed an NLP sentiment classification model using PyTorch, improving prediction accuracy by <b>[X%]</b> and reducing inference latency by <b>[Y ms]</b>."
        </div>
    </div>
    """)

# =========================================================
# TAB 4: SKILL GAP MATRIX & CAREER MATCHING
# =========================================================
with tab_skills:
    render_html("""
    <h3 class='card-title'>📊 Recommendation Engine Flowchart & Technical Mechanics</h3>
    <p style='color: #475569; font-size: 0.95rem;'>Visual step-by-step execution mechanics depicting how <code>recommendation_service.py</code> slices missing skills and generates 3-tier portfolio architectures.</p>
    """)

    # Interactive Step-by-Step Flowchart SVG for recommendation_service.py
    svg_recommendation_flow = """
<svg viewBox="0 0 960 260" width="100%" height="auto">
<defs>
<marker id="arrowOrange" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M 0 0 L 10 5 L 0 10 z" fill="#EA580C"/>
</marker>
</defs>

<!-- Step 1: Missing Skills Input -->
<rect x="20" y="70" width="150" height="70" rx="8" fill="#FFF7ED" stroke="#EA580C" stroke-width="2"/>
<text x="95" y="95" font-size="11" font-weight="bold" text-anchor="middle" fill="#7C2D12">1. Missing Skills Vector</text>
<text x="95" y="112" font-size="9" text-anchor="middle" fill="#C2410C">Docker, MLOps, FastAPI</text>

<line x1="170" y1="105" x2="205" y2="105" stroke="#EA580C" stroke-width="2.5" marker-end="url(#arrowOrange)"/>

<!-- Step 2: Gap Vector Slicer -->
<rect x="210" y="70" width="150" height="70" rx="8" fill="#FEF3C7" stroke="#D97706" stroke-width="2"/>
<text x="285" y="95" font-size="11" font-weight="bold" text-anchor="middle" fill="#78350F">2. Gap Vector Slicer</text>
<text x="285" y="112" font-size="9" text-anchor="middle" fill="#B45309">Splits into Tier 1,2,3</text>

<line x1="360" y1="105" x2="395" y2="105" stroke="#EA580C" stroke-width="2.5" marker-end="url(#arrowOrange)"/>

<!-- Step 3: Pattern Generator -->
<rect x="400" y="70" width="170" height="70" rx="8" fill="#F0FDF4" stroke="#16A34A" stroke-width="2"/>
<text x="485" y="95" font-size="11" font-weight="bold" text-anchor="middle" fill="#14532D">3. Architecture Engine</text>
<text x="485" y="112" font-size="9" text-anchor="middle" fill="#15803D">Microservices / MLOps</text>
<text x="485" y="124" font-size="8" text-anchor="middle" fill="#166534">Dashboards & Tech Stack</text>

<line x1="570" y1="105" x2="605" y2="105" stroke="#EA580C" stroke-width="2.5" marker-end="url(#arrowOrange)"/>

<!-- Step 4: Employability Reasoner -->
<rect x="610" y="70" width="160" height="70" rx="8" fill="#EFF6FF" stroke="#2563EB" stroke-width="2"/>
<text x="690" y="95" font-size="11" font-weight="bold" text-anchor="middle" fill="#1E3A8A">4. Recruiter Reasoner</text>
<text x="690" y="112" font-size="9" text-anchor="middle" fill="#1D4ED8">Attaches Employability</text>
<text x="690" y="124" font-size="8" text-anchor="middle" fill="#1E40AF">Justification & Difficulty</text>

<line x1="770" y1="105" x2="805" y2="105" stroke="#EA580C" stroke-width="2.5" marker-end="url(#arrowOrange)"/>

<!-- Step 5: Output Schema -->
<rect x="810" y="70" width="135" height="70" rx="8" fill="#FFEDD5" stroke="#EA580C" stroke-width="2"/>
<text x="877" y="95" font-size="11" font-weight="bold" text-anchor="middle" fill="#9A3412">5. Output List</text>
<text x="877" y="112" font-size="9" text-anchor="middle" fill="#C2410C">ProjectRecommendation</text>
<text x="877" y="124" font-size="8" text-anchor="middle" fill="#7C2D12">Pydantic Schemas</text>
</svg>
"""
    render_svg_card(svg_recommendation_flow, height=270)

    # Detailed Recommendation Service Technical Specification Card
    render_html("""
    <div class="dashboard-card" style="border-left: 4px solid #EA580C;">
        <h4 style="color: #C2410C; margin-top: 0;">🔬 Mechanics of <code>recommendation_service.py</code></h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; color: #334155; font-size: 0.88rem;">
            <div>
                <b>1. Skill Gap Vector Mapping:</b><br/>
                Extracts missing technical skills identified by <code>skill_gap_service.py</code> and slices them into targeted sub-vectors to assign to specific project architectures.
            </div>
            <div>
                <b>2. Portfolio Architecture Templates:</b><br/>
                Maps skill gaps into 3 enterprise architecture tiers:
                <ul>
                    <li><i>Tier 1 (Microservices)</i>: Docker, REST APIs, FastAPI endpoints.</li>
                    <li><i>Tier 2 (MLOps Pipeline)</i>: MLflow tracking, CI/CD, model drift monitoring.</li>
                    <li><i>Tier 3 (Full Stack Dashboard)</i>: Streamlit, Plotly, document schema Q&A.</li>
                </ul>
            </div>
            <div>
                <b>3. Employability Justification Generator:</b><br/>
                Attaches a recruiter employability reason to each project recommendation, explaining why building this specific project proves candidate job readiness.
            </div>
        </div>
    </div>
    """)

# =========================================================
# TAB 5: FINE-TUNED QWEN2.5 & LLM MECHANICS
# =========================================================
with tab_llm:
    render_html("""
    <h3 class='card-title'>🤖 Fine-Tuned Qwen2.5-0.5B-Instruct Model Specifications</h3>
    <p style='color: #475569; font-size: 0.95rem;'>Detailed technical specification of our domain-adapted small LLM fine-tuned using Unsloth, LoRA, and GGUF quantization.</p>
    """)

    # Qwen Hyperparameters Grid
    col1, col2 = st.columns(2)
    with col1:
        render_html("""
        <div class="dashboard-card">
            <h4 style="color: #1E293B;">🎛️ Training Hyperparameters & Setup</h4>
            <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; color: #334155;">
                <tr style="border-bottom: 1px solid #E2E8F0;"><td style="padding: 0.4rem 0;"><b>Base Model</b></td><td><code>unsloth/Qwen2.5-0.5B-Instruct-bnb-4bit</code></td></tr>
                <tr style="border-bottom: 1px solid #E2E8F0;"><td style="padding: 0.4rem 0;"><b>Fine-Tuning Framework</b></td><td>Unsloth + HuggingFace TRL (<code>SFTTrainer</code>)</td></tr>
                <tr style="border-bottom: 1px solid #E2E8F0;"><td style="padding: 0.4rem 0;"><b>LoRA Rank / Alpha</b></td><td>r = 16, lora_alpha = 16</td></tr>
                <tr style="border-bottom: 1px solid #E2E8F0;"><td style="padding: 0.4rem 0;"><b>Target Modules</b></td><td>q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj</td></tr>
                <tr style="border-bottom: 1px solid #E2E8F0;"><td style="padding: 0.4rem 0;"><b>Learning Rate</b></td><td>2e-4 (AdamW, Warmup = 5 steps)</td></tr>
                <tr style="border-bottom: 1px solid #E2E8F0;"><td style="padding: 0.4rem 0;"><b>Hardware Platform</b></td><td>Google Colab (Free T4 GPU, FP16/BF16 mixed precision)</td></tr>
                <tr><td style="padding: 0.4rem 0;"><b>Quantization Format</b></td><td>GGUF 4-Bit <code>Q4_K_M</code> (Local CPU/GPU inference via <code>llama-cpp</code>)</td></tr>
            </table>
        </div>
        """)

    with col2:
        render_html("""
        <div class="dashboard-card">
            <h4 style="color: #1E293B;">🛡️ Qwen Fine-Tuned Features Matrix</h4>
            <ul style="color: #334155; font-size: 0.88rem; line-height: 1.7; padding-left: 1.2rem;">
                <li><b>Factual Executive Profile Synthesis (<code>profile_service.py</code>)</b>:<br/>Fine-tuned to synthesize LinkedIn headlines, bios, and summaries directly from candidate experience facts without credential fabrication.</li>
                <li><b>Quantifiable Bullet Rewriting (<code>ats_service.py</code>)</b>:<br/>Fine-tuned to transform vague job descriptions into action-verb bullet points with metric placeholders.</li>
                <li><b>30-Day Skill Gap Action Plans (<code>skill_gap_service.py</code>)</b>:<br/>Fine-tuned to break down missing technical skills into phased 10-day acquisition milestones.</li>
                <li><b>Interactive Mock Interview Grading (<code>interview_service.py</code>)</b>:<br/>Instruction-tuned for 4-dimension rubric scoring (Relevance, Correctness, Completeness, Clarity).</li>
            </ul>
        </div>
        """)

    st.info("💡 **Colab Notebook:** To re-train or inspect the fine-tuning script, open [`notebooks/Fine_Tune_CareerGPT.ipynb`](file:///d:/MS_AI_ML/Trimester%204/LLM/CIA%203/notebooks/Fine_Tune_CareerGPT.ipynb) or run `notebooks/fine_tune_colab.py`.")
