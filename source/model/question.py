class Question():
  
  def __init__(self,text, QUESTIONTYPE):
    self.text = text # the question text
    self.type = int(QUESTIONTYPE) # QUESTIONTYPE is enum
    self.facts = [] # the fact associated to the question (only one?)
    self.factTruthValues = [] # the negations associated with the read facts
    self.options = None
    if self.type == 0: #YES/NO question
      self.options = 2 #FactList will have 2 lists
      for i in range(2):
        self.facts.append([])
        self.factTruthValues.append([])
    elif self.type == 1: #3Choice question
      self.options = 3#FactList will have 3 lists
      for i in range(2):
        self.facts.append([])
        self.factTruthValues.append([])
    elif self.type == 2:  #Implement another question type if needed
      pass

    self.askedStatus = False

  def __repr__(self):
    return self.text

  def addFact(self, fact, truthValue, button):
      self.facts[button].append(fact)
      self.factTruthValues[button].append(truthValue)
      fact.addQuestion()

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

  def getFacts(self, answer):
      return self.facts


  def adjustFactValues(self, facts, values):
    for i in range(len(facts)):
            facts[i].setValue(values[i])
            facts[i].deleteQuestion()

  def setTruthValuesToAnsweredFacts(self, answer):
      if(answer == "YES"):
        answerIdx = 0
      elif(answer == "NO"):
        answerIdx = 1
      #For non-YES/NO question with more than 2 answers
      elif(anser == "ANSWER_3"):
        answerIdx = 2
      facts = self.facts[answerIdx]
      values = self.factTruthValues[answerIdx]
      self.adjustFactValues(facts,values)
      self.setAskedStatus()

  def getFactTruthValues(self):
      return self.factTruthValues

  def getOptions(self):
      return self.options

  def getType(self):
      return self.type
