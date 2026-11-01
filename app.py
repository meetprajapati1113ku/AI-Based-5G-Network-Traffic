import streamlit as st
import pandas as pd
import joblib
import numpy as np

# PAGE CONFIG
st.set_page_config(
    page_title="5G Smart Network AI",
    page_icon="📡",
    layout="wide"
)

# LOAD MODEL
@st.cache_resource
def load_model():
    return joblib.load("5G_Traffic_Model.pkl")

try:
    model = load_model()
except Exception as e:
    st.error(f"Model loading error: {e}")
    st.stop()

# CUSTOM CSS
st.markdown("""
<style>
.stApp {
    background-color: #080e1c;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #111b30;
}

h1, h2, h3 {
    color: #38bdf8 !important;
}

.metric-card {
    background: linear-gradient(135deg,#172b49,#102039);
    padding: 22px;
    border-radius: 15px;
    border: 1px solid #245078;
    text-align: center;
    margin-bottom: 15px;
}

.metric-card h2 {
    color: #38bdf8;
    font-size: 28px;
}

.metric-card p {
    color: #cbd5e1;
}

.result-card {
    background: #142b40;
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #38bdf8;
    text-align: center;
}

.stButton button {
    background: linear-gradient(90deg,#0284c7,#2563eb);
    color: white;
    border-radius: 10px;
    height: 50px;
    font-weight: bold;
    border: none;
}

</style>
""", unsafe_allow_html=True)

# HEADER
st.title("📡 5G SMART NETWORK")
st.subheader("AI-Based Network Traffic Prediction System")

st.markdown(
    "Intelligent network traffic prediction using "
    "Machine Learning and Random Forest Classifier."
)

st.divider()

# SIDEBAR
st.sidebar.title("🌐 NETWORK CONTROL")

st.sidebar.success("AI Model: Loaded")
st.sidebar.info("Algorithm: Random Forest")
st.sidebar.info("Language: Python")
st.sidebar.info("Framework: Streamlit")

st.sidebar.markdown("---")
st.sidebar.write("Prediction Classes")
st.sidebar.write("🟢 LOW")
st.sidebar.write("🟡 MEDIUM")
st.sidebar.write("🔴 HIGH")

# INPUT SECTION
st.header("⚙️ Network Parameters")

col1, col2 = st.columns(2)

with col1:

    users = st.number_input(
        "👥 Connected Users",
        10, 1999, 1500, 10
    )

    bandwidth = st.number_input(
        "📶 Bandwidth (Mbps)",
        50, 999, 200, 10
    )

    signal = st.number_input(
        "📡 Signal Strength",
        1, 100, 80, 1
    )

with col2:

    packets = st.number_input(
        "📊 Packet Rate",
        100, 9999, 8500, 100
    )

    hour = st.slider(
        "🕒 Network Hour",
        0, 23, 20
    )

st.divider()

# LIVE STATISTICS
st.header("📈 Network Statistics")

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(
        f'<div class="metric-card"><p>Connected Users</p>'
        f'<h2>{users}</h2></div>',
        unsafe_allow_html=True
    )

with m2:
    st.markdown(
        f'<div class="metric-card"><p>Bandwidth</p>'
        f'<h2>{bandwidth}</h2><p>Mbps</p></div>',
        unsafe_allow_html=True
    )

with m3:
    st.markdown(
        f'<div class="metric-card"><p>Signal Strength</p>'
        f'<h2>{signal}%</h2></div>',
        unsafe_allow_html=True
    )

with m4:
    st.markdown(
        f'<div class="metric-card"><p>Packet Rate</p>'
        f'<h2>{packets}</h2></div>',
        unsafe_allow_html=True
    )

st.divider()

# PREDICTION
st.header("🤖 AI Traffic Prediction")

if st.button(
    "🚀 PREDICT NETWORK TRAFFIC",
    use_container_width=True
):

    input_data = pd.DataFrame([{
        "connected_users": users,
        "bandwidth_mbps": bandwidth,
        "signal_strength": signal,
        "packet_rate": packets,
        "hour": hour
    }])

    prediction = str(model.predict(input_data)[0])

    st.session_state["prediction"] = prediction
    st.session_state["input_data"] = input_data

    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(input_data)[0]

        st.session_state["probabilities"] = probabilities

        st.session_state["classes"] = model.classes_

