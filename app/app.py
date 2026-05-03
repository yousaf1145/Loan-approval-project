import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(
    page_title="CareXpert · Risk Intelligence",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=DM+Mono:wght@300;400;500&family=Outfit:wght@300;400;500;600&display=swap');
*{box-sizing:border-box;}
html,body,[data-testid="stAppViewContainer"]{background:#080C1A !important;font-family:'Outfit',sans-serif;color:#F0EDE8;}
[data-testid="stAppViewContainer"]::before{content:"";position:fixed;inset:0;background:radial-gradient(ellipse 70% 50% at 15% 20%,rgba(201,168,76,0.05) 0%,transparent 60%),radial-gradient(ellipse 50% 40% at 85% 80%,rgba(59,158,255,0.04) 0%,transparent 60%);pointer-events:none;z-index:0;}
[data-testid="stHeader"]{background:transparent !important;}
.block-container{padding-top:1.5rem !important;padding-bottom:3rem !important;max-width:1400px !important;}
#MainMenu,footer,header{visibility:hidden;}
/* inputs */
label[data-testid="stWidgetLabel"] p{font-family:'DM Mono',monospace !important;font-size:0.65rem !important;letter-spacing:0.12em !important;text-transform:uppercase !important;color:#8A8FA8 !important;}
[data-testid="stSelectbox"]>div>div{background:rgba(255,255,255,0.04) !important;border:1px solid rgba(255,255,255,0.09) !important;border-radius:8px !important;color:#F0EDE8 !important;}
[data-testid="stSelectbox"]>div>div:hover{border-color:#C9A84C !important;}
[data-testid="stNumberInput"] input{background:rgba(255,255,255,0.04) !important;border:1px solid rgba(255,255,255,0.09) !important;border-radius:8px !important;color:#F0EDE8 !important;font-family:'DM Mono',monospace !important;}
[data-testid="stNumberInput"] input:focus{border-color:#C9A84C !important;}
/* main submit button */
section.main [data-testid="stButton"]>button{width:100% !important;background:linear-gradient(135deg,#C9A84C 0%,#A07B2E 100%) !important;color:#080C1A !important;font-family:'Outfit',sans-serif !important;font-weight:600 !important;font-size:0.88rem !important;letter-spacing:0.08em !important;text-transform:uppercase !important;border:none !important;border-radius:10px !important;padding:0.8rem 2rem !important;box-shadow:0 4px 20px rgba(201,168,76,0.25) !important;transition:all .25s !important;}
section.main [data-testid="stButton"]>button:hover{transform:translateY(-2px) !important;box-shadow:0 8px 28px rgba(201,168,76,0.4) !important;}
[data-testid="stAlert"]{display:none !important;}
[data-testid="stMetric"]{display:none !important;}
</style>
""", unsafe_allow_html=True)

# ── LOAD MODEL ──────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path  = os.path.join(current_dir, "..", "model")
    try:
        model    = joblib.load(os.path.join(model_path, "loan_logistic_model.pkl"))
        features = joblib.load(os.path.join(model_path, "feature_names.pkl"))
        return model, features
    except FileNotFoundError:
        st.error(f"Model files not found at: {os.path.abspath(model_path)}")
        return None, None

model, model_features = load_model()

# ── CREDIT OPTIONS ──────────────────────────────────────────────────────────
credit_options = {
    "0.8 - 1.0  |  Excellent":          {"value":1.0,"icon":"✦","color":"#2ECC71","bg":"rgba(46,204,113,0.12)","border":"rgba(46,204,113,0.4)","desc":"Highest trust tier. Consistent on-time repayment history. Strongest approval signal in the model."},
    "0.6 - 0.8  |  Good":               {"value":0.7,"icon":"◈","color":"#3B9EFF","bg":"rgba(59,158,255,0.12)","border":"rgba(59,158,255,0.4)","desc":"Reliable repayment with only minor delays. Model treats this favorably."},
    "0.4 - 0.6  |  Average":            {"value":0.5,"icon":"◇","color":"#F5A623","bg":"rgba(245,166,35,0.12)","border":"rgba(245,166,35,0.4)","desc":"Neutral zone or first-time borrowers. Model shifts weight to income and education."},
    "0.2 - 0.4  |  Below Average":      {"value":0.3,"icon":"▽","color":"#F5A623","bg":"rgba(245,166,35,0.08)","border":"rgba(245,166,35,0.3)","desc":"Some missed payments on record. Strong co-applicant may partially offset."},
    "0.0 - 0.2  |  Very Poor":          {"value":0.0,"icon":"✕","color":"#E74C3C","bg":"rgba(231,76,60,0.12)","border":"rgba(231,76,60,0.4)","desc":"Frequent defaults detected. Critical risk flag — very difficult to offset."},
}

CREDIT_HELP = "Ranges from 0.0 (very poor) to 1.0 (excellent). Request your e-CIB report from your bank or sbp.org.pk to find your score."

# ── HELPERS ─────────────────────────────────────────────────────────────────
def html_card(content, extra=""):
    return f'''<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:14px;padding:1.4rem 1.6rem;margin-bottom:1rem;{extra}">{content}</div>'''

def sec_label(text):
    return f'''<div style="font-family:'DM Mono',monospace;font-size:0.6rem;letter-spacing:0.2em;color:#C9A84C;text-transform:uppercase;margin-bottom:0.9rem;display:flex;align-items:center;gap:0.6rem;">{text}<span style="flex:1;height:1px;background:linear-gradient(90deg,rgba(255,255,255,0.08),transparent);display:inline-block;"></span></div>'''

def gold_div():
    return '<div style="height:1px;background:linear-gradient(90deg,transparent,#C9A84C,transparent);margin:1.2rem 0;opacity:0.25;"></div>'

# ── LAYOUT: left guide panel + right form ───────────────────────────────────
left_col, right_col = st.columns([1, 2.8], gap="large")

# ══════════════════════════════════════════════════════
#  LEFT PANEL — Credit Score Guide
# ══════════════════════════════════════════════════════
with left_col:
    st.markdown('''
    <div style="background:#0D1326;border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:1.6rem 1.4rem;position:sticky;top:1rem;">

        <div style="font-family:'Cormorant Garamond',serif;font-size:1.6rem;font-weight:700;color:#C9A84C;margin-bottom:2px;">⬡ CareXpert</div>
        <div style="font-family:'DM Mono',monospace;font-size:0.55rem;letter-spacing:0.18em;text-transform:uppercase;color:#2A2F44;margin-bottom:1rem;">Risk Intelligence v2.0</div>
        <div style="height:1px;background:rgba(255,255,255,0.07);margin-bottom:1rem;"></div>

        <div style="font-family:'DM Mono',monospace;font-size:0.6rem;letter-spacing:0.16em;text-transform:uppercase;color:#C9A84C;margin-bottom:0.5rem;">📊 Credit Score Guide</div>
        <div style="font-size:0.75rem;color:#8A8FA8;line-height:1.5;margin-bottom:1rem;">Select a range in the form. Your matching tier is highlighted below.</div>
    ''', unsafe_allow_html=True)

    selected_credit = st.session_state.get("main_credit_score", list(credit_options.keys())[0])

    for key, meta in credit_options.items():
        is_active = (key == selected_credit)
        short     = key.split("|")[0].strip()
        name      = key.split("|")[1].strip()
        fg        = meta["color"]
        if is_active:
            bg     = meta["bg"]
            border = "1.5px solid " + fg
            bl     = "4px solid " + fg
            nc     = "#F0EDE8"
            dc     = "#A0A5B8"
            op     = "1"
            tag    = "<span style=\"float:right;font-size:0.52rem;font-family:monospace;text-transform:uppercase;letter-spacing:0.1em;color:" + fg + ";background:" + meta["bg"] + ";border:1px solid " + fg + "55;border-radius:3px;padding:1px 5px;\">Active</span>"
        else:
            bg     = "rgba(255,255,255,0.02)"
            border = "1px solid rgba(255,255,255,0.07)"
            bl     = "3px solid rgba(255,255,255,0.08)"
            nc     = "#4A5066"
            dc     = "#353A50"
            op     = "0.6"
            tag    = ""

        card = (
            "<div style=\"background:" + bg + ";border:" + border + ";border-left:" + bl +
            ";border-radius:9px;padding:0.6rem 0.85rem;margin-bottom:0.4rem;opacity:" + op + "\">"
            "<div style=\"display:flex;align-items:center;justify-content:space-between;margin-bottom:2px;\">"
            "<span style=\"font-family:monospace;font-size:0.65rem;color:" + fg + "\">" + short + "</span>" + tag +
            "</div>"
            "<div style=\"font-size:0.78rem;font-weight:600;color:" + nc + ";margin-bottom:2px;\">" + meta["icon"] + " " + name + "</div>"
            "<div style=\"font-size:0.68rem;color:" + dc + ";line-height:1.4;\">" + meta["desc"] + "</div>"
            "</div>"
        )
        st.markdown(card, unsafe_allow_html=True)

    st.markdown('''
        <div style="height:1px;background:rgba(255,255,255,0.07);margin:1rem 0;"></div>
        <div style="font-family:'DM Mono',monospace;font-size:0.6rem;letter-spacing:0.15em;text-transform:uppercase;color:#C9A84C;margin-bottom:0.5rem;">🏦 How to Check Your Score</div>
        <div style="background:rgba(201,168,76,0.07);border:1px solid rgba(201,168,76,0.22);border-radius:9px;padding:0.85rem;font-size:0.74rem;color:#8A8FA8;line-height:1.7;">
            <span style="color:#E8C97A;font-weight:600;">e-CIB Report</span><br>
            <span style="color:#C9A84C;">①</span> Visit your bank branch<br>
            <span style="color:#C9A84C;">②</span> Go to <strong style="color:#C9A84C;">sbp.org.pk</strong> → eCIB<br>
            <span style="color:#C9A84C;">③</span> Match score to range above
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑  Clear Form", key="clear_form", use_container_width=True):
        for k in [k for k in st.session_state if k != "clear_form"]:
            del st.session_state[k]
        st.rerun()

# ══════════════════════════════════════════════════════
#  RIGHT PANEL — Form + Report
# ══════════════════════════════════════════════════════
with right_col:

    # Hero
    st.markdown('''
    <div style="background:linear-gradient(135deg,#0D1326 0%,#0A1228 100%);border:1px solid rgba(255,255,255,0.08);border-top:2px solid #C9A84C;border-radius:14px;padding:2rem 2.2rem;margin-bottom:1.6rem;position:relative;overflow:hidden;">
        <div style="position:absolute;right:1.8rem;top:50%;transform:translateY(-50%);font-size:6rem;color:rgba(201,168,76,0.06);">⬡</div>
        <div style="font-family:'DM Mono',monospace;font-size:0.6rem;letter-spacing:0.2em;color:#C9A84C;text-transform:uppercase;margin-bottom:0.4rem;">▸ Underwriting Intelligence Platform</div>
        <div style="font-family:'Cormorant Garamond',serif;font-size:2.2rem;font-weight:700;line-height:1.1;margin-bottom:0.3rem;">AI <span style="color:#C9A84C;">Loan</span> Predicator</div>
        <div style="color:#8A8FA8;font-size:0.88rem;font-weight:300;">Complete the applicant profile below to generate a structured risk assessment.</div>
    </div>
    ''', unsafe_allow_html=True)

    # 01 Demographics
    st.markdown(sec_label("01 · Applicant Demographics"), unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        gender     = st.selectbox("Gender", ["Male","Female"])
    with c2:
        married    = st.selectbox("Marital Status", ["Yes","No"], format_func=lambda x:"Married" if x=="Yes" else "Single")
    with c3:
        dependents = st.selectbox("Dependents", ["0","1","2","3+"])
    c4, c5 = st.columns(2)
    with c4:
        education     = st.selectbox("Education Level", ["Graduate","Not Graduate"])
    with c5:
        self_employed = st.selectbox("Employment Type", ["No","Yes"], format_func=lambda x:"Salaried" if x=="No" else "Self-Employed")

    st.markdown(gold_div(), unsafe_allow_html=True)

    # 02 Financial
    st.markdown(sec_label("02 · Financial Profile"), unsafe_allow_html=True)
    c6, c7 = st.columns(2)
    with c6:
        applicant_income   = st.number_input("Applicant Monthly Income (PKR)", min_value=0, value=5000, step=500)
        loan_amount        = st.number_input("Loan Amount (in thousands)", min_value=0, value=150, step=10)
    with c7:
        coapplicant_income = st.number_input("Co-Applicant Monthly Income (PKR)", min_value=0, value=0, step=500)
        loan_term          = st.number_input("Loan Term (Days)", min_value=0, value=360, step=30)

    st.markdown(gold_div(), unsafe_allow_html=True)

    # 03 Property & Credit
    st.markdown(sec_label("03 · Property & Credit"), unsafe_allow_html=True)
    c8, c9 = st.columns(2)
    with c8:
        property_area = st.selectbox("Property Area", ["Urban","Semiurban","Rural"])
    with c9:
        credit_desc = st.selectbox("Credit History Score Range", list(credit_options.keys()), index=0, key="main_credit_score", help=CREDIT_HELP)

    credit_val = credit_options[credit_desc]["value"]

    # Credit info box — always visible below the dropdown
    cm = credit_options[credit_desc]
    info_box = (
        "<div style=\"background:" + cm["bg"] + ";border:1px solid " + cm["border"] + ";"
        "border-radius:11px;padding:1rem 1.2rem;margin-top:0.5rem;\">"
        "<div style=\"display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;\">"
        "<span style=\"font-size:1rem;\">" + cm["icon"] + "</span>"
        "<span style=\"font-family:monospace;font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;color:" + cm["color"] + ";\">"
        "Selected · " + credit_desc.split("|")[1].strip() + "</span></div>"
        "<div style=\"font-size:0.78rem;color:#A0A5B8;line-height:1.55;margin-bottom:0.7rem;\">" + cm["desc"] + "</div>"
        "<div style=\"height:1px;background:rgba(255,255,255,0.06);margin-bottom:0.7rem;\"></div>"
        "<div style=\"font-family:monospace;font-size:0.58rem;letter-spacing:0.13em;text-transform:uppercase;color:" + cm["color"] + ";margin-bottom:0.4rem;\">🏦 Where to find your credit score</div>"
        "<div style=\"font-size:0.76rem;color:#8A8FA8;line-height:1.75;\">"
        "<span style=\"color:" + cm["color"] + ";font-weight:600;\">①</span> Visit your <strong style=\"color:#C0C5D8;\">bank branch</strong> → request an official <strong style=\"color:#C0C5D8;\">e-CIB report</strong><br>"
        "<span style=\"color:" + cm["color"] + ";font-weight:600;\">②</span> Or go to <strong style=\"color:#C9A84C;\">sbp.org.pk</strong> → eCIB section → check your ECIB standing<br>"
        "<span style=\"color:" + cm["color"] + ";font-weight:600;\">③</span> Match the score on your report to the range selected above"
        "</div></div>"
    )
    st.markdown(info_box, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    submit = st.button("⬡  Generate Risk Intelligence Report", key="submit", use_container_width=True)

    # ── REPORT ────────────────────────────────────────
    if st.session_state.get("submit"):
        if model is None or model_features is None:
            st.stop()

        input_df = pd.DataFrame([{
            "Gender": gender, "Married": married, "Dependents": dependents,
            "Education": education, "Self_Employed": self_employed,
            "ApplicantIncome": applicant_income, "CoapplicantIncome": coapplicant_income,
            "LoanAmount": loan_amount, "Loan_Amount_Term": loan_term,
            "Credit_History": credit_val, "Property_Area": property_area,
        }])
        input_df["Property_Area_Semiurban"] = 1 if property_area == "Semiurban" else 0
        input_df["Property_Area_Urban"]     = 1 if property_area == "Urban"     else 0
        input_df["Gender"]        = 1 if gender        == "Male"     else 0
        input_df["Married"]       = 1 if married        == "Yes"      else 0
        input_df["Education"]     = 1 if education      == "Graduate" else 0
        input_df["Self_Employed"] = 1 if self_employed  == "Yes"      else 0
        input_df["Dependents"]    = input_df["Dependents"].replace("3+", 3).astype(int)
        input_df = input_df.drop(columns=["Property_Area"])[model_features]

        prediction = model.predict(input_df)
        prob       = model.predict_proba(input_df)[0][1]
        annual_inc = (applicant_income + coapplicant_income) * 12
        dti        = (loan_amount * 1000 / annual_inc * 100) if annual_inc > 0 else 0
        approved   = prediction[0] == 1

        if prob >= 0.80:   tier,accent,note = "Tier 1 · High Trust",    "#2ECC71","Auto-Approval Recommended"
        elif prob >= 0.60: tier,accent,note = "Tier 2 · Moderate Risk", "#3B9EFF","Manual Underwriter Review Required"
        elif prob >= 0.35: tier,accent,note = "Tier 3 · High Risk",     "#F5A623","Additional Collateral or Co-Signer Required"
        else:              tier,accent,note = "Tier 4 · Decline",       "#E74C3C","Does Not Meet Minimum Risk Thresholds"

        verdict_word  = "APPROVED" if approved else "DECLINED"
        verdict_icon  = "✦" if approved else "✕"
        verdict_color = "#2ECC71" if approved else "#E74C3C"
        dti_color     = "#F5A623" if dti > 40 else "#2ECC71"

        st.markdown(gold_div(), unsafe_allow_html=True)
        st.markdown(sec_label("04 · Risk Intelligence Report"), unsafe_allow_html=True)

        # KPI row
        st.markdown(
            "<div style=\"display:grid;grid-template-columns:1fr 1fr 1fr;gap:0.9rem;margin-bottom:1rem;\">"
            "<div style=\"background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:1.1rem 1.3rem;border-top:2px solid " + accent + ";\">"
            "<div style=\"font-family:monospace;font-size:0.58rem;letter-spacing:0.15em;text-transform:uppercase;color:#4A5066;margin-bottom:0.4rem;\">Risk Classification</div>"
            "<div style=\"font-family:'Cormorant Garamond',serif;font-size:1.4rem;font-weight:700;color:" + accent + ";line-height:1;margin-bottom:0.2rem;\">" + tier + "</div>"
            "<div style=\"font-size:0.7rem;color:#4A5066;\">" + note + "</div>"
            "</div>"
            "<div style=\"background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:1.1rem 1.3rem;border-top:2px solid #C9A84C;\">"
            "<div style=\"font-family:monospace;font-size:0.58rem;letter-spacing:0.15em;text-transform:uppercase;color:#4A5066;margin-bottom:0.4rem;\">Approval Probability</div>"
            "<div style=\"font-family:'Cormorant Garamond',serif;font-size:1.8rem;font-weight:700;color:#C9A84C;line-height:1;margin-bottom:0.2rem;\">" + f"{prob*100:.1f}%" + "</div>"
            "<div style=\"font-size:0.7rem;color:#4A5066;\">Model confidence score</div>"
            "</div>"
            "<div style=\"background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:1.1rem 1.3rem;border-top:2px solid " + dti_color + ";\">"
            "<div style=\"font-family:monospace;font-size:0.58rem;letter-spacing:0.15em;text-transform:uppercase;color:#4A5066;margin-bottom:0.4rem;\">Debt-to-Income Ratio</div>"
            "<div style=\"font-family:'Cormorant Garamond',serif;font-size:1.8rem;font-weight:700;color:" + dti_color + ";line-height:1;margin-bottom:0.2rem;\">" + f"{dti:.1f}%" + "</div>"
            "<div style=\"font-size:0.7rem;color:#4A5066;\">Loan vs. annual income</div>"
            "</div></div>",
            unsafe_allow_html=True
        )

        # Prob bar
        bar_grad = "linear-gradient(90deg," + accent + "," + accent + "88)"
        st.markdown(
            "<div style=\"margin-bottom:1rem;\">"
            "<div style=\"display:flex;justify-content:space-between;font-family:monospace;font-size:0.65rem;color:#4A5066;margin-bottom:4px;\">"
            "<span>Approval Probability</span><span>" + f"{prob*100:.1f}%" + "</span></div>"
            "<div style=\"background:rgba(255,255,255,0.06);border-radius:99px;height:6px;overflow:hidden;\">"
            "<div style=\"height:100%;border-radius:99px;background:" + bar_grad + ";width:" + f"{prob*100:.1f}%" + ";\"></div></div></div>",
            unsafe_allow_html=True
        )

        # Verdict
        vbg = "linear-gradient(135deg," + verdict_color + "1A," + verdict_color + "0A)"
        st.markdown(
            "<div style=\"background:" + vbg + ";border:1px solid " + verdict_color + "44;border-left:4px solid " + verdict_color + ";border-radius:12px;padding:1.3rem 1.6rem;margin-bottom:1rem;\">"
            "<div style=\"font-family:'Cormorant Garamond',serif;font-size:1.5rem;font-weight:700;color:" + verdict_color + ";margin-bottom:0.2rem;\">"
            + verdict_icon + " Final Verdict: " + verdict_word + "</div>"
            "<div style=\"font-size:0.82rem;color:#8A8FA8;\">Classified as <strong style=\"color:" + verdict_color + ";\">" + tier + "</strong> · " + note + "</div>"
            "</div>",
            unsafe_allow_html=True
        )

        st.markdown(gold_div(), unsafe_allow_html=True)
        st.markdown(sec_label("05 · Decision Interpretability"), unsafe_allow_html=True)

        # Insights
        def insight(icon, cls_color, title, desc):
            bg_map = {"#2ECC71":"rgba(46,204,113,0.12)","#3B9EFF":"rgba(59,158,255,0.12)","#F5A623":"rgba(245,166,35,0.12)","#E74C3C":"rgba(231,76,60,0.12)"}
            ibg = bg_map.get(cls_color, "rgba(255,255,255,0.06)")
            return (
                "<div style=\"display:flex;align-items:flex-start;gap:0.9rem;padding:0.85rem 0;border-bottom:1px solid rgba(255,255,255,0.07);\">"
                "<div style=\"width:32px;height:32px;border-radius:7px;background:" + ibg + ";display:flex;align-items:center;justify-content:center;font-size:0.85rem;flex-shrink:0;\">" + icon + "</div>"
                "<div><strong style=\"display:block;font-size:0.82rem;font-weight:500;color:#F0EDE8;margin-bottom:2px;\">" + title + "</strong>"
                "<span style=\"font-size:0.74rem;color:#4A5066;\">" + desc + "</span></div></div>"
            )

        cv = credit_val
        if   cv >= 0.8: ci,cc,ct,cd = "✦","#2ECC71","Credit Score 0.8-1.0 · Excellent",      "Top-tier credit history. Consistent on-time repayments — the single strongest approval signal."
        elif cv >= 0.6: ci,cc,ct,cd = "◈","#3B9EFF","Credit Score 0.6-0.8 · Good",           "Solid repayment record. Model treats this favorably; strong income compensates the margin."
        elif cv >= 0.4: ci,cc,ct,cd = "◇","#F5A623","Credit Score 0.4-0.6 · Average",        "Neutral zone. Model relies more heavily on income and education."
        elif cv >= 0.2: ci,cc,ct,cd = "▽","#F5A623","Credit Score 0.2-0.4 · Below Average",  "Some missed payments. A strong co-applicant or collateral may offset this."
        else:           ci,cc,ct,cd = "✕","#E74C3C","Credit Score 0.0-0.2 · Very Poor",       "Frequent defaults — dominant reason for rejection, very difficult to offset."

        ti = applicant_income + coapplicant_income
        ii = "✔" if ti > 6000 else "⚠"
        ic = "#2ECC71" if ti > 6000 else "#F5A623"
        it = "Income Capacity · Above Threshold" if ti > 6000 else "Income Capacity · Limited Coverage"
        id_ = f"Combined monthly income of {ti:,} provides stable debt coverage." if ti > 6000 else f"Combined income of {ti:,}/mo is tight. Consider reducing loan size or adding co-applicant."

        di = "✔" if dti < 30 else "◈" if dti < 60 else "⚠"
        dc = "#2ECC71" if dti < 30 else "#3B9EFF" if dti < 60 else "#F5A623"
        dt = "Debt-to-Income · Low Risk" if dti < 30 else "Debt-to-Income · Moderate" if dti < 60 else "Debt-to-Income · Elevated"
        dd = "Loan burden is manageable. Model rewards this favorably." if dti < 30 else "Within acceptable range but leaves limited buffer." if dti < 60 else "High relative to annual income — increases default risk significantly."

        ei = "✔" if education == "Graduate" else "◇"
        ec = "#2ECC71" if education == "Graduate" else "#3B9EFF"
        et = "Education · Graduate" if education == "Graduate" else "Education · Non-Graduate"
        ed = "Graduate status is a positive employment-stability proxy in this model." if education == "Graduate" else "Neutral signal; model compensates via income and credit history."

        rows = insight(ci,cc,ct,cd) + insight(ii,ic,it,id_) + insight(di,dc,dt,dd) + insight(ei,ec,et,ed)
        st.markdown(
            "<div style=\"background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:13px;padding:0.5rem 1.4rem 0.2rem;\">" + rows + "</div>",
            unsafe_allow_html=True
        )

        if approved:
            st.balloons()

    st.markdown(
        "<div style=\"text-align:center;font-family:monospace;font-size:0.55rem;letter-spacing:0.14em;color:#252A3A;text-transform:uppercase;padding:2rem 0 0.5rem;\">"
        "AI Loan Predicator · For Internal Underwriting Use Only · Results are probabilistic, not definitive</div>",
        unsafe_allow_html=True
    )
