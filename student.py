"""
Student Model and Data Representation.
Encapsulates individual student records with validated fields.
"""

from typing import Dict, Any
from validator import (
    validate_email,
    validate_student_id,
    validate_name,
    validate_age,
    validate_gpa,
    validate_course,
)
from exceptions import InvalidInputError

class Student:
    """
    Represents an individual student record.
    """
    def __init__(
        self,
        student_id: str,
        name: str,
        email: str,
        age: int = 18,
        course: str = "General",
        gpa: float = 0.0,
    ):
        self.student_id = validate_student_id(student_id)
        self.name = validate_name(name)
        self.email = validate_email(email)
        self.age = validate_age(age)
        self.course = validate_course(course)
        self.gpa = validate_gpa(gpa)

    def to_dict(self) -> Dict[str, Any]:
        """Convert student record to dictionary representation for JSON persistence."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "course": self.course,
            "gpa": self.gpa,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Student":
        """Reconstruct student instance from dictionary data."""
        required_keys = ["student_id", "name", "email"]
        for key in required_keys:
            if key not in data:
                raise InvalidInputError(key, "", f"Missing required student field '{key}' in data source.")

        return cls(
            student_id=str(data["student_id"]),
            name=str(data["name"]),
            email=str(data["email"]),
            age=int(data.get("age", 18)),
            course=str(data.get("course", "General")),
            gpa=float(data.get("gpa", 0.0)),
        )

    def __repr__(self) -> str:
        return (
            f"<Student id={self.student_id} name='{self.name}' "
            f"email='{self.email}' age={self.age} course='{self.course}' gpa={self.gpa}>"
        )

    def __str__(self) -> str:
        return (
            f"ID: {self.student_id:<8} | Name: {self.name:<20} | Email: {self.email:<26} | "
            f"Age: {self.age:<3} | Course: {self.course:<16} | GPA: {self.gpa:.2f}"
        )
