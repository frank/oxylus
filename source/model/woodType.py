

class WoodType():
  count = 0;  
  admissibleWoods = 0
  dismissedWoods = 0

  def __init__(self, englishName, latinName):
    self.englishName = englishName # name of the wood 
    self.latinName = latinName # name of wood in latin
    #self.image = loadImage..
    self.properties = [] #list of properties associated to the wood type
                         #each property has a value and a boolean to indicate if that property 
                         #still fulfills the criteria set by the user
                         # a property also has a name
    
    self.admissible  = True
    WoodType.count           += 1
    WoodType.admissibleWoods += 1

  def getEnglishName(self):
    return self.englishName

  def getLatinName(self):
    return self.latinName
  
  def addProperty(self, name, value):
    self.properties.append([name,value,True])

  def updatePropertyAdmission(self, name, value, comparisonType ):
    for prop in self.properties:
      # We need to add the enum type that encompasses HIGHER, LOWER and EQUAL.
      if ( prop[0] == name and 
         (comparisonType == HIGHER and prop[1] <= value or
         comparisonType == LOWER  and prop[1] >= value or
         comparisonType == EQUAL  and prop[1] != value) ):
          prop[2] = False
          self.setDismissed()

  def setDismissed(self):
    if self.admissible == true:
      self.admissible = false
      dismissedWoods  += 1
      admissibleWoods -= 1 

  def print(self):
    print("This is the wood named ", self.englishName, " with the following property values:", 		end='')
    for prop in self.properties:
      print(" ",prop[1] , end = '')
    print('')
