
from cliuniapp.database import Database
from cliuniapp.controllers import UniversityApp

def main():
    db = Database(".")
    app = UniversityApp(db)
    app.run()

if __name__ == "__main__":
    main()
