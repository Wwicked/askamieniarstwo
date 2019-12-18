import tkinter as tk
from tkinter import messagebox, ttk

class Controller:
    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data = data

class Gui(Controller, tk.Tk):
    def __init__(self, data, *args, **kwargs):
        super().__init__(data, *args, **kwargs)

        self.data_saved = True

        self.geometry("1024x768")

        # Main frame
        self.main_frame = MainFrame(self, self.data)
        self.main_frame.grid(column = 0, row = 0, sticky = "nswe")

        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)

        # Assign quit event
        self.protocol("WM_DELETE_WINDOW", self.quit)

        # Set title
        self.wm_title("AS Kamieniarstwo")

        # Read data file
        self.open_file()

        # Create menu bar
        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff = False)
        file_menu.add_command(label = "Otwórz", command = self.open_file)
        file_menu.add_command(label = "Zapisz", command = self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label = "Wyjdz", command = self.quit)

        menu_bar.add_cascade(label = "Plik", menu = file_menu)

        self.config(menu = menu_bar)

    def quit(self):
        # Ask wether to save unsaved changes
        if messagebox.askyesno(title = "Wyjdz", message = "Na pewno chcesz zamknac program?"):
            if not self.data_saved:
                if messagebox.askyesno(title = "Wyjdz", message = "Zapisac zmiany przed zamknieciem programu?"):
                    self.save_file()
            
            self.destroy()

    def save_file(self):
        # Update database
        self.data.save()

        # Mark as saved
        self.data_saved = True

    def open_file(self):
        self.data.open()
        self.main_frame.tree_frame.refresh()

class MainFrame(Controller, tk.Frame):
    def __init__(self, master, data):
        self.root = master

        # inicjalizacja pola data, ustawienie parenta dla frame.
        super().__init__(data, self.root)

        self.edit_frame = EditFrame(self, self.data)
        self.edit_frame.grid(column = 0, row = 0, sticky = "nswe")
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)

        self.buttons_frame = ButtonsFrame(self, self.data)
        self.buttons_frame.grid(column = 0, row = 1, sticky = "nswe")
        self.rowconfigure(1, weight = 1)
        self.columnconfigure(1, weight = 1)

        self.tree_frame = TreeFrame(self, self.data)
        self.tree_frame.grid(column = 0, row = 2, sticky = "nswe")
        self.rowconfigure(2, weight = 8)
        self.columnconfigure(2, weight = 8)
        
class TreeFrame(Controller, tk.Frame):
    def __init__(self, master, data):
        self.root = master

        # standardowa + ustawienie marginesu dla klasy bazowej Frame
        super().__init__(data, self.root, borderwidth = 10)

        self.is_sorted = [False] * len(self.data.labels.keys())

        # Treeview chyba lepiej tu siądzie od listview
        self.tree = ttk.Treeview(self, selectmode = "browse", show = "headings")
        self.tree.grid(column = 0, row = 0, sticky = "nswe")

        # Dodanie kolumn z klasy z danymi, ustawia ich id.
        self.tree["columns"] = list(self.data.labels.keys())
        self.tree.bind("<<TreeviewSelect>>", self.focus)
        self.tree.bind("<Button-1>", self.sort)

        for name, text in self.data.labels.items():
            self.tree.column(name, width = 70)
            self.tree.heading(name, text = text)

        self.scroll = tk.Scrollbar(self, orient = "vertical", command = self.tree.yview)
        self.scroll.grid(column = 1, row = 0, sticky = "nswe")

        self.tree.configure(yscrollcommand = self.scroll.set)
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)

        self.update()

    def focus(self, e):
        index = self.tree.focus()
        values = self.tree.item(index)["values"]
        items = self.data.labels.items()

        self.focused = index

        # Show focused record data in entries.
        for i in range(len(items)):
            self.root.edit_frame.text[i].delete("1.0", "end")
            self.root.edit_frame.text[i].insert("1.0", values[i])

        # Enables buttons
        self.root.buttons_frame.set_button_state(_all = True, state = "normal")

    def reset_focus(self):
        self.focused = -1
        self.root.buttons_frame.set_button_state(_all = True, state = "disabled")
        self.root.buttons_frame.set_button_state(names = ["add"], state = "normal")

        for i in range(len(self.data.labels.values())):
            self.root.edit_frame.text[i].delete("1.0", "end")

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        self.update()

    def update(self):
        for x in self.data.records:
            vals = x.get()
            self.tree.insert("", "end", text = x.idx, values = (vals[1:]))

    def sort(self, event):
        if self.tree.identify("region", event.x, event.y) != "heading":
            return

        index = int(self.tree.identify_column(event.x)[1::]) - 1
        reverse = True if self.is_sorted[index] else False

        SortTree(self, index, reverse)

    def set_template(self, child):
        import datetime

        current_date = datetime.date.today().strftime("%Y-%m-%d")

        template = [
            current_date, # Data rozpoczecia
            "", # Data wykonania
            "", # Klient
            "", # Zlecenie
            "", # Akcesoria
            "", # Zmarła
            "", # Miejsce
            "", # Zezwolenie
            "", # Cena
            "", # Zaliczka
            "", # Do zaplaty
            "", # Status zlecenia
            "" # Status akcesoriów
        ]

        for slot in range(len(template)):
            self.tree.set(child, slot, template[slot])

        self.root.root.data_saved = False

