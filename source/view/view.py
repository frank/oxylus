import pygame
import os

FRAMERATE = 60

TRANSPARENT = (255, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
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
        self.RESETbutton_size = [self.questionFrame_size[0]/8, self.questionFrame_size[1]*3/64]
        self.RESETbutton_pos = [self.questionFrame_size[0]*13/16, self.questionFrame_size[1]/48]

        #Currently selected wood Popup
        self.woodPopup_selection = None
        self.woodPopup_size = [160*3 +4 , 90*3 +4]
        self.woodPopup_pos = [pixel_width * 2/3 - self.woodPopup_size[0] - 2, 0]
        self.woodPopup_surf = pygame.Surface(self.woodPopup_size)
        self.woodPopup_surf.set_colorkey(TRANSPARENT)

        #Initiate Main Frame 
        pygame.init()
        pygame.display.set_caption('WoodType Expert System')
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()

        #Initiate texts, text positions, and text fonts
        self.questionFont = pygame.font.SysFont("Sans", 36, bold=True)
        self.questionText_pos = [int(self.questionFrame_size[0]/8), int(self.questionFrame_size[1]/16+10)]
        self.woodLabelEnglishFont = pygame.font.SysFont("Sans", 18)
        self.woodLabelLatinFont = pygame.font.SysFont("Sans", 18, italic=True)
        self.buttonFont = pygame.font.SysFont("Sans", 40, italic=True, bold=True)

    def reset(self):
        self.woodLabelRectList = []
        self.redraw()

    def getSideBar_pos_and_size(self):
        return (self.sideBar_pos, self.sideBar_size)

    def getYESbutton_pos_and_size(self):
    	return (self.YESbutton_pos, self.button_size)

    def getNObutton_pos_and_size(self):
    	return (self.NObutton_pos, self.button_size)

    def getRESETbutton_pos_and_size(self):
        return (self.RESETbutton_pos, self.RESETbutton_size)

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
        self.blit_questionText()
        self.blit_buttons()
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
                    text = question.getText()
                    if question.getAnswer() == "YES":
                        text = text + " Yes."
                    if question.getAnswer() == "NO":
                        text = text + " No."
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
        image_size = int(self.questionFrame_size[0]-2), int(self.questionFrame_size[1]*2/3)
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
            self.woodPopup_surf.blit(image, (2,2))
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
            words = [word.split(' ') for word in self.model.getNextQuestion().getText().splitlines()] # 2D array where each row is a list of words.
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
            if self.model.getNextQuestion().getDescription() != None:
                y += word_height
                descriptionWords = [word.split(' ') for word in self.model.getNextQuestion().getDescription().splitlines()] # 2D array where each row is a list of words.
                for line in descriptionWords:
                    for word in line:
                        word_surface = self.woodLabelEnglishFont.render(word, True, WHITE)
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
            endText = endText + " Use the pictures to choose your favourite."
            endText = endText + " The greener the wood name, the better suited it is for the purpose you chose."
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

        maxRankVal = max(wv, key = lambda wood: wood.getRanking()).getRanking()
        minRankVal = min(wv, key = lambda wood: wood.getRanking()).getRanking()
        difference = maxRankVal - minRankVal
      
        for wood in range(len(wv)):
            if(wv[wood]):
                currentWoodRankVal = wv[wood].getRanking()
                


                if( currentWoodRankVal == maxRankVal ):
                    woodNameColor = GREEN
                elif ( currentWoodRankVal <= 0 ):
                    woodNameColor = RED
                else:
                    x = (maxRankVal - currentWoodRankVal) / difference
                    redPart = int(x * 255)
                    greenPart = int((1-x) * 255) 
                    woodNameColor = [redPart , greenPart ,0]

                englishText = self.woodLabelEnglishFont.render(wv[wood].getEnglishName(), True, woodNameColor)
                latinText = self.woodLabelLatinFont.render(" (" + wv[wood].getLatinName() + ") ", True, woodNameColor)
                textStartYPos = (self.woodLabel_size[1] - englishText.get_size()[1])/2
                self.screen.blit(englishText, (self.sideBar_pos[0]+10, wood*self.woodLabel_size[1]+textStartYPos))
                self.screen.blit(latinText, ((self.sideBar_pos[0]+10) + \
                (englishText.get_width() + 2), wood*self.woodLabel_size[1]+textStartYPos))

    def blit_buttons(self):
        if self.model.getNextQuestion() != None:
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
        RESETbutton1 = pygame.Rect(self.RESETbutton_pos, self.RESETbutton_size)
        RESETbutton2 = pygame.Rect((self.RESETbutton_pos[0]+3,self.RESETbutton_pos[1]+3),\
            (self.RESETbutton_size[0]-6,self.RESETbutton_size[1]-6))
        self.questionFrame_surf.fill(BLUE, RESETbutton1)
        self.questionFrame_surf.fill(GRAYx2, RESETbutton2)
        RESETtext = self.woodLabelEnglishFont.render("Reset", True, BLACK)
        RESETtext_size = RESETtext.get_size()
        self.screen.blit(RESETtext, (self.RESETbutton_pos[0] + (self.RESETbutton_size[0]-RESETtext_size[0])/2,\
            self.RESETbutton_pos[1] + (self.RESETbutton_size[1]-RESETtext_size[1])/2))
        
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
