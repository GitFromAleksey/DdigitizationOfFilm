import tkinter as tk
from tkinter import ttk
import threading

print('import:',__name__)
class FilmGui(threading.Thread):
    
    def __init__(self):
        super().__init__(name = 'FilmGuiThread')
        print('FilmGui__init__()')
        self.win = tk.Tk()
        self.win.geometry('800x600')
        self.ComboBoxAdd(self.win)

    def run(self):
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

    def ComboBoxBind(self, calback):
        self.cmbb.bind('<<ComboboxSelected>>', calback)
        

def main():
    filmgui = FilmGui()

    print('after gui run')
    
    filmgui.ComboBoxAddItems(['1','2','3','4','5'])
    pass

if __name__ == '__main__':
    main()
