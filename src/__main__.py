from frontend import Gui
from backend import Database

def generate_fake_data(db):
	chars = "qwertyuioplkjhgfdsazxcvbnm"

	# fejk data generator
	for x in range(100):
		db.insert(idx = x,
				start_date = "1970-01-01",
				end_date = "2019-12-15",
				client = str(x),
				item = "Something" + str(x),
				accessories = "Accessories" + str(x),
				deceased = "Name" + str(x),
				localization = "Place",
				permission = "Yes/No",
				price = 10.0,
				advance = 3.0,
				remaining = 7.0,
				order_status = "Active",
				accessories_status = "Unknown")

def main():
	database = Database()

	generate_fake_data(database)

	app = Gui(database)
	app.mainloop()

if __name__ == "__main__":
	main()