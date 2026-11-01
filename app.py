import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="NEXUS 5G Intelligence",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# LOAD AI MODEL
# =====================================

@st.cache_resource
def load_model():
    return joblib.load("5G_Traffic_Model.pkl")

try:
    model = load_model()
except Exception as e:
    st.error(f"AI Model Loading Error: {e}")
    st.stop()

# =====================================
# SESSION STATE
# =====================================

if "history" not in st.session_state:
    st.session_state.history = []

if "result" not in st.session_state:
    st.session_state.result = None

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #07111f,
        #101d35,
        #081321
    );
    color: white;
}

section[data-testid="stSidebar"] {
    background: #0c1930;
}

h1, h2, h3 {
    color: #38bdf8 !important;
}

.hero {
    padding: 30px;
    border-radius: 18px;
    background: linear-gradient(
        120deg,
        #102e52,
        #123d65,
        #172554
    );
    border: 1px solid #2563eb;
    text-align: center;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 42px;
    color: #ffffff !important;
}

.hero p {
    color: #bae6fd;
    font-size: 17px;
}

.metric {
    background: linear-gradient(
        145deg,
        #172d4c,
        #102039
    );
    border: 1px solid #245078;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    min-height: 115px;
}

.metric h2 {
    color: #38bdf8;
    font-size: 27px;
}

.metric p {
    color: #cbd5e1;
}

.result {
    background: linear-gradient(
        120deg,
        #102c49,
        #172554
    );
    padding: 30px;
    border-radius: 18px;
    border: 1px solid #38bdf8;
    text-align: center;
}

.team {
    background: #142b46;
    border: 1px solid #2563eb;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    margin: 8px;
}

.team h3 {
    color: #38bdf8;
}

div.stButton > button {
    background: linear-gradient(
        90deg,
        #0284c7,
        #2563eb
    );
    color: white;
    border-radius: 10px;
    height: 50px;
    font-weight: bold;
    border: none;
}

