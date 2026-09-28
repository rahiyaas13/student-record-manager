"""
Automated Unit Tests for Student Record Manager
Verifies all 5 required Module 2 features:
1. Add Student
2. Validate Email using Regex
3. Save Data to File
4. Read Student Data
5. Handle Invalid Input using Exceptions
"""

import os
import unittest
import tempfile
import json
from student import Student
from manager import StudentRecordManager
from validator import validate_email, validate_age, validate_gpa, validate_student_id
from exceptions import (
    InvalidEmailError,
    InvalidInputError,
    DuplicateStudentError,
    StudentNotFoundError,
    FileOperationError,
)


class TestStudentRecordManager(unittest.TestCase):
    """Test suite for the Student Record Manager assignment."""

    def setUp(self):
        """Create a temporary file for test isolation."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_file.close()
        self.manager = StudentRecordManager(self.temp_file.name)

    def tearDown(self):
        """Clean up the temporary file after each test."""
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    # ---------------------------------------------------------
    # FEATURE 1: Add Student
    # ---------------------------------------------------------
    def test_add_student_success(self):
        """Test adding a valid student successfully."""
        student = self.manager.add_student(
            student_id="STU101",
            name="Alice Smith",
            email="alice@example.com",
            age=20,
            course="Computer Science",
            gpa=3.85,
        )
        self.assertEqual(student.student_id, "STU101")
        self.assertEqual(student.name, "Alice Smith")
        self.assertEqual(student.email, "alice@example.com")
        self.assertEqual(student.age, 20)
        self.assertEqual(student.course, "Computer Science")
        self.assertEqual(student.gpa, 3.85)
        self.assertEqual(self.manager.total_students, 1)

    # ---------------------------------------------------------
    # FEATURE 2: Validate Email using Regex
    # ---------------------------------------------------------
    def test_regex_valid_emails(self):
        """Test regex acceptance of standard and complex valid emails."""
        valid_emails = [
            "student@university.edu",
            "john.doe@sub.domain.org",
            "first_last+tag@mail.co.uk",
            "alex123@gmail.com",
        ]
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(validate_email(email))

    def test_regex_invalid_emails(self):
        """Test regex rejection with InvalidEmailError for malformed emails."""
        invalid_emails = [
            "plainaddress",
            "@missingusername.com",
            "missingdomain@.com",
            "missingat.domain.com",
            "two@@at.com",
            "spaces in@email.com",
            "consecutive..dots@domain.com",
            "nodot@domain",
            "",
        ]
        for bad_email in invalid_emails:
            with self.subTest(bad_email=bad_email):
                with self.assertRaises(InvalidEmailError):
                    validate_email(bad_email)

    # ---------------------------------------------------------
    # FEATURE 3: Save Data to File
    # ---------------------------------------------------------
    def test_save_data_to_file(self):
        """Test saving records to a file."""
        self.manager.add_student("S1", "Bob Brown", "bob@school.edu", 21, "Physics", 3.5)
        self.manager.add_student("S2", "Carol White", "carol@school.edu", 22, "Chemistry", 3.9)

        saved_path = self.manager.save_records()
        self.assertTrue(os.path.exists(saved_path))

        with open(saved_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]["student_id"], "S1")
            self.assertEqual(data[1]["student_id"], "S2")

    # ---------------------------------------------------------
    # FEATURE 4: Read Student Data
    # ---------------------------------------------------------
    def test_read_student_data_from_file(self):
        """Test loading and reading records from a saved file."""
        self.manager.add_student("STU99", "David Lee", "david@tech.ac.in", 23, "Robotics", 3.7)
        self.manager.save_records()

        # Create a new manager instance pointing to the same file
        new_manager = StudentRecordManager(self.temp_file.name)
        count = new_manager.load_records()

        self.assertEqual(count, 1)
        student = new_manager.get_student("STU99")
        self.assertEqual(student.name, "David Lee")
        self.assertEqual(student.course, "Robotics")

    # ---------------------------------------------------------
    # FEATURE 5: Handle Invalid Input using Exceptions
    # ---------------------------------------------------------
    def test_duplicate_student_id_exception(self):
        """Test DuplicateStudentError is raised for duplicate IDs."""
        self.manager.add_student("ID001", "Emma", "emma@domain.com", 19, "Biology")
        with self.assertRaises(DuplicateStudentError):
            self.manager.add_student("ID001", "Another Emma", "emma2@domain.com", 20, "Biology")

    def test_student_not_found_exception(self):
        """Test StudentNotFoundError is raised when retrieving a non-existent student."""
        with self.assertRaises(StudentNotFoundError):
            self.manager.get_student("NON_EXISTENT_ID")

    def test_invalid_age_exception(self):
        """Test InvalidInputError is raised for negative or out-of-range age."""
        with self.assertRaises(InvalidInputError):
            validate_age(-5)
        with self.assertRaises(InvalidInputError):
            validate_age(150)
        with self.assertRaises(InvalidInputError):
            validate_age("not_a_number")

    def test_invalid_gpa_exception(self):
        """Test InvalidInputError is raised for out-of-bounds GPA."""
        with self.assertRaises(InvalidInputError):
            validate_gpa(4.5)
        with self.assertRaises(InvalidInputError):
            validate_gpa(-0.1)
        with self.assertRaises(InvalidInputError):
            validate_gpa("not_a_float")

    def test_invalid_id_exception(self):
        """Test InvalidInputError is raised for empty or invalid ID format."""
        with self.assertRaises(InvalidInputError):
            validate_student_id("")
        with self.assertRaises(InvalidInputError):
            validate_student_id("a")  # too short


if __name__ == "__main__":
    unittest.main()
