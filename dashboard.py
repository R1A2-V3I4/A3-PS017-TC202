import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# ------------------------------------------
# PROJECT CONFIGURATION
# ------------------------------------------

DATASET_PATH = "network_traffic.csv"
MODEL_PATH = os.path.join("models", "latency_model.pkl")

FEATURES = [
    "traffic_load",
    "packet_size",
    "congestion",
    "jitter_ms"
]

st.set_page_config(
    page_title="AIORI Tail-Latency Dashboard",
    page_icon="📡",
    layout="wide"
)

# ------------------------------------------
# DASHBOARD HEADER
# ------------------------------------------

st.title("📡 AIORI Network Tail-Latency Dashboard")

st.subheader(
    "Tail-Latency Prediction for URLLC-Like Traffic in Simulation"
)

st.caption("AIORI Hackathon | Problem Statement PS-017")

st.divider()

# ------------------------------------------
# LOAD DATASET
# ------------------------------------------

if not os.path.exists(DATASET_PATH):
    st.error("Dataset not found. Run dataset_generator.py first.")
    st.stop()

data = pd.read_csv(DATASET_PATH)

required_columns = FEATURES + ["latency_ms"]

missing_columns = [
    column for column in required_columns
    if column not in data.columns
]

if missing_columns:
    st.error(f"Missing dataset columns: {missing_columns}")
    st.info(
        "Run dataset_generator.py to generate the correct dataset."
    )
    st.stop()

# ------------------------------------------
# NETWORK STATISTICS
# ------------------------------------------

st.header("📊 Network Traffic Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Packets", f"{len(data):,}")

col2.metric(
    "Average Latency",
    f"{data['latency_ms'].mean():.2f} ms"
)

col3.metric(
    "P95 Latency",
    f"{data['latency_ms'].quantile(0.95):.2f} ms"
)

col4.metric(
    "P99 Latency",
    f"{data['latency_ms'].quantile(0.99):.2f} ms"
)

st.divider()

# ------------------------------------------
# LATENCY ANALYSIS
# ------------------------------------------

st.header("📈 Latency Analysis")

left, right = st.columns(2)

with left:
    st.subheader("Latency Distribution")

    fig1, ax1 = plt.subplots(figsize=(8, 4))

    ax1.hist(data["latency_ms"], bins=40)

    ax1.set_xlabel("Latency (ms)")
    ax1.set_ylabel("Number of Packets")
    ax1.set_title("Distribution of Packet Latency")

    st.pyplot(fig1)
    plt.close(fig1)

with right:
    st.subheader("Traffic Load vs Latency")

    fig2, ax2 = plt.subplots(figsize=(8, 4))

    ax2.scatter(
        data["traffic_load"],
        data["latency_ms"],
        alpha=0.4,
        s=10
    )

    ax2.set_xlabel("Traffic Load")
    ax2.set_ylabel("Latency (ms)")
    ax2.set_title("Traffic Load vs Packet Latency")

    st.pyplot(fig2)
    plt.close(fig2)

# ------------------------------------------
# CONGESTION ANALYSIS
# ------------------------------------------

st.subheader("Congestion vs Latency")

fig3, ax3 = plt.subplots(figsize=(10, 4))

ax3.scatter(
    data["congestion"],
    data["latency_ms"],
    alpha=0.4,
    s=10
)

ax3.set_xlabel("Congestion Level")
ax3.set_ylabel("Latency (ms)")
ax3.set_title("Impact of Congestion on Latency")

st.pyplot(fig3)
plt.close(fig3)

st.divider()

# ------------------------------------------
# FUTURE P99 PREDICTION
# ------------------------------------------

st.header("🤖 Predict Network Latency")

st.write(
    "Enter expected network conditions to estimate packet latency "
    "and the corresponding P95/P99 for the prediction batch."
)

if not os.path.exists(MODEL_PATH):
    st.warning(
        "Trained model not found. Run model_training.py before "
        "using the prediction feature."
    )
else:
    traffic_load = st.slider(
        "Traffic Load",
        min_value=0.0,
        max_value=100.0,
        value=80.0
    )

    packet_size = st.number_input(
        "Packet Size (bytes)",
        min_value=1,
        max_value=65535,
        value=1000
    )

    congestion = st.slider(
        "Congestion Level",
        min_value=0.0,
        max_value=1.0,
        value=0.7
    )

    jitter_ms = st.number_input(
        "Expected Jitter (ms)",
        min_value=0.0,
        value=3.0,
        step=0.5
    )

    if st.button("Predict Latency", type="primary"):

        model = joblib.load(MODEL_PATH)

        future_conditions = pd.DataFrame(
            [[traffic_load, packet_size, congestion, jitter_ms]],
            columns=FEATURES
        )

        # Predict latency for the entered conditions
        predicted_latency = float(
            model.predict(future_conditions)[0]
        )

        # A standard RandomForestRegressor produces one point
        # prediction for identical inputs. Repeating it does not
        # create a valid future latency distribution.
        st.metric(
            "Predicted Packet Latency",
            f"{predicted_latency:.2f} ms"
        )

        st.info(
            "This is a point prediction for packet latency, not a "
            "reliable prediction of future P99. To predict future "
            "P99 accurately, train a model on P99 values calculated "
            "from multiple simulated time windows."
        )

        prediction_result = pd.DataFrame({
            "traffic_load": [traffic_load],
            "packet_size": [packet_size],
            "congestion": [congestion],
            "jitter_ms": [jitter_ms],
            "predicted_latency_ms": [predicted_latency]
        })

        st.download_button(
            "Download Prediction CSV",
            data=prediction_result.to_csv(index=False),
            file_name="latency_prediction.csv",
            mime="text/csv"
        )

st.divider()

# ------------------------------------------
# DATASET PREVIEW AND DOWNLOAD
# ------------------------------------------

st.header("📁 Network Dataset")

with st.expander("View Sample Dataset"):
    st.dataframe(data.head(100), use_container_width=True)

st.download_button(
    "Download Network Dataset",
    data=data.to_csv(index=False),
    file_name="network_traffic.csv",
    mime="text/csv"
)

st.success("Dashboard loaded successfully!")