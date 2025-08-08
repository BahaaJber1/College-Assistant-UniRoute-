import sqlite3

def initialize_database():
    # Connect to SQLite database (creates the file if it doesn't exist)
    connection = sqlite3.connect("data/university_courses.db")
    cursor = connection.cursor()

    # Create users table (for login credentials)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            student_number TEXT PRIMARY KEY,
            password TEXT NOT NULL
        );
    """
    )

    # Create student_info table (for additional student information)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS student_info (
            student_number TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            major TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone_number TEXT,
            address TEXT,
            FOREIGN KEY (student_number) REFERENCES users (student_number)
        );
    """
    )

    # Create courses table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS courses (
            course_code TEXT PRIMARY KEY,
            course_name TEXT NOT NULL,
            category TEXT NOT NULL,
            credit_hours INTEGER NOT NULL
        );
    """
    )

    # Create course_prerequisites table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS course_prerequisites (
            course_code TEXT NOT NULL,
            prerequisite_code TEXT NOT NULL,
            FOREIGN KEY (course_code) REFERENCES courses(course_code),
            FOREIGN KEY (prerequisite_code) REFERENCES courses(course_code)
        );
    """
    )

    # Create completed_courses table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS completed_courses (
            student_number TEXT NOT NULL,
            course_code TEXT NOT NULL,
            PRIMARY KEY (student_number, course_code),
            FOREIGN KEY (student_number) REFERENCES student_info(student_number),
            FOREIGN KEY (course_code) REFERENCES courses(course_code)
        );
        """
    )

    # Create course_of_study table
    cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS course_of_study (
        course_code TEXT NOT NULL,
        course_name TEXT NOT NULL,
        credit_hours INTEGER NOT NULL,
        time TEXT NOT NULL,
        days TEXT NOT NULL,
        FOREIGN KEY (course_code) REFERENCES courses(course_code)
    );
    """
)

    # Commit changes and close the connection
    connection.commit()
    connection.close()
    print("Database and tables initialized successfully.")

# Initialize the database
if __name__ == "__main__":
    initialize_database()
