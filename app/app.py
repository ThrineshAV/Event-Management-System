from flask import Flask, request, jsonify, render_template
from models import db, College, Event, Student, Registration, AttendanceRequest, Feedback ,Attendance
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, redirect, url_for
from flask import Flask, render_template, request, session, redirect, url_for, flash
from models import db, Admin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campus_events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

# Create tables once at startup
with app.app_context():
    db.create_all()

# -------------------- API Routes --------------------

@app.route('/index')
def home():
    return render_template("landing.html")


app.secret_key = "your_secret_key"   # required for session handling

from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, Admin

app.secret_key = "your_secret_key"

# -------------------- Admin Register --------------------
@app.route('/admin/register', methods=['POST'])
def admin_register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # Check if email already exists
    if Admin.query.filter_by(email=email).first():
        flash("Email already registered!", "danger")
        return redirect(url_for('admin_register_form'))

    admin = Admin(username=username, email=email)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()

    flash("Admin registered successfully! Please login.", "success")
    return redirect(url_for('admin_login_form'))   # ✅ redirect to login page


# -------------------- Frontend Route: Register Form --------------------
@app.route('/admin/register_form')
def admin_register_form():
    return render_template("admin/register.html")


# -------------------- Admin Login --------------------
@app.route('/admin/login', methods=['POST'])
def admin_login():
    email = request.form['email']
    password = request.form['password']

    admin = Admin.query.filter_by(email=email).first()
    if admin and admin.check_password(password):
        session['admin_id'] = admin.id
        flash("Login successful!", "success")
        return redirect(url_for('admin_dashboard'))  # ✅ dashboard after login
    else:
        flash("Invalid email or password", "danger")
        return redirect(url_for('admin_login_form'))


# -------------------- Frontend Route: Login Form --------------------
@app.route('/admin/login_form')
def admin_login_form():
    return render_template("admin/login.html")


# -------------------- Admin Logout --------------------
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('admin_login_form'))   # ✅ redirect to login form


# -------------------- Admin Dashboard --------------------
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('admin_login_form'))  # ✅ if not logged in
    return render_template("admin/dashboard.html")


# -------------------- Student Register --------------------
@app.route('/student/register', methods=['POST'])
def student_register():
    try:
        data = request.get_json(force=True)  # <-- accept JSON from JS

        username = data.get('name')
        email = data.get('email')
        password = data.get('password')

        # Validate input
        if not all([username, email, password]):
            return {"error": "All fields are required"}, 400

        # Check if email exists
        if Student.query.filter_by(email=email).first():
            return {"error": "Email already registered"}, 400

        # Create student
        student = Student(username=username, email=email)
        student.set_password(password)
        db.session.add(student)
        db.session.commit()

        return {"message": "Student registered successfully", "student_id": student.id}, 201

    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/register_student_form")
def student_register_form():
    return render_template("student/register.html")



# -------------------- Student Login --------------------
@app.route('/student/login', methods=['POST'])
def student_login():
    try:
        data = request.get_json(force=True)
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return {"error": "Email and password are required"}, 400

        student = Student.query.filter_by(email=email).first()
        if student and student.check_password(password):
            session['student_id'] = student.id
            return {"message": "Login successful"}, 200
        else:
            return {"error": "Invalid email or password"}, 401

    except Exception as e:
        return {"error": str(e)}, 500

# -------------------- Frontend Route: Login Form --------------------
@app.route('/login_student_form')
def login_student_form():
    return render_template("student/login.html")


# -------------------- Student Dashboard --------------------
@app.route('/student/dashboard')
def student_dashboard():
    if 'student_id' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('login_student_form'))
    return render_template("student/dashboard.html")


# -------------------- Student Logout --------------------
@app.route('/student/logout')
def student_logout():
    session.pop('student_id', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('login_student_form'))   # ✅ back to login form



