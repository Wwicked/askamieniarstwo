from tkinter import *
import tkinter.messagebox

class Gui:
	def __init__(self, database):
		self.database = database

		self.window = Tk()

		# Set window size
		self.window.geometry("500x500")

		# Set window title
		self.window.wm_title("AS Kamieniarstwo")

		self.mainWindow()
		self.window.mainloop()

	def mainWindow(self):
		# -- Menu bar
		# Menu options
		menuBar = Menu(self.window)

		fileMenu = Menu(menuBar, tearoff = False)
		fileMenu.add_command(label = "Nowy plik", command = self.newFile)
		fileMenu.add_separator()
		fileMenu.add_command(label = "Wyjdz", command = self.exit)

		menuBar.add_cascade(label = "Plik", menu = fileMenu)

		self.window.config(menu = menuBar)

		# -- Options
		filterMenuOptions = StringVar(self.window)
		filterMenuOptions.set("Filtrowanie")

		filterMenu = OptionMenu(self.window, filterMenuOptions, "1", "2", "3")
		filterMenu.grid(row = 0, column = 0)

		filterButton = Button(self.window, text = "Filtruj", command = lambda: self.refresh(filterMenuOptions))
		filterButton.grid(row = 0, column = 2)

		# -- List box
		# Workaround for list box not apearing
		f = Frame(self.window)
		f.grid(row = 1, column = 0)

		f1 = Frame(f)
		f1.grid(row = 1, column = 0)

		# Create list box
		self.listBox = Listbox(f1)
		self.listBox.grid(row = 2, column = 0, sticky = E+W)

		# Create bar
		scrollBar = Scrollbar(f, orient = "vertical", command = self.listBox.yview)
		scrollBar.grid(row = 1, column = 3, sticky = "NS")

		# Assign bar to list box
		self.listBox.config(yscrollcommand = scrollBar.set)

		self.refresh(0)

	def newFile(self):
		newWindow = Toplevel(self.window)
		inputs = []

		def checkInputs():
			# Get empty fields indexes
			invalidIndexes = [ i for i in range(len(inputs)) if not len(inputs[i].get())]

			if len(invalidIndexes):
				message = "Niektóre z pól nie zostały uzupełnione:"

				# Add missing field name
				for i in invalidIndexes:
					message += f"\n\t{labels[i]}"

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
			inputs.append(StringVar())

			dummy = Label(newWindow, text = label + ":").grid(row = index, column = 0, sticky = W)
			dummy = Entry(newWindow, textvariable = inputs[index]).grid(row = index, column = 2)

		# Add spacing
		dummy = Label(newWindow, text = "")
		dummy.grid(row = len(labels))

		# Add buttons
		for index, button in enumerate(buttons):
			dummy = Button(newWindow, text = button[0], command = button[1])
			dummy.grid(row = len(labels) + 1, column = index)

	def exit(self):
		self.window.destroy()
		quit()

	def refresh(self, _filter = None):
		# Clear it out
		self.listBox.delete(0, END)

		for item in self.database.read(0):
			self.listBox.insert(END, item)

	def addEntry(self, *args):
		# TODO: Send to backend
		for i in range(len(args[0])):
			print(args[0][i].get())