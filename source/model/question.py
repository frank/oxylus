
class Question():
  
  def __init__(self,text, fact, QUESTIONTYPE):
    self.text = text # the question text
    self.fact = fact # the fact associated to the question (only one?)
    self.options = []
    self.type = QUESTIONTYPE # QUESTIONTYPE is enum
