from flask import render_template, Blueprint, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import re
import os

# Define a Blueprint for authentication-related routes
auth_routes = Blueprint("auth", __name__)

# Define the path to the SQLite database
DATABASE_PATH = os.path.abspath("data/university_courses.db")


# Login Route
@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle user login by validating credentials and starting a session.
    """
    if request.method == "POST":
        # Retrieve the submitted student number and password
        student_number = request.form["student_number"]
        password = request.form["password"]

        # Connect to the database
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()

        # Retrieve the hashed password and student name
        cursor.execute(
            """
            SELECT u.password, s.name
            FROM users u
            JOIN student_info s ON u.student_number = s.student_number
            WHERE u.student_number = ?
            """,
            (student_number,),
        )
        user = cursor.fetchone()
        connection.close()

        # Validate the user credentials
        if user and check_password_hash(user[0], password):
            # Password is correct
            session["student_number"] = student_number
            session["student_name"] = user[1]
            flash("Login successful!", "success")
            return redirect(url_for("auth.dashboard"))
        else:
            flash("Invalid credentials. Please try again.", "danger")

    return render_template("login.html")


# Dashboard Route
@auth_routes.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    student_number = session.get("student_number")
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    # Fetch completed courses count
    cursor.execute(
        "SELECT COUNT(*) FROM completed_courses WHERE student_number = ?",
        (student_number,),
    )
    completed_courses = cursor.fetchone()[0]

    # Fetch the remaining credits
    cursor.execute(
        """
        SELECT SUM(c.credit_hours)
        FROM courses c
        WHERE c.course_code NOT IN (
            SELECT cc.course_code FROM completed_courses cc WHERE cc.student_number = ?
        )
        """,
        (student_number,),
    )
    remaining_credits = cursor.fetchone()[0] or 0

    # Fetch GPA (example data; replace with actual GPA calculation)
    gpa = 4.0

    connection.close()

    return render_template(
        "dashboard.html",
        student_name=session.get("student_name", "Student"),
        completed_courses=completed_courses,
        remaining_credits=remaining_credits,
        gpa=gpa,
    )


# Logout Route
@auth_routes.route("/logout")
def logout():
    """
    Log out the user by clearing the session and redirecting to the login page.
    """
    session.clear()  # Clear all session data
    return redirect(url_for("auth.login"))  # Redirect to login page


@auth_routes.route("/register", methods=["GET", "POST"])
def register():
    def is_password_strong(password):
        # Check for at least 8 characters, one uppercase, one lowercase, one digit, and one special character
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>_]", password):
            return False
        return True

    if request.method == "POST":
        # Collect form data
        student_number = request.form.get("student_number", "").strip()
        name = request.form.get("name", "").strip()
        major = request.form.get("major", "").strip()
        email = request.form.get("email", "").strip()
        phone_number = request.form.get("phone_number", "").strip()
        address = request.form.get("address", "").strip()
        password = request.form.get("password", "").strip()

        errors = {}

        # Validate fields
        if not student_number:
            errors["student_number"] = "Student number is required."
        if not name:
            errors["name"] = "Name is required."
        if not email or "@" not in email:
            errors["email"] = "Valid email is required."
        if not password:
            errors["password"] = "Password is required."
        elif not is_password_strong(password):
            errors["password"] = (
                "Password must be at least 8 characters long and include uppercase, lowercase, digit, and special character."
            )
            flash(
                "Password must be at least 8 characters long and include uppercase, lowercase, digit, and special character.","danger"
            )

        # If there are errors, return to the registration form
        if errors:
            return render_template("register.html", errors=errors)

        # Check for duplicates
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT 1 FROM users WHERE student_number = ?", (student_number,)
            )
            if cursor.fetchone():
                errors["student_number"] = "This student number is already registered."

            cursor.execute("SELECT 1 FROM student_info WHERE email = ?", (email,))
            if cursor.fetchone():
                errors["email"] = "This email is already registered."

            # If there are duplicate errors, return to the registration form
            if errors:
                return render_template("register.html", errors=errors)

            # Hash the password and save user data
            hashed_password = generate_password_hash(password)
            cursor.execute(
                "INSERT INTO users (student_number, password) VALUES (?, ?)",
                (student_number, hashed_password),
            )
            cursor.execute(
                """
                INSERT INTO student_info (student_number, name, major, email, phone_number, address)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (student_number, name, major, email, phone_number, address),
            )
            connection.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("auth.login"))
        except sqlite3.Error as e:
            flash("An error occurred during registration. Please try again.", "danger")
            print(f"Database error: {e}")
            return render_template("register.html", errors={})
        finally:
            connection.close()

    return render_template("register.html", errors={})


