"""
Quantum Prisoner's Dilemma — Redesigned
Run: streamlit run app_new.py
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="배신할 것인가, 협력할 것인가?",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Inter:wght@400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    scroll-behavior: smooth;
}

/* ── App background ── */
.stApp {
    background:
        radial-gradient(ellipse 70% 50% at 10% 0%, rgba(88,60,255,.30) 0%, transparent 60%),
        radial-gradient(ellipse 55% 40% at 92% 8%, rgba(0,200,255,.22) 0%, transparent 55%),
        radial-gradient(ellipse 60% 60% at 50% 110%, rgba(0,255,170,.10) 0%, transparent 60%),
        linear-gradient(160deg, #06071A 0%, #0C1130 50%, #040612 100%);
    color: #EEF3FF;
}
.block-container { padding-top: 1.2rem; max-width: 1200px; }

/* ── Streamlit tab bar ── */
div[data-baseweb="tab-list"] {
    gap: 6px;
    background: rgba(255,255,255,.04);
    border-radius: 999px;
    padding: 6px;
    border: 1px solid rgba(255,255,255,.08);
    width: fit-content;
    margin: 0 auto 22px;
}
button[data-baseweb="tab"] {
    border-radius: 999px !important;
    padding: 10px 22px !important;
    background: transparent !important;
    border: none !important;
    transition: all .22s ease;
}
button[data-baseweb="tab"] p {
    color: rgba(238,243,255,.58) !important;
    font-weight: 700 !important;
    font-size: 14px !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(90deg, #5C3BFF, #00C8FF) !important;
    box-shadow: 0 0 22px rgba(0,200,255,.28) !important;
}
button[data-baseweb="tab"][aria-selected="true"] p {
    color: #fff !important;
}

/* ── Slider & inputs ── */
.stSlider > div > div { color: #BDA7FF; }
div[data-testid="stNumberInput"] input { background: rgba(255,255,255,.06); border-color: rgba(255,255,255,.12); color: #EEF3FF; }

/* ── Utility classes ── */
.glass {
    background: rgba(10,14,40,.70);
    border: 1px solid rgba(160,174,255,.18);
    border-radius: 28px;
    box-shadow: 0 20px 60px rgba(0,0,0,.30), inset 0 1px 0 rgba(255,255,255,.07);
    backdrop-filter: blur(14px);
    padding: 28px 32px;
    margin-bottom: 18px;
}
.card {
    background: rgba(255,255,255,.05);
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 20px;
    padding: 18px 20px;
    margin-bottom: 14px;
}
.kpi {
    background: linear-gradient(135deg, rgba(92,59,255,.22), rgba(0,200,255,.10));
    border: 1px solid rgba(160,174,255,.20);
    border-radius: 22px;
    padding: 22px 18px;
    text-align: center;
}
.kpi .lbl { font-size: 12px; font-weight: 700; color: rgba(238,243,255,.55); text-transform: uppercase; letter-spacing: .8px; }
.kpi .val { font-size: 40px; font-weight: 900; color: #BDA7FF; margin-top: 4px; line-height: 1.1; }

.badge {
    display: inline-block;
    padding: 5px 14px;
    border-radius: 999px;
    border: 1px solid rgba(0,200,255,.32);
    background: rgba(0,200,255,.09);
    color: #7EF4FF;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -.5px;
    margin-bottom: 4px;
}
.section-sub {
    color: rgba(238,243,255,.60);
    font-size: 15px;
    margin-bottom: 22px;
}
.muted { color: rgba(238,243,255,.55); font-size: 14px; }
a { color: #7EF4FF; text-decoration: underline; }
hr { border-color: rgba(255,255,255,.08); margin: 20px 0; }

/* ── Hero ── */
.hero-wrap {
    padding: 40px 36px 36px;
    border-radius: 32px;
    background: linear-gradient(140deg, rgba(92,59,255,.30) 0%, rgba(0,200,255,.14) 100%);
    border: 1px solid rgba(160,174,255,.22);
    box-shadow: 0 28px 90px rgba(0,0,0,.32), inset 0 1px 0 rgba(255,255,255,.12);
    margin-bottom: 22px;
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute; inset: 0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.02'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    opacity: .5;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 52px;
    font-weight: 800;
    letter-spacing: -2px;
    line-height: 1.08;
    margin: 0 0 14px;
}
.hero-sub {
    font-size: 18px;
    color: rgba(238,243,255,.72);
    max-width: 620px;
    line-height: 1.6;
}

/* ── Entanglement animation ── */
.ent-board {
    position: relative;
    height: 300px;
    border-radius: 24px;
    background:
        radial-gradient(circle at 50% 45%, rgba(0,200,255,.12), transparent 45%),
        linear-gradient(180deg, rgba(12,18,52,.96), rgba(5,8,22,.96));
    border: 1px solid rgba(135,160,255,.18);
    overflow: hidden;
}
.ent-player {
    position: absolute;
    top: 88px;
    width: 100px; height: 100px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 42px;
    box-shadow: 0 0 36px rgba(0,200,255,.30);
    background: radial-gradient(circle at 35% 30%, #fff, #88E8FF 14%, #6A56FF 55%, #141952 100%);
}
.ent-player.left  { left: 9%;  animation: pLeft 2.6s ease-in-out infinite; }
.ent-player.right { right: 9%; animation: pRight 2.6s ease-in-out infinite; }
.ent-rope {
    position: absolute;
    left: 21%; right: 21%; top: 132px; height: 14px;
    border-radius: 999px;
    background: linear-gradient(90deg, #7352FF, #00D1FF, #7352FF);
    box-shadow: 0 0 28px rgba(0,209,255,.40);
    animation: ropeGlow 1.9s ease-in-out infinite;
}
.ent-orb {
    position: absolute;
    left: 50%; top: 104px;
    transform: translateX(-50%);
    width: 74px; height: 74px;
    border-radius: 50%;
    background: radial-gradient(circle, #fff 0%, #00D1FF 20%, #7352FF 60%, rgba(115,82,255,.1) 76%);
    box-shadow: 0 0 52px rgba(115,82,255,.80);
    animation: orbPulse 2.2s ease-in-out infinite;
}
.ent-caption {
    position: absolute; left: 20px; right: 20px; bottom: 20px;
    font-size: 13px; color: rgba(238,243,255,.65); text-align: center;
}
.ent-label {
    position: absolute; top: 210px; font-size: 12px; font-weight: 700;
    color: rgba(238,243,255,.55); text-align: center; width: 100px;
}
.ent-label.left { left: 9%; }
.ent-label.right { right: 9%; }

@keyframes pLeft  { 0%,100%{transform:translateX(0)}  50%{transform:translateX(-12px)} }
@keyframes pRight { 0%,100%{transform:translateX(0)}  50%{transform:translateX(12px)} }
@keyframes ropeGlow { 0%,100%{filter:brightness(1);transform:scaleY(1)} 50%{filter:brightness(1.4);transform:scaleY(1.18)} }
@keyframes orbPulse { 0%,100%{transform:translateX(-50%) scale(1);filter:brightness(1)} 50%{transform:translateX(-50%) scale(1.10);filter:brightness(1.32)} }

/* ── Scenario story cards ── */
.story-step {
    display: flex; gap: 18px; align-items: flex-start;
    background: rgba(255,255,255,.045);
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 20px;
    padding: 18px 20px;
    margin-bottom: 12px;
}
.step-num {
    min-width: 36px; height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #5C3BFF, #00C8FF);
    display: flex; align-items: center; justify-content: center;
    font-weight: 900; font-size: 16px; flex-shrink: 0;
}
.step-body h4 { margin: 0 0 4px; font-size: 16px; font-weight: 700; }
.step-body p  { margin: 0; font-size: 14px; color: rgba(238,243,255,.68); line-height: 1.55; }

/* ── Payoff matrix table styling ── */
.payoff-table {
    width: 100%; border-collapse: collapse; font-size: 15px;
    border-radius: 16px; overflow: hidden;
}
.payoff-table th {
    background: rgba(92,59,255,.20);
    padding: 10px 16px; font-weight: 700;
    border: 1px solid rgba(255,255,255,.09);
    color: rgba(238,243,255,.88);
}
.payoff-table td {
    padding: 10px 16px; text-align: center;
    border: 1px solid rgba(255,255,255,.07);
    background: rgba(255,255,255,.03);
}
.payoff-table .highlight { background: rgba(0,200,255,.12); font-weight: 700; }
.payoff-table .nash-cell { background: rgba(255,50,100,.14); border: 1px solid rgba(255,80,80,.28) !important; }

/* ── Game play area ── */
.choice-btn-wrap { display: flex; gap: 14px; flex-wrap: wrap; }

/* ── Quantum lab circuit visual ── */
.circuit {
    background: rgba(8,12,35,.90);
    border: 1px solid rgba(115,82,255,.20);
    border-radius: 20px;
    padding: 22px 28px;
    font-family: 'Inter', monospace;
    font-size: 14px;
    line-height: 2.0;
    color: rgba(238,243,255,.80);
}
.circuit .wire  { color: #7EF4FF; font-weight: 700; }
.circuit .gate  { color: #BDA7FF; font-weight: 800; }
.circuit .arrow { color: rgba(238,243,255,.35); }

/* ── Explainer section ── */
.concept-pill {
    display: inline-block;
    padding: 4px 12px; margin-right: 6px; margin-bottom: 6px;
    border-radius: 999px;
    border: 1px solid rgba(0,200,255,.28);
    background: rgba(0,200,255,.07);
    color: #7EF4FF; font-size: 12px; font-weight: 700;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,.03); }
::-webkit-scrollbar-thumb { background: rgba(115,82,255,.35); border-radius: 99px; }

/* ── Info/success/warning overrides ── */
div[data-testid="stAlert"] {
    border-radius: 16px !important;
    border: 1px solid rgba(255,255,255,.09) !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Quantum math helpers
# ─────────────────────────────────────────────
def U_strategy(theta: float, phi: float) -> np.ndarray:
    return np.array([
        [np.exp(1j * phi) * np.cos(theta / 2),  np.sin(theta / 2)],
        [-np.sin(theta / 2), np.exp(-1j * phi) * np.cos(theta / 2)],
    ], dtype=complex)

def J_gate(gamma: float) -> np.ndarray:
    I = np.eye(2, dtype=complex)
    D = U_strategy(np.pi, 0.0)
    return np.cos(gamma / 2) * np.kron(I, I) + 1j * np.sin(gamma / 2) * np.kron(D, D)

def quantum_probs(theta_a, phi_a, theta_b, phi_b, gamma):
    init = np.array([1, 0, 0, 0], dtype=complex)
    J = J_gate(gamma)
    final = J.conj().T @ np.kron(U_strategy(theta_a, phi_a), U_strategy(theta_b, phi_b)) @ J @ init
    p = np.abs(final) ** 2
    return {"CC": float(p[0]), "CD": float(p[1]), "DC": float(p[2]), "DD": float(p[3])}

def expected_payoff(probs, A, B):
    idx = {"CC": (0,0), "CD": (0,1), "DC": (1,0), "DD": (1,1)}
    ea, eb = 0.0, 0.0
    for k, pr in probs.items():
        i, j = idx[k]
        ea += pr * A[i,j];  eb += pr * B[i,j]
    return ea, eb

def classical_nash(A, B):
    out = []
    for i in range(2):
        for j in range(2):
            if A[i,j] == np.max(A[:,j]) and B[i,j] == np.max(B[i,:]):
                out.append((i,j))
    return out

def preset_params(choice):
    mapping = {
        "협력 C":    (0.0, 0.0),
        "배신 D":    (np.pi, 0.0),
        "양자 Q":    (0.0, np.pi/2),
    }
    return mapping.get(choice, (None, None))

# ─────────────────────────────────────────────
# Chart helpers
# ─────────────────────────────────────────────
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,.025)",
    font=dict(color="#EEF3FF", family="Inter"),
    margin=dict(l=22, r=22, t=44, b=22),
)

def prob_bar(probs):
    labels = ["CC\n(둘다협력)", "CD\n(A협력·B배신)", "DC\n(A배신·B협력)", "DD\n(둘다배신)"]
    colors = ["#00C8FF", "#FF6B6B", "#FF9F45", "#BDA7FF"]
    vals = [probs["CC"], probs["CD"], probs["DC"], probs["DD"]]
    fig = go.Figure(go.Bar(
        x=labels, y=vals,
        marker_color=colors,
        text=[f"{v*100:.1f}%" for v in vals],
        textposition="outside",
    ))
    fig.update_layout(**CHART_LAYOUT, height=330, title="결과 확률 분포",
                      yaxis=dict(range=[0,1.15], gridcolor="rgba(255,255,255,.07)", tickformat=".0%"),
                      xaxis=dict(gridcolor="rgba(255,255,255,.05)"))
    return fig

def gamma_sweep_chart(A, B):
    rows = []
    for g in np.linspace(0, np.pi/2, 100):
        p = quantum_probs(0.0, np.pi/2, 0.0, np.pi/2, g)
        ea, eb = expected_payoff(p, A, B)
        rows.append({"γ": g, "기대보수 (양자Q×Q)": ea, "협력확률 P(CC)": p["CC"]})
    df = pd.DataFrame(rows)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["γ"], y=df["기대보수 (양자Q×Q)"],
                             mode="lines", name="기대보수 (Q×Q)",
                             line=dict(color="#BDA7FF", width=2.5)))
    fig.add_trace(go.Scatter(x=df["γ"], y=df["협력확률 P(CC)"],
                             mode="lines", name="협력 확률 P(CC)",
                             line=dict(color="#00C8FF", width=2.5, dash="dot")))
    fig.add_hline(y=float(A[1,1]), line_color="rgba(255,100,100,.55)", line_dash="dash",
                  annotation_text="고전적 (D,D) 보수", annotation_font_color="rgba(255,100,100,.8)")
    fig.update_layout(**CHART_LAYOUT, height=360, title="얽힘 강도 γ에 따른 변화 (Q×Q 전략)",
                      xaxis=dict(title="얽힘 강도 γ", gridcolor="rgba(255,255,255,.06)"),
                      yaxis=dict(gridcolor="rgba(255,255,255,.07)"),
                      legend=dict(bgcolor="rgba(0,0,0,0)"))
    return fig

# ─────────────────────────────────────────────
# Default payoff values
# ─────────────────────────────────────────────
R_default, T_default, S_default, P_default = 3.0, 5.0, 0.0, 1.0

# Sidebar for advanced users
with st.sidebar:
    st.markdown("### ⚙️ 점수판 커스터마이즈")
    st.caption("고전적 죄수의 딜레마 기본값: T > R > P > S")
    R = st.number_input("둘 다 협력 R", value=R_default, step=0.5)
    T = st.number_input("나만 배신 T (최대 보상)", value=T_default, step=0.5)
    S = st.number_input("나만 협력 S (최저 보상)", value=S_default, step=0.5)
    P = st.number_input("둘 다 배신 P", value=P_default, step=0.5)
    st.divider()
    default_gamma = st.slider("기본 얽힘 γ", 0.0, float(np.pi/2), float(np.pi/2), key="sidebar_gamma")

A = np.array([[R, S], [T, P]], dtype=float)
B = np.array([[R, T], [S, P]], dtype=float)


# ─────────────────────────────────────────────
# HERO SECTION
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
  <div class="badge">🎮 Interactive Quantum Game</div>
  <div class="hero-title">배신할 것인가,<br>협력할 것인가?</div>
  <div class="hero-sub">
    당신의 선택 하나가 상대의 운명을, 상대의 선택이 당신의 운명을 바꿉니다.<br>
    그런데 만약 두 사람의 전략이 <b>양자적으로 얽혀</b> 있다면? 규칙이 달라집니다.
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🎭 딜레마란?",
    "🕹️ 게임하기",
    "⚛️ 양자로 보기",
    "📖 프로젝트 스토리",
])


# ══════════════════════════════════════════════
# TAB 1 : 죄수의 딜레마 소개 — 스토리 방식
# ══════════════════════════════════════════════
with tab1:
    st.markdown('<div class="glass">', unsafe_allow_html=True)

    col_left, col_right = st.columns([1.1, 0.9], gap="large")

    with col_left:
        st.markdown('<div class="badge">THE SETUP</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">당신은 지금 심문실에 있습니다</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">형사가 문을 열고 들어옵니다. 선택의 시간.</div>', unsafe_allow_html=True)

        st.markdown("""
