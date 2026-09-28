"""
Custom Exception Classes for Student Record Manager.
Handles domain validation, input formatting errors, and file I/O operations.
"""

from typing import Any

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
    def __init__(self, field_name: str, value: Any = "", message: str = "Invalid input"):
        self.field_name = field_name
        self.value = value
        if value != "":
            self.message = f"{message} for '{field_name}': '{value}'"
        else:
            self.message = f"{message} for '{field_name}'"
        super().__init__(self.message)

class DuplicateStudentError(StudentRecordError):
    """Raised when attempting to add a student with an existing ID."""
    def __init__(self, student_id: str):
        self.student_id = student_id
        super().__init__(f"Student with ID '{student_id}' already exists.")

class StudentNotFoundError(StudentRecordError):
    """Raised when a requested student is not found."""
    def __init__(self, identifier: str):
        self.identifier = identifier
        super().__init__(f"Student with ID/Name '{identifier}' was not found.")

class StorageError(StudentRecordError):
    """Raised when file save/load operations encounter an issue."""
    pass

# Alias for backwards compatibility with tests
FileOperationError = StorageError
