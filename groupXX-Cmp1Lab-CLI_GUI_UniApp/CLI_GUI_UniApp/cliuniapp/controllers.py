
from .database import Database
from .student import Student
from .subject import Subject
from .utils import valid_email, valid_password
import sys

YELLOW = "\033[33m"
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"

def prompt(msg: str) -> str:
    return input(msg)

class UniversityApp:
    def __init__(self, db: Database):
        self.db = db

    def run(self):
        while True:
            choice = prompt("University System: (A)dmin, (S)tudent, or X : ").strip().upper()
            if choice == "A":
                AdminMenu(self.db).run()
            elif choice == "S":
                StudentMenu(self.db).run()
            elif choice == "X":
                print(YELLOW + "Thank You" + RESET)
                break
            else:
                print(RED + "Invalid option" + RESET)

class StudentMenu:
    def __init__(self, db: Database):
        self.db = db

    def run(self):
        while True:
            choice = prompt("        Student System (l/r/x): ").strip().lower()
            if choice == "r":
                print(GREEN + "Student Sign Up" + RESET)
                self.register()
            elif choice == "l":
                print(GREEN + "Student Sign In" + RESET)
                if self.login():
                    CourseMenu(self.db, self.current_student).run()
            elif choice == "x":
                return
            else:
                print(RED + "Invalid option" + RESET)

    def register(self):
        email = prompt("Email: ").strip()
        password = prompt("Password: ").strip()
        if not (valid_email(email) and valid_password(password)):
            print(RED + "Incorrect email or password format" + RESET)
            return
        print(GREEN + "email and password formats acceptable" + RESET)
        existing = self.db.get_by_email(email)
        if existing:
            print(RED + f"Student {existing.name} already exists" + RESET)
            return
        name = prompt("Name: ").strip()
        # Create and assign unique id
        all_ids = {s.id for s in self.db.all_students() if s.id}
        st = Student(name=name, email=email, password=password)
        st.ensure_id(all_ids)
        print(YELLOW + f"Enrolling Student {name}" + RESET)
        self.db.upsert(st)

    def login(self) -> bool:
        email = prompt("Email: ").strip()
        password = prompt("Password: ").strip()
        if not (valid_email(email) and valid_password(password)):
            print(RED + "Incorrect email or password format" + RESET)
            return False
        print(GREEN + "email and password formats acceptable" + RESET)
        st = self.db.get_by_email(email)
        if not st or st.password != password:
            print(RED + "Student does not exist" + RESET)
            return False
        self.current_student = st
        return True

class CourseMenu:
    def __init__(self, db: Database, student: Student):
        self.db = db
        self.student = student

    def run(self):
        while True:
            choice = prompt("        Student Course Menu (c/e/r/s/x): ").strip().lower()
            if choice == "c":
                print(YELLOW + "Updating Password" + RESET)
                p1 = prompt("New Password: ").strip()
                p2 = prompt("Confirm Password: ").strip()
                if p1 != p2:
                    print(RED + "Password does not match - try again" + RESET)
                    continue
                if not valid_password(p1):
                    print(RED + "Incorrect password format" + RESET)
                    continue
                self.student.change_password(p1)
                self.db.upsert(self.student)
            elif choice == "e":
                try:
                    sub = self.student.enrol()
                    print(YELLOW + f"Enrolling in Subject-{sub.id}" + RESET)
                    print(YELLOW + f"You are now enrolled in {len(self.student.subjects)} out of 4 subjects" + RESET)
                    self.db.upsert(self.student)
                except ValueError as e:
                    print(RED + str(e) + RESET)
            elif choice == "r":
                sid = prompt("Remove Subject by ID: ").strip()
                if self.student.remove_subject(sid):
                    print(YELLOW + f"Droping Subject-{sid}" + RESET)
                    print(YELLOW + f"You are now enrolled in {len(self.student.subjects)} out of 4 subjects" + RESET)
                    self.db.upsert(self.student)
                else:
                    print(RED + "Subject not found" + RESET)
            elif choice == "s":
                print(YELLOW + f"Showing {len(self.student.subjects)} subjects" + RESET)
                for s in self.student.subjects:
                    print(" " + s.to_display())
            elif choice == "x":
                return
            else:
                print(RED + "Invalid option" + RESET)

class AdminMenu:
    def __init__(self, db: Database):
        self.db = db

    def run(self):
        while True:
            choice = prompt("    Admin System (c/g/p/r/s/x): ").strip().lower()
            if choice == "s":
                self.show_students()
            elif choice == "g":
                self.group_by_grade()
            elif choice == "p":
                self.partition_pass_fail()
            elif choice == "r":
                sid = prompt("Remove by ID: ").strip()
                if self.db.remove_by_id(sid):
                    print(YELLOW + f"Removing Student {sid} Account" + RESET)
                else:
                    print(RED + f"Student {sid} does not exist" + RESET)
            elif choice == "c":
                print(YELLOW + "Clearing students database" + RESET)
                ans = prompt("Are you sure you want to clear the database (Y)ES/(N)O: ").strip().upper()
                if ans == "Y":
                    self.db.clear()
                    print(YELLOW + "Students data cleared" + RESET)
            elif choice == "x":
                return
            else:
                print(RED + "Invalid option" + RESET)

    def show_students(self):
        studs = self.db.all_students()
        if not studs:
            print("Student List")
            print("        < Nothing to Display >")
            return
        print("Student List")
        for s in studs:
            print(f"{s.name} :: {s.id} --> Email: {s.email}")

    def group_by_grade(self):
        studs = self.db.all_students()
        if not studs:
            print("Grade Grouping")
            print("        < Nothing to Display >")
            return
        groups = {}
        for s in studs:
            g = s.overall_grade()
            groups.setdefault(g, []).append(f"{s.name} :: {s.id} --> GRADE: {g} - MARK: {s.average_mark()}")
        print("Grade Grouping")
        for g, items in sorted(groups.items()):
            print(f"{g} --> {items}")

    def partition_pass_fail(self):
        studs = self.db.all_students()
        if not studs:
            print("PASS/FAIL Partition")
            print("        FAIL --> []")
            print("        PASS --> []")
            return
        fail = []
        pas = []
        for s in studs:
            (pas if s.average_mark() >= 50 else fail).append(f"{s.name} :: {s.id} --> GRADE: {s.overall_grade()} - MARK: {s.average_mark()}")
        print("PASS/FAIL Partition")
        print(f"FAIL --> {fail}")
        print(f"PASS --> {pas}")
