from frontend import Gui
from backend import Database

def main():
	database = Database()

	# fejk data generator
	for x in range(100):
		database.insert(idx = x,
			client = "test" + str(x),
			item = "Something",
			start_date = "1970-01-01")

	app = Gui(database)
	app.mainloop()

if __name__ == "__main__":
	main()