import os
import re
import sys
import tempfile
import streamlit as st

# Allow importing analyzer.py from project root
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from analyzer import analyze_resume 

st.set_page_config(page_title="ResumeLens AI - AI Resume Analyzer", page_icon="✦", layout="wide")


st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">

<style>
:root{
    --bg:#0B0B14; --surface:#14141F; --surface-2:#191926; --border:#232336;
    --violet:#7C5CFC; --teal:#34D9C4; --coral:#FF7A6B; --gold:#F5C453;
    --text:#F1F0F6; --muted:#8A8AA3;
}

#MainMenu, header, footer {visibility:hidden;}
.block-container{padding-top:1.2rem; max-width:1080px;}
html, body, [class*="css"]{
    background:var(--bg) !important;
    color:var(--text);
    font-family:'Inter', sans-serif;
}

/* ---------- NAVBAR ---------- */
.navbar{
    display:flex; align-items:center; justify-content:space-between;
    padding:14px 4px 28px 4px; border-bottom:1px solid var(--border); margin-bottom:8px;
}
.logo{display:flex; align-items:center; gap:10px; font-family:'Sora'; font-weight:700; font-size:1.05rem;}
.logo-mark{
    color:var(--gold); font-size:1.2rem;
    filter:drop-shadow(0 0 6px rgba(245,196,83,0.6));
}
.nav-status{
    font-size:0.78rem; color:var(--muted); border:1px solid var(--border);
    padding:5px 12px; border-radius:999px; letter-spacing:0.02em;
}

/* ---------- HERO ---------- */
.hero{ position:relative; padding:56px 0 40px 0; text-align:center; overflow:hidden;}
.hero-glow{
    position:absolute; top:-120px; left:50%; transform:translateX(-50%);
    width:640px; height:340px; border-radius:50%;
    background:radial-gradient(circle, rgba(124,92,252,0.35) 0%, rgba(52,217,196,0.18) 45%, transparent 75%);
    filter:blur(10px); z-index:0;
}
.eyebrow{
    position:relative; z-index:1; display:inline-block; font-size:0.75rem; font-weight:600;
    letter-spacing:0.12em; color:var(--teal); text-transform:uppercase;
    border:1px solid rgba(52,217,196,0.35); background:rgba(52,217,196,0.06);
    padding:6px 14px; border-radius:999px; margin-bottom:22px;
}
.hero h1{
    position:relative; z-index:1; font-family:'Sora'; font-weight:800;
    font-size:2.7rem; line-height:1.18; color:var(--text); margin:0 0 16px 0;
}
.hero h1 span{
    display:block;
    background:linear-gradient(90deg, var(--violet), var(--teal));
    -webkit-background-clip:text; background-clip:text; color:transparent;
}
.hero-subtitle{
    position:relative; z-index:1; color:var(--muted); font-size:1.02rem;
    max-width:560px; margin:0 auto; line-height:1.6;
}

/* ---------- STEP CARDS ---------- */
.step-tag{
    font-family:'Sora'; font-weight:700; font-size:0.75rem; color:var(--violet);
    letter-spacing:0.08em;
}
.card-title{font-family:'Sora'; font-weight:700; font-size:1.15rem; margin:4px 0 2px 0;}
.card-sub{color:var(--muted); font-size:0.85rem; margin-bottom:14px;}

div[data-testid="stFileUploaderDropzone"]{
    background:var(--surface) !important; border:1.5px dashed var(--border) !important;
    border-radius:14px !important;
}
div[data-testid="stFileUploaderDropzone"]:hover{ border-color:var(--violet) !important; }
[data-testid="stFileUploader"] section span{ color:var(--muted) !important; }
[data-testid="stFileUploader"] small{ color:var(--muted) !important; }

.stTextArea textarea{
    background:var(--surface) !important; color:var(--text) !important;
    border:1px solid var(--border) !important; border-radius:14px !important;
    font-size:0.92rem !important;
}
.stTextArea textarea:focus{ border-color:var(--teal) !important; box-shadow:none !important; }

/* ---------- ANALYZE BUTTON ---------- */
div.stButton{ text-align:center; margin-top:8px; }
div.stButton > button{
    background:linear-gradient(90deg, var(--violet), var(--teal)) !important;
    color:#0B0B14 !important; font-family:'Sora'; font-weight:700; font-size:0.95rem;
    border:none !important; border-radius:999px !important; padding:12px 32px !important;
    box-shadow:0 0 24px rgba(124,92,252,0.35);
}
div.stButton > button:hover{ box-shadow:0 0 34px rgba(124,92,252,0.55); }
.privacy-note{ text-align:center; color:var(--muted); font-size:0.8rem; margin-top:10px; }

