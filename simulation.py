import numpy as np
import pandas as pd


def simulate_network_traffic(number_of_packets=10000):
    """
    Simulate network traffic and calculate packet latency.
    """

    print("\nStarting network traffic simulation...")

    # Generate packet IDs
    packet_ids = np.arange(1, number_of_packets + 1)

    # Simulate network traffic load (percentage)
    traffic_load = np.random.uniform(10, 100, number_of_packets)

    # Simulate packet sizes in bytes
    packet_size = np.random.randint(64, 1501, number_of_packets)

    # Simulate network congestion (0 = low, 1 = high)
    congestion = np.random.uniform(0, 1, number_of_packets)

    # Simulate network latency in milliseconds
    latency = (
        2
        + (traffic_load * 0.08)
        + (packet_size / 1500 * 3)
        + (congestion * 15)
        + np.random.exponential(scale=2, size=number_of_packets)
    )

    # Create a dataset
    dataset = pd.DataFrame({
        "packet_id": packet_ids,
        "traffic_load": traffic_load.round(2),
        "packet_size": packet_size,
        "congestion": congestion.round(3),
        "latency_ms": latency.round(3)
    })

    # Save the dataset
    dataset.to_csv("network_traffic.csv", index=False)

    print("Network traffic simulation completed!")
    print(f"Total packets generated: {number_of_packets}")
    print("Dataset saved as network_traffic.csv")

    print("\nFirst 5 packets:")
    print(dataset.head())

    return dataset


if __name__ == "__main__":
    simulate_network_traffic()