import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def analyze_network_data(dataset_path="network_traffic.csv"):

    print("\n" + "=" * 55)
    print("       NETWORK TRAFFIC DATA ANALYSIS")
    print("       AIORI Hackathon - PS-017")
    print("=" * 55)

    # Load the dataset
    try:
        dataset = pd.read_csv(dataset_path)

    except FileNotFoundError:
        print(f"Error: {dataset_path} not found.")
        print("Please run dataset_generator.py first.")
        return

    # Check required columns
    required_columns = [
        "traffic_load",
        "packet_size",
        "congestion",
        "latency_ms"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in dataset.columns
    ]

    if missing_columns:
        print("Missing columns:", missing_columns)
        return

    # Convert required columns to numeric
    for column in required_columns:
        dataset[column] = pd.to_numeric(
            dataset[column],
            errors="coerce"
        )

    # Remove rows with invalid values
    dataset = dataset.dropna(subset=required_columns)

    # Remove negative latency values
    dataset = dataset[dataset["latency_ms"] >= 0]

    if dataset.empty:
        print("No valid network traffic records found.")
        return

    # Calculate statistics
    latency = dataset["latency_ms"]

    average_latency = latency.mean()
    median_latency = latency.median()
    p95_latency = latency.quantile(0.95)
    p99_latency = latency.quantile(0.99)
    maximum_latency = latency.max()

    print("\n--- Dataset Summary ---")
    print("Total packets:", len(dataset))
    print(f"Average latency: {average_latency:.3f} ms")
    print(f"Median latency: {median_latency:.3f} ms")
    print(f"P95 latency: {p95_latency:.3f} ms")
    print(f"P99 latency: {p99_latency:.3f} ms")
    print(f"Maximum latency: {maximum_latency:.3f} ms")

    # Save descriptive statistics
    dataset[required_columns].describe().to_csv(
        "network_analysis_summary.csv"
    )

    print("\nSummary saved to network_analysis_summary.csv")

    # Graph 1: Packet latency distribution
    plt.figure(figsize=(9, 5))
    plt.hist(latency, bins=50)
    plt.axvline(
        p95_latency,
        linestyle="--",
        label=f"P95 = {p95_latency:.2f} ms"
    )
    plt.axvline(
        p99_latency,
        linestyle="--",
        label=f"P99 = {p99_latency:.2f} ms"
    )
    plt.xlabel("Packet Latency (ms)")
    plt.ylabel("Number of Packets")
    plt.title("Network Packet Latency Distribution")
    plt.legend()
    plt.tight_layout()
    plt.savefig("latency_distribution.png")
    plt.show()

    # Graph 2: Traffic load vs latency
    plt.figure(figsize=(9, 5))
    plt.scatter(
        dataset["traffic_load"],
        dataset["latency_ms"],
        alpha=0.5
    )
    plt.xlabel("Traffic Load (%)")
    plt.ylabel("Latency (ms)")
    plt.title("Traffic Load vs Packet Latency")
    plt.tight_layout()
    plt.savefig("traffic_vs_latency.png")
    plt.show()

    # Graph 3: Network congestion vs latency
    plt.figure(figsize=(9, 5))
    plt.scatter(
        dataset["congestion"],
        dataset["latency_ms"],
        alpha=0.5
    )
    plt.xlabel("Network Congestion (0 to 1)")
    plt.ylabel("Latency (ms)")
    plt.title("Network Congestion vs Packet Latency")
    plt.tight_layout()
    plt.savefig("congestion_vs_latency.png")
    plt.show()

    # Graph 4: Latency percentiles
    percentile_names = ["P95", "P99", "Maximum"]
    percentile_values = [
        p95_latency,
        p99_latency,
        maximum_latency
    ]

    plt.figure(figsize=(8, 5))
    plt.bar(percentile_names, percentile_values)
    plt.ylabel("Latency (ms)")
    plt.title("Tail Latency Comparison")
    plt.tight_layout()
    plt.savefig("tail_latency_comparison.png")
    plt.show()

    print("\nGraphs saved successfully:")
    print("1. latency_distribution.png")
    print("2. traffic_vs_latency.png")
    print("3. congestion_vs_latency.png")
    print("4. tail_latency_comparison.png")

    print("\nData analysis completed successfully!")


if __name__ == "__main__":
    analyze_network_data()