/* ---------- RESULTS ---------- */
.results-heading{
    display:flex; align-items:baseline; justify-content:space-between;
    margin:44px 0 20px 0; border-top:1px solid var(--border); padding-top:32px;
}
.results-heading h2{ font-family:'Sora'; font-weight:800; font-size:1.6rem; margin:4px 0 0 0;}
.result-label{ font-size:0.72rem; letter-spacing:0.1em; color:var(--muted); font-weight:600;}

.result-card{
    background:var(--surface); border:1px solid var(--border); border-radius:16px;
    padding:22px; height:100%;
}
.score-circle{
    width:150px; height:150px; border-radius:50%; margin:16px auto 14px auto;
    display:flex; align-items:center; justify-content:center;
    background:conic-gradient(var(--violet) calc(var(--pct)*1%), var(--surface-2) 0);
}
.score-circle-inner{
    width:118px; height:118px; border-radius:50%; background:var(--surface);
    display:flex; flex-direction:column; align-items:center; justify-content:center;
}
.score-num{ font-family:'Sora'; font-weight:800; font-size:2rem; }
.score-outof{ font-size:0.65rem; color:var(--muted); letter-spacing:0.08em; }
.score-card{ text-align:center; }
.score-card h3{ font-family:'Sora'; margin:6px 0 6px 0; }
.score-card p{ color:var(--muted); font-size:0.88rem; }

.skill-list{ list-style:none; padding:0; margin:10px 0 0 0; }
.skill-list li{
    font-size:0.88rem; padding:8px 0; border-bottom:1px solid var(--border);
}
.skill-list li:last-child{ border-bottom:none; }
.matching-card .result-label{ color:var(--teal); }
.matching-card li::before{ content:"✓ "; color:var(--teal); font-weight:700; }
.missing-card .result-label{ color:var(--coral); }
.missing-card li::before{ content:"— "; color:var(--coral); font-weight:700; }

.suggestions-card{
    background:var(--surface); border:1px solid var(--border); border-radius:16px;
    padding:24px; margin-top:20px;
}
.suggestions-card h3{ font-family:'Sora'; margin:4px 0 4px 0; }
.suggestions-card > p{ color:var(--muted); font-size:0.88rem; margin-bottom:14px;}
.suggestion-item{
    font-size:0.9rem; padding:10px 0; border-bottom:1px solid var(--border); color:var(--text);
}
.suggestion-item:last-child{ border-bottom:none; }

.streamlit-expanderHeader{
    background:var(--surface) !important; color:var(--muted) !important;
    border:1px solid var(--border) !important; border-radius:12px !important;
}
.streamlit-expanderContent{
    background:var(--surface) !important; border:1px solid var(--border) !important;
    border-top:none !important; color:var(--text) !important;
}

footer-note{ display:block; text-align:center; color:var(--muted); font-size:0.8rem;
    margin-top:50px; padding-top:20px; border-top:1px solid var(--border);}
</style>
""", unsafe_allow_html=True)

# NAVBAR + HERO
st.markdown("""
<div class="navbar">
    <div class="logo"><span class="logo-mark">✦</span><span>JobMatch Hero</span></div>
    <div class="nav-status">AI Resume Analysis</div>
</div>
<div class="hero">
    <div class="hero-glow"></div>
    <div class="eyebrow">✦ AI-POWERED RESUME ANALYSIS</div>
    <h1>No more guessing games,<span>let AI fix your CV.</span></h1>
    <p class="hero-subtitle">Match your resume against any job description, discover what's missing,
    and improve your chances of getting noticed.</p>
