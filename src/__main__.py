from frontend import Gui
from backend import Database
import random

def generate_fake_data(db):
    # fejk data generator
    for x in range(100):
        db.insert(idx = x,
                start_date = "%i-01-01" %(random.randint(1970, 2019)),
                end_date = "2019-12-15",
                client = str(random.randint(0, 3)),
                item = "Something" + str(x),
                accessories = "Accessories" + str(x),
                deceased = "Name" + str(x),
                localization = "Place",
                permission = "Yes/No",
                price = float(random.randint(0, 100)),
                advance = 3.0,
                remaining = 7.0,
                order_status = "%s" %(["Active", "Not active", "Completed"][random.randint(0, 2)]),
                accessories_status = "Unknown")

def main():
    database = Database()

    generate_fake_data(database)

    app = Gui(database)
    app.mainloop()

if __name__ == "__main__":
    main()