# -------------------- Create Event API --------------------
@app.route('/create_event', methods=['POST'])
def create_event():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        # Basic validation
        name = data.get('name')
        event_type = data.get('event_type')
        date_str = data.get('date')
        description = data.get('description')
        college_id = data.get('college_id')

        if not name or not date_str or not college_id:
            return jsonify({"error": "College ID, name and date are required"}), 400

        # Parse date
        event_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        # Optional: Check if college exists
        college = College.query.get(college_id)
        if not college:
            return jsonify({"error": "College not found"}), 404

        event = Event(
            name=name,
            event_type=event_type,
            date=event_date,
            description=description
        )
        db.session.add(event)
        db.session.commit()

        return jsonify({"message": "Event created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------- Frontend Route --------------------

@app.route('/create_event_form')
def create_event_form():
    return render_template("admin/create_event.html")

# -------------------- Register College API --------------------
@app.route('/register_college/', methods=['POST'])
def register_college():
    data = request.get_json(force=True)

    # Simple validation
    if not data.get("name") or not data["name"].strip():
        return jsonify({"error": "College name is required"}), 400

    # Check if college already exists
    college = College.query.filter_by(name=data["name"].strip()).first()
    if college:
        return jsonify({"message": "College already exists", "college_id": college.id}), 200

    # Create new college
    college = College(name=data["name"].strip())
    db.session.add(college)
    db.session.commit()

    return jsonify({"message": "College registered successfully", "college_id": college.id}), 201

# -------------------- Frontend Route --------------------
@app.route('/register_college_form')
def register_college_form():
    return render_template("admin/register_college.html")


# -------------------- Student Attendance Request --------------------
@app.route('/student/request_attendance', methods=['POST'])
def student_request_attendance():
    try:
        student_id = request.form.get('student_id')
        event_id = request.form.get('event_id')

        # Convert IDs to integers
        try:
            student_id = int(student_id)
            event_id = int(event_id)
        except (ValueError, TypeError):
            return jsonify({"error": "Student ID and Event ID must be valid numbers"}), 400

        # Check if event exists first
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"error": "Event ID does not exist"}), 404

        # Check if student exists
        student = Student.query.get(student_id)
        if not student:
            return jsonify({"error": "Invalid student ID"}), 404

        # Check if already requested
        existing = AttendanceRequest.query.filter_by(student_id=student_id, event_id=event_id).first()
        if existing:
            return jsonify({"error": "You already requested attendance for this event"}), 400

        # Create attendance request
        request_entry = AttendanceRequest(student_id=student_id, event_id=event_id)
        db.session.add(request_entry)
        db.session.commit()

        return jsonify({"message": "Attendance request submitted! Waiting for admin approval."}), 201

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal server error"}), 500


# -------------------- Student Attendance Request Form --------------------
@app.route('/attendance_request_form')
def attendance_request_form():
    if 'student_id' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('login_student_form'))
    return render_template("student/attendance_request.html")


# -------------------- Admin View Pending Requests --------------------
@app.route('/admin/approve_attendance/<int:request_id>', methods=['POST'])
def approve_attendance(request_id):
    req = AttendanceRequest.query.get_or_404(request_id)

    # Approve → Create real Attendance record
    attendance = Attendance(
        registration_id=req.student_id,  # or registration mapping
        status="Present"
    )
    db.session.add(attendance)

    req.status = "Approved"
    db.session.commit()
    flash("Attendance approved and saved!", "success")
    return redirect(url_for('admin_attendance_requests'))


@app.route('/admin/reject_attendance/<int:request_id>', methods=['POST'])
def reject_attendance(request_id):
    req = AttendanceRequest.query.get_or_404(request_id)
    req.status = "Rejected"
    db.session.commit()
    flash("Attendance request rejected.", "danger")
    return redirect(url_for('admin_attendance_requests'))


@app.route('/admin/attendance_requests')
def admin_attendance_requests():
    if 'admin_id' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('admin_login_form'))

    requests = AttendanceRequest.query.all()

    return render_template("admin/attendance_requests.html", requests=requests)

# -------------------- EVENT REGISTER API --------------------

@app.route('/student/register_event', methods=['POST'])
def register_event():
    if 'student_id' not in session:
        return jsonify({"error": "Student not logged in"}), 401

    try:
        data = request.get_json(force=True)
        student_id = session['student_id']
        event_id = data.get('event_id')

        # Validation
        if not event_id:
            return jsonify({"error": "Event ID is required"}), 400

        try:
            event_id = int(event_id)
        except ValueError:
            return jsonify({"error": "Event ID must be an integer"}), 400

        # Check if event exists
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"error": "Event not found"}), 404

        # Check if already registered
        existing_registration = Registration.query.filter_by(
            student_id=student_id, event_id=event_id
        ).first()
        if existing_registration:
            return jsonify({"error": "Already registered for this event"}), 409

        # Create registration
        registration = Registration(student_id=student_id, event_id=event_id)
        db.session.add(registration)
        db.session.commit()

        return jsonify({
            "message": f"Successfully registered for {event.name}",
            "registration_id": registration.id
        }), 201

    except Exception as e:
        print("Error registering event:", e)
        return jsonify({"error": "Internal server error"}), 500

