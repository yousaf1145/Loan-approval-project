import streamlit as st
import pandas as pd
import joblib
import os  # Added for path handling

# ── 1. PAGE CONFIG ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CareXpert · Risk Intelligence",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 2. GLOBAL CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=DM+Mono:wght@300;400;500&family=Outfit:wght@300;400;500;600&display=swap');

/* ── Root Variables ── */
:root {
    --navy:       #080C1A;
    --navy-2:     #0D1326;
    --navy-3:     #111827;
    --card-bg:    rgba(255,255,255,0.035);
    --border:     rgba(255,255,255,0.07);
    --gold:       #C9A84C;
    --gold-light: #E8C97A;
    --gold-glow:  rgba(201,168,76,0.18);
    --green:      #2ECC71;
    --blue:       #3B9EFF;
    --orange:     #F5A623;
    --red:        #E74C3C;
    --text-primary:   #F0EDE8;
    --text-secondary: #8A8FA8;
    --text-muted:     #4A5066;
}

/* ── Base & Background ── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--navy) !important;
    font-family: 'Outfit', sans-serif;
    color: var(--text-primary);
}

[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 70% 50% at 15% 20%, rgba(201,168,76,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 85% 80%, rgba(59,158,255,0.05) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--navy-2) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

/* ── Header / Toolbar ── */
[data-testid="stHeader"] {
    background: transparent !important;
}

/* ── Remove default padding ── */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
    max-width: 1240px !important;
}

/* ─────────────────────────────────────────────────
   HERO BANNER
───────────────────────────────────────────────── */
.hero-banner {
    background: linear-gradient(135deg, var(--navy-2) 0%, #0A1228 100%);
    border: 1px solid var(--border);
    border-top: 2px solid var(--gold);
    border-radius: 16px;
    padding: 2.8rem 3rem;
    margin-bottom: 2.4rem;
    position: relative;
    overflow: hidden;
}

.hero-banner::after {
    content: "⬡";
    position: absolute;
    right: 2.5rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 8rem;
    color: rgba(201,168,76,0.07);
    line-height: 1;
    letter-spacing: -0.05em;
}

.hero-banner .eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.22em;
    color: var(--gold);
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}

.hero-banner h1 {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 2.8rem !important;
    font-weight: 700 !important;
    line-height: 1.1 !important;
    color: var(--text-primary) !important;
    margin: 0 0 0.5rem !important;
}

.hero-banner h1 span {
    color: var(--gold);
}

.hero-banner p {
    color: var(--text-secondary);
    font-size: 0.95rem;
    font-weight: 300;
    margin: 0;
}

/* ─────────────────────────────────────────────────
   SECTION LABELS
───────────────────────────────────────────────── */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    color: var(--gold);
    text-transform: uppercase;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}

.section-label::after {
    content: "";
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--border), transparent);
}

/* ─────────────────────────────────────────────────
   GLASS CARD
───────────────────────────────────────────────── */
.glass-card {
    background: var(--card-bg);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.8rem;
    margin-bottom: 1.2rem;
}

/* ─────────────────────────────────────────────────
   STREAMLIT WIDGETS — OVERRIDE
───────────────────────────────────────────────── */

/* Labels */
label[data-testid="stWidgetLabel"] p,
.stSelectbox label p,
.stNumberInput label p {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--text-secondary) !important;
    margin-bottom: 0.3rem !important;
}

/* Select boxes */
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    transition: border-color 0.2s ease !important;
}

[data-testid="stSelectbox"] > div > div:hover {
    border-color: var(--gold) !important;
}

/* Number inputs */
[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.9rem !important;
}

[data-testid="stNumberInput"] input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 2px var(--gold-glow) !important;
}

