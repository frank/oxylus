import tkinter as tk

class View():
    '''
    The view currently initializes the frame and "packs" it,
    which means that it arranges the objects in it so as to fill
    the space without much care to the positions.
    Here the side panel is initialized.
    '''
    def __init__(self, master, model):
        self.frame = tk.Frame(master, width = 800, height = 600, bg="red")
        self.frame.pack(side = tk.LEFT,
                        fill = tk.BOTH,
                        expand = 1)
        self.sidepanel = SidePanel(master, model)

class SidePanel():
    '''
    This is a secondary frame.
    '''
    def __init__(self, root, model):
        self.frame2 = tk.Frame(root, height = root.winfo_height(), bg = "Green")
        self.frame2.pack(side = tk.RIGHT, fill = tk.BOTH)
        woodLabels = []
        for wood in range(len(model.getWoods())):
            newLabel = tk.Label(self.frame2, text=str(model.getWoods()[wood].getEnglishName()) + \
                ", (" + str(model.getWoods()[wood].getLatinName()) + ")", fg="Black", anchor = "w")
            newLabel.pack(side = tk.TOP, fill = tk.BOTH)
            newLabel.bind("<Enter>", lambda eff: popup(eff, model, root, newLabel))
            newLabel.bind("<Leave>", lambda eff: deletePopup(eff, root, newLabel))
            woodLabels.append(newLabel)

        # self.plotBut = tk.Button(self.frame2, text = "Plot")
        # self.plotBut.pack(side = "top", fill = tk.BOTH)
        # self.clearButton = tk.Button(self.frame2, text = "Clear")
        # self.clearButton.pack(side = "top", fill = tk.BOTH)

def popup(event, model, root, label):
    print(label.winfo_width(), root.winfo_width())
    woodWindow = tk.Frame(root, width =400, height = 200, bg = "blue")
    woodWindow.pack()
    woodWindow.place(x = root.winfo_width() - label.winfo_width() - 400 ,\
         y = root.winfo_height() - label.winfo_height() - 200)

def deletePopup(event, root, label):
    print("deleted")
    for child in label.winfo_children():
        child.destroy()
        root.update()
