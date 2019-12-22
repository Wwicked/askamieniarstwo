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

    def insert(self, **kwargs):
        self.records.append(Record(**kwargs))

    def open(self):
        pkl_file = open("data.pkl", "rb")
        self.records = pickle.load(pkl_file)

    def save(self):
        output = open("data.pkl", "wb")
        pickle.dump(self.records, output)