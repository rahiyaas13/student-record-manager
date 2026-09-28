"""
Storage Layer for Student Record Manager.
Handles saving student records to file and reading records from file,
with defensive exception handling for file system and JSON parsing issues.
"""

import json
import os
from typing import List, Dict, Any
from exceptions import StorageError

DEFAULT_DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "students.json")

class FileStorage:
    """
    Manages persistence of student data into JSON files.
    """
    def __init__(self, file_path: str = DEFAULT_DATA_FILE):
        self.file_path = file_path
        self._ensure_directory_exists()

    def _ensure_directory_exists(self) -> None:
        """Ensures that the directory enclosing the storage file exists."""
        directory = os.path.dirname(self.file_path)
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
            except OSError as exc:
                raise StorageError(f"Failed to create directory '{directory}': {exc}") from exc

    def save_records(self, records: List[Dict[str, Any]]) -> None:
        """
        Saves a list of student dictionary records to the file.
        
        Args:
            records (List[Dict[str, Any]]): List of student dictionaries.
            
        Raises:
            StorageError: If there's an OS or write permission failure.
        """
        self._ensure_directory_exists()
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(records, file, indent=4)
        except PermissionError as exc:
            raise StorageError(f"Permission denied when writing to '{self.file_path}'.") from exc
        except OSError as exc:
            raise StorageError(f"Operating system error writing to '{self.file_path}': {exc}") from exc
        except Exception as exc:
            raise StorageError(f"Unexpected error while saving data: {exc}") from exc

    def load_records(self) -> List[Dict[str, Any]]:
        """
        Reads student records from the JSON file.
        
        Returns:
            List[Dict[str, Any]]: List of parsed student dictionaries.
            
        Raises:
            StorageError: If the file is corrupted or cannot be read.
        """
        if not os.path.exists(self.file_path):
            # If the file does not exist yet, return an empty list gracefully
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                if not isinstance(data, list):
                    raise StorageError(f"Data file '{self.file_path}' does not contain a valid list of records.")
                return data
        except json.JSONDecodeError as exc:
            raise StorageError(f"File '{self.file_path}' contains corrupted or invalid JSON: {exc}") from exc
        except PermissionError as exc:
            raise StorageError(f"Permission denied when reading from '{self.file_path}'.") from exc
        except OSError as exc:
            raise StorageError(f"Operating system error reading '{self.file_path}': {exc}") from exc
        except Exception as exc:
            raise StorageError(f"Unexpected error while loading data: {exc}") from exc
