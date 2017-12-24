import tkinter as tk
from tkinter import *
import PIL
from PIL import ImageTk, Image
import os

class View():
    '''
    The view currently initializes the frame and "packs" it,
    which means that it arranges the objects in it so as to fill
    the space without much care to the positions.
    Here the side panel is initialized.
    '''
    def __init__(self, master, model):
        self.sidePanel = tk.Frame(master, width = 300, height = master.winfo_height())
        self.sidePanel.pack(side = tk.RIGHT)
        self.frame1 = tk.Frame(master, width = 800, height = 400, bg="red")
        self.frame1.pack(side = tk.TOP, fill = tk.BOTH, expand = 1)
        self.woodLabels = []
        self.woodDisplay = tk.Frame(self.frame1, width =400, height = 200, bg="blue")

        # Create WoodType Labels
        for wood in range(len(model.getWoods())):
            #newWoodFrame = tk.Frame(self.sidePanel, bg="green", height = 20)
            #newWoodFrame.grid(row = wood)
            newLabel = tk.Label(self.sidePanel, text=str(model.getWoods()[wood].getEnglishName()) + \
                ", (" + str(model.getWoods()[wood].getLatinName()) + ")", fg="Black",\
                anchor = "w")
            newLabel.pack(side = tk.TOP, fill = tk.BOTH)
            master.update_idletasks()
            #self.woodFrames.append(newWoodFrame)
            newLabel.bind("<Enter>", lambda eff: popup(eff, master, model, self.frame1, self.woodDisplay,\
                newLabel, wood))
            newLabel.bind("<Leave>", lambda eff: deleteContents(eff, self.woodDisplay))
            self.woodLabels.append(newLabel)

def popup(event, master, model, frame1, woodDisplay, woodLabel, woodNumber):
    deleteContents(event, woodDisplay)
    master.update_idletasks()
    #print(event.y, woodLabel.winfo_height(), master.winfo_y())
    woodDisplay.place(x = frame1.winfo_width() - woodDisplay.winfo_width(),\
     y = event.y_root - master.winfo_y() -  event.y)
    woodDisplay.pack_propagate(False) #Force woodDisplay to not change size as things are packed in it
    # Insert wood picture
    file_path = os.getcwd() + r"\view\pictures\eyy.png"
    print(file_path)
    photo = Image.open(file_path)
    pWidth, pHeight = photo.size
    ratio = pWidth/pHeight
    photo = photo.resize((int((woodDisplay.winfo_height()-25)*ratio), woodDisplay.winfo_height()-25), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(photo)
    woodPicture = tk.Label(woodDisplay, image = photo)
    woodPicture.image = photo
    woodPicture.pack(side = tk.LEFT)
    #Create Text box
    textBox = tk.Frame(woodDisplay)
    textBox.pack(side = tk.RIGHT, fill = tk.BOTH)
    # Inser Wood Name
    woodText = tk.Label(textBox, text = str(model.getWoods()[woodNumber].getEnglishName()), fg = "black")
    woodText.grid(row = 1)
    # Insert Text
    woodText = tk.Label(textBox, text = "Something Something", fg = "black")
    woodText.grid(row = 4)

    master.update_idletasks()
    

def deleteContents(event, woodDisplay):
    for child in woodDisplay.winfo_children():
        child.destroy()
