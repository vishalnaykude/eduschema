
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import datetime

app = Flask(__name__)

# Establish the database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="eduschema1"
)
cursor = conn.cursor()

# Helper function to add a deleted record to the deleted table
def add_to_deleted(table_name, record_id, user_id=None, delete_reason=None):
    try:
        query = ("INSERT INTO deleted (table_name, record_id, user_id, delete_reason) "
                 "VALUES (%s, %s, %s, %s)")
        data = (table_name, record_id, user_id, delete_reason)
        cursor.execute(query, data)
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Failed to add record to deleted table: {err}")

@app.route('/')
def index():
    return render_template('index.html')

# Courses routes
@app.route('/courses')
def courses():
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    return render_template('courses.html', courses=courses)

@app.route('/add_course', methods=['POST'])
def add_course():
    course_name = request.form['course_name']
    description = request.form['description']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    if start_date >= end_date:
        return "Error: Start date must be before end date."

    try:
        query = ("INSERT INTO courses (course_name, description, start_date, end_date) "
                 "VALUES (%s, %s, %s, %s)")
        data = (course_name, description, start_date, end_date)
        cursor.execute(query, data)
        conn.commit()
        return redirect(url_for('courses'))
    except mysql.connector.Error as err:
        return f"Failed to add course: {err}"

@app.route('/delete_course/<int:course_id>', methods=['POST'])
def delete_course(course_id):
    try:
        add_to_deleted('courses', course_id)
        query = "DELETE FROM courses WHERE course_id = %s"
        cursor.execute(query, (course_id,))
        conn.commit()
        return redirect(url_for('courses'))
    except mysql.connector.Error as err:
        return f"Failed to delete course: {err}"

# Instructors routes
@app.route('/instructors')
def instructors():
    cursor.execute("SELECT * FROM instructors")
    instructors = cursor.fetchall()
    return render_template('instructors.html', instructors=instructors)

@app.route('/add_instructor', methods=['POST'])
def add_instructor():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    bio = request.form['bio']
    try:
        query = ("INSERT INTO instructors (first_name, last_name, email, bio) "
                 "VALUES (%s, %s, %s, %s)")
        data = (first_name, last_name, email, bio)
        cursor.execute(query, data)
        conn.commit()
        return redirect(url_for('instructors'))
    except mysql.connector.Error as err:
        return f"Failed to add instructor: {err}"

@app.route('/delete_instructor/<int:instructor_id>', methods=['POST'])
def delete_instructor(instructor_id):
    try:
        add_to_deleted('instructors', instructor_id)
        query = "DELETE FROM instructors WHERE instructor_id = %s"
        cursor.execute(query, (instructor_id,))
        conn.commit()
        return redirect(url_for('instructors'))
    except mysql.connector.Error as err:
        return f"Failed to delete instructor: {err}"

# Students routes
@app.route('/students')
def students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return render_template('students.html', students=students)

@app.route('/add_student', methods=['POST'])
def add_student():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    try:
        query = ("INSERT INTO students (first_name, last_name, email) "
                 "VALUES (%s, %s, %s)")
        data = (first_name, last_name, email)
        cursor.execute(query, data)
        conn.commit()
        return redirect(url_for('students'))
    except mysql.connector.Error as err:
        return f"Failed to add student: {err}"

@app.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    try:
        add_to_deleted('students', student_id)
        query = "DELETE FROM students WHERE student_id = %s"
        cursor.execute(query, (student_id,))
        conn.commit()
        return redirect(url_for('students'))
    except mysql.connector.Error as err:
        return f"Failed to delete student: {err}"

# Enrollments routes
@app.route('/enrollments')
def enrollments():
    cursor.execute("SELECT * FROM enrollments")
    enrollments = cursor.fetchall()
    return render_template('enrollments.html', enrollments=enrollments)

@app.route('/enroll_student', methods=['POST'])
def enroll_student():
    student_id = request.form['student_id']
    course_id = request.form['course_id']
    try:
        query = ("INSERT INTO enrollments (student_id, course_id, progress) "
                 "VALUES (%s, %s, %s)")
        data = (student_id, course_id, 0)
        cursor.execute(query, data)
        conn.commit()
        return redirect(url_for('enrollments'))
    except mysql.connector.Error as err:
        return f"Failed to enroll student: {err}"

@app.route('/delete_enrollment/<int:enrollment_id>', methods=['POST'])
def delete_enrollment(enrollment_id):
    try:
        add_to_deleted('enrollments', enrollment_id)
        query = "DELETE FROM enrollments WHERE enrollment_id = %s"
        cursor.execute(query, (enrollment_id,))
        conn.commit()
        return redirect(url_for('enrollments'))
    except mysql.connector.Error as err:
        return f"Failed to delete enrollment: {err}"

# View Deleted Records
@app.route('/deleted')
def view_deleted():
    cursor.execute("SELECT * FROM deleted")
    deleted = cursor.fetchall()
    return render_template('deleted.html', deleted=deleted)

if __name__ == '__main__':
    app.run(debug=True)
