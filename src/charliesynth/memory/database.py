
import os

import psycopg


DATABASE_URL = os.getenv(
    "CHARLIESYNTH_DATABASE_URL",
    "dbname=charliesynth user=botirjon",
)


def get_connection():
    """Open a connection to CharlieSynth's PostgreSQL database."""
    return psycopg.connect(DATABASE_URL)


def check_connection():
    """Verify database access and return basic connection information."""
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT current_database(), current_user;"
            )
            database, user = cursor.fetchone()

    return {
        "connected": True,
        "database": database,
        "user": user,
    }
