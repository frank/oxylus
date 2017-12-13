import tkinter as tk
import numpy as np
from model import Model
from view import View, SidePanel

class Controller():
    '''
    Initializing the 'root' main container, the model, the view,
    '''
    def __init__(self):
        self.root = tk.Tk()
        self.model = Model()
        self.view = View(self.root)
        self.view.sidepanel.plotBut.bind("<Button>", self.my_plot)
        self.view.sidepanel.clearButton.bind("<Button>", self.clear)

    def run(self):
        self.root.title("Oxylus")
        self.root.geometry('1200x600')
        self.root.iconbitmap(default = 'icons\o24.ico')
        self.root.mainloop()

    # I removed internal objects that required extra packages.
    def clear(self,event):
        print("Doesn't do anything.")

    # Since I removed some commands that required extra packages,
    # probably doesn't do much.
    def my_plot(self,event):
        self.model.calculate()
