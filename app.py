"""
Career मार्ग: Multimodal AI Career Preparation & Intelligence Platform
Main Landing Dashboard & System Overview Page
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import os
import numpy as np
from dotenv import load_dotenv

load_dotenv()

from utils.helpers import init_session_state, apply_custom_style

st.set_page_config(
    page_title="Career मार्ग - Executive Career Intelligence Platform",
    page_icon="assets/logo_icon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
init_session_state(st.session_state)

# ---------------------------------------------------------
# RENDER PURE WHITE ISOMETRIC MARKETING HERO LANDING PAGE (SIDEBAR HIDDEN)
# ---------------------------------------------------------
apply_custom_style(active_page="home")

# Hero Content Grid
col_left, col_right = st.columns([1.1, 1.3], gap="large")

with col_left:
    st.markdown("""<div style="margin-top: 3.5rem;">
<h1 class="hero-main-title">Career मार्ग</h1>
<p class="hero-tagline" style="font-size: 1.35rem; font-weight: 600; color: #4F46E5; margin-bottom: 0.75rem;">Apne Career ko do Raasta</p>
<p class="hero-desc-para">Career मार्ग is an executive career intelligence suite designed to parse resumes using advanced OCR, analyze ATS compatibility metrics, identify critical skill gaps, and simulate active strategy panels.</p>
<div style="margin-top: 1.2rem; margin-bottom: 1.8rem;">
  <a href="https://medium.com/@anuragchowdhury19official/building-career-%E0%A4%AE%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%97-how-i-built-an-executive-multimodal-ai-career-preparation-intelligence-2e85b983ebbd" target="_blank" class="medium-story-btn" style="display: inline-flex; align-items: center; gap: 8px; background: linear-gradient(135deg, #FF5C00 0%, #D43F00 100%); color: #FFFFFF !important; text-decoration: none !important; padding: 0.7rem 1.6rem; border-radius: 30px; font-weight: 700; font-size: 0.95rem; box-shadow: 0 5px 16px rgba(255, 92, 0, 0.35); transition: all 0.2s ease;">
    <span style="color: #FFFFFF !important; text-decoration: none !important; font-weight: 700;">Read on Medium &rarr;</span>
  </a>
</div>
</div>
<details class="learn-more-details">
<summary class="hero-learn-more-btn">
<span class="btn-text-expand">Learn More</span>
<span class="btn-text-collapse">Collapse Blueprint</span>
</summary>
<div class="learn-more-content">
<h3 class="pipeline-title">🚀 Platform Workflow Graph</h3>
<div class="graph-container">
<div class="graph-svg-wrapper">
<svg viewBox="0 0 600 300" width="100%">
<path d="M 60,150 C 130,150 130,70 200,70" class="bg-path" />
<path d="M 60,150 C 130,150 130,230 200,230" class="bg-path" />
<path d="M 200,70 L 380,70" class="bg-path" />
<path d="M 200,230 L 380,230" class="bg-path" />
<path d="M 380,70 C 450,70 450,150 520,150" class="bg-path" />
<path d="M 380,230 C 450,230 450,150 520,150" class="bg-path" />
<path d="M 60,150 C 130,150 130,70 200,70" class="flow-path flow-top-1" />
<path d="M 60,150 C 130,150 130,230 200,230" class="flow-path flow-bot-1" />
<path d="M 200,70 L 380,70" class="flow-path flow-top-2" />
<path d="M 200,230 L 380,230" class="flow-path flow-bot-2" />
<path d="M 380,70 C 450,70 450,150 520,150" class="flow-path flow-top-3" />
<path d="M 380,230 C 450,230 450,150 520,150" class="flow-path flow-bot-3" />
<g class="node-group n-ingest" onclick="showNodeDetail('ingest')">
<circle cx="60" cy="150" r="22" class="node-circle" />
<text x="60" y="156" class="node-icon">📄</text>
<text x="60" y="188" class="node-label">Ingest</text>
</g>
<g class="node-group n-ats" onclick="showNodeDetail('ats')">
<circle cx="200" cy="70" r="22" class="node-circle" />
<text x="200" y="76" class="node-icon">🎯</text>
<text x="200" y="108" class="node-label">ATS Audit</text>
</g>
<g class="node-group n-skills" onclick="showNodeDetail('skills')">
<circle cx="200" cy="230" r="22" class="node-circle" />
<text x="200" y="236" class="node-icon">📊</text>
<text x="200" y="268" class="node-label">Skill Gap</text>
</g>
<g class="node-group n-interview" onclick="showNodeDetail('interview')">
<circle cx="380" cy="70" r="22" class="node-circle" />
<text x="380" y="76" class="node-icon">🎙️</text>
<text x="380" y="108" class="node-label">Interview</text>
</g>
<g class="node-group n-brand" onclick="showNodeDetail('brand')">
<circle cx="380" cy="230" r="22" class="node-circle" />
<text x="380" y="236" class="node-icon">✨</text>
<text x="380" y="268" class="node-label">Brand</text>
</g>
<g class="node-group n-success" onclick="showNodeDetail('success')">
<circle cx="520" cy="150" r="22" class="node-circle" />
<text x="520" y="156" class="node-icon">🏆</text>
<text x="520" y="188" class="node-label">Success</text>
</g>
</svg>
</div>
<div class="graph-details-box">
<div class="detail-card d-default">
<h4>💡 Interactive Platform Blueprint</h4>
<p>Hover over any node in the graph above to trace the pipeline flow and discover how the executive platform processes candidate metrics in detail.</p>
</div>
<div class="detail-card d-ingest">
<h4>📄 Step 1: Resume Ingestion & Parsing</h4>
<p>Upload files in PDF format. Mistral OCR extracts text layers, structured candidate records, contact details, and experience blocks with high fidelity.</p>
</div>
<div class="detail-card d-ats">
<h4>🎯 Step 2: ATS Optimization</h4>
<p>Runs a 5-factor analysis mapping impact sentences, action verbs, formatting, and structural metrics. Offers immediate AI bullet rewrite recommendations.</p>
</div>
<div class="detail-card d-skills">
<h4>📊 Step 3: Skill Gap Analysis</h4>
<p>Compares your experiences against job specifications. Maps missing capabilities into categorised lists and generates 30-day action plans.</p>
</div>
<div class="detail-card d-interview">
<h4>🎙️ Step 4: Active Interview Simulator</h4>
<p>Generates target questions across core criteria (behavioral, technical). Simulates dynamic audio evaluations with prompt grading.</p>
</div>
<div class="detail-card d-brand">
<h4>✨ Step 5: Executive Brand Generator</h4>
<p>Builds structured LinkedIn headlines, biographical summaries, and professional markdown bios, matching recruiter search terms.</p>
</div>
<div class="detail-card d-success">
<h4>🏆 Step 6: Executive Dashboard & Tracking</h4>
<p>Aggregates application statuses, offers, searches, and preparation benchmarks in a central executive tracking control board.</p>
</div>
</div>
</div>
<div style="text-align: center; margin-top: 1.5rem;">
<a href="/Resume_Analysis" target="_self" class="get-started-btn">Launch Platform OS →</a>
</div>
</div>
<script>
function showNodeDetail(nodeName) {
document.querySelectorAll('.detail-card').forEach(card => {
card.style.display = 'none';
});
const card = document.querySelector('.d-' + nodeName);
if (card) {
card.style.display = 'block';
}
}
</script>
</details>""", unsafe_allow_html=True)
    
with col_right:
    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    if os.path.exists("assets/hero_illustration.png"):
        st.image("assets/hero_illustration.png", use_container_width=True)
