import pandas as pd
import numpy as np


def calculate_latency_statistics(
    dataset_path="network_traffic.csv"
):
    """
    Calculate latency statistics, including P95 and P99.
    """

    print("\n" + "=" * 50)
    print("       LATENCY ANALYSIS SYSTEM")
    print("=" * 50)

    # Load the generated dataset
    try:
        dataset = pd.read_csv(dataset_path)
    except FileNotFoundError:
        print(f"Error: {dataset_path} was not found.")
        print("Run dataset_generator.py first.")
        return None

    # Check whether the required column exists
    if "latency_ms" not in dataset.columns:
        print("Error: The dataset has no latency_ms column.")
        return None

    # Convert latency values to numeric
    dataset["latency_ms"] = pd.to_numeric(
        dataset["latency_ms"],
        errors="coerce"
    )

    # Remove missing and invalid latency values
    latency = dataset["latency_ms"].dropna()

    # Latency cannot be negative
    latency = latency[latency >= 0]

    if latency.empty:
        print("Error: No valid latency values found.")
        return None

    # Calculate latency statistics
    average_latency = latency.mean()
    median_latency = latency.median()
    minimum_latency = latency.min()
    maximum_latency = latency.max()

    p95_latency = np.percentile(latency, 95)
    p99_latency = np.percentile(latency, 99)

    # Display the results
    print(f"\nTotal valid packets: {len(latency)}")

    print("\n--- Latency Statistics ---")
    print(f"Average latency : {average_latency:.3f} ms")
    print(f"Median latency  : {median_latency:.3f} ms")
    print(f"Minimum latency : {minimum_latency:.3f} ms")
    print(f"Maximum latency : {maximum_latency:.3f} ms")

    print("\n--- Tail Latency ---")
    print(f"P95 latency     : {p95_latency:.3f} ms")
    print(f"P99 latency     : {p99_latency:.3f} ms")

    # Save the statistics
    statistics = pd.DataFrame({
        "metric": [
            "Average latency",
            "Median latency",
            "Minimum latency",
            "Maximum latency",
            "P95 latency",
            "P99 latency"
        ],
        "latency_ms": [
            average_latency,
            median_latency,
            minimum_latency,
            maximum_latency,
            p95_latency,
            p99_latency
        ]
    })

    statistics.to_csv(
        "latency_statistics.csv",
        index=False
    )

    print("\nStatistics saved to latency_statistics.csv")
    print("=" * 50)

    return statistics


if __name__ == "__main__":
    calculate_latency_statistics()