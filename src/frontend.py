from tkinter import *
import tkinter.messagebox

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
		# Menu options
		menuBar = Menu(self.window)

		fileMenu = Menu(menuBar, tearoff = 0)
		fileMenu.add_command(label = "Nowy plik", command = self.newFile)
		fileMenu.add_separator()
		fileMenu.add_command(label = "Wyjdz", command = self.exit)

		menuBar.add_cascade(label = "Plik", menu = fileMenu)

		self.window.config(menu = menuBar)

		# Workaround for list box not apearing
		f = Frame(self.window).place(x = 0, y = 0, width = 100, height = 100)
		f1 = Frame(f).place(x = 0, y = 0, width = 100, height = 100)

		# Create list box
		listBox = Listbox(f1)
		listBox.pack(side = "left", fill = "y")

		# Create bar
		scrollBar = Scrollbar(f, orient = "vertical", command = listBox.yview)
		scrollBar.pack(side = "right", fill = "y")

		# Assign bar to list box
		listBox.config(yscrollcommand = scrollBar.set)

		for i in range(100):
			listBox.insert(END, str(i))

	def newFile(self):
		newWindow = Toplevel(self.window)
		inputs = []

		def checkInputs():
			invalidIndexes = []

			# Get empty fields indexes
			for i in range(len(inputs)):
				if not len(inputs[i].get()):
					invalidIndexes.append(i)

			if len(invalidIndexes):
				message = "Niektóre z pól nie zostały uzupełnione:"	

				# Add missing field name
				for i in invalidIndexes:
					message += "\n\t%s" %(labels[i])

				return (False, message)
			
			return (True, "")

		def apply():
			valid = checkInputs()

			# Show error if one occured
			if not valid[0]:
				tkinter.messagebox.showerror("Bląd", valid[1])

			else:
				self.addEntry(inputs)

		def cancel():
			newWindow.destroy()

		def reset():
			# Set all to empty
			for i in range(len(inputs)):
				inputs[i].set("")

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
			[ "Resetuj dane", reset ],
			[ "Anuluj", cancel ]
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

	def addEntry(self, *args):
		# TODO: Send to backend
		for i in range(len(args[0])):
			print(args[0][i].get())