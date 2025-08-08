# Course Suggestion System

A comprehensive web application designed to help university students manage their study plans, track completed courses, and generate optimal course schedules based on prerequisites, available times, and credit requirements.

<img width="1914" height="905" alt="image" src="https://github.com/user-attachments/assets/3db5004b-2668-4c99-b901-be7b9e41cfb5" />

<img width="1916" height="911" alt="image" src="https://github.com/user-attachments/assets/659aed98-17f4-4126-8b85-fee8cfaf8027" />


<img width="1911" height="905" alt="image" src="https://github.com/user-attachments/assets/f4f6963e-da34-49cf-8c1b-47b15f37e1a4" />

<img width="1911" height="905" alt="image" src="https://github.com/user-attachments/assets/fd108060-1e6f-4dcf-9c42-3fcbc9a79d9a" />

<img width="1910" height="904" alt="image" src="https://github.com/user-attachments/assets/e8407cc9-d4c8-4256-a761-1af8540be8ba" />

<img width="1916" height="904" alt="image" src="https://github.com/user-attachments/assets/e0b729d2-d4e4-4c42-ba1d-d230be7882a6" />

<img width="1916" height="906" alt="image" src="https://github.com/user-attachments/assets/bf1c04f7-3587-4ff2-862d-d5d981f1f94c" />

<img width="1911" height="900" alt="image" src="https://github.com/user-attachments/assets/f52b1e7b-7002-4ead-8c76-4cf8b592ca0c" />








## Features

- **User Authentication**: Secure registration, login, and password reset functionality.
- **Dashboard**: Overview of completed courses, remaining credits, and GPA.
- **Student Information Management**: View and update personal and academic details.
- **Study Plan Management**: Track completed and pending courses, save progress.
- **Course Plan Generation**: Automatically generate a course schedule based on user preferences, prerequisites, and time conflicts.
- **Excel Export**: Export generated study plans to Excel for offline use.
- **Dynamic Content Loading**: Partial templates for modular UI updates.

## Technologies Used

- **Backend**: Python, Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript (with static assets)
- **Excel Export**: xlsxwriter

## Project Structure

```
Course Suggestion System/
├── app.py
├── requirements.txt
├── data/
│   ├── courses_cis.py
│   ├── university_courses.db
├── models/
│   ├── db_operations.py
│   ├── setup_db.py
├── routes/
│   └── auth_routes.py
├── static/
│   ├── css/
│   ├── images/
│   └── js/
├── templates/
│   ├── dashboard.html
│   ├── forgot_password.html
│   ├── login.html
│   ├── register.html
│   └── partials/
│       ├── generate_plan.html
│       ├── generated_plan.html
│       ├── guidance_plan.html
│       ├── student_info.html
│       └── study_plan.html
```

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd "Course Suggestion System"
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Database Setup**
   - Ensure `university_courses.db` exists in the `data/` directory.
   - If needed, run `models/setup_db.py` to initialize tables.
4. **Run the Application**
   ```bash
   python app.py
   ```
5. **Access the Web App**
   - Open your browser and go to `http://localhost:5000`

## Usage

- **Register**: Create a new account with your student information.
- **Login**: Access your dashboard and manage your study plan.
- **Update Info**: Edit your personal and academic details.
- **Generate Plan**: Specify desired credit hours and generate a conflict-free course schedule.
- **Export Plan**: Download your generated plan as an Excel file.

## Database Schema Overview

- **users**: Stores authentication credentials.
- **student_info**: Stores student details.
- **courses**: List of all available courses.
- **completed_courses**: Tracks courses completed by each student.
- **course_of_study**: Contains course scheduling info (time, days).
- **course_prerequisites**: Maps course prerequisites.

## Security Notes

- Passwords are securely hashed using Werkzeug.
- Input validation and duplicate checks are implemented during registration.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License.

## Contact

For questions or support, please contact the project maintainer.
