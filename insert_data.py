import os

import MySQLdb
from dotenv import load_dotenv

load_dotenv()

# Add this section in your imports and environment configuration
# Make sure this is set to your MySQL connection string or configure directly
HOST = os.getenv("MYSQL_HOST")
USER = os.getenv("MYSQL_USER")
PASSWORD = os.getenv("MYSQL_PASSWORD")
DB = os.getenv("MYSQL_DB")
PORT = int(os.getenv("MYSQL_PORT"))


def insert_food_suggestion(age, weight, gender, time, type_food, gpt_response, img_url):
    try:
        # Connect to your MySQL database
        conn = MySQLdb.connect(
            host=HOST, user=USER, passwd=PASSWORD, db=DB, port=PORT, ssl_mode="REQUIRED"
        )
        cursor = conn.cursor()

        # Insert data into the food_suggestions table
        insert_query = """
        INSERT INTO food_suggestions (age, weight, gender, time, type_food, gpt_response, img_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(
            insert_query, (age, weight, gender, time, type_food, gpt_response, img_url)
        )

        # Commit the transaction and close the connection
        conn.commit()
        suggestion_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return suggestion_id
    except Exception as e:
        print(f"Error inserting data: {e}")
        return None
