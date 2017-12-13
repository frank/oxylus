

class Rule():
  
  def __init__(self, conclusion):
    self.conclusion = conclusion
    self.premises = [] # list of all the facts that need to be true
    self.negations = [] # list of negations associated to list of facts   

  def addPremise(fact, negate):
    self.premises.append(fact)
    self.negations.append(negate)
