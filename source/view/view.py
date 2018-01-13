import pygame
import os

FRAMERATE = 60

TRANSPARENT = (255, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 220, 0)
BLUE = (100, 100, 255)
PURPLE = (220, 0, 220)
ORANGE = (249, 210, 184)
YELLOW = (249, 249, 185)
COLORS = (BLACK, PURPLE, GREEN, BLUE, ORANGE, YELLOW)
GRAYx1 = (200, 200, 200)
GRAYx2 = (150, 150, 150)
GRAYx3 = (100, 100, 100)
GRAYx4 = (50, 50, 50)
GRAY_scale = (WHITE, GRAYx1, GRAYx2, GRAYx3, GRAYx4, BLACK)

BG_COLOR = BLACK

class View():
    '''
    The view currently initializes the frame and "packs" it,
    which means that it arranges the objects in it so as to fill
    the space without much care to the positions.
    Here the side panel is initialized.
    '''
    def __init__(self, pixel_width, pixel_height, model):
        self.model = model

        #Add listener in model
        model.register_listener(self.model_event)

    #Frame sizes, positions, and surface initializations
        self.screen_size = pixel_width, pixel_height
        #Question frame
        self.questionFrame_size = [pixel_width *2/3, pixel_height]
        self.questionFrame_pos = [0,0]
        self.questionFrame_surf = pygame.Surface(self.questionFrame_size)
        self.questionFrame_surf.set_colorkey(TRANSPARENT)
        #Asked questions list frame
        self.askedFrame_size = [pixel_width *2/3 -2, pixel_height*1/3]
        self.askedFrame_pos = [0,pixel_height*2/3]
        self.askedFrame_surf = pygame.Surface(self.askedFrame_size)
        self.askedFrame_surf.set_colorkey(TRANSPARENT)
        #SideBar frame
        self.sideBar_size = [pixel_width / 3, pixel_height]
        self.sideBar_pos = [pixel_width * 2/3, 0]
        self.sideBar_surf = pygame.Surface(self.sideBar_size)
        self.sideBar_surf.set_colorkey(TRANSPARENT)
        #Wood label rectangles
        self.woodLabelRectList = []
        if int(pixel_height / len(model.getWoods())) < 26:
            self.woodLabel_size = [pixel_width / 3, 26]
        else:
            self.woodLabel_size = [pixel_width / 3, pixel_height / len(model.getWoods())]
        #YES/NO Question Response buttons
        self.button_size = [self.questionFrame_size[0]/4, self.questionFrame_size[1]/8]
        self.YESbutton_pos = [self.questionFrame_size[0]/8, (self.questionFrame_size[1]*2/3)*5/8]
        self.NObutton_pos = [self.questionFrame_size[0]*5/8, (self.questionFrame_size[1]*2/3)*5/8]
        #Currently selected wood Popup
        self.woodPopup_selection = None
        self.woodPopup_size = [160*3 + 2, 90*3 + 1 + 200]
        self.woodPopup_pos = [pixel_width * 2/3 - self.woodPopup_size[0] - 2, 0]
        self.woodPopup_surf = pygame.Surface(self.woodPopup_size)
        self.woodPopup_surf.set_colorkey(TRANSPARENT)

        #Initiate Main Frame 
        pygame.init()
        pygame.display.set_caption('WoodType Expert System')
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()

        #Initiate texts, text positions, and text fonts
        self.questionFont = pygame.font.SysFont(None, 40)
        self.questionText_pos = [int(self.questionFrame_size[0]/8), int(self.questionFrame_size[1]/8)]
        self.woodLabelEnglishFont = pygame.font.SysFont(None, 24)
        self.woodLabelLatinFont = pygame.font.SysFont(None, 24, italic=True)
        self.questionText = None    
        self.buttonFont = pygame.font.SysFont(None, 40, italic=True)

    def getSideBar_pos_and_size(self):
        return (self.sideBar_pos, self.sideBar_size)

    def getYESbutton_pos_and_size(self):
    	return (self.YESbutton_pos, self.button_size)

    def getNObutton_pos_and_size(self):
    	return (self.NObutton_pos, self.button_size)

    def mouseInsideSideBar(self, mousePos):
        wv = self.model.getWoods()
        for wood in range(len(wv)):
            #Current Y_displacement on list
            list_disp = wood*self.woodLabel_size[1]
            #label_Ydimensions: [Y_top, Y_bottom]
            lb = [self.sideBar_pos[1] + list_disp, self.sideBar_pos[1] + self.woodLabel_size[1] + list_disp]
            #If cursor currently in woodLabel
            if (mousePos > lb[0] and mousePos < lb[1]):
                self.woodPopup_update(lb[0], wv[wood])

    def woodPopup_update(self, Ypos, woodSelection):
        if self.screen_size[1] - (Ypos + self.woodPopup_size[1]) > 0:
            self.woodPopup_pos[1] = Ypos
        else:
            self.woodPopup_pos[1] = self.screen_size[1] - self.woodPopup_size[1]
        self.woodPopup_selection = woodSelection

    def __draw_askedQuestionFrame(self):
        if(self.model.getNextQuestion() != None):
            self.questionText = self.model.getNextQuestion().getText()
        else:
            self.questionText = None
        self.askedFrame_surf.fill(WHITE)

    def __draw_sideBar(self):
        self.sideBar_surf.fill(TRANSPARENT)
        #Make wood vector a local variable
        wv = self.model.getWoods()
        # Create WoodType Labels
        for wood in range(len(wv)):
            if(wv[wood]):
                newLabel = pygame.Rect(0, wood*self.woodLabel_size[1], self.woodLabel_size[0], self.woodLabel_size[1]-1)
                self.sideBar_surf.fill(WHITE, newLabel)
                self.woodLabelRectList.append(newLabel)
                
    def __draw_woodPopup(self):
        self.woodPopup_surf.fill(YELLOW)

    def redraw(self):
        self.__draw_askedQuestionFrame()
        self.__draw_sideBar()
        self.__draw_woodPopup()

    def blit(self):
        #Blank the screen, draw background later
        self.screen.fill(BG_COLOR)
        self.blit_questionFrame()
        if self.model.getNextQuestion() != None:
            self.blit_buttonText()
        self.blit_questionText()
        self.screen.blit(self.askedFrame_surf, self.askedFrame_pos)
        self.blit_askedQuestionsText()
        self.screen.blit(self.sideBar_surf, self.sideBar_pos)
        self.blit_labelText()
        if self.woodPopup_selection:
            self.screen.blit(self.woodPopup_surf, self.woodPopup_pos)
            self.blit_popUpContent()
        pygame.display.flip()
        self.clock.tick(FRAMERATE)

    def blit_askedQuestionsText(self):
        space = self.questionFont.size(' ')[0]  # The width of a space.
        max_width = self.questionFrame_size[0] - 10
        x, y = self.askedFrame_pos
        if self.model.getQuestions() != None:
            for question in self.model.getAskedQuestions():
                if question.getAskedStatus() == True:
                    text = question.getText() + " -->" + question.getAnswer()
                    words = [word.split(' ') for word in text.splitlines()] # 2D array where each row is a list of words.
                    word_surface = self.woodLabelEnglishFont.render(" -", True, BLACK)
                    self.screen.blit(word_surface, (x, y))
                    x += word_surface.get_size()[0] + space
                    for line in words:
                        for word in line:
                            word_surface = self.woodLabelEnglishFont.render(word, True, BLACK)
                            word_width, word_height = word_surface.get_size()
                            if x + word_width >= max_width:
                                x = self.askedFrame_pos[0] + 30  # Reset the x.
                                y += word_height  # Start on new row.
                            self.screen.blit(word_surface, (x, y))
                            x += word_width + space
                        x = self.askedFrame_pos[0]  # Reset the x.
                        y += word_height  # Start on new row.

    def blit_questionFrame(self):
        self.screen.blit(self.questionFrame_surf, self.questionFrame_pos)
        file_path = os.path.join(os.getcwd(), "view", "backGround.jpeg")
        image = pygame.image.load(file_path).convert()
        image_size = int(self.questionFrame_size[0]), int(self.questionFrame_size[1]*2/3)
        image = pygame.transform.scale(image, image_size)
        self.questionFrame_surf.blit(image, self.questionFrame_pos)

    def blit_popUpContent(self):
        file_name = ""
        if self.woodPopup_selection != None:
            #Picture
            for char in self.woodPopup_selection.getSpanishName():
                if char == " ":
                    file_name = file_name + "_"
                else:
                    file_name = file_name + char
            file_name = file_name + ".jpg"
            file_path = os.path.join(os.getcwd(), "view", "pictures", file_name)
            image = pygame.image.load(file_path).convert()
            image_size = 160*3, 90*3
            image = pygame.transform.scale(image, image_size)
            self.woodPopup_surf.blit(image, (1,1))
            #Text
            y_displacement = 0
            for item in self.woodPopup_selection.getInfo_from_appliedFilters():
                text_surface = self.woodLabelEnglishFont.render("- " + item, True, BLACK)
                self.screen.blit(text_surface, (self.woodPopup_pos[0] + 15,\
                    self.woodPopup_pos[1] + (1 + image_size[1] + 3 + y_displacement)))
                y_displacement = y_displacement + text_surface.get_size()[1]


    def blit_questionText(self):
        space = self.questionFont.size(' ')[0]  # The width of a space.
        max_width = self.questionFrame_size[0] * 7 / 8
        x, y = self.questionText_pos
        if not self.model.getEnd():
            words = [word.split(' ') for word in self.questionText.splitlines()] # 2D array where each row is a list of words.
            for line in words:
                for word in line:
                    word_surface = self.questionFont.render(word, True, WHITE)
                    word_width, word_height = word_surface.get_size()
                    if x + word_width >= max_width:
                        x = self.questionText_pos[0]  # Reset the x.
                        y += word_height  # Start on new row.
                    self.screen.blit(word_surface, (x, y))
                    x += word_width + space
                x = self.questionText_pos[0]  # Reset the x.
                y += word_height  # Start on new row.
        else:
            endText = "The available woods appear in the list on the right."
            filters = self.model.getActivatedFilterDescription()
            if filters != "":
                endText = endText + " They have been ordered according to their " + filters
            endText = endText + " Use the wood pictures to choose your favourite."
            words = [word.split(' ') for word in endText.splitlines()]
            for line in words:
                for word in line:
                    word_surface = self.questionFont.render(word, True, WHITE)
                    word_width, word_height = word_surface.get_size()
                    if x + word_width >= max_width:
                        x = self.questionText_pos[0]  # Reset the x.
                        y += word_height  # Start on new row.
                    self.screen.blit(word_surface, (x, y))
                    x += word_width + space
                x = self.questionText_pos[0]  # Reset the x.
                y += word_height  # Start on new row.


    def blit_labelText(self):
        wv = self.model.getWoods()
        for wood in range(len(wv)):
            if(wv[wood]):
                englishText = self.woodLabelEnglishFont.render(wv[wood].getEnglishName(), True, RED)
                latinText = self.woodLabelLatinFont.render(" (" + wv[wood].getLatinName() + ") ", True, RED)
                textStartYPos = (self.woodLabel_size[1] - englishText.get_size()[1])/2
                self.screen.blit(englishText, (self.sideBar_pos[0]+10, wood*self.woodLabel_size[1]+textStartYPos))
                self.screen.blit(latinText, ((self.sideBar_pos[0]+10) + \
                (englishText.get_width() + 2), wood*self.woodLabel_size[1]+textStartYPos))

    def blit_buttonText(self):
        YESbutton = pygame.Rect(self.YESbutton_pos, self.button_size)
        NObutton = pygame.Rect(self.NObutton_pos, self.button_size)
        self.questionFrame_surf.fill(WHITE, YESbutton)
        self.questionFrame_surf.fill(WHITE, NObutton)
        YEStext = self.buttonFont.render("YES", True, BLACK)
        NOtext = self.buttonFont.render("NO", True, BLACK)
        YEStext_size = YEStext.get_size()
        NOtext_size = NOtext.get_size()
        self.screen.blit(YEStext, (self.YESbutton_pos[0] + (self.button_size[0]-YEStext_size[0])/2,\
            self.YESbutton_pos[1] + (self.button_size[1]-YEStext_size[1])/2))
        self.screen.blit(NOtext, (self.NObutton_pos[0] + (self.button_size[0]-NOtext_size[0])/2,\
            self.NObutton_pos[1] + (self.button_size[1]-NOtext_size[1])/2))

    def model_event(self, event_name):
        #In case you want to redraw only part of the screen use the if-statements with event names
        if event_name == "woodTypes_rearranged":
            self.__draw_sideBar()
            self.__draw_woodPopup()
            self.blit()

        if event_name == "next_question":
            self.__draw_sideBar()
            self.__draw_woodPopup()
            self.__draw_questionFrame()
            self.blit()

        #Else just redraw everything
        self.redraw()
        self.blit()
