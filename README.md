# Event-Management-System
This project implements an Event Management System to handle event creation, student registrations, attendance tracking, and feedback collection. It provides an interactive dashboard and reports for admins to monitor events and student participation efficiently.
# Campus Event System

A web-based Campus Event Management System that allows students to register, login, view events, and provide feedback. This system also enables admins to manage events, registrations, and attendance.

## Table of Contents

- Features
- Tech Stack
- Project Structure
- Setup Instructions
- Usage
- API Endpoints
- Contributing
- License

## Features

- Student registration and login
- Admin dashboard to manage events
- Event registration and attendance tracking
- Feedback submission by students
- Responsive UI for desktop and mobile

## Tech Stack

- Backend: Flask (Python)
- Frontend: HTML, CSS, JavaScript
- Database: SQLite
- ORM: SQLAlchemy
- Templating: Jinja2

## Project Structure

campus-event-system/

app.py                 # Main Flask app
models.py              # SQLAlchemy database models
static/                # CSS, JS, images
templates/             # HTML templates
  admin/
  student/
  common/
requirements.txt       # Python dependencies
README.txt             # Project documentation

## Setup Instructions

Follow these steps to run the project locally:

### 1. Clone the repository


git clone <your-repo-url>
cd campus-event-system


### 2. Create a virtual environment

python -m venv venv


### 3. Activate the virtual environment

- Windows:

venv\Scripts\activate

- Linux / macOS:

source venv/bin/activate


### 4. Install dependencies


pip install -r requirements.txt

### 5. Run the Flask app


python app.py


Open your browser and go to:


http://127.0.0.1:5000/


## Usage

- Navigate to the home page to view events
- Students can register and login
- Admin can add, update, or delete events
- Students can register for events and submit feedback

## API Endpoints (Sample)

| Method | Endpoint | Description |
|--------|---------|-------------|
| GET    | `/`     | Home page |
| POST   | `/register_student_form` | Register a student |
| POST   | `/login_student_form`    | Login student |
| GET    | `/events` | List all events |
| POST   | `/submit_feedback` | Submit event feedback |

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature-xyz`)
3. Make your changes
4. Commit your changes (`git commit -m "Add feature xyz"`)
5. Push to the branch (`git push origin feature-xyz`)
6. Create a Pull Request


