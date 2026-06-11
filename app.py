import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Quantum Game Lab", layout="wide")

st.title("Quantum Game Lab")
st.caption("Classical Nash Equilibrium vs EWL Quantum Game Simulator")

# ----------------------------
# Core functions
# ----------------------------

def classical_nash_equilibria(payoff_A, payoff_B):
    equilibria = []

    for i in range(2):
        for j in range(2):
            a_best = payoff_A[i, j] == np.max(payoff_A[:, j])
            b_best = payoff_B[i, j] == np.max(payoff_B[i, :])

            if a_best and b_best:
                equilibria.append((i, j))

    return equilibria


def U_strategy(theta, phi):
    return np.array([
        [np.exp(1j * phi) * np.cos(theta / 2), np.sin(theta / 2)],
        [-np.sin(theta / 2), np.exp(-1j * phi) * np.cos(theta / 2)]
    ], dtype=complex)


def J_gate(gamma):
    I = np.eye(2, dtype=complex)
    D = U_strategy(np.pi, 0)

    return (
        np.cos(gamma / 2) * np.kron(I, I)
        + 1j * np.sin(gamma / 2) * np.kron(D, D)
    )


def quantum_game_probabilities(theta_A, phi_A, theta_B, phi_B, gamma):
    initial_state = np.array([1, 0, 0, 0], dtype=complex)

    J = J_gate(gamma)
    J_dagger = J.conj().T

    U_A = U_strategy(theta_A, phi_A)
    U_B = U_strategy(theta_B, phi_B)

    final_state = J_dagger @ np.kron(U_A, U_B) @ J @ initial_state
    probs = np.abs(final_state) ** 2

    return {
        "CC": probs[0],
        "CD": probs[1],
        "DC": probs[2],
        "DD": probs[3]
    }


def expected_payoff(probs, payoff_A, payoff_B):
    mapping = {
        "CC": (0, 0),
        "CD": (0, 1),
        "DC": (1, 0),
        "DD": (1, 1)
    }

    EA, EB = 0, 0

    for outcome, prob in probs.items():
        i, j = mapping[outcome]
        EA += prob * payoff_A[i, j]
        EB += prob * payoff_B[i, j]

    return EA, EB


# ----------------------------
# Payoff input
# ----------------------------

st.sidebar.header("1. Payoff Matrix")

st.sidebar.write("Default: Prisoner's Dilemma")

A_CC = st.sidebar.number_input("A payoff: CC", value=3.0)
A_CD = st.sidebar.number_input("A payoff: CD", value=0.0)
A_DC = st.sidebar.number_input("A payoff: DC", value=5.0)
A_DD = st.sidebar.number_input("A payoff: DD", value=1.0)

B_CC = st.sidebar.number_input("B payoff: CC", value=3.0)
B_CD = st.sidebar.number_input("B payoff: CD", value=5.0)
B_DC = st.sidebar.number_input("B payoff: DC", value=0.0)
B_DD = st.sidebar.number_input("B payoff: DD", value=1.0)

payoff_A = np.array([[A_CC, A_CD], [A_DC, A_DD]])
payoff_B = np.array([[B_CC, B_CD], [B_DC, B_DD]])

# ----------------------------
# Quantum parameters
# ----------------------------

st.sidebar.header("2. Quantum Strategy Parameters")

gamma = st.sidebar.slider("Entanglement γ", 0.0, np.pi / 2, np.pi / 2)

theta_A = st.sidebar.slider("Player A θ", 0.0, np.pi, 0.0)
phi_A = st.sidebar.slider("Player A φ", 0.0, np.pi / 2, np.pi / 2)

theta_B = st.sidebar.slider("Player B θ", 0.0, np.pi, 0.0)
phi_B = st.sidebar.slider("Player B φ", 0.0, np.pi / 2, np.pi / 2)

# ----------------------------
# Classical result
# ----------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("Classical Game")

    payoff_df = pd.DataFrame({
        "B: Cooperate": [f"({A_CC}, {B_CC})", f"({A_DC}, {B_DC})"],
        "B: Defect": [f"({A_CD}, {B_CD})", f"({A_DD}, {B_DD})"]
    }, index=["A: Cooperate", "A: Defect"])

    st.table(payoff_df)

    ne = classical_nash_equilibria(payoff_A, payoff_B)

    label = {
        (0, 0): "(C, C)",
        (0, 1): "(C, D)",
        (1, 0): "(D, C)",
        (1, 1): "(D, D)"
    }

    st.write("Classical Nash Equilibrium:")
    if ne:
        st.success(", ".join([label[x] for x in ne]))
    else:
        st.warning("No pure-strategy Nash equilibrium found.")

# ----------------------------
# Quantum result
# ----------------------------

with col2:
    st.subheader("Quantum Game Result")

    probs = quantum_game_probabilities(theta_A, phi_A, theta_B, phi_B, gamma)
    EA, EB = expected_payoff(probs, payoff_A, payoff_B)

    st.metric("Expected Payoff A", round(EA, 4))
    st.metric("Expected Payoff B", round(EB, 4))

    prob_df = pd.DataFrame({
        "Outcome": list(probs.keys()),
        "Probability": list(probs.values())
    })

    fig = px.bar(prob_df, x="Outcome", y="Probability", title="Measurement Probabilities")
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# Entanglement sweep
# ----------------------------

st.subheader("Payoff Change by Entanglement Level")

gammas = np.linspace(0, np.pi / 2, 100)

rows = []
for g in gammas:
    p = quantum_game_probabilities(theta_A, phi_A, theta_B, phi_B, g)
    ea, eb = expected_payoff(p, payoff_A, payoff_B)
    rows.append({
        "gamma": g,
        "Player A Payoff": ea,
        "Player B Payoff": eb,
        "Cooperation Probability": p["CC"]
    })

sweep_df = pd.DataFrame(rows)

fig_payoff = px.line(
    sweep_df,
    x="gamma",
    y=["Player A Payoff", "Player B Payoff"],
    title="Expected Payoff by Entanglement"
)

st.plotly_chart(fig_payoff, use_container_width=True)

fig_coop = px.line(
    sweep_df,
    x="gamma",
    y="Cooperation Probability",
    title="Cooperation Probability P(CC) by Entanglement"
)

st.plotly_chart(fig_coop, use_container_width=True)

st.markdown("""
### Interpretation

- γ = 0 means the game is close to the classical case.
- γ = π/2 means maximal entanglement.
- θ and φ represent each player's quantum strategy.
- The outcome probabilities are calculated from the final quantum state.
- Expected payoff is calculated by multiplying each outcome probability by the original payoff matrix.
""")