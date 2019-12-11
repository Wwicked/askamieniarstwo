import sqlite3

class Database:
	def __init__(self, name):
		self.init()

	def init(self):
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
		
		dummy = self.cursor.fetchall()

		# TODO: delete this
		for item in dummy:
			print(item)

		return dummy