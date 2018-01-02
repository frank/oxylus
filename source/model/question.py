
class Question():
  
  def __init__(self,text, QUESTIONTYPE, factList):
    self.text = text # the question text
    self.type = int(QUESTIONTYPE) # QUESTIONTYPE is enum
    self.facts = [] # the fact associated to the question (only one?)
    self.options = None
    if self.type == 0: #YES/NO question
      self.options = 2 #FactList will have 2 lists
      self.facts = factList
    elif self.type == 1: #3Choice question
      self.options = 3#FactList will have 3 lists
      self.facts = factList
    elif self.type == 2:  #Implement another question type if needed
      pass

  def getText(self):
  	return self.text

  def getFacts(self):
  	return self.facts

  def getOptions(self):
  	return self.options

  def getType(self):
  	return self.type