div.stButton > button:hover {
    background: #0ea5e9;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("📡 NEXUS 5G")

st.sidebar.success("AI MODEL: ONLINE")

st.sidebar.markdown("---")

st.sidebar.subheader("SYSTEM INFORMATION")

st.sidebar.write("🤖 Algorithm: Random Forest")
st.sidebar.write("🐍 Language: Python")
st.sidebar.write("⚡ Framework: Streamlit")
st.sidebar.write("🧠 AI Status: Loaded")

st.sidebar.markdown("---")

st.sidebar.subheader("TRAFFIC CATEGORIES")

st.sidebar.write("🟢 LOW TRAFFIC")
st.sidebar.write("🟡 MEDIUM TRAFFIC")
st.sidebar.write("🔴 HIGH TRAFFIC")

st.sidebar.markdown("---")

st.sidebar.caption(
    "NEXUS 5G Intelligence | Academic Project"
)

# =====================================
# HERO SECTION
# =====================================

st.markdown("""
<div class="hero">

<h1>🚀 NEXUS 5G INTELLIGENCE</h1>

<p>
AI-POWERED NETWORK COMMAND CENTER
</p>

<p>
Next Generation 5G Network Traffic Prediction
</p>

</div>
""", unsafe_allow_html=True)

st.success("SYSTEM STATUS: AI MODEL LOADED SUCCESSFULLY")

# =====================================
# PROJECT INFORMATION
# =====================================

with st.expander("📘 About Our Project"):

    st.write("""
    NEXUS 5G is an AI-based network traffic
    prediction system.

    It uses Machine Learning to classify
    network traffic into Low, Medium and High.

    Algorithm: Random Forest Classifier

    Programming Language: Python

    Framework: Streamlit

    Dataset: 5G Network Traffic Dataset
    """)

# =====================================
# NETWORK INPUTS
# =====================================

st.header("⚙️ NETWORK CONTROL CENTER")

st.write(
    "Enter network parameters to generate "
    "an AI-based traffic prediction."
)

c1, c2 = st.columns(2)

with c1:

    users = st.number_input(
        "👥 Connected Users",
        min_value=10,
        max_value=1999,
        value=1500,
        step=10
    )

    bandwidth = st.number_input(
        "📶 Bandwidth (Mbps)",
        min_value=50,
        max_value=999,
        value=200,
        step=10
    )

    signal = st.number_input(
        "📡 Signal Strength",
        min_value=1,
        max_value=100,
        value=80
    )

with c2:

    packets = st.number_input(
        "📊 Packet Rate",
        min_value=100,
        max_value=9999,
        value=8500,
        step=100
    )

    hour = st.slider(
        "🕒 Network Hour",
        0,
        23,
        20
    )

# =====================================
# STATISTICS CARDS
# =====================================

st.divider()

st.header("📊 NETWORK STATISTICS")

a, b, c, d, e, f = st.columns(6)

cards = [
    (a, "👥 USERS", users),
    (b, "📶 BANDWIDTH", f"{bandwidth} Mbps"),
    (c, "📡 SIGNAL", f"{signal}%"),
    (d, "📦 PACKETS", packets),
    (e, "🕒 HOUR", f"{hour}:00"),
    (f, "🤖 MODEL", "ACTIVE")
]

for column, title, value in cards:

    with column:

        st.markdown(
            f"""
            <div class="metric">
                <p>{title}</p>
                <h2>{value}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

# =====================================
# AI PREDICTION
# =====================================

st.divider()

st.header("🧠 AI PREDICTION ENGINE")

if st.button(
    "🚀 GENERATE AI TRAFFIC PREDICTION",
    use_container_width=True
):

    input_data = pd.DataFrame([{
        "connected_users": users,
        "bandwidth_mbps": bandwidth,
        "signal_strength": signal,
        "packet_rate": packets,
        "hour": hour
    }])

    try:

        prediction = str(model.predict(input_data)[0])

        probabilities = None

        if hasattr(model, "predict_proba"):

            probabilities = model.predict_proba(
                input_data
            )[0]

        st.session_state.result = {
            "prediction": prediction,
            "probabilities": probabilities,
            "input": input_data.copy(),
            "time": datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )
        }

        st.session_state.history.append({
            "Time": datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            ),
            "Users": users,
            "Bandwidth": bandwidth,
            "Signal": signal,
            "Packets": packets,
            "Prediction": prediction
        })

    except Exception as error:

        st.error(f"Prediction Error: {error}")

# =====================================
# DISPLAY RESULT
# =====================================

result = st.session_state.result

if result:

    prediction = result["prediction"]

    st.divider()

    st.header("🎯 AI PREDICTION RESULT")

    if prediction.lower() == "low":

        icon = "🟢"
        recommendation = (
            "Low network traffic predicted. "
            "Normal network operation can continue."
        )

    elif prediction.lower() == "medium":

        icon = "🟡"
        recommendation = (
            "Moderate traffic predicted. "
            "Monitor bandwidth and network performance."
        )

    else:

        icon = "🔴"
        recommendation = (
            "High network traffic predicted. "
            "Consider load balancing and resource allocation."
        )

    st.markdown(
        f"""
        <div class="result">
            <h1>{icon} {prediction.upper()} TRAFFIC</h1>
            <p>AI Random Forest Classification Result</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =================================
    # PROBABILITY
    # =================================

    if result["probabilities"] is not None:

        st.subheader("📈 Prediction Confidence")

        probability_df = pd.DataFrame({
            "Traffic Category": model.classes_,
            "Probability (%)": np.round(
                result["probabilities"] * 100,
                2
            )
        })

        st.bar_chart(
            probability_df.set_index("Traffic Category")
        )

        st.dataframe(
            probability_df,
            use_container_width=True,
            hide_index=True
        )

    # =================================
    # WHAT IF ANALYSIS
    # =================================

    st.divider()

    st.header("🔍 WHAT-IF ANALYSIS")

    st.write(
        "Observe how prediction probabilities change "
        "when connected users increase."
    )

    if hasattr(model, "predict_proba"):

        scenario_users = sorted(set([
            max(10, users - 400),
            max(10, users - 200),
            users,
            min(1999, users + 200),
            min(1999, users + 400)
        ]))

        scenario_data = []

        for count in scenario_users:

            scenario = result["input"].copy()

            scenario["connected_users"] = count

            probs = model.predict_proba(scenario)[0]

            for category, probability in zip(
                model.classes_,
                probs
            ):

                scenario_data.append({
                    "Connected Users": count,
                    "Category": str(category),
                    "Probability (%)": probability * 100
                })

        scenario_df = pd.DataFrame(scenario_data)

        chart = scenario_df.pivot(
            index="Connected Users",
            columns="Category",
            values="Probability (%)"
        )

        st.line_chart(chart)

        st.caption(
            "Illustrative what-if scenarios generated "
            "using the trained model."
        )

    # =================================
    # TRAFFIC ANALYSIS
    # =================================

    st.divider()

    st.header("📊 TRAFFIC ANALYSIS")

    x, y = st.columns(2)

    with x:

        st.metric(
            "Predicted Traffic",
            prediction.upper()
        )

    with y:

        if result["probabilities"] is not None:

            confidence = max(
                result["probabilities"]
            ) * 100

            st.metric(
                "Top Class Probability",
                f"{confidence:.2f}%"
            )

        else:

            st.metric(
                "Top Class Probability",
                "Not available"
            )

    # =================================
    # RECOMMENDATIONS
    # =================================

    st.divider()

    st.header("💡 AI NETWORK RECOMMENDATIONS")

    st.info(recommendation)

    if signal < 40:

        st.warning(
            "Weak signal input: Review signal coverage "
            "and possible interference."
        )

    if bandwidth < 150:

        st.warning(
            "Bandwidth input is relatively low. "
            "Review available network capacity."
        )

    if packets > 8000:

        st.warning(
            "High packet rate input. "
            "Monitor packet processing performance."
        )

    st.success("AI ANALYSIS COMPLETED")

# =====================================
# PREDICTION HISTORY
# =====================================

st.divider()

st.header("📜 PREDICTION HISTORY")

if st.session_state.history:

    history_df = pd.DataFrame(
        st.session_state.history
    )

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

    csv = history_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇️ DOWNLOAD PREDICTION REPORT",
        data=csv,
        file_name="NEXUS_5G_Prediction_Report.csv",
        mime="text/csv"
    )

    if st.button("🗑️ CLEAR HISTORY"):

        st.session_state.history = []

        st.rerun()

else:

    st.info(
        "No predictions yet. Generate your first prediction."
    )

# =====================================
# DATASET EXPLORER
# =====================================

st.divider()

st.header("🗂️ DATASET EXPLORER")

try:

    dataset = pd.read_csv(
        "5G_Network_Traffic_Dataset.csv"
    )

    st.write("Dataset Preview")

    st.dataframe(
        dataset.head(20),
        use_container_width=True
    )

    st.metric(
        "Total Dataset Records",
        len(dataset)
    )

    st.metric(
        "Total Dataset Columns",
        len(dataset.columns)
    )

    st.download_button(
        "⬇️ DOWNLOAD DATASET",
        dataset.to_csv(index=False).encode("utf-8"),
        file_name="5G_Network_Dataset.csv",
        mime="text/csv"
    )

except Exception:

    st.warning(
        "Dataset file is not available."
    )

# =====================================
# TEAM SECTION
# =====================================

st.divider()

st.header("👨‍💻 MEET OUR DEVELOPMENT TEAM")

st.markdown("""
<p style="color:#bae6fd;font-size:17px;">
Designed and developed as a Computer Networks Mini Project.
</p>
""", unsafe_allow_html=True)

t1, t2, t3 = st.columns(3)

team = [
    (t1, "01", "MIT PRAJAPATI"),
    (t2, "02", "RENCE VITHLANI"),
    (t3, "03", "ZEEL DUDHAT")
]

for col, number, name in team:

    with col:

        st.markdown(
            f"""
            <div class="team">
                <h2>👨‍💻</h2>
                <h3>{name}</h3>
                <p>TEAM MEMBER {number}</p>
                <p>NEXUS 5G PROJECT</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# =====================================
# PROJECT DETAILS
# =====================================

st.divider()

with st.expander("🎓 PROJECT TECHNOLOGY"):

    st.write("""
    Project: AI-Based 5G Network Traffic Prediction

    Algorithm: Random Forest Classifier

    Programming Language: Python

    Libraries: Pandas, NumPy, Scikit-learn

    Web Framework: Streamlit

    Model Type: Machine Learning Classification

    Prediction Classes: Low, Medium, High
    """)

# =====================================
# FOOTER
# =====================================

st.markdown("""
<div class="hero">

<h2>🚀 NEXUS 5G INTELLIGENCE</h2>

<p>
AI-POWERED NETWORK TRAFFIC PREDICTION
</p>

<p>
Developed by Mit Prajapati | Rence Vithlani |
Zeel Dudhat
</p>

<p>
Computer Networks Mini Project
</p>

</div>
""", unsafe_allow_html=True)

st.caption(
    "Academic demonstration using a synthetic-data-trained model. "
    "This dashboard does not connect to a live 5G telecom network."
)
