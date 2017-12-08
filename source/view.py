import tkinter as tk
import numpy as np

class View():
    '''
    The view currently initializes the frame and "packs" it,
    which means that it arranges the objects in it so as to fill
    the space without much care to the positions.
    Here the side panel is initialized.
    '''
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.frame.pack(side = tk.LEFT,
                        fill = tk.BOTH,
                        expand = 1)
        self.sidepanel = SidePanel(master)

class SidePanel():
    '''
    This is a secondary frame.
    '''
    def __init__(self, root):
        self.frame2 = tk.Frame(root)
        self.frame2.pack(side = tk.LEFT,
                         fill = tk.BOTH,
                         expand = 1)
        self.plotBut = tk.Button(self.frame2, text = "Plot")
        self.plotBut.pack(side = "top", fill = tk.BOTH)
        self.clearButton = tk.Button(self.frame2, text = "Clear")
        self.clearButton.pack(side = "top", fill = tk.BOTH)
