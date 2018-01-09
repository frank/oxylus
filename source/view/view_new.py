import pygame
import PIL
from PIL import ImageTk, Image
import os

FRAMERATE = 60

TRANSPARENT = (255, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 220, 0)
BLUE = (0, 0, 220)
PURPLE = (220, 0, 220)
COLORS = (BLACK, PURPLE, GREEN, BLUE)

BG_COLOR = BLACK

class View_new():
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
        self.YESbutton_pos = [self.questionFrame_size[0]/8, self.questionFrame_size[1]*5/8]
        self.NObutton_pos = [self.questionFrame_size[0]*5/8, self.questionFrame_size[1]*5/8]
        #Currently selected wood Popup
        self.woodPopup_selection = None
        self.woodPopup_size = [600, 300]
        self.woodPopup_pos = [pixel_width * 2/3 - self.woodPopup_size[0] - 1, 0]
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

    def __draw_questionFrame(self):
        self.questionFrame_surf.fill(BLACK)
        self.questionText = self.model.getNextQuestion().getText()
        YESbutton = pygame.Rect(self.YESbutton_pos, self.button_size)
        NObutton = pygame.Rect(self.NObutton_pos, self.button_size)
        self.questionFrame_surf.fill(WHITE, YESbutton)
        self.questionFrame_surf.fill(WHITE, NObutton)

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
        self.woodPopup_surf.fill(WHITE)
    
    def redraw(self):
        self.__draw_questionFrame()
        self.__draw_sideBar()
        self.__draw_woodPopup()

    def blit(self):
        #Blank the screen, draw background later
        self.screen.fill(BG_COLOR)
        self.screen.blit(self.questionFrame_surf, self.questionFrame_pos)
        self.screen.blit(self.sideBar_surf, self.sideBar_pos)
        self.blit_questionText()
        self.blit_labelText()
        self.blit_buttonText()
        if self.woodPopup_selection:
            self.screen.blit(self.woodPopup_surf, self.woodPopup_pos)
            self.blit_popUpContent()
        pygame.display.flip()
        self.clock.tick(FRAMERATE)

    def blit_popUpContent(self):
        file_name = ""
        if self.woodPopup_selection != None:
            for char in self.woodPopup_selection.getSpanishName():
                if char == " ":
                    file_name = file_name + "_"
                else:
                    file_name = file_name + char
            file_name = file_name + ".jpg"
            file_path = os.getcwd() + r"\view\pictures\\" + file_name
            image = pygame.image.load(file_path).convert()
            pygame.transform.scale(image, (300,200))
            self.woodPopup_surf.blit(image, (2,2))

    def blit_questionText(self):
        words = [word.split(' ') for word in self.questionText.splitlines()] # 2D array where each row is a list of words.
        space = self.questionFont.size(' ')[0]  # The width of a space.
        max_width = self.questionFrame_size[0]*7/8
        x, y = self.questionText_pos
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
                self.screen.blit(englishText, (self.sideBar_pos[0]+10, wood*self.woodLabel_size[1]+2))
                self.screen.blit(latinText, ((self.sideBar_pos[0]+10) + \
                (englishText.get_width() + 2), wood*self.woodLabel_size[1]+2))

    def blit_buttonText(self):
        YEStext = self.buttonFont.render("YES", True, BLACK)
        NOtext = self.buttonFont.render("NO", True, BLACK)
        YEStext_size = YEStext.get_size()
        NOtext_size = NOtext.get_size()
        self.screen.blit(YEStext, (self.YESbutton_pos[0] + (self.button_size[0]-YEStext_size[0])/2,\
            self.YESbutton_pos[1] + (self.button_size[1]-YEStext_size[1])/2))
        self.screen.blit(NOtext, (self.NObutton_pos[0] + (self.button_size[0]-NOtext_size[0])/2,\
            self.NObutton_pos[1] + (self.button_size[1]-NOtext_size[1])/2))

    def model_event(self, event_name, data):
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
