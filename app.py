import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="AI-Based 5G Network Traffic Prediction",
    page_icon="📡",
    layout="wide"
)

@st.cache_resource
def load_model():
    return joblib.load("5G_Traffic_Model.pkl")

try:
    model = load_model()
except Exception as e:
    st.error("Could not load 5G_Traffic_Model.pkl. Make sure the model file is in the same folder as app.py.")
    st.stop()

st.title("📡 AI-Based 5G Network Traffic Prediction")
st.write(
    "Enter the network details below. The trained Random Forest model "
    "will predict the traffic category."
)

st.sidebar.header("About the project")
st.sidebar.write("Algorithm: Random Forest Classifier")
st.sidebar.write("Prediction classes: Low, Medium, High")
st.sidebar.caption(
    "Note: The current notebook trains on a synthetically generated dataset. "
    "Predictions reflect patterns in that generated data, not validated live 5G measurements."
)

left, right = st.columns(2)

with left:
    connected_users = st.number_input(
        "Connected users",
        min_value=10,
        max_value=1999,
        value=1500,
        step=10
    )
    bandwidth_mbps = st.number_input(
        "Bandwidth (Mbps)",
        min_value=50,
        max_value=999,
        value=200,
        step=10
    )
    signal_strength = st.number_input(
        "Signal strength",
        min_value=1,
        max_value=100,
        value=80,
        step=1
    )

with right:
    packet_rate = st.number_input(
        "Packet rate",
        min_value=100,
        max_value=9999,
        value=8500,
        step=100
    )
    hour = st.number_input(
        "Hour (0–23)",
        min_value=0,
        max_value=23,
        value=20,
        step=1
    )

if st.button("Predict Traffic", type="primary", use_container_width=True):
    input_data = pd.DataFrame([{
        "connected_users": connected_users,
        "bandwidth_mbps": bandwidth_mbps,
        "signal_strength": signal_strength,
        "packet_rate": packet_rate,
        "hour": hour
    }])

    prediction = model.predict(input_data)[0]

    st.subheader("Prediction result")
    if str(prediction) == "Low":
        st.success("Predicted traffic: LOW")
    elif str(prediction) == "Medium":
        st.warning("Predicted traffic: MEDIUM")
    else:
        st.error("Predicted traffic: HIGH")

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(input_data)[0]
        probability_df = pd.DataFrame({
            "Traffic category": model.classes_,
            "Model probability (%)": (probabilities * 100).round(2)
        }).set_index("Traffic category")

        st.write("Model class probabilities")
        st.bar_chart(probability_df)

    st.caption("This is a model prediction, not a live measurement of a telecom network.")