<div class="story-step">
  <div class="step-num">1</div>
  <div class="step-body">
    <h4>🚔 상황: 당신과 공범이 각각 다른 방에 갇혔습니다</h4>
    <p>서로 연락은 불가능합니다. 형사는 각자에게 같은 제안을 합니다.<br>
    "상대를 신고하면 당신은 풀려납니다. 둘 다 침묵하면 둘 다 가볍게 처벌받습니다."</p>
  </div>
</div>
<div class="story-step">
  <div class="step-num">2</div>
  <div class="step-body">
    <h4>🤝 협력(침묵) vs ⚔️ 배신(신고)</h4>
    <p>둘 다 침묵 → 가벼운 처벌 (각 1년). 한 명만 신고 → 신고자 석방, 상대 5년.<br>
    둘 다 신고 → 둘 다 3년. 어떻게 해야 할까요?</p>
  </div>
</div>
<div class="story-step">
  <div class="step-num">3</div>
  <div class="step-body">
    <h4>😱 역설: 합리적으로 행동하면 왜 둘 다 손해 볼까?</h4>
    <p>상대가 침묵하든 신고하든, 나는 신고하는 게 항상 유리합니다.<br>
    상대도 같은 생각 → 결국 둘 다 신고 → 둘 다 3년형. 함께 침묵했으면 1년씩인데!</p>
  </div>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="card" style="background:rgba(255,200,0,.07);border-color:rgba(255,200,0,.18);">
  <b>💡 이게 왜 중요한가요?</b><br>
  <span style="font-size:14px;color:rgba(238,243,255,.72);">
  죄수의 딜레마는 단순한 게임이 아닙니다. 핵 군비 경쟁, 기후 협약, 가격 담합, SNS 알고리즘 설계까지
  — 현실 세계에서 "합리적 개인"이 모여 "비합리적 집단 결과"를 만드는 패턴 그 자체입니다.
  자세히 알고 싶다면 → <a href="https://ko.wikipedia.org/wiki/%EC%A3%84%EC%88%98%EC%9D%98_%EB%94%9C%EB%A0%88%EB%A7%88" target="_blank">위키백과: 죄수의 딜레마</a>
  | <a href="https://plato.stanford.edu/entries/prisoner-dilemma/" target="_blank">Stanford Encyclopedia (영문)</a>
  </span>