/* ─────────────────────────────────────────────────
   SUBMIT BUTTON
───────────────────────────────────────────────── */
[data-testid="stButton"] > button {
    width: 100% !important;
    background: linear-gradient(135deg, var(--gold) 0%, #A07B2E 100%) !important;
    color: var(--navy) !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.85rem 2rem !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 24px rgba(201,168,76,0.25) !important;
    margin-top: 0.5rem !important;
}

[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(201,168,76,0.4) !important;
}

[data-testid="stButton"] > button:active {
    transform: translateY(0px) !important;
}

/* ─────────────────────────────────────────────────
   METRIC CARDS
───────────────────────────────────────────────── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin: 1.5rem 0;
}

.kpi-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
}

.kpi-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}

.kpi-card.green::before  { background: linear-gradient(90deg, var(--green), transparent); }
.kpi-card.blue::before   { background: linear-gradient(90deg, var(--blue), transparent); }
.kpi-card.orange::before { background: linear-gradient(90deg, var(--orange), transparent); }
.kpi-card.red::before    { background: linear-gradient(90deg, var(--red), transparent); }
.kpi-card.gold::before   { background: linear-gradient(90deg, var(--gold), transparent); }

.kpi-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
}

.kpi-value {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 0.3rem;
}

.kpi-value.green  { color: var(--green); }
.kpi-value.blue   { color: var(--blue); }
.kpi-value.orange { color: var(--orange); }
.kpi-value.red    { color: var(--red); }
.kpi-value.gold   { color: var(--gold); }

.kpi-sub {
    font-size: 0.75rem;
    color: var(--text-muted);
}

/* ─────────────────────────────────────────────────
   VERDICT BANNER
───────────────────────────────────────────────── */
.verdict-approved {
    background: linear-gradient(135deg, rgba(46,204,113,0.12), rgba(46,204,113,0.04));
    border: 1px solid rgba(46,204,113,0.3);
    border-left: 4px solid var(--green);
    border-radius: 12px;
    padding: 1.6rem 2rem;
}

.verdict-review {
    background: linear-gradient(135deg, rgba(59,158,255,0.12), rgba(59,158,255,0.04));
    border: 1px solid rgba(59,158,255,0.3);
    border-left: 4px solid var(--blue);
    border-radius: 12px;
    padding: 1.6rem 2rem;
}

.verdict-caution {
    background: linear-gradient(135deg, rgba(245,166,35,0.12), rgba(245,166,35,0.04));
    border: 1px solid rgba(245,166,35,0.3);
    border-left: 4px solid var(--orange);
    border-radius: 12px;
    padding: 1.6rem 2rem;
}

.verdict-declined {
    background: linear-gradient(135deg, rgba(231,76,60,0.12), rgba(231,76,60,0.04));
    border: 1px solid rgba(231,76,60,0.3);
    border-left: 4px solid var(--red);
    border-radius: 12px;
    padding: 1.6rem 2rem;
}

.verdict-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.6rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
}

.verdict-note {
    font-size: 0.85rem;
    color: var(--text-secondary);
}

/* ─────────────────────────────────────────────────
   PROBABILITY BAR
───────────────────────────────────────────────── */
.prob-bar-wrap {
    margin: 1.2rem 0;
}

.prob-bar-label {
    display: flex;
    justify-content: space-between;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
}

.prob-bar-track {
    background: rgba(255,255,255,0.06);
    border-radius: 99px;
    height: 6px;
    overflow: hidden;
}

.prob-bar-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

/* ─────────────────────────────────────────────────
   INSIGHT ROWS (Decision Interpretability)
───────────────────────────────────────────────── */
.insight-row {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 1rem 0;
    border-bottom: 1px solid var(--border);
}

.insight-row:last-child { border-bottom: none; }

.insight-icon {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}

.insight-icon.good    { background: rgba(46,204,113,0.12); }
.insight-icon.neutral { background: rgba(59,158,255,0.12); }
.insight-icon.warn    { background: rgba(245,166,35,0.12); }
.insight-icon.bad     { background: rgba(231,76,60,0.12); }

.insight-body strong {
    display: block;
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--text-primary);
    margin-bottom: 0.2rem;
}

.insight-body span {
    font-size: 0.78rem;
    color: var(--text-muted);
}

/* ─────────────────────────────────────────────────
   SIDEBAR STYLES
───────────────────────────────────────────────── */
.sidebar-badge {
    background: var(--gold-glow);
    border: 1px solid rgba(201,168,76,0.25);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-size: 0.82rem;
    color: var(--text-secondary);
    line-height: 1.5;
    margin-top: 0.5rem;
}

