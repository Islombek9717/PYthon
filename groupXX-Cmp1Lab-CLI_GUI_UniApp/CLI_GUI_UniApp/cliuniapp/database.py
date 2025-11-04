
import os, pickle
from typing import List, Optional
from .student import Student

DATA_FILE = "students.data"

class Database:
    def __init__(self, path:str="."):
        self.base = path
        self.file = os.path.join(self.base, DATA_FILE)
        if not os.path.exists(self.file):
            # ensure file exists
            with open(self.file,"wb") as f:
                pickle.dump([], f)

    def _read_all(self) -> List[Student]:
        try:
            with open(self.file,"rb") as f:
                return pickle.load(f)
        except Exception:
            # reset corrupt file
            with open(self.file,"wb") as f:
                pickle.dump([], f)
            return []

    def _write_all(self, students: List[Student]):
        with open(self.file,"wb") as f:
            pickle.dump(students, f)

    def all_students(self) -> List[Student]:
        return self._read_all()

    def get_by_email(self, email: str) -> Optional[Student]:
        for s in self._read_all():
            if s.email == email:
                return s
        return None

    def upsert(self, student: Student):
        students = self._read_all()
        for i, s in enumerate(students):
            if s.email == student.email or (student.id and s.id == student.id):
                students[i] = student
                self._write_all(students)
                return
        students.append(student)
        self._write_all(students)

    def remove_by_id(self, sid: str) -> bool:
        students = self._read_all()
        new = [s for s in students if s.id != sid]
        changed = len(new) != len(students)
        if changed:
            self._write_all(new)
        return changed

    def clear(self):
        self._write_all([])