# Forgot Password Route
@auth_routes.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    """
    Handle password reset requests.
    """
    def update_password(student_number, hashed_password):
        """Update the user's password in the database."""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET password = ? WHERE student_number = ?",
            (hashed_password, student_number),
        )
        conn.commit()
        conn.close()

    if request.method == "POST":
        student_number = request.form["student_number"]
        new_password = request.form["password"]

        # Hash the new password
        from werkzeug.security import generate_password_hash

        hashed_password = generate_password_hash(new_password)

        # Check if the student number exists
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE student_number = ?", (student_number,)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            # Update password with the hashed value
            update_password(student_number, hashed_password)
            flash(
                "Password reset successfully! You can now log in with your new password.",
                "success",
            )
            return redirect(url_for("auth.login"))
        else:
            flash("Student number not found. Please try again.", "danger")

    return render_template("forgot_password.html")


# Route to load partial content dynamically
@auth_routes.route("/load-partial/<section>")
def load_partial(section):
    """
    Dynamically loads partial content based on the section requested.
    """
    if section == "student_info":
        return render_template("partials/student_info.html")
    elif section == "study_plan":
        return render_template("partials/study_plan.html")
    elif section == "generate_plan":
        return render_template("partials/generate_plan.html")
    else:
        return "<p>Section not found.</p>", 404


@auth_routes.route("/load-partial/student_info", methods=["GET", "POST"])
def load_partial_student_info():
    """
    Handles displaying and updating student information for the logged-in user.
    """
    student_number = session.get(
        "student_number"
    )  # Retrieve the logged-in student's number from the session

    if not student_number:
        return (
            "<p>Error: User not logged in.</p>",
            403,
        )  # Return error if the user is not logged in

    conn = sqlite3.connect("data/university_courses.db")
    cursor = conn.cursor()

    if request.method == "POST":
        # Get updated data from the form
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")
        major = request.form.get("major")
        password = request.form.get("password")  # New password (if provided)

        # Debugging: Log received data
        print(f"Updating student info: {name}, {email}, {phone}, {address}, {major}")

        # Update the student_info table
        cursor.execute(
            """
            UPDATE student_info
            SET name = ?, email = ?, phone_number = ?, address = ?, major = ?
            WHERE student_number = ?
        """,
            (name, email, phone, address, major, student_number),
        )

        # If a new password is provided, update it in the users table
        if password:
            print(f"Updating password for student_number: {student_number}")
            cursor.execute(
                """
                UPDATE users
                SET password = ?
                WHERE student_number = ?
            """,
                (password, student_number),
            )

        conn.commit()
        flash("Your information has been updated successfully!", "success")

    # Fetch the current data to display
    cursor.execute(
        "SELECT * FROM student_info WHERE student_number = ?", (student_number,)
    )
    student = cursor.fetchone()
    conn.close()

    if not student:
        return "<p>Student not found.</p>", 404

    # Pass the updated student info to the template
    return render_template("partials/student_info.html", student=student)


@auth_routes.route("/load-partial/study_plan")
def load_study_plan():
    student_number = session.get("student_number")
    connection = sqlite3.connect("data/university_courses.db")
    cursor = connection.cursor()

    # Fetch all courses with a flag indicating if they are completed
    cursor.execute(
        """
        SELECT c.course_code, c.course_name, c.category, c.credit_hours,
        CASE WHEN cc.course_code IS NOT NULL THEN 1 ELSE 0 END AS completed
        FROM courses c
        LEFT JOIN completed_courses cc ON c.course_code = cc.course_code AND cc.student_number = ?
    """,
        (student_number,),
    )
    courses = cursor.fetchall()
    connection.close()

    return render_template("partials/study_plan.html", courses=courses)


@auth_routes.route("/save-study-plan", methods=["POST"])
def save_study_plan():
    student_number = session.get("student_number")
    if not student_number:
        return {"error": "Not authenticated"}, 403

    data = request.json
    completed_courses = data.get("completed_courses", [])

    connection = sqlite3.connect("data/university_courses.db")
    cursor = connection.cursor()

    # Clear old completed courses for this student
    cursor.execute(
        "DELETE FROM completed_courses WHERE student_number = ?", (student_number,)
    )

    # Insert new completed courses
    for course_code in completed_courses:
        cursor.execute(
            "INSERT INTO completed_courses (student_number, course_code) VALUES (?, ?)",
            (student_number, course_code),
        )

    connection.commit()
    connection.close()
    return {"success": True}


def parse_time_range(time_range):
    """Convert a time range string (e.g., '10:00 AM-11:30 AM') into a tuple of start and end times in 24-hour format."""
    import datetime

    start_time_str, end_time_str = time_range.split("-")
    start_time = datetime.datetime.strptime(start_time_str.strip(), "%I:%M %p").time()
    end_time = datetime.datetime.strptime(end_time_str.strip(), "%I:%M %p").time()
    return start_time, end_time


