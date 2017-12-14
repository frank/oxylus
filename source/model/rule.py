

class Rule():
  
  def __init__(self, conclusion):
    self.conclusion = conclusion
    self.premises = [] # list of all the facts that need to be true
    self.negations = [] # list of negations associated to list of facts   
    self.fired = False
    self.available = True

  def addPremise(self,fact, negate):
    self.premises.append(fact)
    self.negations.append(negate)

  def canFire(self):
    for i in range(0, len(premises)):
      # if a premise has an incorrect truth value, the rule can't fire anymore
      if premises[i].getValue() == TRUE and
         negations[i] == False or
         premises[i].getValue() == FALSE and
         negations[i] == True or
         premises[i].getValue() == MAYBE: #we might want to adopt our policy on MAYBE's later on
        return False
    return True

  def fire(self):
    self.conclusion.setTrue()
    self.conclusion.activate() # if conclusion is a decisive fact then activate its consequences
