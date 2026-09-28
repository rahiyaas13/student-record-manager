"""
================================================================================
STUDENT RECORD MANAGEMENT SYSTEM
Module 2 Assignment Submission
================================================================================
Features Implemented:
1. Add Student
2. Validate Email using Regex (re module)
3. Save Data to File (JSON format)
4. Read Student Data (from file and search)
5. Handle Invalid Input using Exceptions (custom & built-in hierarchy)
================================================================================
"""

import os
import sys
import re
import json

# Ensure UTF-8 output encoding across all operating systems
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


# ==============================================================================
# FEATURE 5 & 2: CUSTOM EXCEPTION HIERARCHY
# ==============================================================================

class StudentRecordError(Exception):
    """Base exception class for Student Record Manager."""
    pass


class InvalidEmailError(StudentRecordError):
    """Raised when an email address does not match the regex pattern."""
    def __init__(self, email: str, message: str = "Invalid email format"):
        self.email = email
        self.message = f"{message}: '{email}'"
        super().__init__(self.message)


class InvalidInputError(StudentRecordError):
    """Raised when user input fails type or range validation."""
    def __init__(self, field_name: str, value: str, message: str = "Invalid input"):
        self.field_name = field_name
        self.value = value
        self.message = f"{message} for '{field_name}': '{value}'"
        super().__init__(self.message)


class DuplicateStudentError(StudentRecordError):
    """Raised when attempting to add a student with an existing ID."""
    def __init__(self, student_id: str):
        self.student_id = student_id
        super().__init__(f"Student with ID '{student_id}' already exists.")


class StudentNotFoundError(StudentRecordError):
    """Raised when a requested student record cannot be found."""
    def __init__(self, student_id: str):
        self.student_id = student_id
        super().__init__(f"Student with ID '{student_id}' was not found.")


class FileOperationError(StudentRecordError):
    """Raised when a file read or write operation fails."""
    def __init__(self, filename: str, operation: str, details: str):
        self.filename = filename
        self.operation = operation
        super().__init__(f"Failed to {operation} '{filename}': {details}")


# ==============================================================================
# FEATURE 2: REGEX VALIDATION FUNCTIONS
# ==============================================================================

# RFC-5322 compliant regular expression for email validation
EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}$"
)

# Pattern for student ID: letters, numbers, hyphens (2 to 20 chars)
STUDENT_ID_REGEX = re.compile(r"^[a-zA-Z0-9_-]{2,20}$")

# Pattern for student name: alphabets, spaces, dots, hyphens (2 to 60 chars)
NAME_REGEX = re.compile(r"^[A-Za-z\s.'-]{2,60}$")


def validate_email(email: str) -> str:
    """
    Validates email format using regular expressions.
    Raises InvalidEmailError if format does not match.
    """
    if not isinstance(email, str):
        raise InvalidEmailError(str(email), "Email must be a string")

    cleaned = email.strip()
    if not cleaned:
        raise InvalidEmailError("", "Email address cannot be empty")

    if ".." in cleaned:
        raise InvalidEmailError(cleaned, "Email cannot contain consecutive dots")

    if not EMAIL_REGEX.match(cleaned):
        raise InvalidEmailError(
            cleaned,
            "Email must follow standard format: username@domain.extension (e.g. alex@univ.edu)"
        )

    return cleaned.lower()


def validate_student_id(student_id: str) -> str:
    """Validates student ID format. Raises InvalidInputError on failure."""
    if not isinstance(student_id, str):
        raise InvalidInputError("Student ID", str(student_id), "ID must be a string")

    cleaned = student_id.strip().upper()
    if not cleaned:
        raise InvalidInputError("Student ID", "", "Student ID cannot be empty")

    if not STUDENT_ID_REGEX.match(cleaned):
        raise InvalidInputError(
            "Student ID",
            cleaned,
            "ID must be 2-20 characters long with letters, digits, or dashes only"
        )
    return cleaned


def validate_name(name: str) -> str:
    """Validates student name format. Raises InvalidInputError on failure."""
    if not isinstance(name, str):
        raise InvalidInputError("Name", str(name), "Name must be a string")

    cleaned = name.strip()
    if not cleaned:
        raise InvalidInputError("Name", "", "Name cannot be empty")

    if not NAME_REGEX.match(cleaned):
        raise InvalidInputError(
            "Name",
            cleaned,
            "Name must be 2-60 characters and contain letters or spaces only"
        )
    return cleaned.title()


