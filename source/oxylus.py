from controller.controller import Controller
from model.model import *
from view.view import View
import sys


# Main function. It initalizes the controller.
if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        os.chdir(sys._MEIPASS)
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 900
    
    model = Model()
    view = View(SCREEN_WIDTH, SCREEN_HEIGHT, model)
    controller = Controller(model, view)
    view.redraw()

    while controller.running:
        controller.process_input()
        view.blit()