# -------------------- Frontend Route --------------------
@app.route('/event_registration_form')
def event_registration_form():
    if 'student_id' not in session:
        flash("Please login first", "warning")
        return redirect(url_for('login_student_form'))
    return render_template("student/event_register.html")


# -------------------- Submit Feedback API --------------------
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    try:
        data = request.get_json(force=True)

        # Validate required fields (student_id not needed)
        required_fields = ("event_id", "feedback_text", "rating")
        if not all(k in data for k in required_fields):
            return jsonify({"error": "event_id, feedback_text, and rating are required"}), 400

        # Get student_id from session
        student_id = session.get('student_id')
        if not student_id:
            return jsonify({"error": "Student not logged in"}), 401

        # Convert IDs and validate rating
        try:
            event_id = int(data['event_id'])
            rating = int(data['rating'])
            if rating < 1 or rating > 5:
                return jsonify({"error": "Rating must be between 1 and 5"}), 400
        except ValueError:
            return jsonify({"error": "event_id and rating must be integers"}), 400

        # Check if student and event exist
        student = Student.query.get(student_id)
        event = Event.query.get(event_id)
        if not student:
            return jsonify({"error": "Invalid student"}), 404
        if not event:
            return jsonify({"error": "Invalid event"}), 404

        # Check if feedback already exists for this student and event
        existing_feedback = Feedback.query.filter_by(student=student_id, event=event_id).first()
        if existing_feedback:
            return jsonify({"error": "You have already submitted feedback for this event"}), 400

        # Create feedback
        feedback = Feedback(
            student=student_id,
            event=event_id,
            feedback_text=data['feedback_text'].strip(),
            rating=rating
        )
        db.session.add(feedback)
        db.session.commit()

        return jsonify({"message": "Feedback submitted successfully", "feedback_id": feedback.id}), 201

    except Exception as e:
        print("Error submitting feedback:", e)
        return jsonify({"error": "Internal server error"}), 500


# -------------------- Feedback Form Page --------------------
@app.route('/feedback_form')
def feedback_form():
    if 'student_id' not in session:
        flash("Please login first", "warning")
        return redirect(url_for('login_student_form'))
    return render_template("student/feedback.html")


@app.route('/get_events', methods=['GET'])
def get_events():
    events = Event.query.all()
    event_list = [{"id": e.id, "name": e.name} for e in events]
    return jsonify(event_list)

from sqlalchemy import func, desc

@app.route("/admin/dashboard_data")
def admin_dashboard_data():
    # Fetch base data
    colleges = College.query.all()
    events = Event.query.all()
    students = Student.query.all()

    # Count registrations per event
    reg_counts = (
        db.session.query(
            Registration.event_id,
            Event.name.label("event_name"),
            func.count(Registration.id).label("registration_count")
        )
        .join(Event, Event.id == Registration.event_id)
        .group_by(Registration.event_id)
        .all()
    )

    registrations_per_event = [
        {"event_id": r.event_id, "event_name": r.event_name, "count": r.registration_count}
        for r in reg_counts
    ]

    # Top 3 active students by number of registrations
    top_students_query = (
        db.session.query(
            Registration.student_id,
            Student.username.label("student_name"),
            func.count(Registration.id).label("total_registrations")
        )
        .join(Student, Student.id == Registration.student_id)
        .group_by(Registration.student_id)
        .order_by(desc("total_registrations"))
        .limit(3)
        .all()
    )

    top_students = [
        {"student_id": s.student_id, "student_name": s.student_name, "registrations": s.total_registrations}
        for s in top_students_query
    ]

    # Convert base data to JSON-serializable dicts
    return {
        "colleges": [{"id": c.id, "name": c.name} for c in colleges],
        "events": [{"id": e.id, "name": e.name, "event_type": e.event_type, "date": str(e.date)} for e in events],
        "students": [{"id": s.id, "username": s.username, "email": s.email} for s in students],
        "registrations_per_event": registrations_per_event,
        "top_students": top_students
    }






# -------------------- Run App --------------------
if __name__ == '__main__':
    app.run(debug=True)
