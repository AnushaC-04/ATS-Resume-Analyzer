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
    --bg:#070D1D; --surface:#101A35; --surface-2:#142244; --border:#263B70;
    --violet:#7857FF; --blue:#12B8FF; --teal:#28D9CB; --coral:#FF7B88; --gold:#FFD166;
    --text:#F5F7FF; --muted:#AAB8D6;
}

#MainMenu, header, footer {visibility:hidden;}
.stApp {background:radial-gradient(ellipse at 50% 5%, #172B59 0%, var(--bg) 52%) !important; color:var(--text);}
.block-container{padding-top:1rem; padding-bottom:2.5rem; max-width:1240px;}
html, body, [class*="css"]{color:var(--text); font-family:'Inter',sans-serif;}
[data-testid="stAppViewContainer"] {background:transparent;}

/* ---------- NAVBAR ---------- */
.navbar{display:flex; align-items:center; justify-content:space-between; padding:14px 4px 22px; border-bottom:1px solid rgba(102,145,255,.25); margin-bottom:8px;}
.logo{display:flex; align-items:center; gap:10px; font-family:'Sora',sans-serif; font-weight:800; font-size:1.15rem; color:#F7F8FF;}
.logo-mark{color:var(--gold); font-size:1.45rem; filter:drop-shadow(0 0 9px rgba(255,209,102,.65));}
.nav-status{font-size:.8rem; color:#D7E4FF; border:1px solid #344F91; background:rgba(23,44,91,.72); padding:8px 15px; border-radius:999px; letter-spacing:.02em;}

/* ---------- HERO ---------- */
.hero{position:relative; padding:38px 0 30px; text-align:center; overflow:hidden;}
.hero-glow{position:absolute; top:-120px; left:50%; transform:translateX(-50%); width:780px; height:360px; border-radius:50%; background:radial-gradient(circle,rgba(83,91,255,.32) 0%,rgba(18,184,255,.16) 42%,transparent 72%); filter:blur(18px); z-index:0; pointer-events:none;}
.eyebrow{position:relative; z-index:1; display:inline-block; font-size:.76rem; font-weight:700; letter-spacing:.14em; color:#55F0E1; text-transform:uppercase; border:1px solid rgba(40,217,203,.52); background:rgba(16,39,76,.72); padding:8px 17px; border-radius:999px; margin-bottom:19px; box-shadow:0 0 24px rgba(40,217,203,.08);}
.hero h1{position:relative; z-index:1; font-family:'Sora',sans-serif; font-weight:800; font-size:clamp(2.25rem,4.2vw,3.45rem); line-height:1.12; color:var(--text); margin:0 0 16px; letter-spacing:-.035em;}
.hero h1 span{display:block; background:linear-gradient(95deg,#16C8F7 8%,#668BFF 52%,#B15CFF 95%); -webkit-background-clip:text; background-clip:text; color:transparent; padding-bottom:3px;}
.hero-subtitle{position:relative; z-index:1; color:#B7C4E2; font-size:1rem; max-width:630px; margin:0 auto; line-height:1.7;}

/* ---------- INPUT PANELS ---------- */
.step-tag{display:inline-flex; align-items:center; justify-content:center; width:36px; height:36px; border-radius:12px; background:linear-gradient(135deg,#138DFF,#7857FF); color:white; font-family:'Sora',sans-serif; font-weight:800; font-size:.8rem; letter-spacing:.03em; box-shadow:0 5px 18px rgba(63,104,255,.3); margin-bottom:10px;}
.card-title{font-family:'Sora',sans-serif; font-weight:700; font-size:1.2rem; color:#F5F7FF; margin:2px 0 5px;}
.card-sub{color:#B3C0DD; font-size:.9rem; margin-bottom:16px;}
/* Give each real Streamlit column its own visible card without wrapping widgets in HTML. */
.stColumn:has([data-testid="stFileUploader"]) > div[data-testid="stVerticalBlock"],
.stColumn:has(.stTextArea) > div[data-testid="stVerticalBlock"]{
    height:100%; min-height:320px; box-sizing:border-box; padding:24px !important;
    border-radius:22px; background:linear-gradient(145deg,rgba(22,43,83,.96),rgba(14,23,49,.98)) !important;
    border:1px solid rgba(57,112,221,.9); box-shadow:0 0 0 1px rgba(18,184,255,.10),0 12px 34px rgba(0,0,0,.22);
    position:relative; overflow:hidden;
}
.stColumn:has([data-testid="stFileUploader"]) > div[data-testid="stVerticalBlock"]{border-color:rgba(18,184,255,.9);}
.stColumn:has(.stTextArea) > div[data-testid="stVerticalBlock"]{border-color:rgba(120,87,255,.92);}
.stColumn:has([data-testid="stFileUploader"]) > div[data-testid="stVerticalBlock"]:before,
.stColumn:has(.stTextArea) > div[data-testid="stVerticalBlock"]:before{content:""; position:absolute; top:0; left:20px; right:20px; height:2px; background:linear-gradient(90deg,var(--blue),var(--violet)); opacity:.95;}

[data-testid="stFileUploader"]{margin-top:4px;}
div[data-testid="stFileUploaderDropzone"]{background:rgba(8,19,43,.66) !important; border:1.5px dashed #398CF4 !important; border-radius:16px !important; min-height:150px; transition:border-color .2s,background .2s;}
div[data-testid="stFileUploaderDropzone"]:hover{border-color:#7B6BFF !important; background:rgba(23,38,78,.86) !important;}
[data-testid="stFileUploader"] section span,[data-testid="stFileUploader"] small{color:#B8C7E8 !important;}
[data-testid="stFileUploader"] button{border-radius:10px !important; border:1px solid #4C6FC0 !important; color:#F4F7FF !important; background:#182B55 !important;}
[data-testid="stFileUploader"] button:hover{border-color:var(--blue) !important; background:#203C73 !important;}
.stTextArea textarea{background:rgba(8,18,42,.78) !important; color:#F4F7FF !important; border:1px solid #354F8F !important; border-radius:15px !important; font-size:.94rem !important; line-height:1.6 !important; min-height:180px; transition:border-color .2s,box-shadow .2s;}
.stTextArea textarea::placeholder{color:#9CAFD4 !important; opacity:1;}
.stTextArea textarea:focus{border-color:#4BC9FF !important; box-shadow:0 0 0 2px rgba(18,184,255,.18) !important;}
[data-testid="stFileUploaderFile"]{background:rgba(3,39,52,.88) !important; border:1px solid rgba(40,217,203,.55) !important; border-radius:12px !important;}

/* ---------- ANALYZE BUTTON ---------- */
div.stButton{text-align:center; margin-top:8px;}
div.stButton > button{background:linear-gradient(100deg,#10B8F4 0%,#4D65FF 52%,#8547F5 100%) !important; color:white !important; font-family:'Sora',sans-serif; font-weight:700; font-size:1rem; border:1px solid rgba(183,207,255,.18) !important; border-radius:999px !important; padding:14px 30px !important; box-shadow:0 8px 28px rgba(76,91,255,.3); transition:transform .18s,box-shadow .18s;}
div.stButton > button:hover{transform:translateY(-2px); box-shadow:0 12px 34px rgba(76,91,255,.45); border-color:rgba(118,193,255,.6) !important;}
.privacy-note{text-align:center; color:#9CAED1; font-size:.82rem; margin-top:10px;}

/* ---------- RESULTS ---------- */
.results-heading{display:flex; align-items:baseline; justify-content:space-between; margin:44px 0 20px; border-top:1px solid rgba(102,145,255,.25); padding-top:30px;}
.results-heading h2{font-family:'Sora',sans-serif; font-weight:800; font-size:1.65rem; margin:4px 0 0; color:#F6F8FF;}
.result-label{font-size:.72rem; letter-spacing:.1em; color:#AFC4F1; font-weight:700;}
.result-card{background:linear-gradient(145deg,rgba(20,34,68,.98),rgba(13,22,46,.98)); border:1px solid #2B457D; border-radius:18px; padding:22px; height:100%; box-shadow:0 8px 28px rgba(0,0,0,.16);}
.score-circle{width:150px; height:150px; border-radius:50%; margin:16px auto 14px; display:flex; align-items:center; justify-content:center; background:conic-gradient(var(--violet) calc(var(--pct)*1%),#1D2A4B 0); box-shadow:0 0 24px rgba(120,87,255,.15);}
.score-circle-inner{width:118px; height:118px; border-radius:50%; background:#101A35; display:flex; flex-direction:column; align-items:center; justify-content:center;}
.score-num{font-family:'Sora',sans-serif; font-weight:800; font-size:2rem; color:#F6F8FF;}
.score-outof{font-size:.65rem; color:var(--muted); letter-spacing:.08em;}
.score-card{text-align:center;}.score-card h3{font-family:'Sora',sans-serif; margin:6px 0; color:#F6F8FF;}.score-card p{color:#B3C0DD; font-size:.88rem;}
.skill-list{list-style:none; padding:0; margin:10px 0 0;}.skill-list li{font-size:.88rem; padding:9px 0; border-bottom:1px solid rgba(98,128,190,.2); color:#E6EDFF;}.skill-list li:last-child{border-bottom:none;}
.matching-card .result-label{color:var(--teal);}.matching-card li::before{content:"✓ "; color:var(--teal); font-weight:700;}.missing-card .result-label{color:var(--coral);}.missing-card li::before{content:"— "; color:var(--coral); font-weight:700;}
.suggestions-card{background:linear-gradient(145deg,rgba(20,34,68,.98),rgba(13,22,46,.98)); border:1px solid #2B457D; border-radius:18px; padding:24px; margin-top:20px; box-shadow:0 8px 28px rgba(0,0,0,.16);}
.suggestions-card h3{font-family:'Sora',sans-serif; margin:4px 0; color:#F6F8FF;}.suggestions-card > p{color:#B3C0DD; font-size:.88rem; margin-bottom:14px;}.suggestion-item{font-size:.9rem; padding:11px 0; border-bottom:1px solid rgba(98,128,190,.2); color:#E6EDFF;}.suggestion-item:last-child{border-bottom:none;}
[data-testid="stExpander"] details{background:#101A35 !important; border:1px solid #2B457D !important; border-radius:12px !important;}.streamlit-expanderHeader{color:#DCE7FF !important;}.streamlit-expanderContent{background:#101A35 !important; border-color:#2B457D !important; color:var(--text) !important;}
footer-note{display:block; text-align:center; color:#8295BB; font-size:.8rem; margin-top:48px; padding-top:20px; border-top:1px solid rgba(102,145,255,.22);}

@media (max-width: 760px){.block-container{padding-left:1rem;padding-right:1rem}.hero{padding:30px 0 24px}.hero h1{font-size:2.15rem}.stColumn:has([data-testid="stFileUploader"]) > div[data-testid="stVerticalBlock"],.stColumn:has(.stTextArea) > div[data-testid="stVerticalBlock"]{min-height:0;padding:18px !important}.navbar{padding-bottom:16px}.nav-status{font-size:.7rem}}
</style>
""", unsafe_allow_html=True)

# NAVBAR + HERO
st.markdown("""
<div class="navbar">
    <div class="logo"><span class="logo-mark">✦</span><span>ResumeLens AI</span></div>
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
    <div class="input-card-heading">
        <span class="step-tag">01</span>
        <div class="card-title">Upload your CV</div>
        <div class="card-sub">PDF format · Max 10MB</div>
    </div>
    """, unsafe_allow_html=True)
    resume_file = st.file_uploader(" ", type=["pdf"], label_visibility="collapsed")

with col2:
    st.markdown("""
    <div class="input-card-heading">
        <span class="step-tag">02</span>
        <div class="card-title">Add the job description</div>
        <div class="card-sub">Paste the role you're applying for</div>
    </div>
    """, unsafe_allow_html=True)
    job_description = st.text_area(" ", height=180, placeholder="Paste the job description here...",
                                    label_visibility="collapsed")

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
<footer-note>ResumeLens AI &nbsp;·&nbsp; Built with Python · LangChain · Gemini</footer-note>
""", unsafe_allow_html=True)