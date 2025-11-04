
# CLIUniApp & GUIUniApp (Python)

University application with CLI and optional GUI that manages students and their subject enrolment.
All student data persists to `students.data` (pickle).

## Project Overview
- **CLIUniApp**: Implements University, Student, Admin, and Subject Enrolment systems.
- **GUIUniApp**: Optional Tkinter app for students: Login → Enrolment (enrol/remove/list).
- **Models**: `Student`, `Subject`, `Database`
- **Controllers**: Text menus; I/O closely follows the provided sample.

## System Requirements
- Python 3.10+
- No external dependencies

## Installation & Setup
```bash
python -V   # ensure Python 3.10+
```

## How to Run
### CLI
```bash
python main.py
```

### GUI (challenge task)
```bash
python guiuniapp.py
```

## Configuration
- Data file path: `students.data` created in project root on first run.

## How to Test / Use
- Use the menus to register/login and enrol subjects.
- Email format: must end with `@university.com` and use lowercase words joined by dots (e.g., `john.smith@university.com`).
- Password format: starts with uppercase, has at least 5 letters total, followed by **3+ digits** (e.g., `Helloworld123`).

## Notes
- Do **not** commit cache, build, or logs. Only source code and this README.
