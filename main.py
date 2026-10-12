from database import get_connection


def check_database_connection():
    """Check whether the MySQL database is accessible."""
    try:
        connection = get_connection()

        if connection and connection.is_connected():
            print("MySQL database connected successfully!")
            connection.close()
            return True

    except Exception as error:
        print("Database connection failed:", error)

    return False


def display_menu():
    """Display the project menu."""
    print("\n" + "=" * 55)
    print("  TAIL-LATENCY PREDICTION SYSTEM")
    print("  AIORI Hackathon - PS-017")
    print("=" * 55)

    print("1. Check MySQL Database Connection")
    print("2. Run Network Traffic Simulation")
    print("3. Generate Network Dataset")
    print("4. Calculate Packet Latency")
    print("5. Calculate P95 and P99 Tail Latency")
    print("6. Perform Data Analysis")
    print("7. Train Machine Learning Model")
    print("8. Evaluate Model")
    print("9. Predict Future P99 Latency")
    print("10. Exit")

    print("=" * 55)


def main():
    """Main function of the application."""

    while True:
        display_menu()

        choice = input("Enter your choice (1-10): ").strip()

        if choice == "1":
            check_database_connection()

        elif choice == "2":
            print("\nNetwork simulation will be implemented in simulation.py.")

        elif choice == "3":
            print("\nDataset generation will be implemented in dataset_generator.py.")

        elif choice == "4":
            print("\nLatency calculation will be implemented in latency_calculator.py.")

        elif choice == "5":
            print("\nTail-latency calculation will be implemented in tail_latency.py.")

        elif choice == "6":
            print("\nData analysis will be implemented in data_analysis.py.")

        elif choice == "7":
            print("\nModel training will be implemented in model_training.py.")

        elif choice == "8":
            print("\nModel evaluation will be implemented in model_evaluation.py.")

        elif choice == "9":
            print("\nP99 prediction will be implemented in prediction.py.")

        elif choice == "10":
            print("\nThank you for using the Tail-Latency Prediction System!")
            break

        else:
            print("\nInvalid choice. Please enter a number between 1 and 10.")


if __name__ == "__main__":
    main()