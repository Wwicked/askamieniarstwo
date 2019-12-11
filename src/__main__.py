from frontend import Gui
from backend import Database

database = Database("test.db")

if __name__ == "__main__":
	database.read(0)
	database.insert(1,1,1,1,1,1,1,1,1,1,1,1)

	gui = Gui(database)