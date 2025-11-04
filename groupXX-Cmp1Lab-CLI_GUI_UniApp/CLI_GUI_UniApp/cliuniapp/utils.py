
import re

EMAIL_RE = re.compile(r"^[a-z]+(?:\.[a-z]+)*@university\.com$")
# Password: starts with uppercase, then at least 4 more letters (total letters >=5), then 3+ digits
# Example: Hello123, Helloworld222
PASS_RE = re.compile(r"^[A-Z][a-zA-Z]{4,}\d{3,}$")

def valid_email(email: str) -> bool:
    return bool(EMAIL_RE.match(email.strip()))

def valid_password(pw: str) -> bool:
    return bool(PASS_RE.match(pw.strip()))
