
from dataclasses import dataclass, field
from typing import List, Optional
from .subject import Subject, grade_from_mark
import random

def _generate_student_id(existing:set[str])->str:
    # 6-digit zero-padded unique id
    while True:
        n = random.randint(1, 999999)
        sid = f"{n:06d}"
        if sid not in existing:
            return sid

def _generate_subject_id(existing:set[str])->str:
    while True:
        n = random.randint(1, 999)
        sid = f"{n:03d}"
        if sid not in existing:
            return sid

@dataclass
class Student:
    name: str
    email: str
    password: str
    id: str = None
    subjects: List[Subject] = field(default_factory=list)

    def ensure_id(self, existing_ids:set[str]):
        if self.id is None:
            self.id = _generate_student_id(existing_ids)

    def enrol(self, subject_id: Optional[str]=None) -> Subject:
        if len(self.subjects) >= 4:
            raise ValueError("Students are allowed to enrol in 4 subjects only")
        existing_ids = {s.id for s in self.subjects}
        sid = subject_id or _generate_subject_id(existing_ids)
        sub = Subject(id=sid)
        self.subjects.append(sub)
        return sub

    def remove_subject(self, subject_id: str) -> bool:
        for i, s in enumerate(self.subjects):
            if s.id == subject_id:
                self.subjects.pop(i)
                return True
        return False

    def change_password(self, new_password: str):
        self.password = new_password

    def average_mark(self) -> float:
        if not self.subjects:
            return 0.0
        return round(sum(s.mark for s in self.subjects) / len(self.subjects), 2)

    def overall_grade(self) -> str:
        return grade_from_mark(int(self.average_mark()))
