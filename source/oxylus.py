import tkinter as tk
import numpy as np
from controller import Controller

# Main function. It initalizes the controller.
if __name__ == '__main__':
    controller = Controller()
    controller.run()
    controller.loadDataFromFiles() #load facts, rules, questions, wood types
    controller.fuckFranky()        #fucks franky furiously but softly
    controller.
