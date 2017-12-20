import tkinter as tk
import numpy as np
from controller.controller import Controller
from model import *
import csv

# Main function. It initalizes the controller.
if __name__ == '__main__':


    with open('Wood_data.csv', 'rb') as csvfile:
        reader = csv.reader(open('Wood_data.csv', newline=''), delimiter=',', quotechar='|')
        for row in reader:
           pass
           #print(', '.join(row))
    controller = Controller()
    controller.run()
    
    
    
