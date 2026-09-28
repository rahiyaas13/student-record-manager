"""
Validation Utilities with Regular Expressions and Exception Handling
"""

import re
from exceptions import InvalidEmailError, InvalidInputError

# Regular expression pattern for RFC 5322-compliant email validation
EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}$"
)

# Pattern for alphanumeric Student ID (e.g. STU101, S001, 1001)
STUDENT_ID_REGEX = re.compile(r"^[a-zA-Z0-9_-]{2,20}$")

# Pattern for human names (alphabets, spaces, apostrophes, hyphens)
NAME_REGEX = re.compile(r"^[A-Za-z\s.'-]{2,60}$")


def validate_email(email: str) -> str:
    """
    Validates email format using regular expressions.
    Raises InvalidEmailError if invalid.
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
            "Email must match format 'username@domain.extension' (e.g. student@university.edu)"
        )

    return cleaned.lower()


def validate_student_id(student_id: str) -> str:
    """
    Validates student ID format.
    Raises InvalidInputError if invalid.
    """
    if not isinstance(student_id, str):
        raise InvalidInputError("Student ID", str(student_id), "ID must be a string")

    cleaned = student_id.strip().upper()
    if not cleaned:
        raise InvalidInputError("Student ID", "", "Student ID cannot be empty")

    if not STUDENT_ID_REGEX.match(cleaned):
        raise InvalidInputError(
            "Student ID",
            cleaned,
            "ID must be 2-20 characters long and contain only letters, numbers, or dashes"
        )

    return cleaned


def validate_name(name: str) -> str:
    """
    Validates student name format.
    Raises InvalidInputError if invalid.
    """
    if not isinstance(name, str):
        raise InvalidInputError("Name", str(name), "Name must be a string")

    cleaned = name.strip()
    if not cleaned:
        raise InvalidInputError("Name", "", "Name cannot be empty")

    if not NAME_REGEX.match(cleaned):
        raise InvalidInputError(
            "Name",
            cleaned,
            "Name must be 2-60 characters and contain only letters, spaces, or hyphens"
        )

    return cleaned.title()


def validate_age(age_input: any) -> int:
    """
    Validates student age (must be an integer between 15 and 120).
    Raises InvalidInputError if invalid.
    """
    try:
        age = int(str(age_input).strip())
    except (ValueError, TypeError):
        raise InvalidInputError("Age", str(age_input), "Age must be a valid whole number")

    if age < 15 or age > 120:
        raise InvalidInputError("Age", str(age), "Age must be between 15 and 120")

    return age


def validate_gpa(gpa_input: any) -> float:
    """
    Validates GPA (must be a float between 0.0 and 4.0).
    Raises InvalidInputError if invalid.
    """
    try:
        gpa = float(str(gpa_input).strip())
    except (ValueError, TypeError):
        raise InvalidInputError("GPA", str(gpa_input), "GPA must be a valid decimal number")

    if gpa < 0.0 or gpa > 4.0:
        raise InvalidInputError("GPA", str(gpa), "GPA must be between 0.00 and 4.00")

    return round(gpa, 2)


def validate_course(course: str) -> str:
    """
    Validates student enrolled course/major.
    Raises InvalidInputError if invalid.
    """
    if not isinstance(course, str):
        raise InvalidInputError("Course", str(course), "Course must be a string")

    cleaned = course.strip()
    if not cleaned:
        raise InvalidInputError("Course", "", "Course cannot be empty")

    if len(cleaned) < 2 or len(cleaned) > 50:
        raise InvalidInputError("Course", cleaned, "Course must be between 2 and 50 characters")

    return cleaned.title()
