import mysql.connector
from config import DB_CONFIG


def get_connection():
    connection = mysql.connector.connect(**DB_CONFIG)
    return connection


if __name__ == "__main__":
    try:
        connection = get_connection()

        if connection.is_connected():
            print("MySQL database connected successfully!")
            print("Database:", DB_CONFIG["database"])

        connection.close()

    except mysql.connector.Error as error:
        print("MySQL connection failed:", error)