from frontend import Gui
from backend import Database
import random

def generate_fake_data(db):
    for x in range(100):
        db.insert(idx = x,
                start_date = "%i-01-01" %(random.randint(1970, 2019)),
                end_date = "2019-12-15",
                client = "Client%i" %(x),
                item = "Something" + str(x),
                accessories = "Accessories" + str(x),
                deceased = "Name" + str(x),
                localization = "Place",
                permission = "Yes/No",
                price = "%0.2f" %(float([33, 4, 3][random.randint(0, 2)])),
                advance = "%0.2f" %(3.0),
                remaining = "%0.2f" %(7.0),
                order_status = "%s" %(["Active", "Not active", "Completed"][random.randint(0, 2)]),
                accessories_status = "Unknown")

def main():
    database = Database()

    generate_fake_data(database)

    app = Gui(database)
    app.mainloop()

if __name__ == "__main__":
    main()