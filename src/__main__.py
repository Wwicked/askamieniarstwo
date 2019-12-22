from frontend import Gui
from backend import Database

def main():
    database = Database()

    app = Gui(database)
    app.mainloop()

if __name__ == "__main__":
    main()