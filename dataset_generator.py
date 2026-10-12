import numpy as np
import pandas as pd


def generate_dataset(number_of_packets=10000):

    print("\nGenerating network traffic dataset...")

    # Make the results reproducible
    np.random.seed(42)

    # Generate packet IDs
    packet_id = np.arange(1, number_of_packets + 1)

    # Generate traffic load (percentage)
    traffic_load = np.random.uniform(10, 100, number_of_packets)

    # Generate packet sizes (bytes)
    packet_size = np.random.randint(64, 1501, number_of_packets)

    # Generate network congestion (0 to 1)
    congestion = np.random.uniform(0, 1, number_of_packets)

    # Generate network jitter (milliseconds)
    jitter_ms = np.random.exponential(1.5, number_of_packets)

    # Generate packet latency (milliseconds)
    latency_ms = (
        2
        + (traffic_load * 0.08)
        + (packet_size / 1500 * 3)
        + (congestion * 15)
        + jitter_ms
        + np.random.exponential(2, number_of_packets)
    )

    # Create the dataset
    dataset = pd.DataFrame({
        "packet_id": packet_id,
        "traffic_load": traffic_load.round(2),
        "packet_size": packet_size,
        "congestion": congestion.round(3),
        "jitter_ms": jitter_ms.round(3),
        "latency_ms": latency_ms.round(3)
    })

    # Save the dataset as a CSV file
    dataset.to_csv("network_traffic.csv", index=False)

    # Display dataset information
    print("\nDataset generated successfully!")
    print("Total packets:", len(dataset))
    print("Saved file: network_traffic.csv")

    print("\nFirst 5 records:")
    print(dataset.head())

    print("\nLatency Statistics:")
    print("Average latency:", round(dataset["latency_ms"].mean(), 3), "ms")
    print("Maximum latency:", round(dataset["latency_ms"].max(), 3), "ms")
    print("P95 latency:", round(dataset["latency_ms"].quantile(0.95), 3), "ms")
    print("P99 latency:", round(dataset["latency_ms"].quantile(0.99), 3), "ms")

    return dataset


if __name__ == "__main__":
    generate_dataset()