class EditFrame(Controller, tk.Frame):
    def __init__(self, master, data):
        self.root = master
        self.text = []

        super().__init__(data, self.root, bd = 10)

        labels = list(self.data.labels.values())

        c = 0
        r = 0
        heights = [2] * len(labels)
        heights = [1, 1, 1, 3, 1, 3, 1, 1, 1, 1, 1, 1, 3]

        for iterator in range(len(labels)):
            c = iterator % 2 == 0 and 1 or 0 # Limit 2 columns per row
            if iterator % 2 == 0: r += 1 # Limit 2 columns per row

            dummy = tk.Label(self, text = labels[iterator] + ":")
            dummy.grid(column = c, row = r, pady = 6, sticky = "w")

            self.text.append(tk.Text(self, height = heights[iterator], width = 40))
            self.text[iterator].grid(column = c, row = r, padx = 105, sticky = "e")
            
            self.rowconfigure(r, weight = 2)

class ButtonsFrame(Controller, tk.Frame):
    def __init__(self, master, data):
        self.root = master
        self.buttons = {}

        super().__init__(data, self.root, bd = 10)

        self.buttons["save"] = tk.Button(self, text = "Zapisz wpisz", command = self.save)
        self.buttons["save"].grid(column = 0, row = 0)

        self.buttons["clear"] = tk.Button(self, text = "Wyczysc wpis", command = self.clear)
        self.buttons["clear"].grid(column = 1, row = 0, padx = 10)

        self.buttons["delete"] = tk.Button(self, text = "Usun wpis", command = self.delete)
        self.buttons["delete"].grid(column = 2, row = 0)

        self.buttons["add"] = tk.Button(self, text = "Dodaj wpis", command = self.add)
        self.buttons["add"].grid(column = 3, row = 0, padx = 30)

        self.set_button_state(_all = True, state = "disabled")
        self.set_button_state(names = ["add"], state = "normal")

    def save(self):
        index = self.root.tree_frame.focused
        data_length = range(len(self.data.labels.values()))
        data = [self.root.edit_frame.text[i].get("1.0", "end") for i in data_length]

        for i in data_length:
            self.root.tree_frame.tree.set(index, i, data[i])

    def delete(self):
        index = self.root.tree_frame.focused
        self.root.tree_frame.tree.delete(index)

        self.root.tree_frame.reset_focus()

    def clear(self):
        for i in range(len(self.data.labels.values())):
            self.root.edit_frame.text[i].delete("1.0", "end")

    def add(self):
        # Add treeview item
        self.root.tree_frame.tree.insert("", "end", values = [""] * len(self.data.labels))
        
        # Get new item's id
        child_index = self.root.tree_frame.tree.get_children()[-1]

        # Focus on that item
        self.root.tree_frame.tree.focus(child_index)
        self.root.tree_frame.tree.selection_set(child_index)
        self.root.tree_frame.tree.yview_moveto(1)

        # Fill the template data
        self.root.tree_frame.set_template(child_index)

        # Send it to database
        text = self.root.edit_frame.text
        self.data.insert(idx = len(self.data.records),
                        start_date = text[0].get("1.0", "end"),
                        end_date = text[1].get("1.0", "end"),
                        client = text[2].get("1.0", "end"),
                        item = text[3].get("1.0", "end"),
                        accessories = text[4].get("1.0", "end"),
                        deceased = text[5].get("1.0", "end"),
                        localization = text[6].get("1.0", "end"),
                        permission = text[7].get("1.0", "end"),
                        price = text[8].get("1.0", "end"),
                        advance = text[9].get("1.0", "end"),
                        remaining = text[10].get("1.0", "end"),
                        order_status = text[11].get("1.0", "end"),
                        accessories_status = text[12].get("1.0", "end"))

        # Mark program as unsaved
        self.root.root.data_saved = False

    def set_button_state(self, _all = False, names = [], state = ""):
        # Return if state was not provided
        if not len(state):
            return

        # Return if invalid targets were provided
        if not _all and not len(names):
            return

        if _all:
            for name in self.buttons.keys():
                self.buttons[name]["state"] = state
        else:
            for name in names:
                if name not in self.buttons.keys():
                    continue

                self.buttons[name]["state"] = state

class SortTree:
    def __init__(self, parent, column, reverse):
        self.parent = parent
        self.tree = parent.tree
        self.data = parent.data
        self.column = column

        tree_children = self.tree.get_children()

        # Do nothing if theres no data to sort
        if not len(tree_children):
            return

        sorted_data = []

        # Get all tree columns data and create dictionary containing sort-type and column data
        for col in tree_children:
            column_data = self.tree.item(col)["values"]

            sorted_data.append({
                "data" : column_data,
                "sort_by" : column_data[self.column]
                })
        
        # Convert data to floats so sorting doesnt fail
        if self.parent.data.record_types[self.column] in [float, int]:
            for i in range(len(sorted_data)):
                sorted_data[i]["sort_by"] = float(sorted_data[i]["sort_by"]) # ValueError if column data is not an int/float
                # Also check if it has length
        
        # Sort data
        sorted_data.sort(key = lambda x : x["sort_by"], reverse = reverse)

        # Delete all items from tree
        self.tree.delete(*self.tree.get_children())

        # Add data again in sorted order
        for index in range(len(sorted_data)):
            self.tree.insert("", "end", text = index, values = sorted_data[index]["data"])

        # Mark as sorted/reverse-sorted
        self.parent.is_sorted[self.column] = False if reverse else True