

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
    count           += 1
    admissibleWoods += 1
  
  def addProperty(name, value)
    self.properties.append([name,value,True])

  def updatePropertyAdmission(name, value, comparisonType ):
    for prop in self.properties:
      # We need to add the enum type that encompasses HIGHER, LOWER and EQUAL.
      if prop[0] == name and 
         (comparisonType == HIGHER and prop[1] <= value or
         comparisonType == LOWER  and prop[1] >= value or
         comparisonType == EQUAL  and prop[1] != value):
          prop[2] = False
          self.setDismissed()

  def setDismissed():
    if self.admissible == true:
      self.admissible = false
      dismissedWoods  += 1
      admissibleWoods -= 1 

          
          
