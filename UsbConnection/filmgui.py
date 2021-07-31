import tkinter as tk
from tkinter import ttk

print('import:',__name__)
class FilmGui():

    def __init__(self):
        print('FilmGui__init__()')
        self.win = tk.Tk()
        self.win.geometry('800x600')
        self.ComboBoxAdd(self.win)

        self.win.mainloop()

    def ComboBoxAdd(self, win):
        self.cmbb = ttk.Combobox(win)
        self.cmbb.pack(padx = 0, pady = 0)

    def ComboBoxAddItems(self, items_list):
        print(items_list)
        vals = list(self.cmbb['values'])
        for item in items_list:
            vals.append(item)
        self.cmbb['values'] = vals
        print(self.cmbb['values'])
        

def main():
    filmgui = FilmGui()
    
    filmgui.ComboBoxAddItems(['1','2','3','4','5'])
    pass

if __name__ == '__main__':
    main()
