import sqlite3


DATABASE = "applications.db"


def create_table():
    """
    Creates the applications table if it does not exist.
    """

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            location TEXT,
            status TEXT NOT NULL,
            applied_date TEXT,
            job_url TEXT
        )
    """)

    connection.commit()
    connection.close()



def add_application(
    company,
    role,
    location,
    status,
    applied_date,
    job_url
):
    """
    Adds a new job application to the database.
    """

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO applications
        (company, role, location, status, applied_date, job_url)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        company,
        role,
        location,
        status,
        applied_date,
        job_url
    ))

    connection.commit()
    connection.close()



def get_applications():
    """
    Returns all job applications from the database.
    """

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM applications
        ORDER BY id DESC
    """)

    applications = cursor.fetchall()

    connection.close()

    return applications



def update_application_status(application_id, new_status):
    """
    Updates the status of an existing job application.
    """

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE applications
        SET status = ?
        WHERE id = ?
    """, (new_status, application_id))

    connection.commit()
    connection.close()



def delete_application(application_id):
    """
    Deletes an application from the database.
    """

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM applications
        WHERE id = ?
    """, (application_id,))

    connection.commit()
    connection.close()