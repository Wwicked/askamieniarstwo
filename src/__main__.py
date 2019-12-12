from frontend import Gui
from backend import Database

database = Database("test.db")

if __name__ == "__main__":
	database.read(0)
	database.insert(start = "123")

	gui = Gui(database)