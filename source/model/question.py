
class Question():
  
  def __init__(self,text, fact, QUESTIONTYPE):
    self.text = text # the question text
    self.facts = [] # the fact associated to the question (only one?)
    for x in fact:
      self.facts.append(x)
    self.options = []
    self.type = QUESTIONTYPE # QUESTIONTYPE is enum

  def getText(self):
  	return self.text

  def getFacts(self):
  	return self.facts

  def getOptions(self):
  	return self.options

  def getType(self):
  	return self.type
