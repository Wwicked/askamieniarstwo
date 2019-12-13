from frontend import Gui
from backend import Database

def main():
    database = Database()
    # fejk data generator
    # for x in range(10):
    #     database.insert(idx = x, client="wololo"+str(x))
    app = Gui(database)
    app.mainloop()

if __name__ == "__main__":
    main()