from tkinter import *

class Gui:
	def __init__(self):
		self.window = Tk()

		# Set window size
		self.window.geometry("500x500")

		# Set window title
		self.window.wm_title("AS Kamieniarstwo")

		self.window.mainloop()