def validate_age(age_val: any) -> int:
    """Validates age as an integer between 15 and 120. Raises InvalidInputError."""
    try:
        age = int(str(age_val).strip())
    except (ValueError, TypeError):
        raise InvalidInputError("Age", str(age_val), "Age must be an integer number")

    if age < 15 or age > 120:
        raise InvalidInputError("Age", str(age), "Age must be between 15 and 120")
    return age


def validate_gpa(gpa_val: any) -> float:
    """Validates GPA as a float between 0.0 and 4.0. Raises InvalidInputError."""
    try:
        gpa = float(str(gpa_val).strip())
    except (ValueError, TypeError):
        raise InvalidInputError("GPA", str(gpa_val), "GPA must be a valid decimal number")

    if gpa < 0.0 or gpa > 4.0:
        raise InvalidInputError("GPA", str(gpa), "GPA must be between 0.00 and 4.00")
    return round(gpa, 2)


def validate_course(course: str) -> str:
    """Validates course name. Raises InvalidInputError."""
    cleaned = str(course).strip()
    if not cleaned:
        raise InvalidInputError("Course", "", "Course cannot be empty")
    if len(cleaned) < 2 or len(cleaned) > 50:
        raise InvalidInputError("Course", cleaned, "Course must be between 2 and 50 characters")
    return cleaned.title()


# ==============================================================================
# FEATURE 1: STUDENT DATA MODEL
# ==============================================================================

