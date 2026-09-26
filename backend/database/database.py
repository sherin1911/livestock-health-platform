import os
import sqlite3
from flask import current_app


def get_db_connection():
    """
    Create and return a connection to the SQLite database.
    """

    database_path = current_app.config["DATABASE_PATH"]

    os.makedirs(os.path.dirname(database_path), exist_ok=True)

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    return connection


def init_database():
    """
    Create the database and required tables.
    """

    database_path = current_app.config["DATABASE_PATH"]

    os.makedirs(os.path.dirname(database_path), exist_ok=True)

    connection = sqlite3.connect(database_path)

    cursor = connection.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'FARMER',
            language TEXT NOT NULL DEFAULT 'en',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Animals table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS animals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            animal_name TEXT,
            species TEXT NOT NULL,
            breed TEXT,
            age INTEGER,
            gender TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Health reports table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS health_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            animal_id INTEGER,
            species TEXT,
            symptoms TEXT,
            severity TEXT,
            description TEXT,
            latitude REAL,
            longitude REAL,
            photo_path TEXT,
            audio_path TEXT,
            status TEXT DEFAULT 'NEW',
            risk_score REAL DEFAULT 0,
            risk_level TEXT DEFAULT 'LOW',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (animal_id) REFERENCES animals(id)
        )
    """)

    # Alerts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            health_report_id INTEGER,
            risk_level TEXT NOT NULL,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            status TEXT DEFAULT 'NEW',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (health_report_id) REFERENCES health_reports(id)
        )
    """)

    # Vaccination table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vaccinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            animal_id INTEGER NOT NULL,
            vaccine_name TEXT NOT NULL,
            vaccination_date TEXT,
            next_due_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (animal_id) REFERENCES animals(id)
        )
    """)

    # Mortality reports
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mortality_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            animal_id INTEGER,
            species TEXT,
            death_count INTEGER DEFAULT 1,
            suspected_reason TEXT,
            latitude REAL,
            longitude REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (animal_id) REFERENCES animals(id)
        )
    """)

    connection.commit()
    connection.close()

    print("Database initialized successfully.")