.sidebar-badge strong {
    color: var(--gold-light);
    display: block;
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}

/* ─────────────────────────────────────────────────
   DIVIDER
───────────────────────────────────────────────── */
.gold-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    margin: 2rem 0;
    opacity: 0.3;
}

/* ─────────────────────────────────────────────────
   FOOTER
───────────────────────────────────────────────── */
.footer {
    text-align: center;
    padding: 2rem 0 1rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.15em;
    color: var(--text-muted);
    text-transform: uppercase;
}

/* ── Streamlit overrides ── */
[data-testid="stMetric"] { display: none !important; }
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, var(--gold), var(--gold-light)) !important;
}

/* Hide streamlit default alert boxes — we use custom HTML */
[data-testid="stAlert"] { display: none !important; }

/* Sidebar header */
[data-testid="stSidebar"] h2 {
    font-family: 'Cormorant Garamond', serif !important;
    color: var(--gold) !important;
    font-size: 1.4rem !important;
}

[data-testid="stSidebar"] h3 {
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: var(--text-secondary) !important;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── 3. LOAD MODEL (Updated for Deployment) ───────────────────────────────────
@st.cache_resource
def load_model():
    """
    Finds the model folder regardless of whether the app is running
    locally or in a cloud container.
    """
    # Get the directory where app.py is located
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Move up one level to the project root, then into the model folder
    model_path = os.path.join(current_dir, "..", "model")

    # Define file paths
    model_file   = os.path.join(model_path, 'loan_logistic_model.pkl')
    feature_file = os.path.join(model_path, 'feature_names.pkl')

    try:
        model    = joblib.load(model_file)
        features = joblib.load(feature_file)
        return model, features
    except FileNotFoundError:
        st.error(
            f"Deployment Error: Model files not found at '{os.path.abspath(model_path)}'. "
            "Ensure your GitHub repository has the /model folder at the project root."
        )
        return None, None

model, model_features = load_model()


# ── 4. CREDIT OPTIONS (numeric score ranges) ─────────────────────────────────
credit_options = {
    "0.8 – 1.0  ·  Excellent": {
        "value": 1.0,
        "icon":  "✦",
        "color": "green",
        "info":  "Score 0.8–1.0: Highest trust tier. Consistent, on-time repayment history. "
                 "Strongly increases approval probability — this is the most influential factor in the model."
    },
    "0.6 – 0.8  ·  Good": {
        "value": 0.7,
        "icon":  "◈",
        "color": "blue",
        "info":  "Score 0.6–0.8: Reliable repayment with only minor delays. "
                 "Model treats this favorably; stable income further compensates any marginal risk."
    },
    "0.4 – 0.6  ·  Average / No History": {
        "value": 0.5,
        "icon":  "◇",
        "color": "orange",
        "info":  "Score 0.4–0.6: Neutral zone or first-time borrowers. "
                 "Model shifts weight to education level and income capacity to fill the gap."
    },
    "0.2 – 0.4  ·  Below Average": {
        "value": 0.3,
        "icon":  "▽",
        "color": "orange",
        "info":  "Score 0.2–0.4: Some missed payments or late repayments on record. "
                 "Reduces approval odds; strong income or co-applicant may partially offset."
    },
    "0.0 – 0.2  ·  Very Poor": {
        "value": 0.0,
        "icon":  "✕",
        "color": "red",
        "info":  "Score 0.0–0.2: Frequent defaults or serious delinquencies detected. "
                 "Critical risk flag — requires exceptional secondary factors for any approval."
    },
}

CREDIT_HELP = (
    "ℹ️ What is a Credit Score?\n\n"
    "Your credit score reflects your history of repaying loans and bills. "
    "It ranges from 0.0 (very poor) to 1.0 (excellent).\n\n"
    "📄 How to check yours:\n"
    "• Request an e-CIB report from your bank branch\n"
    "• Visit the State Bank of Pakistan (SBP) portal: sbp.org.pk\n"
    "• Ask your bank for your official ECIB credit standing\n\n"
    "Select the range that matches your official report score."
)


# ── 5. SIDEBAR ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⬡ CareXpert")
    st.markdown(
        '<p style="font-family:\'DM Mono\',monospace;font-size:0.62rem;'
        'letter-spacing:0.15em;color:#4A5066;text-transform:uppercase;margin-top:-0.4rem;">'
        'Risk Intelligence v2.0</p>',
        unsafe_allow_html=True
    )
    st.markdown("---")

    # ── Credit Score Guide Header ──
    st.markdown(
        '<p style="font-family:\'DM Mono\',monospace;font-size:0.62rem;letter-spacing:0.18em;'
        'text-transform:uppercase;color:#C9A84C;margin-bottom:0.6rem;">📊 Credit Score Guide</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p style="font-size:0.78rem;color:#8A8FA8;margin-bottom:1rem;line-height:1.5;">'
        'Select a range in the form. The tier matching your e-CIB score is highlighted below.</p>',
        unsafe_allow_html=True
    )

    # Read currently selected tier
    first_option    = list(credit_options.keys())[0]
    selected_credit = st.session_state.get("main_credit_score", first_option)

    # Color lookup
    color_map = {
        "green":  ("#2ECC71", "rgba(46,204,113,0.10)", "rgba(46,204,113,0.03)"),
        "blue":   ("#3B9EFF", "rgba(59,158,255,0.10)",  "rgba(59,158,255,0.03)"),
        "orange": ("#F5A623", "rgba(245,166,35,0.10)",  "rgba(245,166,35,0.03)"),
        "red":    ("#E74C3C", "rgba(231,76,60,0.10)",   "rgba(231,76,60,0.03)"),
    }

    # ── Render ALL 5 tiers as a guide list ──
    tiers_html = ""
    for label, meta in credit_options.items():
        is_selected = (label == selected_credit)
        fg, border_active, border_idle = color_map[meta["color"]]
        short_range = label.split("·")[0].strip()   # e.g. "0.8 – 1.0"
        tier_name   = label.split("·")[1].strip()   # e.g. "Excellent"

        if is_selected:
            card_style = (
                f"background:{border_active};"
                f"border:1.5px solid {fg};"
                f"border-left:4px solid {fg};"
                "border-radius:10px;"
                "padding:0.75rem 1rem;"
                "margin-bottom:0.5rem;"
            )
            range_color = fg
            name_color  = "#F0EDE8"
            desc_color  = "#A0A5B8"
            selected_tag = (
                f'<span style="float:right;font-family:\'DM Mono\',monospace;'
                f'font-size:0.55rem;letter-spacing:0.12em;text-transform:uppercase;'
                f'color:{fg};background:{border_active};border:1px solid {fg}44;'
                f'border-radius:4px;padding:2px 6px;">Selected</span>'
            )
        else:
            card_style = (
                f"background:rgba(255,255,255,0.02);"
                f"border:1px solid rgba(255,255,255,0.06);"
                "border-left:3px solid rgba(255,255,255,0.08);"
                "border-radius:10px;"
                "padding:0.7rem 1rem;"
                "margin-bottom:0.5rem;"
                "opacity:0.65;"
            )
            range_color = "#6A7090"
            name_color  = "#6A7090"
            desc_color  = "#4A5066"
            selected_tag = ""

        tiers_html += f"""
        <div style="{card_style}">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.25rem;">
                <span style="font-family:'DM Mono',monospace;font-size:0.72rem;
                             font-weight:500;color:{range_color};">{short_range}</span>
                {selected_tag}
            </div>
            <div style="font-family:'Outfit',sans-serif;font-size:0.82rem;
                        font-weight:600;color:{name_color};margin-bottom:0.3rem;">
                {meta['icon']} &nbsp;{tier_name}
            </div>
            <div style="font-size:0.72rem;color:{desc_color};line-height:1.45;">
                {meta['info']}
            </div>
        </div>
        """

    st.markdown(tiers_html, unsafe_allow_html=True)

    # ── How to Verify section ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<p style="font-family:\'DM Mono\',monospace;font-size:0.62rem;letter-spacing:0.18em;'
        'text-transform:uppercase;color:#C9A84C;margin-bottom:0.6rem;">🏦 How to Check Your Score</p>',
        unsafe_allow_html=True
    )
    st.markdown("""
    <div style="background:rgba(201,168,76,0.06);border:1px solid rgba(201,168,76,0.2);
                border-radius:10px;padding:1rem 1.1rem;font-size:0.78rem;
                color:#8A8FA8;line-height:1.6;">
        <div style="color:#E8C97A;font-weight:600;margin-bottom:0.4rem;">e-CIB Report</div>
        <div>① Visit your bank branch and request an e-CIB report</div>
        <div style="margin-top:0.3rem;">② Or go online to
            <span style="color:#C9A84C;font-weight:500;">sbp.org.pk</span>
            and check your official ECIB credit standing</div>
        <div style="margin-top:0.3rem;">③ Match your score to the range above</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<p style="font-family:\'DM Mono\',monospace;font-size:0.58rem;color:#2A2F44;'
        'text-transform:uppercase;letter-spacing:0.12em;text-align:center;">'
        'Powered by Logistic Regression · PKR</p>',
        unsafe_allow_html=True
    )


# ── 6. HERO BANNER ───────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="eyebrow">▸ Underwriting Intelligence Platform</div>
    <h1>AI <span>Loan</span> Predicator</h1>
    <p>Complete the applicant profile below to generate a structured risk assessment and lending recommendation.</p>
</div>
""", unsafe_allow_html=True)


