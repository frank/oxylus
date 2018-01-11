class Rule():

    def __init__(self, conclusion):
        self.conclusion = conclusion
        self.conclusion.setIsConclusion(True)
        self.premises = []  # list of all the facts that need to be true
        self.truthValues = []  # list of truth values associated to list of facts
        self.available = True

    def addPremise(self, fact, truthValue):
        self.premises.append(fact)
        self.truthValues.append(truthValue)

    def getPremises(self):
        return self.premises

    def canFire(self):
        if self.available is False:
            return False
        for i in range(0, len(self.premises)):
            # if a premise has an incorrect truth value, the rule can't fire anymore
            if (self.premises[i].getValue() == TRUE and
                    self.negations[i] == False or
                    self.premises[i].getValue() == FALSE and
                    self.negations[i] == True or
                    self.premises[i].getValue() == MAYBE):
                self.available = False
                return False
        return True

    def isAvailable(self):
        return self.available

    def fire(self):
        self.available = False
        self.conclusion.setTrue()
        self.conclusion.activate()  # if conclusion is a decisive fact then activate its consequences

    def setAvailable(self, isAvailable):
        self.available = isAvailable
