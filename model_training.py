import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# Project paths
DATASET_PATH = "network_traffic.csv"
MODEL_DIRECTORY = "models"
MODEL_PATH = os.path.join(MODEL_DIRECTORY, "latency_model.pkl")


def train_model():

    print("\n" + "=" * 60)
    print("       TAIL-LATENCY PREDICTION - MODEL TRAINING")
    print("       AIORI Hackathon - PS-017")
    print("=" * 60)

    # 1. Load the dataset
    try:
        dataset = pd.read_csv(DATASET_PATH)

    except FileNotFoundError:
        print(f"Error: {DATASET_PATH} not found.")
        print("Run dataset_generator.py first.")
        return None

    # 2. Check required columns
    features = [
        "traffic_load",
        "packet_size",
        "congestion",
        "jitter_ms"
    ]

    target = "latency_ms"

    required_columns = features + [target]

    missing_columns = [
        column for column in required_columns
        if column not in dataset.columns
    ]

    if missing_columns:
        print("Missing required columns:", missing_columns)
        print("Please check network_traffic.csv.")
        return None

    # 3. Prepare the data
    for column in required_columns:
        dataset[column] = pd.to_numeric(
            dataset[column],
            errors="coerce"
        )

    dataset = dataset.dropna(subset=required_columns)

    if len(dataset) < 10:
        print("Error: Not enough valid records to train the model.")
        return None

    X = dataset[features]
    y = dataset[target]

    # 4. Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )

    print(f"\nTotal records: {len(dataset)}")
    print(f"Training records: {len(X_train)}")
    print(f"Testing records: {len(X_test)}")

    # 5. Create the machine learning model
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        random_state=42,
        n_jobs=-1
    )

    # 6. Train the model
    print("\nTraining Random Forest model...")
    model.fit(X_train, y_train)

    print("Model training completed!")

    # 7. Make predictions on the test dataset
    predictions = model.predict(X_test)

    # 8. Evaluate the model
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = mse ** 0.5
    r2 = r2_score(y_test, predictions)

    print("\n--- Model Evaluation ---")
    print(f"MAE  : {mae:.4f} ms")
    print(f"RMSE : {rmse:.4f} ms")
    print(f"R²   : {r2:.4f}")

    # 9. Save the trained model
    os.makedirs(MODEL_DIRECTORY, exist_ok=True)

    joblib.dump(model, MODEL_PATH)

    print(f"\nModel saved to: {MODEL_PATH}")

    # 10. Save actual and predicted results
    results = pd.DataFrame({
        "actual_latency_ms": y_test.to_numpy(),
        "predicted_latency_ms": predictions
    })

    results.to_csv(
        "model_predictions.csv",
        index=False
    )

    print("Test predictions saved to model_predictions.csv")

    # 11. Show feature importance
    importance = pd.DataFrame({
        "feature": features,
        "importance": model.feature_importances_
    }).sort_values(
        by="importance",
        ascending=False
    )

    print("\n--- Feature Importance ---")
    print(importance.to_string(index=False))

    importance.to_csv(
        "feature_importance.csv",
        index=False
    )

    print("\nFeature importance saved to feature_importance.csv")
    print("=" * 60)

    return model


if __name__ == "__main__":
    train_model()