# ── 7. APPLICANT PROFILE FORM ────────────────────────────────────────────────
st.markdown('<div class="section-label">01 · Applicant Demographics</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    gender = st.selectbox("Gender", ["Male", "Female"])
with col2:
    married = st.selectbox("Marital Status", ["Yes", "No"], format_func=lambda x: "Married" if x == "Yes" else "Single")
with col3:
    dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])

col4, col5 = st.columns(2)
with col4:
    education = st.selectbox("Education Level", ["Graduate", "Not Graduate"])
with col5:
    self_employed = st.selectbox("Employment Type", ["No", "Yes"], format_func=lambda x: "Salaried" if x == "No" else "Self-Employed")

st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">02 · Financial Profile</div>', unsafe_allow_html=True)

col6, col7 = st.columns(2)
with col6:
    applicant_income    = st.number_input("Applicant Monthly Income (PKR)", min_value=0, value=5000, step=500)
    loan_amount         = st.number_input("Loan Amount (in thousands)", min_value=0, value=150, step=10)
with col7:
    coapplicant_income  = st.number_input("Co-Applicant Monthly Income (PKR)", min_value=0, value=0, step=500)
    loan_term           = st.number_input("Loan Term (Days)", min_value=0, value=360, step=30)

st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">03 · Property & Credit</div>', unsafe_allow_html=True)

