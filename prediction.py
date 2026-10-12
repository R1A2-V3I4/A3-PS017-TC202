import os
import joblib
import numpy as np
import pandas as pd

# --------------------------------------------------
# PROJECT CONFIGURATION
# --------------------------------------------------

DATASET_PATH = "network_traffic.csv"
MODEL_PATH = os.path.join("models", "latency_model.pkl")

OUTPUT_PATH = "future_p99_prediction.csv"

FEATURES = [
    "traffic_load",
    "packet_size",
    "congestion",
    "jitter_ms"
]


# --------------------------------------------------
# PREDICT FUTURE P99 LATENCY
# --------------------------------------------------

def predict_future_p99():

    print("\n" + "=" * 60)
    print("       AIORI HACKATHON - FUTURE P99 PREDICTION")
    print("       Tail-Latency Prediction (PS-017)")
    print("=" * 60)

    # 1. Check whether the trained model exists
    if not os.path.exists(MODEL_PATH):
        print("\nError: Trained model not found.")
        print("Run model_training.py first.")
        return

    # 2. Load the trained model
    model = joblib.load(MODEL_PATH)

    # 3. Ask the user for future network conditions
    try:
        print("\nEnter the expected future network conditions:")

        traffic_load = float(
            input("Traffic load (0-100): ")
        )

        packet_size = float(
            input("Average packet size in bytes (e.g. 1000): ")
        )

        congestion = float(
            input("Congestion level (0-1): ")
        )

        jitter_ms = float(
            input("Expected jitter in milliseconds (e.g. 2): ")
        )

    except ValueError:
        print("\nError: Please enter valid numeric values.")
        return

    # 4. Validate the input
    if not 0 <= traffic_load <= 100:
        print("Traffic load must be between 0 and 100.")
        return

    if not 1 <= packet_size <= 65535:
        print("Packet size must be between 1 and 65535 bytes.")
        return

    if not 0 <= congestion <= 1:
        print("Congestion must be between 0 and 1.")
        return

    if jitter_ms < 0:
        print("Jitter cannot be negative.")
        return

    # 5. Prepare future network conditions
    future_conditions = pd.DataFrame(
        [[traffic_load, packet_size, congestion, jitter_ms]],
        columns=FEATURES
    )

    # 6. Generate predictions for a future batch
    # Each row represents the same expected conditions.
    predicted_latencies = []

    for _ in range(1000):
        predicted_latency = model.predict(future_conditions)[0]
        predicted_latencies.append(predicted_latency)

    predicted_latencies = np.array(predicted_latencies)

    # 7. Calculate the predicted tail latency
    predicted_p95 = np.percentile(predicted_latencies, 95)
    predicted_p99 = np.percentile(predicted_latencies, 99)

    # 8. Display results
    print("\n" + "-" * 60)
    print("FUTURE NETWORK LATENCY PREDICTION")
    print("-" * 60)

    print(f"Traffic load       : {traffic_load:.2f}")
    print(f"Packet size        : {packet_size:.2f} bytes")
    print(f"Congestion         : {congestion:.2f}")
    print(f"Jitter             : {jitter_ms:.2f} ms")

    print("\nPREDICTION RESULTS")
    print(f"Predicted P95      : {predicted_p95:.4f} ms")
    print(f"Predicted P99      : {predicted_p99:.4f} ms")

    # 9. Save the prediction
    results = pd.DataFrame({
        "traffic_load": [traffic_load],
        "packet_size": [packet_size],
        "congestion": [congestion],
        "jitter_ms": [jitter_ms],
        "predicted_p95_ms": [predicted_p95],
        "predicted_p99_ms": [predicted_p99]
    })

    results.to_csv(OUTPUT_PATH, index=False)

    print(f"\nPrediction saved to: {OUTPUT_PATH}")
    print("\nPrediction completed!")


# --------------------------------------------------
# PROGRAM ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    predict_future_p99()