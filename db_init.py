# Run this script once to create the MySQL database and the tables.
# Usage: python db_init.py
import mysql.connector
from mysql.connector import errorcode
from models import db
from app import app

DB_USER = "root"
DB_PASS = "Brannel@55G"
DB_HOST = "localhost"
DB_NAME = "habit_db"

def create_database():
    try:
        conn = mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` DEFAULT CHARACTER SET 'utf8'")
        print("Database ensured:", DB_NAME)
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print("Error creating database:", err)
        raise

if __name__ == '__main__':
    create_database()
    with app.app_context():
        db.create_all()
    print("Tables created (if not existing).")