col8, col9 = st.columns(2)
with col8:
    property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])
with col9:
    credit_desc_main = st.selectbox(
        "Credit History Score Range",
        list(credit_options.keys()),
        index=0,
        key="main_credit_score",
        help=CREDIT_HELP,
    )

credit_history_val = credit_options[credit_desc_main]["value"]

st.markdown("<br>", unsafe_allow_html=True)
st.button("⬡  Generate Risk Intelligence Report", key="submit")


# ── 8. REPORT ────────────────────────────────────────────────────────────────
if st.session_state.get("submit"):

    # Guard: stop if model failed to load
    if model is None or model_features is None:
        st.stop()

    # Build input
    input_df = pd.DataFrame([{
        'Gender':            gender,
        'Married':           married,
        'Dependents':        dependents,
        'Education':         education,
        'Self_Employed':     self_employed,
        'ApplicantIncome':   applicant_income,
        'CoapplicantIncome': coapplicant_income,
        'LoanAmount':        loan_amount,
        'Loan_Amount_Term':  loan_term,
        'Credit_History':    credit_history_val,
        'Property_Area':     property_area,
    }])

    input_df['Property_Area_Semiurban'] = 1 if property_area == "Semiurban" else 0
    input_df['Property_Area_Urban']     = 1 if property_area == "Urban"     else 0
    input_df['Gender']       = 1 if gender       == "Male"        else 0
    input_df['Married']      = 1 if married       == "Yes"         else 0
    input_df['Education']    = 1 if education     == "Graduate"    else 0
    input_df['Self_Employed']= 1 if self_employed == "Yes"         else 0
    input_df['Dependents']   = input_df['Dependents'].replace('3+', 3).astype(int)
    input_df = input_df.drop(columns=['Property_Area'])
    input_df = input_df[model_features]

    prediction = model.predict(input_df)
    prob       = model.predict_proba(input_df)[0][1]

    annual_income = (applicant_income + coapplicant_income) * 12
    dti           = (loan_amount * 1000 / annual_income * 100) if annual_income > 0 else 0

    # Tier logic
    if prob >= 0.80:
        tier, accent, verdict_class = "Tier 1 · High Trust",    "green",  "verdict-approved"
        note = "Auto-Approval Recommended"
    elif prob >= 0.60:
        tier, accent, verdict_class = "Tier 2 · Moderate Risk", "blue",   "verdict-review"
        note = "Manual Underwriter Review Required"
    elif prob >= 0.35:
        tier, accent, verdict_class = "Tier 3 · High Risk",     "orange", "verdict-caution"
        note = "Additional Collateral or Co-Signer Required"
    else:
        tier, accent, verdict_class = "Tier 4 · Decline",       "red",    "verdict-declined"
        note = "Does Not Meet Minimum Risk Thresholds"

    verdict_word  = "APPROVED" if prediction[0] == 1 else "DECLINED"
    verdict_emoji = "✦" if prediction[0] == 1 else "✕"

    # ── REPORT HEADER ──
    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">04 · Risk Intelligence Report</div>', unsafe_allow_html=True)

    # ── KPI GRID ──
    bar_color_map = {
        "green":  "linear-gradient(90deg,#2ECC71,#27ae60)",
        "blue":   "linear-gradient(90deg,#3B9EFF,#2980b9)",
        "orange": "linear-gradient(90deg,#F5A623,#e67e22)",
        "red":    "linear-gradient(90deg,#E74C3C,#c0392b)",
    }

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card {accent}">
            <div class="kpi-label">Risk Classification</div>
            <div class="kpi-value {accent}">{tier}</div>
            <div class="kpi-sub">{note}</div>
        </div>
        <div class="kpi-card gold">
            <div class="kpi-label">Approval Probability</div>
            <div class="kpi-value gold">{prob*100:.1f}%</div>
            <div class="kpi-sub">Model confidence score</div>
        </div>
        <div class="kpi-card {'orange' if dti > 40 else 'green'}">
            <div class="kpi-label">Debt-to-Income Ratio</div>
            <div class="kpi-value {'orange' if dti > 40 else 'green'}">{dti:.1f}%</div>
            <div class="kpi-sub">Loan vs. annual income</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── PROBABILITY BAR ──
    bar_gradient = bar_color_map[accent]
    st.markdown(f"""
    <div class="prob-bar-wrap">
        <div class="prob-bar-label">
            <span>Approval Probability</span>
            <span>{prob*100:.1f}%</span>
        </div>
        <div class="prob-bar-track">
            <div class="prob-bar-fill" style="width:{prob*100:.1f}%;background:{bar_gradient};"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── VERDICT BOX ──
    verdict_color_map = {
        "green": "#2ECC71", "blue": "#3B9EFF",
        "orange": "#F5A623", "red": "#E74C3C"
    }
    vc = verdict_color_map[accent]
    st.markdown(f"""
    <div class="{verdict_class}">
        <div class="verdict-title" style="color:{vc};">
            {verdict_emoji} Final Verdict: {verdict_word}
        </div>
        <div class="verdict-note">
            Classified as <strong style="color:{vc};">{tier}</strong> · {note}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # ── DECISION INTERPRETABILITY ──
    st.markdown('<div class="section-label">05 · Decision Interpretability</div>', unsafe_allow_html=True)

    # Credit insight — matches new 5-tier score ranges
    score_label = credit_desc_main.split('·')[0].strip()   # e.g. "0.8 – 1.0"
    if credit_history_val >= 0.8:
        c_icon, c_cls = "✦", "good"
        c_title = f"Credit Score {score_label}  ·  Excellent"
        c_desc  = "Top-tier credit history. Consistent on-time repayments — the single strongest approval signal in the model."
    elif credit_history_val >= 0.6:
        c_icon, c_cls = "◈", "neutral"
        c_title = f"Credit Score {score_label}  ·  Good"
        c_desc  = "Solid repayment record with minor irregularities. Model treats this favorably; strong income compensates the margin."
    elif credit_history_val >= 0.4:
        c_icon, c_cls = "◇", "neutral"
        c_title = f"Credit Score {score_label}  ·  Average / No History"
        c_desc  = "Neutral zone. No strong positive or negative signal — model relies more heavily on income and education."
    elif credit_history_val >= 0.2:
        c_icon, c_cls = "▽", "warn"
        c_title = f"Credit Score {score_label}  ·  Below Average"
        c_desc  = "Some missed payments on record. Partially penalising score — a strong co-applicant or collateral may offset this."
    else:
        c_icon, c_cls = "✕", "bad"
        c_title = f"Credit Score {score_label}  ·  Very Poor"
        c_desc  = "Frequent defaults or serious delinquencies. This is the dominant reason for rejection — very difficult to offset with other factors."

    # Income insight
    total_income = applicant_income + coapplicant_income
    if total_income > 6000:
        i_icon, i_cls, i_title, i_desc = "✔", "good", "Income Capacity · Above Threshold", f"Combined monthly income of {total_income:,} provides stable debt coverage relative to loan size."
    else:
        i_icon, i_cls, i_title, i_desc = "⚠", "warn", "Income Capacity · Limited Coverage", f"Combined income of {total_income:,}/mo is tight. Consider reducing loan size or adding co-applicant."

    # DTI insight
    if dti < 30:
        d_icon, d_cls, d_title, d_desc = "✔", "good", "Debt-to-Income · Low Risk", "Loan burden is manageable relative to annual income. Model rewards this favorably."
    elif dti < 60:
        d_icon, d_cls, d_title, d_desc = "◈", "neutral", "Debt-to-Income · Moderate", "Loan is within acceptable range but leaves limited financial buffer."
    else:
        d_icon, d_cls, d_title, d_desc = "⚠", "warn", "Debt-to-Income · Elevated", "Loan amount is high relative to annual income. This increases default risk significantly."

    # Education insight
    if education == "Graduate":
        e_icon, e_cls, e_title, e_desc = "✔", "good", "Education · Graduate", "Graduate status is treated as a positive employment-stability proxy in this model."
    else:
        e_icon, e_cls, e_title, e_desc = "◇", "neutral", "Education · Non-Graduate", "Neutral signal; model compensates by focusing on income and credit history."

    st.markdown(f"""
    <div class="glass-card">
        <div class="insight-row">
            <div class="insight-icon {c_cls}">{c_icon}</div>
            <div class="insight-body">
                <strong>{c_title}</strong>
                <span>{c_desc}</span>
            </div>
        </div>
        <div class="insight-row">
            <div class="insight-icon {i_cls}">{i_icon}</div>
            <div class="insight-body">
                <strong>{i_title}</strong>
                <span>{i_desc}</span>
            </div>
        </div>
        <div class="insight-row">
            <div class="insight-icon {d_cls}">{d_icon}</div>
            <div class="insight-body">
                <strong>{d_title}</strong>
                <span>{d_desc}</span>
            </div>
        </div>
        <div class="insight-row">
            <div class="insight-icon {e_cls}">{e_icon}</div>
            <div class="insight-body">
                <strong>{e_title}</strong>
                <span>{e_desc}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if prediction[0] == 1:
        st.balloons()

# ── 9. FOOTER ────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="footer"> AI loan predicator · For Internal Underwriting Use Only · '
    'Results are probabilistic, not definitive</div>',
    unsafe_allow_html=True
)
