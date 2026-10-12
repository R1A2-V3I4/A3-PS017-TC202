import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# Project file paths
DATASET_PATH = "network_traffic.csv"
MODEL_PATH = os.path.join("models", "latency_model.pkl")

RESULTS_PATH = "model_evaluation_results.csv"
PLOT_PATH = "actual_vs_predicted_latency.png"


def evaluate_model():
    print("\n" + "=" * 60)
    print("       AIORI HACKATHON - MODEL EVALUATION")
    print("       Tail-Latency Prediction (PS-017)")
    print("=" * 60)

    # 1. Check whether the dataset exists
    if not os.path.exists(DATASET_PATH):
        print("Error: network_traffic.csv not found.")
        print("Run dataset_generator.py first.")
        return

    # 2. Check whether the trained model exists
    if not os.path.exists(MODEL_PATH):
        print("Error: Trained model not found.")
        print("Run model_training.py first.")
        return

    # 3. Load the dataset and trained model
    data = pd.read_csv(DATASET_PATH)
    model = joblib.load(MODEL_PATH)

    # 4. Select the input features and actual target
    features = [
        "traffic_load",
        "packet_size",
        "congestion",
        "jitter_ms"
    ]

    target = "latency_ms"

    # 5. Check required columns
    required_columns = features + [target]
    missing_columns = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        print("Error: Missing dataset columns:", missing_columns)
        print("Run dataset_generator.py to generate the correct dataset.")
        return

    # 6. Prepare the input and actual values
    X = data[features]
    y_actual = data[target]

    # 7. Generate predictions
    y_predicted = model.predict(X)

    # 8. Calculate evaluation metrics
    mae = mean_absolute_error(y_actual, y_predicted)
    mse = mean_squared_error(y_actual, y_predicted)
    rmse = mse ** 0.5
    r2 = r2_score(y_actual, y_predicted)

    # 9. Display evaluation results
    print("\nMODEL PERFORMANCE")
    print("-" * 40)
    print(f"Total packets evaluated : {len(data)}")
    print(f"Mean Absolute Error     : {mae:.4f} ms")
    print(f"Mean Squared Error      : {mse:.4f}")
    print(f"Root Mean Squared Error : {rmse:.4f} ms")
    print(f"R2 Score                : {r2:.4f}")

    # 10. Save actual and predicted values
    results = pd.DataFrame({
        "actual_latency_ms": y_actual,
        "predicted_latency_ms": y_predicted,
        "prediction_error_ms": y_actual - y_predicted
    })

    results.to_csv(RESULTS_PATH, index=False)

    print(f"\nEvaluation results saved to: {RESULTS_PATH}")

    # 11. Plot actual versus predicted latency
    sample_size = min(200, len(data))

    plt.figure(figsize=(10, 6))

    plt.plot(
        range(sample_size),
        y_actual.iloc[:sample_size],
        label="Actual Latency"
    )

    plt.plot(
        range(sample_size),
        y_predicted[:sample_size],
        label="Predicted Latency",
        linestyle="--"
    )

    plt.xlabel("Packet Number")
    plt.ylabel("Latency (ms)")
    plt.title("Actual vs Predicted Packet Latency")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(PLOT_PATH, dpi=300)

    print(f"Comparison graph saved to: {PLOT_PATH}")

    plt.show()

    print("\nModel evaluation completed successfully!")


if __name__ == "__main__":
    evaluate_model()