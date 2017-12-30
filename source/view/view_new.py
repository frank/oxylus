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
    def __init__(self, width, height, model):
        self.model = model
        self.woodLabelList = []

        #Add listener in model
        model.register_listener(self.model_event)

        #Frame sizes and positions
        self.screen_size = pixel_width, pixel_height
        self.questionFrame_size = pixel_width * 2/3, pixel_height
        self.questionFrame_pos = 0,0
        self.sideBar_size = pixel_width / 3, pixel_height
        self.sideBar_pos = pixel_width * 2/3, 0
        self.woodLabel_size = pixel_width / 3, pixel_height / len(model.getWoods())

        #Currently selected wood Popup
        self.woodPopup_selection = None
        self.woodPopup_size = 400, 300
        self.woodPopup_pos = pixel_width * 2/3 - woodPopup_size[0], 0        

        #Initiate Frame 
        pygame.init()
        pygame.display.set_caption('WoodType Expert System')
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()

        #Initiate surfaces
        self.questionFrame_surf = pygame.Surface(self.screen_size)
        self.questionFrame_surf.set_colorkey(TRANSPARENT)

        self.sideBar_surf = pygame.Surface(self.sideBar_size)
        self.sideBar_surf.set_colorkey(TRANSPARENT)

        self.woodPopup_surf = pygame.Surface(self.screen_size)
        self.woodPopup_surf.set_colorkey(TRANSPARENT)

    def getSideBar_pos_and_size():
    	return (self.sideBar_pos, self.sideBar_size)

    def mouseInsideSideBar(mousePos):
    	pass

    def woodPopup_update(pos, woodSelection):
    	self.woodPopup_pos[1] = woodLabel_size[1] * int(pos[1] / woodLabel_size[1])
    	self.woodPopup_selection = woodSelection

	def __draw_questionFrame(self):
        self.select_surf.fill(TRANSPARENT)
        self.model.

    def __draw_sideBar(self):
    	self.game_surf.fill(TRANSPARENT)
    	#Make wood vector a local variable
    	wv = self.model.getWoods()
    	# Create WoodType Labels
        for wood in range(len(wv)):
        	if(wv[wood]):
	            newLabel = pygame.Rect((self.woodLabel_size[0], wood*self.woodLabel_size[1]), self.woodLabel_size)
	            self.game_surf.fill(WHITE, newLabel)
	            self.screen.blit(self.font.render('Hello!', True, (255,0,0)), (200, 100))
	            self.woodLabelList.append(newLabel)

	def __draw_woodPopup(self, event, master, model, frame1, woodDisplay, woodLabel, woodNumber):
		pass
	    # deleteContents(event, woodDisplay)
	    # #print(event.y, woodLabel.winfo_height(), master.winfo_y())
	    # woodDisplay.place(x = frame1.winfo_width() - woodDisplay.winfo_width(),\
	    #  y = event.y_root - master.winfo_y() -  event.y)
	    # woodDisplay.pack_propagate(False) #Force woodDisplay to not change size as things are packed in it
	    # master.update_idletasks()
	    # # Insert wood picture
	    # file_path = os.getcwd() + r"\view\pictures\Olivo.jpg"
	    # photo = Image.open(file_path)
	    # pWidth, pHeight = photo.size
	    # print(pWidth, pHeight)
	    # ratio = pWidth/pHeight
	    # print(woodDisplay.winfo_height(), ratio, (woodDisplay.winfo_height()-25)*ratio)
	    # photo = photo.resize((int((woodDisplay.winfo_height()-25)*ratio), woodDisplay.winfo_height()-25), Image.ANTIALIAS)
	    # photo = ImageTk.PhotoImage(photo)
	    # woodPicture = tk.Label(woodDisplay, image = photo)
	    # woodPicture.image = photo
	    # woodPicture.pack(side = tk.LEFT)
	    # #Create Text box
	    # textBox = tk.Frame(woodDisplay)
	    # textBox.pack(side = tk.RIGHT, fill = tk.BOTH)
	    # # Inser Wood Name
	    # print(woodNumber)
	    # woodText = tk.Label(textBox, text = str(model.getWoods()[woodNumber].getEnglishName()), fg = "black")
	    # woodText.grid(row = 1)
	    # # Insert Text
	    # woodText = tk.Label(textBox, text = "Something Something", fg = "black")
	    # woodText.grid(row = 4)

	    # master.update_idletasks()
    
	def redraw(self):
        self.__draw_questionFrame()
        self.__draw_sideBar()
        self.__draw_woodPopup()

    def blit(self):
    	#Blank the screen, draw background later
        self.screen.fill(BG_COLOR)
        self.screen.blit(self.questionFrame_surf, self.questionFrame_pos)
        self.screen.blit(self.sideBar_surf, self.questionFrame_pos)
        if self.woodPopup_selection:
            self.screen.blit(self.select_surf, self.woodPopup_pos)
        pygame.display.flip()
        self.clock.tick(FRAMERATE)

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
