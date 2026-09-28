"""
Command-Line Interface (CLI) for Student Record Manager.
Provides an interactive menu with robust exception handling and input validation.
"""

import sys
from manager import StudentRecordManager
from exceptions import (
    InvalidEmailError,
    InvalidInputError,
    DuplicateStudentError,
    StudentNotFoundError,
    StorageError,
    StudentRecordError,
)

def print_header(title: str) -> None:
    """Prints a styled section header."""
    print("\n" + "=" * 50)
    print(f" {title.upper()} ".center(50, "="))
    print("=" * 50)

def display_students_table(students: list) -> None:
    """Prints students formatted as a clean table."""
    if not students:
        print("\n[!] No student records found.")
        return

    print("\n" + "-" * 75)
    print(f"{'ID':<10} | {'NAME':<20} | {'EMAIL':<25} | {'COURSE':<15}")
    print("-" * 75)
    for s in students:
        print(f"{s.student_id:<10} | {s.name:<20} | {s.email:<25} | {s.course:<15}")
    print("-" * 75)
    print(f"Total Records: {len(students)}")

def handle_add_student(manager: StudentRecordManager) -> None:
    """Guides user to add a new student with immediate validation error feedback."""
    print_header("Add New Student")
    print("Enter the student details below. Invalid inputs will prompt error messages.")

    try:
        student_id = input("Enter Student ID (e.g. STU101, 1001): ").strip()
        name = input("Enter Student Full Name: ").strip()
        email = input("Enter Student Email (e.g. name@domain.com): ").strip()
        course = input("Enter Course / Department [Default: General]: ").strip()

        new_student = manager.add_student(
            student_id=student_id,
            name=name,
            email=email,
            course=course if course else "General"
        )
        print(f"\n[+] Success: Student '{new_student.name}' (ID: {new_student.student_id}) added successfully!")

    except (InvalidEmailError, InvalidInputError, DuplicateStudentError) as err:
        print(f"\n[-] Validation Error: {err}")
    except Exception as err:
        print(f"\n[-] Unexpected Error: {err}")

def handle_view_students(manager: StudentRecordManager) -> None:
    """Displays all current students in a tabular view."""
    print_header("All Student Records")
    students = manager.get_all_students()
    display_students_table(students)

def handle_search_student(manager: StudentRecordManager) -> None:
    """Searches for students by ID, Name, or Email."""
    print_header("Search Student Records")
    query = input("Enter Student ID, Name, or Email to search: ").strip()
    
    if not query:
        print("[-] Search query cannot be empty.")
        return

    results = manager.search_students(query)
    display_students_table(results)

def handle_delete_student(manager: StudentRecordManager) -> None:
    """Removes a student by their ID."""
    print_header("Delete Student Record")
    student_id = input("Enter the ID of the student to remove: ").strip()
    try:
        deleted = manager.delete_student(student_id)
        print(f"\n[+] Success: Student '{deleted.name}' (ID: {deleted.student_id}) has been removed.")
    except StudentNotFoundError as err:
        print(f"\n[-] Not Found: {err}")
    except Exception as err:
        print(f"\n[-] Error: {err}")

def handle_save_to_file(manager: StudentRecordManager) -> None:
    """Persists records to disk file."""
    print_header("Save Data to File")
    try:
        count = manager.save_records()
        print(f"\n[+] Successfully saved {count} student record(s) to '{manager.storage.file_path}'.")
    except StorageError as err:
        print(f"\n[-] File Save Error: {err}")

def handle_load_from_file(manager: StudentRecordManager) -> None:
    """Reads records from disk file."""
    print_header("Read Student Data from File")
    try:
        count = manager.load_records()
        print(f"\n[+] Successfully loaded {count} student record(s) from '{manager.storage.file_path}'.")
    except StorageError as err:
        print(f"\n[-] File Read Error: {err}")

def show_menu() -> None:
    """Displays the main CLI navigation menu."""
    print("\n" + "=" * 50)
    print("      STUDENT RECORD MANAGER (MODULE 2)       ")
    print("=" * 50)
    print(" 1. Add Student (with Regex Email Validation)")
    print(" 2. View All Students")
    print(" 3. Search Student by ID / Name / Email")
    print(" 4. Save Records to File")
    print(" 5. Read / Reload Student Data from File")
    print(" 6. Delete a Student Record")
    print(" 7. Exit")
    print("-" * 50)

def main() -> None:
    """Main program execution loop with defensive error handling."""
    manager = StudentRecordManager()
    
    print("\nWelcome to Student Record Manager!")
    print(f"Data file initialized: {manager.storage.file_path}")
    if manager.students:
        print(f"Loaded {len(manager.students)} existing record(s) from storage.")

    while True:
        try:
            show_menu()
            choice = input("Enter choice (1-7): ").strip()

            if choice == "1":
                handle_add_student(manager)
            elif choice == "2":
                handle_view_students(manager)
            elif choice == "3":
                handle_search_student(manager)
            elif choice == "4":
                handle_save_to_file(manager)
            elif choice == "5":
                handle_load_from_file(manager)
            elif choice == "6":
                handle_delete_student(manager)
            elif choice == "7":
                # Prompt to save if there are unsaved changes
                save_prompt = input("\nSave changes before exiting? (y/n) [default: y]: ").strip().lower()
                if save_prompt in ("", "y", "yes"):
                    try:
                        manager.save_records()
                        print("[+] Changes saved successfully.")
                    except StorageError as err:
                        print(f"[-] Failed to save changes: {err}")
                print("\nThank you for using Student Record Manager. Goodbye!\n")
                sys.exit(0)
            else:
                print("\n[-] Invalid choice. Please choose a number from 1 to 7.")

        except KeyboardInterrupt:
            print("\n\nOperation interrupted by user. Exiting safely...")
            sys.exit(0)
        except EOFError:
            print("\n\nInput stream closed. Exiting safely...")
            sys.exit(0)
        except Exception as err:
            print(f"\n[-] An unexpected error occurred: {err}")

if __name__ == "__main__":
    main()
