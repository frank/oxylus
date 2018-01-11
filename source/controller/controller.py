import pygame
from model.model import Model
from view.view import *

class Controller():
    '''
    Initializing the 'root' main container, the model, the view,
    '''
    def __init__(self, model, view):

        self.model = model
        self.view = view
        self.running = True

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == True:
                    #if YES button was clicked
                    if pygame.mouse.get_pos()[0] > self.view.getYESbutton_pos_and_size()[0][0] and \
                    pygame.mouse.get_pos()[1] > self.view.getYESbutton_pos_and_size()[0][1] and \
                    pygame.mouse.get_pos()[0] < self.view.getYESbutton_pos_and_size()[0][0] + self.view.getYESbutton_pos_and_size()[1][0] and \
                    pygame.mouse.get_pos()[1] < self.view.getYESbutton_pos_and_size()[0][1] + self.view.getYESbutton_pos_and_size()[1][1]:
                        self.model.setAnswerToQuestion("YES")
                    #if NO button was clicked
                    if pygame.mouse.get_pos()[0] > self.view.getNObutton_pos_and_size()[0][0] and \
                    pygame.mouse.get_pos()[1] > self.view.getNObutton_pos_and_size()[0][1] and \
                    pygame.mouse.get_pos()[0] < self.view.getNObutton_pos_and_size()[0][0] + self.view.getNObutton_pos_and_size()[1][0] and \
                    pygame.mouse.get_pos()[1] < self.view.getNObutton_pos_and_size()[0][1] + self.view.getNObutton_pos_and_size()[1][1]:
                        self.model.setAnswerToQuestion("YES")
                        
            elif event.type == pygame.MOUSEMOTION:
                #if in sidebar
                if pygame.mouse.get_pos()[0] > self.view.getSideBar_pos_and_size()[0][0] and \
                pygame.mouse.get_pos()[1] > self.view.getSideBar_pos_and_size()[0][1] and \
                pygame.mouse.get_pos()[0] < self.view.getSideBar_pos_and_size()[0][0] + self.view.getSideBar_pos_and_size()[1][0] and \
                pygame.mouse.get_pos()[1] < self.view.getSideBar_pos_and_size()[0][1] + self.view.getSideBar_pos_and_size()[1][1]:

                    self.view.mouseInsideSideBar(pygame.mouse.get_pos()[1])
                else:
                    self.view.woodPopup_update(0, None)

                    


    # I removed internal objects that required extra packages.
    def clear(self,event):
        print("Doesn't do anything.")

    # Since I removed some commands that required extra packages,
    # probably doesn't do much.
    def my_plot(self,event):
        print("Reads and Prints all the scanned woodnames and the fifth property")
        #self.model.readWoods()
        self.model.printWoods()
       

