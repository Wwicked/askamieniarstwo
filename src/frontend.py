import tkinter as tk
from tkinter import messagebox, ttk

'''Klasa Controller zawiera w sobie pole data które słóży do obsługi modelu danych, można tam wstawić klaske do obsługi bazy danych, plików, czy czegokolwiek innego'''
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
        self.main_frame.grid(column=0, row=0, sticky='nswe')

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

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
        if messagebox.askyesno(title="Quit", message="Are you sure you want to quit?"):
            self.destroy()

    # https://www.python.org/dev/peps/pep-0008/#naming-conventions funkcje i zmienne snake_case, nazwy klas CamelCase :P
    def new_record(self):
        NewWindow(self.data)

    def save_file(self):
        self.data.save()

    def open_file(self):
        self.data.open()
        self.main_frame.refresh()

'''Główny kontenerek typu frame, Controller daje mu pole data, będzie zawierał w sobie pozostałe elementy'''
class MainFrame(Controller, tk.Frame):
    def __init__(self, master, data):
        self.root = master

		# inicjalizacja pola data, ustawienie parenta dla frame.
        super().__init__(data, self.root)

		# wstawienie contentu do głównego frejmu, możesz olać jezeli chcesz inny design.
        self.nb = ttk.Notebook(self)
        self.tab1 = DefaultFrame(self.nb, self.data)
        self.tab2 = tk.Frame(self.nb)
        self.tab3 = tk.Frame(self.nb)
        self.nb.add(self.tab1, text='Nazwa zakładki 1')
        self.nb.add(self.tab2, text='Nazwa zakładki 2')
        self.nb.add(self.tab3, text='Nazwa zakładki 3')
        self.nb.grid(column=0, row=0, sticky='nswe')

        # opcja bez zakładek
        # self.content = DefaultFrame(self, self.data)
        # self.content.grid(column=0, row=0, sticky='nswe')

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def refresh(self):
        self.tab1.refresh()
        

class DefaultFrame(Controller, tk.Frame):
    def __init__(self, master, data):
        self.root = master

        # standardowa + ustawienie marginesu dla klasy bazowej Frame
        super().__init__(data, self.root, borderwidth=5)

        # Treeview chyba lepiej tu siądzie od listview
        self.tree = ttk.Treeview(self, selectmode='browse', show="headings")

        # Dodanie kolumn z klasy z danymi, ustawia ich id. 
        self.tree["columns"] = list(self.data.labels.keys())
        for name, text in self.data.labels.items():
                self.tree.column(name, width=70)
                self.tree.heading(name, text=text)
        self.tree.grid(column=0, row=0, sticky='nswe')

        scroll = tk.Scrollbar(self, orient = "vertical", command = self.tree.yview)
        scroll.grid(column = 1, row=0, sticky = "ns")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.update()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        self.update()

    def update(self):
        for x in self.data.records:
            vals = x.get()
            self.tree.insert('', 'end', text=x.idx, values=(vals[1:]))

# Klaska do nowego okienka, resztę bebechów można dodać jako pola tej klaski
class NewWindow(Controller, tk.Toplevel):
    def __init__(self, data):
        super().__init__(data)