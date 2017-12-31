from controller.controller_new import Controller_new
from model.model_new import *
from view.view_new import View_new
import csv

# Main function. It initalizes the controller.
if __name__ == '__main__':

    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 600
    with open('Wood_data.csv', 'rb') as csvfile:
        reader = csv.reader(open('Wood_data.csv', newline=''), delimiter=',', quotechar='|')
        for row in reader:
           pass
           #print(', '.join(row))
    model = Model_new()
    view = View_new(SCREEN_WIDTH, SCREEN_HEIGHT, model)
    controller = Controller_new(model, view)
    view.redraw()

    while controller.running:
    	controller.process_input()
    	view.blit()
