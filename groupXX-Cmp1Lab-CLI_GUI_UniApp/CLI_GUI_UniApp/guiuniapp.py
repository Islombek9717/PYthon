
import tkinter as tk
from tkinter import messagebox
from cliuniapp.database import Database
from cliuniapp.utils import valid_email, valid_password
from cliuniapp.student import Student

class GUIUniApp:
    def __init__(self, master):
        self.master = master
        self.db = Database(".")
        self.master.title("GUIUniApp - Login")
        self.build_login()

    def build_login(self):
        self.clear_frame()
        tk.Label(self.master, text="Student Login").grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(self.master, text="Email").grid(row=1, column=0, sticky="e")
        tk.Label(self.master, text="Password").grid(row=2, column=0, sticky="e")
        self.email_var = tk.StringVar()
        self.pw_var = tk.StringVar()
        tk.Entry(self.master, textvariable=self.email_var, width=30).grid(row=1, column=1, padx=5)
        tk.Entry(self.master, textvariable=self.pw_var, width=30, show="*").grid(row=2, column=1, padx=5)
        tk.Button(self.master, text="Login", command=self.login).grid(row=3, column=0, columnspan=2, pady=10)

    def clear_frame(self):
        for w in self.master.winfo_children():
            w.destroy()

    def login(self):
        email = self.email_var.get().strip()
        pw = self.pw_var.get().strip()
        if not email or not pw:
            messagebox.showerror("Error", "Email and Password required")
            return
        if not (valid_email(email) and valid_password(pw)):
            messagebox.showerror("Error", "Invalid email or password format")
            return
        st = self.db.get_by_email(email)
        if not st or st.password != pw:
            messagebox.showerror("Error", "Student not found or wrong password")
            return
        self.student = st
        self.build_enrolment()

    def build_enrolment(self):
        self.clear_frame()
        tk.Label(self.master, text=f"Welcome {self.student.name} ({self.student.id})").grid(row=0, column=0, columnspan=3, pady=10)
        self.listbox = tk.Listbox(self.master, width=50, height=6)
        self.listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        tk.Button(self.master, text="Enroll Subject", command=self.enrol).grid(row=2, column=0, pady=5)
        tk.Button(self.master, text="Remove Selected", command=self.remove).grid(row=2, column=1, pady=5)
        tk.Button(self.master, text="Refresh", command=self.refresh).grid(row=2, column=2, pady=5)
        self.refresh()

    def enrol(self):
        if len(self.student.subjects) >= 4:
            messagebox.showwarning("Limit", "Students are allowed to enrol in 4 subjects only")
            return
        sub = self.student.enrol()
        self.db.upsert(self.student)
        self.refresh()

    def remove(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        line = self.listbox.get(sel[0])
        sid = line.split()[1].split("::")[1]
        if self.student.remove_subject(sid):
            self.db.upsert(self.student)
            self.refresh()

    def refresh(self):
        self.listbox.delete(0, tk.END)
        for s in self.student.subjects:
            self.listbox.insert(tk.END, s.to_display())

def main():
    root = tk.Tk()
    app = GUIUniApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