class Student:
    """Represents a student entity with validated properties."""
    def __init__(self, student_id: str, name: str, email: str, age: int, course: str, gpa: float = 0.0):
        self.student_id = validate_student_id(student_id)
        self.name = validate_name(name)
        self.email = validate_email(email)
        self.age = validate_age(age)
        self.course = validate_course(course)
        self.gpa = validate_gpa(gpa)

    def to_dict(self):
        """Serialize student to dictionary."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "course": self.course,
            "gpa": self.gpa,
        }

    @classmethod
    def from_dict(cls, data):
        """Deserialize dictionary to Student instance."""
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            email=data["email"],
            age=data["age"],
            course=data["course"],
            gpa=data.get("gpa", 0.0),
        )

    def __str__(self):
        return (
            f"  ID     : {self.student_id}\n"
            f"  Name   : {self.name}\n"
            f"  Email  : {self.email}\n"
            f"  Age    : {self.age}\n"
            f"  Course : {self.course}\n"
            f"  GPA    : {self.gpa:.2f}"
        )


# ==============================================================================
# FEATURE 3 & 4: STUDENT RECORD MANAGER & FILE PERSISTENCE
# ==============================================================================

class StudentRecordManager:
    """Manages collection of students with file reading and writing."""
    def __init__(self, filename: str = "students.json"):
        self.filename = filename
        self.students = {}

    def add_student(self, student_id: str, name: str, email: str, age: int, course: str, gpa: float = 0.0) -> Student:
        """Adds a student record. Raises DuplicateStudentError if ID already exists."""
        norm_id = student_id.strip().upper()
        if norm_id in self.students:
            raise DuplicateStudentError(norm_id)

        student = Student(
            student_id=norm_id,
            name=name,
            email=email,
            age=age,
            course=course,
            gpa=gpa,
        )
        self.students[student.student_id] = student
        return student

    def get_student(self, student_id: str) -> Student:
        """Retrieves a student by ID. Raises StudentNotFoundError if not found."""
        norm_id = student_id.strip().upper()
        if norm_id not in self.students:
            raise StudentNotFoundError(norm_id)
        return self.students[norm_id]

    def get_all_students(self):
        """Returns list of all students."""
        return list(self.students.values())

    def delete_student(self, student_id: str) -> Student:
        """Deletes a student. Raises StudentNotFoundError if not found."""
        norm_id = student_id.strip().upper()
        if norm_id not in self.students:
            raise StudentNotFoundError(norm_id)
        return self.students.pop(norm_id)

    # FEATURE 3: Save Data to File
    def save_to_file(self, filepath: str = None) -> str:
        """Saves all students to JSON file. Raises FileOperationError on failure."""
        target_path = filepath or self.filename
        try:
            records = [s.to_dict() for s in self.students.values()]
            with open(target_path, "w", encoding="utf-8") as f:
                json.dump(records, f, indent=4, ensure_ascii=False)
            return os.path.abspath(target_path)
        except Exception as e:
            raise FileOperationError(target_path, "save", str(e))

    # FEATURE 4: Read Student Data from File
    def read_from_file(self, filepath: str = None) -> int:
        """Loads students from JSON file. Returns count of loaded records."""
        target_path = filepath or self.filename
        if not os.path.exists(target_path):
            return 0

        try:
            with open(target_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return 0
                data_list = json.loads(content)

            if not isinstance(data_list, list):
                raise FileOperationError(target_path, "read", "Expected a list of student records")

            count = 0
            for item in data_list:
                try:
                    student = Student.from_dict(item)
                    self.students[student.student_id] = student
                    count += 1
                except Exception:
                    continue
            return count
        except json.JSONDecodeError as e:
            raise FileOperationError(target_path, "parse JSON", f"Corrupt file: {e}")
        except Exception as e:
            raise FileOperationError(target_path, "read", str(e))


# ==============================================================================
# FEATURE 5: CLI INTERFACE WITH EXCEPTION HANDLING
# ==============================================================================

def display_table(students):
    """Renders records in a clean tabular view."""
    if not students:
        print("\n[INFO] No student records found.")
        return

    print("\n" + "=" * 88)
    print(f"{'ID':<10} | {'NAME':<20} | {'EMAIL':<28} | {'AGE':<5} | {'COURSE':<12} | {'GPA':<5}")
    print("=" * 88)
    for s in students:
        print(f"{s.student_id:<10} | {s.name[:20]:<20} | {s.email[:28]:<28} | {s.age:<5} | {s.course[:12]:<12} | {s.gpa:<5.2f}")
    print("=" * 88)
    print(f"Total Students: {len(students)}")


def cli_add_student(manager: StudentRecordManager):
    """Guides user through adding a student, catching all input errors."""
    print("\n--- ADD NEW STUDENT ---")
    print("(Type 'cancel' at any prompt to return to main menu)")

    # 1. Student ID
    while True:
        try:
            val = input("Enter Student ID (e.g. STU101): ").strip()
            if val.lower() == 'cancel': return
            if not val:
                raise InvalidInputError("Student ID", "", "Student ID cannot be empty")
            if val.upper() in manager.students:
                raise DuplicateStudentError(val.upper())
            student_id = validate_student_id(val)
            break
        except (InvalidInputError, DuplicateStudentError) as e:
            print(f"   [Error]: {e}")

    # 2. Student Name
    while True:
        try:
            val = input("Enter Full Name: ").strip()
            if val.lower() == 'cancel': return
            name = validate_name(val)
            break
        except InvalidInputError as e:
            print(f"   [Error]: {e}")

    # 3. Email with Regex Validation
    while True:
        try:
            val = input("Enter Email Address: ").strip()
            if val.lower() == 'cancel': return
            email = validate_email(val)
            break
        except InvalidEmailError as e:
            print(f"   [Regex Validation Failed]: {e}")

    # 4. Age
    while True:
        try:
            val = input("Enter Age (15-120): ").strip()
            if val.lower() == 'cancel': return
            age = validate_age(val)
            break
        except InvalidInputError as e:
            print(f"   [Input Error]: {e}")

    # 5. Course
    while True:
        try:
            val = input("Enter Course / Major: ").strip()
            if val.lower() == 'cancel': return
            course = validate_course(val)
            break
        except InvalidInputError as e:
            print(f"   [Input Error]: {e}")

    # 6. GPA
    while True:
        try:
            val = input("Enter GPA (0.0 to 4.0) [default: 0.0]: ").strip()
            if val.lower() == 'cancel': return
            gpa = validate_gpa(val if val else 0.0)
            break
        except InvalidInputError as e:
            print(f"   [Input Error]: {e}")

    try:
        new_student = manager.add_student(student_id, name, email, age, course, gpa)
        print(f"\n[SUCCESS] Student '{new_student.name}' (ID: {new_student.student_id}) added successfully!")
    except StudentRecordError as e:
        print(f"\n[ERROR] Failed to add student: {e}")


def cli_search_student(manager: StudentRecordManager):
    """Searches student by ID."""
    print("\n--- SEARCH STUDENT BY ID ---")
    query = input("Enter Student ID: ").strip()
    try:
        student = manager.get_student(query)
        print("\nStudent Record:")
        print("-" * 35)
        print(student)
        print("-" * 35)
    except StudentNotFoundError as e:
        print(f"[ERROR] {e}")


def cli_test_regex():
    """Standalone test for email regex validation."""
    print("\n--- TEST EMAIL REGEX VALIDATION ---")
    test_str = input("Enter an email string to test regex: ").strip()
    try:
        result = validate_email(test_str)
        print(f"[PASSED] '{result}' matches valid email pattern!")
    except InvalidEmailError as e:
        print(f"[FAILED] {e}")


def cli_save_file(manager: StudentRecordManager):
    """Saves records to disk."""
    print("\n--- SAVE DATA TO FILE ---")
    try:
        path = manager.save_to_file()
        print(f"[SUCCESS] Saved {len(manager.students)} records to:\n  {path}")
    except FileOperationError as e:
        print(f"[ERROR] {e}")


def cli_reload_file(manager: StudentRecordManager):
    """Reloads records from file."""
    print("\n--- READ / RELOAD DATA FROM FILE ---")
    try:
        count = manager.read_from_file()
        print(f"[SUCCESS] Loaded {count} records from '{manager.filename}'.")
    except FileOperationError as e:
        print(f"[ERROR] {e}")


def cli_delete_student(manager: StudentRecordManager):
    """Deletes student record."""
    print("\n--- DELETE STUDENT ---")
    val = input("Enter Student ID to delete: ").strip()
    try:
        del_stu = manager.delete_student(val)
        print(f"[SUCCESS] Student '{del_stu.name}' (ID: {del_stu.student_id}) deleted.")
    except StudentNotFoundError as e:
        print(f"[ERROR] {e}")


def main():
    """Main terminal loop."""
    print("=" * 65)
    print("            STUDENT RECORD MANAGEMENT SYSTEM            ")
    print("             Module 2 Assignment Submission             ")
    print("=" * 65)

    manager = StudentRecordManager("students.json")

    # Auto-load existing records on startup
    try:
        count = manager.read_from_file()
        if count > 0:
            print(f"[INFO] Auto-loaded {count} student records from 'students.json'.")
        else:
            print("[INFO] Starting with fresh session (students.json initialized).")
    except Exception as e:
        print(f"[WARNING] Could not load file: {e}")

    while True:
        print("\n" + "-" * 40)
        print("               MAIN MENU               ")
        print("-" * 40)
        print(" [1] Add Student")
        print(" [2] View All Students (Read Data)")
        print(" [3] Search Student by ID")
        print(" [4] Validate Email with Regex (Standalone Test)")
        print(" [5] Save Data to File")
        print(" [6] Reload Data from File")
        print(" [7] Delete Student Record")
        print(" [0] Exit Application")
        print("-" * 40)

        choice = input("Select an option (0-7): ").strip()

        try:
            if choice == "1":
                cli_add_student(manager)
            elif choice == "2":
                display_table(manager.get_all_students())
            elif choice == "3":
                cli_search_student(manager)
            elif choice == "4":
                cli_test_regex()
            elif choice == "5":
                cli_save_file(manager)
            elif choice == "6":
                cli_reload_file(manager)
            elif choice == "7":
                cli_delete_student(manager)
            elif choice == "0":
                if manager.students:
                    ans = input("\nSave changes before exit? (y/n) [default: y]: ").strip().lower()
                    if ans != "n":
                        manager.save_to_file()
                        print("[INFO] Changes saved.")
                print("\nGoodbye!\n")
                sys.exit(0)
            else:
                print("[WARNING] Invalid option. Enter a number between 0 and 7.")
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)
        except Exception as e:
            print(f"\n[ERROR] An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
