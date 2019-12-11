from tkinter import *

class Gui:
	def __init__(self):
		self.window = Tk()

		# Set window size
		self.window.geometry("500x500")

		# Set window title
		self.window.wm_title("AS Kamieniarstwo")

		self.mainWindow()
		self.window.mainloop()

	def mainWindow(self):
		menuBar = Menu(self.window)

		fileMenu = Menu(menuBar, tearoff = 0)
		fileMenu.add_command(label = "Nowy plik", command = self.newFile)
		fileMenu.add_separator()
		fileMenu.add_command(label = "Wyjdz", command = self.exit)

		menuBar.add_cascade(label = "Plik", menu = fileMenu)

		self.window.config(menu = menuBar)

	def newFile(self):
		def apply():
			pass

		def cancel():
			for i in range(len(inputs)):
				inputs[i].set("")

		def reset():
			pass

		newWindow = Toplevel(self.window)
		inputs = []

		labels = [
			"Data rozpoczecia",
			"Data wykonania",
			"Klient",
			"Zlecenie",
			"Akcesoria",
			"Zmarła",
			"Miejsce",
			"Zezwolenie",
			"Cena",
			"Zaliczka",
			"Do zaplaty",
			"Status zlecenia",
			"Status akcesoriów"
		]

		buttons = [
			[ "Ok", apply ],
			[ "Anuluj", cancel ],
			[ "Resetuj dane", reset ]
		]

		# Add labels
		for index, label in enumerate(labels):
			dummy = Label(newWindow, text = label + ":")
			dummy.grid(row = index, column = 0)

			inputs.append(StringVar())
			dummy = Entry(newWindow, textvariable = inputs[index])
			dummy.grid(row = index, column = 2)

		# Add spacing
		dummy = Label(newWindow, text = "")
		dummy.grid(row = len(labels))

		# Add buttons
		for index, button in enumerate(buttons):
			dummy = Button(newWindow, text = button[0], command = button[1])
			dummy.grid(row = len(labels) + 1, column = index)

	def exit(self):
		pass