# SHOW RESULT
if "prediction" in st.session_state:

    prediction = st.session_state["prediction"]

    st.subheader("🎯 Prediction Result")

    if prediction.lower() == "low":

        st.success("🟢 LOW NETWORK TRAFFIC")

        recommendation = (
            "Network traffic is predicted to be low. "
            "Normal network operation can continue."
        )

    elif prediction.lower() == "medium":

        st.warning("🟡 MEDIUM NETWORK TRAFFIC")

        recommendation = (
            "Moderate network traffic is predicted. "
            "Monitor bandwidth and network performance."
        )

    else:

        st.error("🔴 HIGH NETWORK TRAFFIC")

        recommendation = (
            "High network traffic is predicted. "
            "Consider load balancing and resource allocation."
        )

    st.markdown(
        f'<div class="result-card">'
        f'<h2>AI Prediction: {prediction.upper()}</h2>'
        f'<p>Random Forest Classifier Result</p>'
        f'</div>',
        unsafe_allow_html=True
    )

    st.divider()

    # PROBABILITY GRAPH
    if "probabilities" in st.session_state:

        st.header("📊 AI Prediction Probability")

        probability_df = pd.DataFrame({
            "Traffic Category": st.session_state["classes"],
            "Probability (%)":
                np.round(
                    st.session_state["probabilities"] * 100,
                    2
                )
        }).set_index("Traffic Category")

        st.bar_chart(probability_df)

        st.dataframe(
            probability_df,
            use_container_width=True
        )

    # TRAFFIC ANALYSIS
    st.header("📈 Traffic Analysis")

    if prediction.lower() == "low":
        st.info("Network load category: LOW")

    elif prediction.lower() == "medium":
        st.info("Network load category: MEDIUM")

    else:
        st.info("Network load category: HIGH")

    # WHAT-IF GRAPH
    st.subheader("🔍 Connected Users Sensitivity Analysis")

    user_values = sorted(set([
        max(10, users - 400),
        max(10, users - 200),
        users,
        min(1999, users + 200),
        min(1999, users + 400)
    ]))

    scenario_rows = []

    for user_count in user_values:

        scenario = st.session_state["input_data"].copy()

        scenario["connected_users"] = user_count

        if hasattr(model, "predict_proba"):

            probs = model.predict_proba(scenario)[0]

            for cls, prob in zip(model.classes_, probs):

                scenario_rows.append({
                    "Connected Users": user_count,
                    "Traffic Category": str(cls),
                    "Probability (%)": round(prob * 100, 2)
                })

    if scenario_rows:

        scenario_df = pd.DataFrame(scenario_rows)

        chart_df = scenario_df.pivot(
            index="Connected Users",
            columns="Traffic Category",
            values="Probability (%)"
        )

        st.line_chart(chart_df)

        st.caption(
            "What-if analysis: model probabilities when "
            "connected-user count changes while other inputs "
            "remain constant."
        )

    # RECOMMENDATIONS
    st.header("💡 AI Network Recommendations")

    st.info(recommendation)

    if signal < 40:

        st.warning(
            "Weak signal input: investigate signal coverage "
            "and interference."
        )

    if bandwidth < 150:

        st.warning(
            "Lower bandwidth input: review available bandwidth."
        )

    if packets > 8000:

        st.warning(
            "High packet-rate input: monitor packet processing."
        )

    st.success("AI prediction completed successfully!")

st.divider()

# FOOTER
st.markdown("""
<center>

### 📡 5G SMART NETWORK

AI-Based 5G Network Traffic Prediction

Developed using Python | Machine Learning | Streamlit

**Team Project**

</center>
""", unsafe_allow_html=True)

st.caption(
    "Educational prototype using a model trained on synthetic data. "
    "Predictions are not live telecom network measurements."
)
