from view.view import *


class Controller:
    """
    Initializing the 'root' main container, the model, the view,
    """

    def __init__(self, model, view):

        self.model = model
        self.view = view
        self.running = True

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    # if YES button was clicked
                    if self.model.getNextQuestion() != None and not self.model.getEnd():
                        if pygame.mouse.get_pos()[0] > self.view.getYESbutton_pos_and_size()[0][0] and \
                                pygame.mouse.get_pos()[1] > self.view.getYESbutton_pos_and_size()[0][1] and \
                                pygame.mouse.get_pos()[0] < self.view.getYESbutton_pos_and_size()[0][0] + \
                                self.view.getYESbutton_pos_and_size()[1][0] and \
                                pygame.mouse.get_pos()[1] < self.view.getYESbutton_pos_and_size()[0][1] + \
                                self.view.getYESbutton_pos_and_size()[1][1]:
                            self.model.setAnswerToQuestion("YES")
                        # if NO button was clicked
                        if pygame.mouse.get_pos()[0] > self.view.getNObutton_pos_and_size()[0][0] and \
                                pygame.mouse.get_pos()[1] > self.view.getNObutton_pos_and_size()[0][1] and \
                                pygame.mouse.get_pos()[0] < self.view.getNObutton_pos_and_size()[0][0] + \
                                self.view.getNObutton_pos_and_size()[1][0] and \
                                pygame.mouse.get_pos()[1] < self.view.getNObutton_pos_and_size()[0][1] + \
                                self.view.getNObutton_pos_and_size()[1][1]:
                            self.model.setAnswerToQuestion("NO")
                    # if RESET button was clicked
                    if pygame.mouse.get_pos()[0] > self.view.getRESETbutton_pos_and_size()[0][0] and \
                            pygame.mouse.get_pos()[1] > self.view.getRESETbutton_pos_and_size()[0][1] and \
                            pygame.mouse.get_pos()[0] < self.view.getRESETbutton_pos_and_size()[0][0] + \
                            self.view.getRESETbutton_pos_and_size()[1][0] and \
                            pygame.mouse.get_pos()[1] < self.view.getRESETbutton_pos_and_size()[0][1] + \
                            self.view.getRESETbutton_pos_and_size()[1][1]:
                        self.model.reset()
                        self.view.reset()
            elif event.type == pygame.MOUSEMOTION:
                # if in sidebar
                if pygame.mouse.get_pos()[0] > self.view.getSideBar_pos_and_size()[0][0] and \
                        pygame.mouse.get_pos()[1] > self.view.getSideBar_pos_and_size()[0][1] and \
                        pygame.mouse.get_pos()[0] < self.view.getSideBar_pos_and_size()[0][0] + \
                        self.view.getSideBar_pos_and_size()[1][0] and \
                        pygame.mouse.get_pos()[1] < self.view.getSideBar_pos_and_size()[0][1] + \
                        self.view.getSideBar_pos_and_size()[1][1]:

                    self.view.mouseInsideSideBar(pygame.mouse.get_pos()[1])
                else:
                    self.view.woodPopup_update(0, None)
