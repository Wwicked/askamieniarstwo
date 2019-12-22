from collections import OrderedDict
import pickle

class Record():
    __slots__ = ["idx", "start_date", "end_date", "client", "item", "accessories", "deceased",
                "localization", "permission", "price", "advance", "remaining", "order_status", "accessories_status"]
                
    def __init__(self, **kwargs):
        for key in self.__slots__:
            if key in kwargs.keys():
                setattr(self, key, kwargs[key])
            else:
                setattr(self, key, "")

    def get(self):
        return [getattr(self, x) for x in self.__slots__]

class Database:
    def __init__(self):
        self.labels = OrderedDict([
                        ("start_date", "Data rozpoczecia"),
                        ("end_date", "Data wykonania"),
                        ("client", "Klient"),
                        ("item", "Zlecenie"),
                        ("accessories", "Akcesoria"),
                        ("deceased", "Zmarła"),
                        ("localization", "Miejsce"),
                        ("permission", "Zezwolenie"),
                        ("price", "Cena"),
                        ("advance", "Zaliczka"),
                        ("remaining", "Do zaplaty"),
                        ("order_status", "Status zlecenia"),
                        ("accessories_status", "Status akcesoriów")])
        self.record_types = [str, str, str, str, str, str, str, str, float, float, float, str, str]
        self.records = []
        self.pickle_file = "data.pkl"

    def insert(self, **kwargs):
        self.records.append(Record(**kwargs))

    def remove(self, index):
        # Store current records as a list
        recs = list(self.records)
        
        # Remove the item
        del recs[index]
        
        # Clear out records
        self.records = []

        # Create records once again
        for r in recs:
            self.records.append(r)

        # Save the file
        self.save()

    def open(self):
        pkl_file = open(self.pickle_file, "rb")
        self.records = pickle.load(pkl_file)

    def save(self):
        output = open(self.pickle_file, "wb")
        pickle.dump(self.records, output)