</div>
""", unsafe_allow_html=True)

    with col_right:
        # Animated entanglement board
        st.markdown("""
<div class="ent-board">
  <div class="ent-rope"></div>
  <div class="ent-orb"></div>
  <div class="ent-player left">😰</div>
  <div class="ent-player right">😰</div>
  <div class="ent-label left">당신</div>
  <div class="ent-label right">공범</div>
  <div class="ent-caption">
    두 사람은 독립적으로 선택하는 것 같지만,<br>결과는 하나의 운명으로 연결되어 있습니다.
  </div>
</div>
""", unsafe_allow_html=True)

        # Payoff matrix — visually highlighted
        st.markdown("<br>", unsafe_allow_html=True)
        nash_cells = classical_nash(A, B)

        def cell_class(i, j):
            return "nash-cell" if (i, j) in nash_cells else ""

        nash_label = {(0,0):"C,C", (0,1):"C,D", (1,0):"D,C", (1,1):"D,D"}
        nash_str = ", ".join(f"({nash_label[n]})" for n in nash_cells) if nash_cells else "순수전략 균형 없음"

        st.markdown(f"""
<table class="payoff-table">
  <tr>
    <th></th>
    <th>상대: 협력 🤝</th>
    <th>상대: 배신 ⚔️</th>
  </tr>
  <tr>
    <th>나: 협력 🤝</th>
    <td class="{cell_class(0,0)}">나 <b>{A[0,0]:.0f}점</b>, 상대 <b>{B[0,0]:.0f}점</b></td>
    <td class="{cell_class(0,1)}">나 <b>{A[0,1]:.0f}점</b>, 상대 <b>{B[0,1]:.0f}점</b></td>
  </tr>
  <tr>
    <th>나: 배신 ⚔️</th>
    <td class="{cell_class(1,0)}">나 <b>{A[1,0]:.0f}점</b>, 상대 <b>{B[1,0]:.0f}점</b></td>
    <td class="{cell_class(1,1)}">나 <b>{A[1,1]:.0f}점</b>, 상대 <b>{B[1,1]:.0f}점</b></td>
  </tr>
