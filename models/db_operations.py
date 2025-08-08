import sqlite3
from data.courses_cis import courses_data, course_of_study

DATABASE_PATH = "data/university_courses.db"


def insert_courses_and_prerequisites():
    """Insert courses and their prerequisites into the database."""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    try:
        for course in courses_data:
            course_code, course_name, category, credit_hours, prerequisites = course

            # Insert course
            cursor.execute(
                """
                INSERT OR IGNORE INTO courses (course_code, course_name, category, credit_hours)
                VALUES (?, ?, ?, ?)
            """,
                (course_code, course_name, category, credit_hours),
            )

            # Insert prerequisites
            if prerequisites:
                prerequisite_codes = prerequisites.split(
                    ","
                )  # Split multiple prerequisites
                for prereq in prerequisite_codes:
                    cursor.execute(
                        """
                        INSERT OR IGNORE INTO course_prerequisites (course_code, prerequisite_code)
                        VALUES (?, ?)
                    """,
                        (course_code, prereq.strip()),
                    )

        connection.commit()
        print("Courses and prerequisites inserted successfully.")
    except sqlite3.Error as e:
        print(f"Error inserting data: {e}")
    finally:
        connection.close()


def fetch_prerequisites(course_code):
    """
    Retrieve prerequisites for a given course.
    :param course_code: The code of the course whose prerequisites you want to retrieve.
    :return: A list of prerequisite course codes.
    """
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT prerequisite_code 
            FROM course_prerequisites 
            WHERE course_code = ?
        """,
            (course_code,),
        )
        prerequisites = cursor.fetchall()
        return [
            prereq[0] for prereq in prerequisites
        ]  # Extract the first element from each tuple
    except sqlite3.Error as e:
        print(f"Error fetching prerequisites: {e}")
        return []
    finally:
        connection.close()


def insert_course_of_study():
    """Insert data into the course_of_study table."""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    try:
        for course in course_of_study:
            course_code, course_name, credit_hours, time, days = course[
                :5
            ]  # Only take relevant fields

            # Insert course into course_of_study table
            cursor.execute(
                """
                INSERT OR IGNORE INTO course_of_study (course_code, course_name, credit_hours, time, days)
                VALUES (?, ?, ?, ?, ?)
                """,
                (course_code, course_name, credit_hours, time, days),
            )

        connection.commit()
        print("Course of study inserted successfully.")
    except sqlite3.Error as e:
        print(f"Error inserting course of study: {e}")
    finally:
        connection.close()


insert_courses_and_prerequisites()
insert_course_of_study()
# course_code = "0601222"  # Example course code
# prerequisites = fetch_prerequisites(course_code)
# print(f"Prerequisites for course {course_code}: {prerequisites}")