</div>
""", unsafe_allow_html=True)

# ANALYZER GRID
col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown("""
    <div class="result-card">
        <span class="step-tag">01</span>
        <div class="card-title">Upload your CV</div>
        <div class="card-sub">PDF format · Max 10MB</div>
    """, unsafe_allow_html=True)
    resume_file = st.file_uploader(" ", type=["pdf"], label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="result-card">
        <span class="step-tag">02</span>
        <div class="card-title">Add the job description</div>
        <div class="card-sub">Paste the role you're applying for</div>
    """, unsafe_allow_html=True)
    job_description = st.text_area(" ", height=180, placeholder="Paste the job description here...",
                                    label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

_, mid, _ = st.columns([1, 1, 1])
with mid:
    analyze_clicked = st.button("✦  Analyze my resume   →", use_container_width=True)

st.markdown("<p class='privacy-note'>🔒 Your resume is processed securely and isn't stored.</p>",
            unsafe_allow_html=True)

# RESULT PARSING HELPERS

def parse_score(text):
    match = re.search(r'(\d{1,3})\s*(?:/\s*100|out of 100|%)', text, re.IGNORECASE)
    if match:
        return max(0, min(100, int(match.group(1))))
    return None


def parse_bullet_section(text, headings):
    for heading in headings:
        pattern = rf'{heading}.*?:?\s*\n(.*?)(?:\n\s*\n|\n[A-Z][^\n]*:|\Z)'
        m = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if m:
            lines = re.findall(r'[-*•]\s*(.+)', m.group(1))
            if lines:
                return [l.strip() for l in lines if l.strip()][:8]
    return []


# RUN ANALYSIS
if analyze_clicked:
    if not resume_file:
        st.error("Please upload a resume PDF.")
    elif not job_description.strip():
        st.error("Please enter a job description.")
    else:
        with st.spinner("Comparing your experience with the job description..."):
            temp_path = None
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                    temp_file.write(resume_file.read())
                    temp_path = temp_file.name

                result = analyze_resume(temp_path, job_description)
                st.session_state["result"] = result

            except Exception as e:
                st.error(f"Something went wrong: {e}")
            finally:
                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)

# RESULTS
if "result" in st.session_state:
    result = st.session_state["result"]
    score = parse_score(result)
    matching = parse_bullet_section(result, ["Matching skills", "Matching Skills"])
    missing = parse_bullet_section(result, ["Missing skills", "Missing Skills"])
    suggestions = parse_bullet_section(result, ["Content improvements", "Improvements", "Suggestions"])

    score_display = score if score is not None else 0
    score_label_text = f"{score}" if score is not None else "--"

    st.markdown(f"""
    <div class="results-heading">
        <div>
            <span class="result-label">✦ ANALYSIS COMPLETE</span>
            <h2>Your match, decoded.</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 1], gap="medium")

    with c1:
        st.markdown(f"""
        <div class="result-card score-card">
            <span class="result-label">ATS MATCH SCORE</span>
            <div class="score-circle" style="--pct:{score_display}">
                <div class="score-circle-inner">
                    <span class="score-num">{score_label_text}</span>
                    <span class="score-outof">OUT OF 100</span>
                </div>
            </div>
            <h3>Your ATS score</h3>
            <p>{"Strong alignment with the role." if score_display >= 70 else
                 "Some room to strengthen your match." if score_display >= 40 else
                 "See suggestions below to improve alignment."}</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        items = "".join(f"<li>{s}</li>" for s in matching) or "<li style='color:var(--muted)'>See full analysis below</li>"
        st.markdown(f"""
        <div class="result-card matching-card">
            <span class="result-label">ALREADY COMING THROUGH</span>
            <h3>Matching skills</h3>
            <ul class="skill-list">{items}</ul>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        items = "".join(f"<li>{s}</li>" for s in missing) or "<li style='color:var(--muted)'>See full analysis below</li>"
        st.markdown(f"""
        <div class="result-card missing-card">
            <span class="result-label">SIGNALS TO CONSIDER</span>
            <h3>Missing skills</h3>
            <ul class="skill-list">{items}</ul>
        </div>
        """, unsafe_allow_html=True)

    sugg_items = "".join(f"<div class='suggestion-item'>{s}</div>" for s in suggestions) or \
                 "<div class='suggestion-item' style='color:var(--muted)'>See full analysis below</div>"
    st.markdown(f"""
    <div class="suggestions-card">
        <span class="result-label">NEXT MOVES</span>
        <h3>Improve your match</h3>
        <p>Content-focused suggestions based on the role.</p>
        {sugg_items}
    </div>
    """, unsafe_allow_html=True)

    with st.expander("View full AI analysis"):
        st.markdown(result)

st.markdown("""
<footer-note>JobMatch Hero &nbsp;·&nbsp; Built with Python · LangChain · Gemini</footer-note>
""", unsafe_allow_html=True)
