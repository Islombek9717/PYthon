
from dataclasses import dataclass, field
import random

def grade_from_mark(mark:int)->str:
    if mark >= 85:
        return "HD"
    if mark >= 75:
        return "D"
    if mark >= 65:
        return "C"
    if mark >= 50:
        return "P"
    return "F"

@dataclass
class Subject:
    id: str
    mark: int = field(default_factory=lambda: random.randint(25,100))
    grade: str = None

    def __post_init__(self):
        if self.grade is None:
            self.grade = grade_from_mark(self.mark)

    def to_display(self) -> str:
        return f"[ Subject::{self.id} -- mark = {self.mark} -- grade =  {self.grade} ]"