@auth_routes.route("/generate-plan", methods=["GET", "POST"])
def generate_plan():
    import random
    from datetime import datetime

    # Fetch the desired credit hours from the form
    desired_credit_hours = int(request.form["credit_hours"])
    student_number = session.get("student_number")

    conn = sqlite3.connect("data/university_courses.db")
    cursor = conn.cursor()

    # Fetch completed courses
    cursor.execute(
        """
        SELECT c.course_code, c.category, c.credit_hours
        FROM completed_courses cc
        JOIN courses c ON cc.course_code = c.course_code
        WHERE cc.student_number = ?
        """,
        (student_number,),
    )
    completed_courses = cursor.fetchall()

    # Fetch uncompleted courses
    cursor.execute(
        """
        SELECT c.course_code, c.course_name, c.category, c.credit_hours
        FROM courses c
        WHERE c.course_code NOT IN (
            SELECT cc.course_code FROM completed_courses cc WHERE cc.student_number = ?
        )
        """,
        (student_number,),
    )
    uncompleted_courses = cursor.fetchall()

    # Fetch available courses
    cursor.execute(
        """
        SELECT s.course_code, s.time, s.days
        FROM course_of_study s
        """
    )
    available_courses = {
        row[0]: {"time": row[1], "days": row[2]} for row in cursor.fetchall()
    }

    # Fetch prerequisites
    cursor.execute(
        """
        SELECT course_code, prerequisite_code
        FROM course_prerequisites
        """
    )
    prerequisites = cursor.fetchall()
    prereq_dict = {}
    for course_code, prerequisite_code in prerequisites:
        prereq_dict.setdefault(course_code, set()).add(prerequisite_code)

    # Calculate remaining hours
    category_limits = {
        "mandatory_university": 21,
        "elective_university": 6,
        "mandatory_college": 24,
        "mandatory_specialization": 74,
        "elective_specialization": 9,
    }
    remaining_hours = category_limits.copy()
    for _, category, credit_hours in completed_courses:
        remaining_hours[category] -= credit_hours

    # Step 1: Store all eligible courses (static order)
    eligible_courses = []
    for course_code, course_name, category, credit_hours in uncompleted_courses:
        if course_code not in available_courses:
            continue

        if course_code in prereq_dict and not prereq_dict[course_code].issubset(
            {c[0] for c in completed_courses}
        ):
            continue

        if remaining_hours[category] < credit_hours:
            continue

        eligible_courses.append(
            (
                course_code,
                course_name,
                category,
                credit_hours,
                available_courses[course_code]["time"],
                available_courses[course_code]["days"],
            )
        )

    # Step 2: Randomized course selection for generated plan
    remaining_eligible_courses = eligible_courses.copy()
    random.shuffle(remaining_eligible_courses)  # Randomize selection process
    generated_plan = []
    total_hours = 0
    planned_times = []

    for (
        course_code,
        course_name,
        category,
        course_credit_hours,
        time,
        days,
    ) in remaining_eligible_courses:
        # Stop if we've reached the desired credit hours
        if total_hours >= desired_credit_hours:
            break

        # Check if adding this course exceeds the desired credit hours
        if total_hours + course_credit_hours > desired_credit_hours:
            continue

        # Parse the course time into a start and end range
        course_start, course_end = parse_time_range(time)

        # Check for time conflicts
        conflict = False
        for planned in planned_times:
            planned_start, planned_end = parse_time_range(planned["time"])
            if set(days.split()).intersection(
                set(planned["days"].split())
            ) and (  # Days overlap
                course_start < planned_end and course_end > planned_start
            ):  # Times overlap
                conflict = True
                break

        if conflict:
            continue

        # Add the course to the plan
        generated_plan.append(
            (course_code, course_name, course_credit_hours, time, days)
        )
        planned_times.append({"time": time, "days": days})
        remaining_hours[category] -= course_credit_hours
        total_hours += course_credit_hours

    # Step 3: Sort the generated plan by days and then by time
    generated_plan.sort(
        key=lambda course: (
            course[4],  # Days
            datetime.strptime(
                course[3].split("-")[0].strip(), "%I:%M %p"
            ),  # Start time
        )
    )

    print("Final Generated Plan (Sorted):", generated_plan)
    conn.close()

    # Pass eligible courses (unsorted), the generated plan (sorted), and conflict courses to the template
    return render_template(
        "partials/generated_plan.html",
        eligible_courses=eligible_courses,
        plan=generated_plan,
    )


@auth_routes.route("/load-partial/guidance_plan", methods=["GET"])
def load_guidance_plan():
    return render_template("partials/guidance_plan.html")


import xlsxwriter
from flask import send_file, jsonify


@auth_routes.route("/export-plan/excel", methods=["POST"])
def export_plan_excel():
    data = request.json.get("plan", [])
    plan_type = request.json.get("plan_type", "study_plan")
    file_path = f"{plan_type}_plan.xlsx"

    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet()

    # Write headers
    headers = ["Course Code", "Course Name", "Credit Hours", "Time", "Days"]
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    # Write data
    for row_num, row in enumerate(data, 1):
        for col_num, value in enumerate(row):
            worksheet.write(row_num, col_num, value)

    workbook.close()

    return send_file(file_path, as_attachment=True)
