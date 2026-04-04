import tkinter as tk
from tkinter import ttk
import threading

print('import:',__name__)

MOUSE_BTN = '<Button-'
MOUSE_LEFT_BTN = MOUSE_BTN+'1>'
MOUSE_RIGHT_BTN = MOUSE_BTN+'3>'
MOUSE_SCROLL_BTN = MOUSE_BTN+'2>'

def CalbackCombobox(args):
    port_name = args.widget.get()
    print('ComboCalback:', port_name)

def CallbackButtonSearchPorts(args):
    print('CallbackButtonSearchPorts press:',args)

def CallbackButtonOpenPort(args):
    print('CallbackButtonOpenPort press:',args)

def CallbackButtonGetImage(args):
    print('CallbackButtonGetImage press:',args)

class FilmGui():
    
    def __init__(self):
        self.win = tk.Tk()
        self.win.geometry('800x600')
        self.ComboBoxAdd(self.win)
        self.ButtonSearchPortsAdd(self.win)
        self.ButtonOpenPortAdd(self.win)
        self.ButtonGetImage(self.win)
        self.TextBoxAdd(self.win)
        
    def Start(self):
        self.win.mainloop()
    
    def ComboBoxAdd(self, win):
        self.cmbb = ttk.Combobox(win)
        self.cmbb.pack(padx = 0, pady = 0)
        self.cmbb.place(x = 5, y = 5, width = 100, height = 25,)

    def ComboBoxAddItems(self, items_list):
        print(items_list)
        vals = list(self.cmbb['values'])
        for item in items_list:
            vals.append(item)
        self.cmbb['values'] = vals
        print(self.cmbb['values'])

    def ComboBoxBind(self, callback):
        self.cmbb.bind('<<ComboboxSelected>>', callback)

    def ButtonSearchPortsAdd(self, win):
        self.btn_search_ports = tk.Button(
            win,
            text = 'SEARCH PORTS',
            bg = 'blue',
            fg = 'yellow')
        self.btn_search_ports.pack()
        self.btn_search_ports.place(x = 110, y = 5, width = 100, height = 25,)

    def ButtonSearchPortsBind(self, calback):
        self.btn_search_ports.bind(MOUSE_LEFT_BTN, calback)

    def ButtonOpenPortAdd(self, win):
        self.btn_open_port = tk.Button(
            win,
            text = 'OPEN PORT',
            bg = 'blue',
            fg = 'yellow')
        self.btn_open_port.pack()
        self.btn_open_port.place(x = 215, y = 5, width = 100, height = 25,)
        
    def ButtonOpenPortBind(self, calback):
        self.btn_open_port.bind(MOUSE_LEFT_BTN, calback)

    def ButtonGetImage(self, win):
        self.btn_get_image = tk.Button(
            win,
            text = 'GET IMAGE',
            bg = 'blue',
            fg = 'yellow')
        self.btn_get_image.pack()
        self.btn_get_image.place(x = 320, y = 5, width = 100, height = 25,)

    def ButtonGetImageBind(self, calback):
        self.btn_get_image.bind(MOUSE_LEFT_BTN, calback)

    def TextBoxAdd(self, win):
        self.text_box = tk.Text(
            win,
            height = 33)
        self.text_box.pack()
        self.text_box.place(x = 5, y = 50)

    def TextBoxAddText(self, text):
        tb_text = self.text_box.get(1.0, tk.END)
        tb_text = tb_text + text
        self.text_box.insert(1.0, text+'\n')

##class FilmGui(threading.Thread):
##    
##    def __init__(self):
##        super().__init__(name = 'FilmGuiThread')
##        print('FilmGui__init__()')
##        self.win = tk.Tk()
##        self.win.geometry('800x600')
##        self.ComboBoxAdd(self.win)
##
##    def run(self):
##        print('FilmGui run()')
##        self.win.mainloop()
##
##    def ComboBoxAdd(self, win):
##        self.cmbb = ttk.Combobox(win)
##        self.cmbb.pack(padx = 0, pady = 0)
##
##    def ComboBoxAddItems(self, items_list):
##        print(items_list)
##        vals = list(self.cmbb['values'])
##        for item in items_list:
##            vals.append(item)
##        self.cmbb['values'] = vals
##        print(self.cmbb['values'])
##
##    def ComboBoxBind(self, calback):
##        self.cmbb.bind('<<ComboboxSelected>>', calback)
        

def main():
    filmgui = FilmGui()

    filmgui.ComboBoxBind(CalbackCombobox)
    filmgui.ButtonSearchPortsBind(CallbackButtonSearchPorts)
    filmgui.ButtonOpenPortBind(CallbackButtonOpenPort)
    filmgui.ButtonGetImageBind(CallbackButtonGetImage)
    
    filmgui.ComboBoxAddItems(['1','2','3','4','5'])

    filmgui.Start()

    print('filmgui.thread.join()')
    pass

if __name__ == '__main__':
    main()
