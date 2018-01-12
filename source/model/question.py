class Question():
  
  def __init__(self,text, QUESTIONTYPE, factList, factValueList):
    self.text = text # the question text
    self.type = int(QUESTIONTYPE) # QUESTIONTYPE is enum
    self.facts = [] # the fact associated to the question (only one?)
    self.factTruthValues = [] # the negations associated with the read facts
    self.options = None
    if self.type == 0: #YES/NO question
      self.options = 2 #FactList will have 2 lists
      self.facts = factList
      self.factTruthValues = factValueList
    elif self.type == 1: #3Choice question
      self.options = 3#FactList will have 3 lists
      self.facts = factList
    elif self.type == 2:  #Implement another question type if needed
      pass

    self.askedStatus = False

  def __repr__(self):
    return self.text

  def getType(self):
      return self.type

  def setAskedStatus(self):
      self.askedStatus = True

  def getAskedStatus(self):
      return self.askedStatus

  def getText(self):
      return self.text

  def getAllFacts(self):
    if( self.type == 0 ):
        return self.facts[0] + self.facts[1]

  def getFacts(self):
      return self.facts

  def getFactTruthValues(self):
      return self.factTruthValues

  def getOptions(self):
      return self.options

  def getType(self):
      return self.type
