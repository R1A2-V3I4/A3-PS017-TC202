import pandas as pd
import numpy as np


def analyze_tail_latency(dataset_path="network_traffic.csv"):
    """
    Analyze tail latency using P90, P95, P99, and P99.9.
    """

    print("\n" + "=" * 55)
    print("           TAIL LATENCY ANALYSIS")
    print("           AIORI Hackathon - PS-017")
    print("=" * 55)

    # Load the network traffic dataset
    try:
        dataset = pd.read_csv(dataset_path)
    except FileNotFoundError:
        print(f"Error: {dataset_path} not found.")
        print("Run dataset_generator.py first.")
        return None

    # Check required column
    if "latency_ms" not in dataset.columns:
        print("Error: 'latency_ms' column is missing.")
        return None

    # Convert latency values to numeric
    latency = pd.to_numeric(
        dataset["latency_ms"],
        errors="coerce"
    ).dropna()

    # Remove invalid negative latency values
    latency = latency[latency >= 0]

    if latency.empty:
        print("Error: No valid latency measurements found.")
        return None

    # Calculate percentiles
    percentiles = {
        "P90": np.percentile(latency, 90),
        "P95": np.percentile(latency, 95),
        "P99": np.percentile(latency, 99),
        "P99.9": np.percentile(latency, 99.9)
    }

    # Calculate average and maximum latency
    average_latency = latency.mean()
    maximum_latency = latency.max()

    print(f"\nTotal valid packets: {len(latency)}")
    print(f"Average latency: {average_latency:.3f} ms")
    print(f"Maximum latency: {maximum_latency:.3f} ms")

    print("\n--- Tail Latency Percentiles ---")

    for name, value in percentiles.items():
        print(f"{name} latency: {value:.3f} ms")

    # Identify packets at or above the P99 threshold
    p99_latency = percentiles["P99"]
    high_latency_packets = dataset.loc[
        pd.to_numeric(
            dataset["latency_ms"],
            errors="coerce"
        ) >= p99_latency
    ].copy()

    print("\n--- High-Latency Packet Analysis ---")
    print(f"P99 threshold: {p99_latency:.3f} ms")
    print(f"Packets at or above P99: {len(high_latency_packets)}")

    # Save percentile results
    results = pd.DataFrame({
        "percentile": list(percentiles.keys()),
        "latency_ms": list(percentiles.values())
    })

    results.to_csv("tail_latency_results.csv", index=False)

    # Save high-latency packets
    high_latency_packets.to_csv(
        "high_latency_packets.csv",
        index=False
    )

    print("\nFiles generated successfully:")
    print("1. tail_latency_results.csv")
    print("2. high_latency_packets.csv")
    print("=" * 55)

    return results


if __name__ == "__main__":
    analyze_tail_latency()