from controller.controller import Controller_new
from model.model import *
from view.view import View_new
import csv

# Main function. It initalizes the controller.
if __name__ == '__main__':

    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 600
    
    model = Model_new()
    view = View_new(SCREEN_WIDTH, SCREEN_HEIGHT, model)
    controller = Controller_new(model, view)
    view.redraw()

    while controller.running:
    	controller.process_input()
    	view.blit()
