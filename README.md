# 🎓 Student Record Manager (Module 2 Assignment)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests Status](https://img.shields.io/badge/tests-12%2F12%20passing-brightgreen.svg)]()

A robust, menu-driven Python application for managing student academic records. Built with object-oriented design, defensive exception handling, regex validation, and persistent file storage.

---

## 📋 Table of Contents
- [Assignment Features](#-assignment-features)
- [Project Architecture](#-project-architecture)
- [Requirements](#-requirements)
- [Getting Started](#-getting-started)
- [How It Works](#-how-it-works)
  - [1. Regex Email Validation](#1-regex-email-validation)
  - [2. Custom Exception Hierarchy](#2-custom-exception-hierarchy)
  - [3. File Storage & Persistence](#3-file-storage--persistence)
- [Running Unit Tests](#-running-unit-tests)
- [Deploying to GitHub](#-deploying-to-github)
- [License](#-license)

---

## ✨ Assignment Features

| Feature | Description | Implementation File |
| :--- | :--- | :--- |
| **Add Student** | Add new students with ID, Name, Email, and Course | [`student.py`](student.py), [`manager.py`](manager.py) |
| **Validate Email using Regex** | Strict RFC-compliant regex pattern verifying valid email syntax, domain, and TLD | [`student.py`](student.py) |
| **Save Data to File** | Persists student records to structured JSON file on disk | [`storage.py`](storage.py) |
| **Read Student Data** | Reads, parses, and displays student records in clean formatted tables | [`storage.py`](storage.py), [`main.py`](main.py) |
| **Exception Handling** | Custom exception hierarchy handling invalid inputs, file corruption, duplicates, and missing records | [`exceptions.py`](exceptions.py) |

---

## 📂 Project Architecture

```text
student_record_manager/
│
├── data/
│   └── students.json              # Persistent JSON database
│
├── tests/
│   ├── __init__.py
│   └── test_student_manager.py    # Unit tests for validation, CRUD, and errors
│
├── exceptions.py                  # Custom domain & input exception classes
├── student.py                     # Student entity & regex validation logic
├── storage.py                     # File I/O persistence handler
├── manager.py                     # Business logic and record manager controller
├── main.py                        # Interactive CLI application
├── requirements.txt               # Optional development dependencies
├── .gitignore                     # Standard Python gitignore
└── README.md                      # Documentation & GitHub guide
```

---

## ⚙️ Requirements
- **Python**: Version 3.8 or higher.
- Standard Library only (no external packages required to run the core application).

---

## 🚀 Getting Started

### 1. Clone or Navigate to the Repository
```bash
cd student_record_manager
```

### 2. Run the Application
On **Windows (PowerShell / Command Prompt)**:
```powershell
py main.py
```
*(Or `python main.py` if python is in your PATH)*

On **macOS / Linux**:
```bash
python3 main.py
```

### 3. Example CLI Menu
```text
==================================================
      STUDENT RECORD MANAGER (MODULE 2)       
==================================================
 1. Add Student (with Regex Email Validation)
 2. View All Students
 3. Search Student by ID / Name / Email
 4. Save Records to File
 5. Read / Reload Student Data from File
 6. Delete a Student Record
 7. Exit
--------------------------------------------------
Enter choice (1-7):
```

---

## 🔍 How It Works

### 1. Regex Email Validation
The email validation uses regular expressions to enforce valid email formats:
```python
EMAIL_REGEX_PATTERN = re.compile(
    r"^[a-zA-Z0-9]+([._%+-][a-zA-Z0-9]+)*@[a-zA-Z0-9]+([.-][a-zA-Z0-9]+)*\.[a-zA-Z]{2,}$"
)
```
- **Rules Enforced**:
  - Alphanumeric start and end in local-part.
  - Prohibits consecutive dots (`user..name@domain.com` is rejected).
  - Validates domain name and guarantees a top-level domain (TLD) of at least 2 characters.
  - Raises `InvalidEmailError` when invalid.

### 2. Custom Exception Hierarchy
Located in [`exceptions.py`](exceptions.py):
- `StudentRecordError` (Base class)
  - `InvalidEmailError` — Raised on malformed emails.
  - `InvalidInputError` — Raised on empty fields, invalid names, or bad IDs.
  - `DuplicateStudentError` — Raised when adding a student whose ID or Email already exists.
  - `StudentNotFoundError` — Raised when querying an unregistered student.
  - `StorageError` — Raised during file permission or corruption issues.

### 3. File Storage & Persistence
- Automatically creates enclosing `data/` directory.
- Handles `json.JSONDecodeError` (corrupt file detection), `PermissionError`, and `FileNotFoundError`.
- Records are serialized to and loaded from `data/students.json`.

---

## 🧪 Running Unit Tests

The test suite covers regex verification, model constraints, duplicate detection, and file persistence.

Run tests using the built-in `unittest` runner:
```powershell
# Windows
py -m unittest discover -s tests -p "test_*.py"

# Linux / macOS
python3 -m unittest discover -s tests -p "test_*.py"
```

Expected output:
```text
............
----------------------------------------------------------------------
Ran 12 tests in 0.013s

OK
```

---

## 🌐 Deploying to GitHub

Follow these steps to upload this project to your GitHub account:

### Option A: Using Git CLI (Recommended)
1. Open terminal inside the project directory:
   ```bash
   cd student_record_manager
   ```
2. Initialize local Git repository:
   ```bash
   git init
   git branch -M main
   ```
3. Stage and commit files:
   ```bash
   git add .
   git commit -m "Initial commit: Student Record Manager for Module 2"
   ```
4. Create a new repository on [GitHub](https://github.com/new) named `student-record-manager` (do **not** check "Initialize with README").
5. Link your local repository to GitHub and push:
   ```bash
   git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/student-record-manager.git
   git push -u origin main
   ```

### Option B: Upload via GitHub Web Interface
1. Create a new repository on [GitHub](https://github.com/new).
2. Click on **"uploading an existing file"**.
3. Drag and drop all project files into the browser.
4. Add a commit message (`Initial commit: Student Record Manager`) and click **Commit changes**.

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).
