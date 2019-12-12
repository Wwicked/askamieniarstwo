import sqlite3

class Database:
	def __init__(self, name):
		self.init(name)

	def init(self, name):
		self.connection = sqlite3.connect(name)
		self.cursor = self.connection.cursor()

		# Send request
		self.cursor.execute("CREATE TABLE IF NOT EXISTS test\
			(id INT PRIMARY KEY,\
			start_date INT,\
			end_date INT,\
			client TEXT,\
			item TEXT,\
			accesories TEXT,\
			deceased TEXT,\
			localisation TEXT,\
			price REAL,\
			advance REAL,\
			remaining REAL,\
			order_status INT,\
			accessories_status INT);")

		# Save changes
		self.connection.commit()

	def read(self, filter):
		self.cursor.execute("SELECT * FROM test WHERE 1;")

		return self.cursor.fetchall()

	def insert(self, start = "", end = "", client = "", item = "", accesories = "", deceased = "", localisation = "", price = "", advance = "", remaining = "", order_status = "", accessories_status = ""):
		self.cursor.execute(f"INSERT INTO test VALUES \
			(NULL,?,?,?,?,?,?,?,?,?,?,?,?)",
			(start,
			end,
			client,
			item,
			accesories,
			deceased,
			localisation,
			price,
			advance,
			remaining,
			order_status,
			accessories_status))

		self.connection.commit()
