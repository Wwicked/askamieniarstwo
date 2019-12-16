import tkinter as tk
from tkinter import messagebox, ttk

'''Klasa Controller zawiera w sobie pole data które służy do obsługi modelu danych, można tam wstawić klaske do obsługi bazy danych, plików, czy czegokolwiek innego'''
class Controller:
    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data = data

'''Klasa gui dziedziczy po Controllerze ( będzie miała w sobie pole data dzięki temu), oraz po tk.Tk czyli podstawowym okienku aplikacji tkintera (windows u Ciebie)'''
class Gui(Controller, tk.Tk):
    def __init__(self, data, *args, **kwargs):
        super().__init__(data, *args, **kwargs)

        self.geometry("1024x768")

        # stworzenie głównego frame dla okienka w którym będą wszystkie inne widgety i przekazanie mu pola data
        self.main_frame = MainFrame(self, self.data)
        self.main_frame.grid(column = 0, row = 0, sticky = "nswe")

        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)

        # przypisanie funkcji quit do zamknięcia okienka
        self.protocol("WM_DELETE_WINDOW", self.quit)

        self.wm_title("AS Kamieniarstwo")

        # meniu
        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff = False)
        file_menu.add_command(label = "Nowy wpis", command = self.new_record)
        file_menu.add_command(label = "Otwórz", command = self.open_file)
        file_menu.add_command(label = "Zapisz", command = self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label = "Wyjdz", command = self.quit)

        menu_bar.add_cascade(label = "Plik", menu = file_menu)

        self.config(menu = menu_bar)

    def quit(self):
        if messagebox.askyesno(title = "Quit", message = "Are you sure you want to quit?"):
            self.destroy()

    # https://www.python.org/dev/peps/pep-0008/#naming-conventions funkcje i zmienne snake_case, nazwy klas CamelCase :P
    def new_record(self):
        NewWindow(self, self.data)

    def save_file(self):
        self.data.save()

    def open_file(self):
        self.data.open()
        self.main_frame.content.refresh()

'''Główny kontenerek typu frame, Controller daje mu pole data, będzie zawierał w sobie pozostałe elementy'''
class MainFrame(Controller, tk.Frame):
    def __init__(self, master, data):
        self.root = master

        # inicjalizacja pola data, ustawienie parenta dla frame.
        super().__init__(data, self.root)

        self.edit = EditFrame(self, self.data)
        self.edit.grid(column = 0, row = 0, sticky = "nswe")
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)

        self.edit_options = EditButtons(self, self.data)
        self.edit_options.grid(column = 0, row = 1, sticky = "nswe")
        self.rowconfigure(1, weight = 3)
        self.columnconfigure(1, weight = 3)

        self.content = DefaultFrame(self, self.data)
        self.content.grid(column = 0, row = 2, sticky = "nswe")
        self.rowconfigure(2, weight = 5)
        self.columnconfigure(2, weight = 5)
        
class DefaultFrame(Controller, tk.Frame):
    def __init__(self, master, data):
        self.root = master

        # standardowa + ustawienie marginesu dla klasy bazowej Frame
        super().__init__(data, self.root, borderwidth = 10, bg = "green")

        # Treeview chyba lepiej tu siądzie od listview
        self.tree = ttk.Treeview(self, selectmode = "browse", show = "headings")
        self.tree.grid(column = 0, row = 1, sticky = "nswe")

        # Dodanie kolumn z klasy z danymi, ustawia ich id. 
        self.tree["columns"] = list(self.data.labels.keys())
        self.tree.bind("<<TreeviewSelect>>", self.focus)

        for name, text in self.data.labels.items():
            self.tree.column(name, width = 70)
            self.tree.heading(name, text = text)

        scroll = tk.Scrollbar(self, orient = "vertical", command = self.tree.yview)
        scroll.grid(column = 1, row = 1, sticky = "nswe")

        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)

        self.update()

    def focus(self, e):
        index = self.tree.focus()
        values = self.tree.item(index)["values"]
        items = self.data.labels.items()

        self.focused = index

        try:
            for i in range(len(items)):
                self.root.edit.entry_values[i].set(values[i])

        except IndexError:
            return

        # IndexError przy pierwszym zaznaczeniu

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        self.update()

    def update(self):
        for x in self.data.records:
            vals = x.get()
            self.tree.insert("", "end", text = x.idx, values = (vals[1:]))

class EditFrame(Controller, tk.Frame):
    def __init__(self, master, data):
        self.root = master
        self.entry_values = []

        super().__init__(data, self.root, bd = 10, bg = "blue")

        labels = list(self.data.labels.values())

        c = 0
        r = 0
        py = 0

        for b in range(len(labels)):
            c = b % 2 == 0 and 1 or 0 # Column
            if b % 2 == 0: r += 1 # Row
            if b == 2: py = 15 # Pady

            self.entry_values.append(tk.StringVar())

            dummy = tk.Label(self, text = labels[b] + ":")
            dummy.grid(column = c, row = r, pady = py, sticky = "w")

            dummy = tk.Entry(self, textvariable = self.entry_values[b], width = 50)
            dummy.grid(column = c, row = r, padx = 125, sticky = "e")

class EditButtons(Controller, tk.Frame):
    def __init__(self, master, data):
        self.root = master

        super().__init__(data, self.root, bd = 10, bg = "red")

        b_save = tk.Button(self, text = "Zapisz zmiany", command = self.save)
        b_save.grid(column = 0, row = 0)

    def save(self):
        index = self.root.content.focused
        labels = self.data.labels.values()
        data = [self.root.edit.entry_values[i].get() for i in range(len(labels))]

        self.root.content.update()
        self.root.content.refresh()

# Klaska do nowego okienka, resztę bebechów można dodać jako pola tej klaski
class NewWindow(Controller, tk.Toplevel):
    def __init__(self, master, data):
        self.root = master

        super().__init__(data, self.root)

        self.geometry("640x480")
        self.wm_title("Dodawanie wpisu")