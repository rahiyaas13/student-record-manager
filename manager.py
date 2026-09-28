"""
Student Record Manager business logic controller.
Coordinates CRUD operations, data storage, and domain constraints.
"""

from typing import List, Dict, Optional, Any
from student import Student
from storage import FileStorage, DEFAULT_DATA_FILE
from exceptions import DuplicateStudentError, StudentNotFoundError, StorageError

class StudentRecordManager:
    """
    Manages collection of student records and provides operations for adding,
    viewing, searching, saving, and loading student data.
    """
    def __init__(self, storage_file: str = DEFAULT_DATA_FILE):
        self.storage = FileStorage(storage_file)
        self.students: Dict[str, Student] = {}
        # Automatically load existing records if file exists
        self.load_records(suppress_error=True)

    @property
    def total_students(self) -> int:
        """Returns the total number of currently stored students."""
        return len(self.students)

    def add_student(
        self,
        student_id: str,
        name: str,
        email: str,
        age_or_course: Any = None,
        course: str = "General",
        gpa: float = 0.0,
        age: Optional[int] = None,
        **kwargs: Any,
    ) -> Student:
        """
        Validates and adds a new student to the in-memory record store.
        Flexible signature supporting positional/keyword arguments for both:
        - (id, name, email, course)
        - (id, name, email, age, course, gpa)
        """
        # Determine actual age and course from parameters
        actual_course = course
        if age is not None:
            actual_age = age
        elif age_or_course is not None:
            if isinstance(age_or_course, int):
                actual_age = age_or_course
            elif isinstance(age_or_course, str) and age_or_course.strip().lstrip("-+").isdigit():
                actual_age = int(age_or_course.strip())
            elif isinstance(age_or_course, str):
                actual_course = age_or_course
                actual_age = kwargs.get("age", 18)
            else:
                actual_age = age_or_course
        else:
            actual_age = kwargs.get("age", 18)

        actual_gpa = kwargs.get("gpa", gpa)

        new_student = Student(
            student_id=student_id,
            name=name,
            email=email,
            age=actual_age,
            course=actual_course,
            gpa=actual_gpa,
        )

        # Check for duplicate ID
        if new_student.student_id in self.students:
            raise DuplicateStudentError(new_student.student_id)

        # Check for duplicate Email
        for existing in self.students.values():
            if existing.email == new_student.email:
                raise DuplicateStudentError(f"Email '{new_student.email}' is already registered to ID {existing.student_id}")

        self.students[new_student.student_id] = new_student
        return new_student

    def get_student(self, student_id: str) -> Student:
        """
        Retrieves a student by ID.
        
        Raises:
            StudentNotFoundError: If no student matches the ID.
        """
        clean_id = student_id.strip().upper()
        if clean_id not in self.students:
            raise StudentNotFoundError(clean_id)
        return self.students[clean_id]

    def search_students(self, keyword: str) -> List[Student]:
        """
        Searches students by ID, Name, Email, or Course (case-insensitive substring match).
        """
        term = keyword.strip().lower()
        if not term:
            return list(self.students.values())

        return [
            s for s in self.students.values()
            if term in s.student_id.lower() or term in s.name.lower() or term in s.email.lower() or term in s.course.lower()
        ]

    def get_all_students(self) -> List[Student]:
        """Returns a list of all currently loaded students."""
        return list(self.students.values())

    def delete_student(self, student_id: str) -> Student:
        """
        Deletes a student by ID.
        
        Raises:
            StudentNotFoundError: If student is not found.
        """
        clean_id = student_id.strip().upper()
        if clean_id not in self.students:
            raise StudentNotFoundError(clean_id)
        return self.students.pop(clean_id)

    def save_records(self) -> str:
        """
        Persists all in-memory student records to the configured file.
        
        Returns:
            str: Path to the saved file.
            
        Raises:
            StorageError: If file saving fails.
        """
        serialized = [student.to_dict() for student in self.students.values()]
        self.storage.save_records(serialized)
        return self.storage.file_path

    def load_records(self, suppress_error: bool = False) -> int:
        """
        Loads student records from file and populates in-memory dictionary.
        
        Args:
            suppress_error (bool): If True, ignores missing file and doesn't raise exception.
            
        Returns:
            int: Number of records loaded.
            
        Raises:
            StorageError: If file cannot be read or contains corrupted data.
        """
        try:
            records = self.storage.load_records()
            self.students.clear()
            for record in records:
                student = Student.from_dict(record)
                self.students[student.student_id] = student
            return len(self.students)
        except StorageError:
            if suppress_error:
                return 0
            raise