</table>
<div style="margin-top:10px;font-size:13px;color:rgba(238,243,255,.55);">
  🔴 붉은 칸 = 고전적 내쉬균형: <b>{nash_str}</b>
  — 어느 쪽도 혼자 전략을 바꿀 유인이 없는 균형점입니다.
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="card" style="margin-top:14px;">
  <b>⚛️ 양자 게임이 다른 이유</b><br>
  <span style="font-size:13px;color:rgba(238,243,255,.65);">
  전략을 '협력' 또는 '배신' 둘 중 하나로 고정하지 않고,
  두 가능성이 <b>동시에 공존하는 큐비트 상태</b>로 표현합니다.
  얽힘(Entanglement)이 충분할 때, 고전적 균형의 딜레마가 사라질 수 있습니다.
  </span>
</div>
""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Bottom teaser
    st.markdown("""
<div style="text-align:center;padding:14px 0 4px;">
  <span style="color:rgba(238,243,255,.45);font-size:14px;">
    ↓ 직접 선택해보고 싶다면 <b>🕹️ 게임하기</b> 탭으로 이동하세요
  </span>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 2 : 게임 플레이
# ══════════════════════════════════════════════
with tab2:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('<div class="badge">LIVE GAME</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">직접 선택하고 결과를 확인하세요</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">당신은 Player A입니다. 상대(Player B)와의 전략 조합 + 얽힘 강도를 바꿔가며 기대 점수를 관찰해보세요.</div>', unsafe_allow_html=True)

    # Entanglement slider — front and center
    gamma_col, _, _ = st.columns([2, 1, 1])
    with gamma_col:
        gamma = st.slider(
            "⚛️ 얽힘 강도 γ (0 = 고전 게임, π/2 = 완전 양자 얽힘)",
            0.0, float(np.pi/2), float(np.pi/2), key="game_gamma",
            help="γ=0이면 순수 고전 게임, γ=π/2면 두 플레이어가 완전히 얽혀있는 양자 게임입니다."
        )

    st.markdown("<hr>", unsafe_allow_html=True)

    # Strategy selection — left/right
    pa_col, pb_col = st.columns(2, gap="large")
    with pa_col:
        st.markdown("#### 🙋 나 (Player A) 전략 선택")
        choice_a = st.radio("", ["협력 C", "배신 D", "양자 Q", "직접 설정"],
                             horizontal=True, key="ga_choice",
                             captions=["🤝 협력", "⚔️ 배신", "🌀 양자", "🎛️ 커스텀"])
        theta_a, phi_a = preset_params(choice_a)
        if choice_a == "직접 설정":
            theta_a = st.slider("A: θ (협력↔배신 비율)", 0.0, float(np.pi), 0.0, key="ga_t")
            phi_a   = st.slider("A: φ (위상 각도)",       0.0, float(np.pi/2), float(np.pi/2), key="ga_p")

    with pb_col:
        st.markdown("#### 🤖 상대 (Player B) 전략 선택")
        choice_b = st.radio("", ["협력 C", "배신 D", "양자 Q", "직접 설정"],
                             horizontal=True, key="gb_choice",
                             captions=["🤝 협력", "⚔️ 배신", "🌀 양자", "🎛️ 커스텀"])
        theta_b, phi_b = preset_params(choice_b)
        if choice_b == "직접 설정":
            theta_b = st.slider("B: θ", 0.0, float(np.pi), 0.0, key="gb_t")
            phi_b   = st.slider("B: φ", 0.0, float(np.pi/2), float(np.pi/2), key="gb_p")

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Compute ──
    probs = quantum_probs(theta_a, phi_a, theta_b, phi_b, gamma)
    ea, eb = expected_payoff(probs, A, B)
    cc_pct = probs["CC"] * 100

    # ── KPIs ──
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f'<div class="kpi"><div class="lbl">나의 기대 점수</div><div class="val">{ea:.2f}</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="kpi"><div class="lbl">상대의 기대 점수</div><div class="val">{eb:.2f}</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="kpi"><div class="lbl">협력 확률 P(CC)</div><div class="val">{cc_pct:.1f}%</div></div>', unsafe_allow_html=True)
    with k4:
        nash_val = P  # classical DD payoff
        delta = ea - nash_val
        sign = "+" if delta >= 0 else ""
        color = "#00C8FF" if delta >= 0 else "#FF6B6B"
        st.markdown(f'<div class="kpi"><div class="lbl">고전균형 대비 내 이득</div><div class="val" style="color:{color};">{sign}{delta:.2f}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    chart_col, result_col = st.columns([1.3, 0.7], gap="large")
    with chart_col:
        st.plotly_chart(prob_bar(probs), use_container_width=True)

    with result_col:
        st.markdown('<div class="card"><b>📊 결과 해석</b><br><br>', unsafe_allow_html=True)

        both_better = ea > P and eb > P
        if both_better:
            st.success(f"🎉 두 플레이어 모두 고전적 균형(D,D={P:.0f}점)보다 높은 점수를 얻고 있습니다!\n양자 전략이 딜레마를 완화했습니다.")
        elif ea > P:
            st.info("나는 고전 균형보다 유리하지만, 상대는 아직 아닙니다.")
        elif eb > P:
            st.info("상대가 고전 균형보다 유리하지만, 나는 아직 아닙니다.")
        else:
            st.warning(f"두 플레이어 모두 고전 균형 수준입니다.\n얽힘 γ를 올리거나 양자 Q 전략을 써보세요.")

        st.markdown(f"""
<br>
<span class="muted">
선택한 전략<br>
<b>나 A</b>: {choice_a} — θ={theta_a:.2f}, φ={phi_a:.2f}<br>
<b>상대 B</b>: {choice_b} — θ={theta_b:.2f}, φ={phi_b:.2f}<br>
얽힘 γ = {gamma:.3f}
</span>
""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
<div class="card">
<b>🧪 추천 실험</b>
<ol style="font-size:13px;color:rgba(238,243,255,.68);padding-left:18px;margin:8px 0 0;">
<li>두 플레이어 모두 <b>배신 D</b> → 고전 딜레마 재현</li>
<li>둘 다 <b>양자 Q</b> + γ=π/2 → 딜레마 탈출!</li>
<li>한 명만 <b>Q</b>, 한 명은 <b>D</b> → 누가 유리할까?</li>
</ol>
</div>
""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 3 : 양자 개념 해설
# ══════════════════════════════════════════════
with tab3:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('<div class="badge">QUANTUM EXPLAINER</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">게임 뒤에 숨은 양자 이론</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">수식 없이 개념을 먼저, 수식이 궁금하면 링크를 타고 이동하세요.</div>', unsafe_allow_html=True)

    left_col, right_col = st.columns([1, 1], gap="large")

    with left_col:
        # Entanglement animation — reused
        st.markdown("""
<div class="ent-board">
  <div class="ent-rope"></div>
  <div class="ent-orb"></div>
  <div class="ent-player left">|0⟩</div>
  <div class="ent-player right">|1⟩</div>
  <div class="ent-label left">Player A</div>
  <div class="ent-label right">Player B</div>
  <div class="ent-caption">
    EWL 흐름: |00⟩ → <b>J</b> → U_A⊗U_B → <b>J†</b> → 측정
  </div>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="circuit" style="margin-top:16px;">
  <div><span class="wire">q₀ :</span> ─|0⟩─ <span class="gate">[J]</span> ─ <span class="gate">[U_A(θ,φ)]</span> ─ <span class="gate">[J†]</span> ─ <span class="gate">M</span></div>
  <div><span class="wire">q₁ :</span> ─|0⟩─ <span class="gate">[J]</span> ─ <span class="gate">[U_B(θ,φ)]</span> ─ <span class="gate">[J†]</span> ─ <span class="gate">M</span></div>
  <div style="margin-top:10px;font-size:12px;color:rgba(238,243,255,.40);">
  J = cos(γ/2)·I⊗I + i·sin(γ/2)·D⊗D
  </div>
</div>
<div style="margin-top:12px;font-size:13px;color:rgba(238,243,255,.55);">
  수식 전체를 보고 싶다면 →
  <a href="https://arxiv.org/abs/quant-ph/9806088" target="_blank">EWL 원 논문 (Eisert et al. 1999)</a>
  | <a href="https://en.wikipedia.org/wiki/Quantum_game_theory" target="_blank">Quantum Game Theory (Wikipedia)</a>
</div>
""", unsafe_allow_html=True)

    with right_col:
        st.markdown("""
<div class="card">
  <h4>🌀 1. 중첩 (Superposition)</h4>
  <p style="font-size:14px;color:rgba(238,243,255,.68);">
  고전 게임에서 전략은 '협력 또는 배신', 딱 하나입니다.
  양자 게임에서 전략은 U(θ, φ) 게이트 — 두 가능성이 <b>동시에 존재</b>합니다.
  θ=0이면 완전 협력, θ=π이면 완전 배신, 중간값이면 중첩 상태.
  </p>
  <span class="concept-pill">θ ∈ [0, π]</span>
  <span class="concept-pill">φ ∈ [0, π/2]</span>
</div>

<div class="card">
  <h4>🔗 2. 얽힘 (Entanglement)</h4>
  <p style="font-size:14px;color:rgba(238,243,255,.68);">
  J 게이트가 두 큐비트를 '얽어' 놓습니다. γ=0이면 독립적인 고전 게임,
  γ=π/2이면 두 플레이어의 결합 상태가 분리 불가능한 <b>완전 얽힘</b>이 됩니다.
  이 때 전략 공간이 근본적으로 달라집니다.
  </p>
  <span class="concept-pill">γ = 0 → 고전</span>
  <span class="concept-pill">γ = π/2 → 완전 얽힘</span>
  <a href="https://ko.wikipedia.org/wiki/%EC%96%BD%ED%9E%98" target="_blank" style="font-size:12px;">얽힘이란? →</a>
</div>

<div class="card">
  <h4>🔄 3. 간섭 (Interference)</h4>
  <p style="font-size:14px;color:rgba(238,243,255,.68);">
  위상 φ는 결과 경로들 사이의 <b>간섭</b>을 제어합니다.
  양자 협력 전략 Q = U(0, π/2)는 위상 조작으로 (D,D) 결과를 억누르고
  (C,C) 결과를 강화합니다 — 얽힘이 충분할 때만.
  </p>
  <span class="concept-pill">φ = π/2 → 양자 Q 전략</span>
</div>

<div class="card">
  <h4>⚖️ 4. 양자 내쉬균형</h4>
  <p style="font-size:14px;color:rgba(238,243,255,.68);">
  완전 얽힘(γ=π/2) 상태에서 두 플레이어가 모두 Q 전략을 쓰면,
  어느 쪽도 혼자 전략을 바꿔서 이득을 볼 수 없습니다.
  이것이 <b>양자 내쉬균형</b>이며, (C,C)와 동일한 보수를 줍니다.
  </p>
  <a href="https://en.wikipedia.org/wiki/Nash_equilibrium" target="_blank" style="font-size:12px;">내쉬균형이란? →</a>
</div>
""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Gamma sweep chart
    st.markdown("#### 얽힘 강도가 올라갈수록 무슨 일이 생길까? — Q×Q 전략 시뮬레이션")
    st.plotly_chart(gamma_sweep_chart(A, B), use_container_width=True)

    st.info("""
**읽는 법**: γ가 증가할수록 Q×Q 전략에서의 기대보수가 상승하고, 협력 확률 P(CC)도 높아집니다.
빨간 점선(고전적 (D,D) 보수)을 넘는 순간이 딜레마가 완화되는 지점입니다.
양자 전략은 '협력을 강요'하는 게 아니라, '협력이 합리적인 균형이 될 수 있는 공간'을 만드는 것입니다.
""")

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 4 : 프로젝트 스토리
# ══════════════════════════════════════════════
with tab4:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('<div class="badge">PROJECT STORY</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">이 앱은 어떻게 만들어졌나</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Qiskit 수업 기말 대체 프로젝트 — 문제 설정부터 배포까지의 여정</div>', unsafe_allow_html=True)

    r1c1, r1c2 = st.columns(2, gap="large")
    with r1c1:
        st.markdown("""
<div class="card">
  <h4>🎯 문제 설정</h4>
  <p style="font-size:14px;color:rgba(238,243,255,.68);">
  죄수의 딜레마는 '합리적 개인이 모여 비효율적 집단 결과를 만드는' 역설입니다.
  수업에서 배운 <b>중첩·얽힘</b>을 게임 전략 공간에 도입하면 이 역설이 사라질 수 있을까?
  라는 질문에서 시작했습니다.
  </p>
</div>
<div class="card">
  <h4>🔬 EWL 모델 채택</h4>
  <p style="font-size:14px;color:rgba(238,243,255,.68);">
  Eisert·Wilkens·Lewenstein(1999)이 제안한 EWL 모델이 양자 게임이론의 표준입니다.
  얽힘 게이트 J로 두 큐비트를 얽은 뒤, 각 플레이어가 U(θ,φ) 전략을 적용하고,
  J†로 역변환 후 측정합니다.
  <a href="https://arxiv.org/abs/quant-ph/9806088" target="_blank">원 논문 →</a>
  </p>
</div>
""", unsafe_allow_html=True)

    with r1c2:
        st.markdown("""
<div class="card">
  <h4>⚙️ 개발 과정</h4>
  <p style="font-size:14px;color:rgba(238,243,255,.68);">
  Python(NumPy)으로 EWL 행렬 연산 구현 → Plotly로 시각화 →
  Streamlit으로 인터랙티브 웹앱 제작 → Streamlit Cloud 배포.
  Qiskit 수업에서 배운 양자 게이트 관점을 수치 시뮬레이션으로 연결했습니다.
  </p>
</div>
<div class="card">
  <h4>🧗 어려웠던 점</h4>
  <p style="font-size:14px;color:rgba(238,243,255,.68);">
  '양자 내쉬균형'을 자동 탐색하려면 연속 전략 공간 위의 최적화가 필요합니다.
  현재는 사용자가 파라미터를 직접 조작하는 시뮬레이션 방식으로 구현했습니다.
  Streamlit Cloud 배포 시 Qiskit 의존성 충돌을 requirements.txt 조정으로 해결했습니다.
  </p>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="card" style="background:rgba(92,59,255,.10);border-color:rgba(92,59,255,.26);">
  <h4>💬 회고</h4>
  <p style="font-size:14px;color:rgba(238,243,255,.72);">
  AI 도구(LLM)는 아이디어 구체화, 코드 초안, 디버깅에 큰 도움이 됐습니다.
  하지만 각 행렬 연산이 EWL 모델에서 무엇을 의미하는지, 왜 γ=π/2에서 딜레마가 완화되는지
  — 결국 이해는 스스로 해야 했습니다.
  향후 방향: 자동 균형 탐색, 3인 게임 확장, 다양한 경제학 게임 적용.
  </p>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.code("고전적 죄수의 딜레마를 EWL 양자 게임 모델로 확장하여, 얽힘과 위상이 협력 가능성과 기대보수를 어떻게 바꾸는지 사용자가 직접 실험할 수 있는 웹앱입니다.", language=None)

    st.markdown("""
<div style="margin-top:16px;font-size:13px;color:rgba(238,243,255,.45);">
  참고 자료:
  <a href="https://arxiv.org/abs/quant-ph/9806088">Eisert et al. (1999)</a> ·
  <a href="https://en.wikipedia.org/wiki/Quantum_game_theory">Quantum Game Theory (Wikipedia)</a> ·
  <a href="https://qiskit.org/documentation/">Qiskit Docs</a>
</div>
""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# Footer
st.markdown("""
<div style="text-align:center;padding:24px 0 10px;color:rgba(238,243,255,.30);font-size:13px;">
  ⚛️ Quantum Prisoner's Dilemma · EWL Model · Built with Streamlit + NumPy + Plotly
</div>
""", unsafe_allow_html=True)
