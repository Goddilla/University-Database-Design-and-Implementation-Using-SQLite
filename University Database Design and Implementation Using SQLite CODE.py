import sqlite3
import random
from faker import Faker

# Creating an instance of the Faker library for generating random data
fake = Faker()

# Connecting to SQLite database (it will create the database if it doesn't exist)
conn = sqlite3.connect('university_students_data.db')
cursor = conn.cursor()

# Droping tables if they exist to avoid conflicts
cursor.execute("DROP TABLE IF EXISTS Attendance")
cursor.execute("DROP TABLE IF EXISTS Enrollments")
cursor.execute("DROP TABLE IF EXISTS Grades")
cursor.execute("DROP TABLE IF EXISTS Students")
cursor.execute("DROP TABLE IF EXISTS Courses")
cursor.execute("DROP TABLE IF EXISTS Professors")
cursor.execute("DROP TABLE IF EXISTS Departments")
cursor.execute("DROP TABLE IF EXISTS Course_Offerings")

# Creating Departments table
cursor.execute('''CREATE TABLE Departments 
               (
                    department_id INTEGER PRIMARY KEY,
                    department_name TEXT UNIQUE NOT NULL,
                    location TEXT NOT NULL
                 )''')

# Creating Professors table
cursor.execute('''CREATE TABLE Professors 
               (
                    professor_id INTEGER PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    department_id INTEGER,
                    salary INTEGER CHECK (salary > 0),
                    FOREIGN KEY (department_id) REFERENCES Departments(department_id)
                 )''')

# Creating Courses table
cursor.execute('''CREATE TABLE Courses 
               (
                    course_id INTEGER PRIMARY KEY,
                    course_name TEXT NOT NULL,
                    department_id INTEGER,
                    credit_hours INTEGER CHECK (credit_hours BETWEEN 1 AND 5),
                    FOREIGN KEY (department_id) REFERENCES Departments(department_id)
                 )''')

# Creating Students table
cursor.execute('''CREATE TABLE Students 
               (
                    student_id INTEGER PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    birthdate DATE NOT NULL,
                    major TEXT NOT NULL,
                    gpa REAL CHECK (gpa BETWEEN 0 AND 4.0)
                 )''')

# Creating Course Offerings table
cursor.execute('''CREATE TABLE Course_Offerings 
               (
                    offering_id INTEGER PRIMARY KEY,
                    course_id INTEGER NOT NULL,
                    semester TEXT CHECK (semester IN ('Fall', 'Spring', 'Summer')),
                    year INTEGER CHECK (year BETWEEN 2020 AND 2025),
                    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
                 )''')

# Creating Enrollments table with compound key
cursor.execute('''CREATE TABLE Enrollments 
               (
                    student_id INTEGER NOT NULL,
                    course_id INTEGER NOT NULL,
                    grade TEXT CHECK (grade IN ('A', 'B', 'C', 'D', 'F')),
                    PRIMARY KEY (student_id, course_id),
                    FOREIGN KEY (student_id) REFERENCES Students(student_id),
                    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
                 )''')

# Creating Attendance table
cursor.execute('''CREATE TABLE Attendance 
               (
                    attendance_id INTEGER PRIMARY KEY,
                    student_id INTEGER NOT NULL,
                    course_id INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    status TEXT CHECK (status IN ('Present', 'Absent')),
                    FOREIGN KEY (student_id) REFERENCES Students(student_id),
                    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
                 )''')



# Inserting Departments data
departments = ['Computer Science', 'Electrical Engineering', 'Physics', 'Mathematics', 'Chemistry']
for department in departments:
    location = fake.city()
    cursor.execute("INSERT INTO Departments (department_name, location) VALUES (?, ?)", (department, location))
    
# Inserting Professors data
for _ in range(10):
    first_name = fake.first_name()
    last_name = fake.last_name()
    department_id = random.randint(1, len(departments))
    salary = random.randint(50000, 120000)
    cursor.execute("INSERT INTO Professors (first_name, last_name, department_id, salary) VALUES (?, ?, ?, ?)",
                   (first_name, last_name, department_id, salary))


# Inserting Courses data
courses = ['Introduction to Programming', 'Data Structures', 'Database Systems', 'Machine Learning', 'Operating Systems']
for course_name in courses:
    department_id = random.randint(1, len(departments))
    credit_hours = random.choice([3, 4, 5])
    cursor.execute("INSERT INTO Courses (course_name, department_id, credit_hours) VALUES (?, ?, ?)",
                   (course_name, department_id, credit_hours))

# Inserting Students data
for _ in range(1000):
    first_name = fake.first_name()
    last_name = fake.last_name()
    birthdate = fake.date_of_birth(minimum_age=18, maximum_age=22).strftime("%Y-%m-%d")
    major = random.choice(departments)
    gpa = round(random.uniform(2.5, 4.0), 2)
    cursor.execute("INSERT INTO Students (first_name, last_name, birthdate, major, gpa) VALUES (?, ?, ?, ?, ?)",
                   (first_name, last_name, birthdate, major, gpa))


# Inserting Course Offerings data
for course_id in range(1, len(courses) + 1):
    semester = random.choice(['Fall', 'Spring', 'Summer'])
    year = random.randint(2020, 2025)
    cursor.execute("INSERT INTO Course_Offerings (course_id, semester, year) VALUES (?, ?, ?)",
                   (course_id, semester, year))

# Inserting Enrollments data
for student_id in range(1, 1001):
    enrolled_courses = random.sample(range(1, len(courses) + 1), k=3)
    for course_id in enrolled_courses:
        grade = random.choice(['A', 'B', 'C', 'D', 'F'])
        cursor.execute("INSERT INTO Enrollments (student_id, course_id, grade) VALUES (?, ?, ?)",
                       (student_id, course_id, grade))


# Inserting Attendance data
for student_id in range(1, 1001):
    for _ in range(5):
        course_id = random.randint(1, len(courses))
        date = fake.date_this_decade().strftime("%Y-%m-%d")
        status = random.choice(['Present', 'Absent'])
        cursor.execute("INSERT INTO Attendance (student_id, course_id, date, status) VALUES (?, ?, ?, ?)",
                       (student_id, course_id, date, status))


# Commiting and closing
conn.commit()
conn.close()