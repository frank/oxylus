from .fact import factValue

class Rule():
    def __init__(self):
        self.premises = []  # list of all the facts that need to be true
        self.truthValues = []  # list of truth values associated to list of facts
        self.available = True
        self.conclusion = None
        self.conclusionTruthValue = None

    def __repr__(self):
        return "This is a rule with the following conclusion "+ self.conclusion.__repr__()


    def addPremise(self, fact, truthValue):
        self.premises.append(fact)
        self.truthValues.append(truthValue)

    def addConclusion(self, fact, truthValue):
        self.conclusion = fact
        self.conclusionTruthValue = truthValue

    def getPremises(self):
        return self.premises

    def canFire(self):
        if self.available is False:
            return False
        # the first truthvalue belongs to the conclusion:
        for i in range(0, len(self.premises)):
            # if a premise has an incorrect truth value, the rule can't fire anymore
            factVal = self.premises[i].getValue()
            if( factVal == factValue.TRUE and self.truthValues[i] == factValue.FALSE 
                or factVal == factValue.FALSE and self.truthValues[i] == factValue.TRUE):
                print("eyy")
                #self.available = False
                return False
        return True

    def isAvailable(self):
        return self.available

    def fire(self):
        self.available = False
        if( self.truthValues[0] == True ):
            self.conclusion.setValue(factValue.TRUE)
        else:
            self.conclusion.setValue(factValue.FALSE)
        self.conclusion.activate()  # if conclusion is a decisive fact then activate its consequences

    def setAvailable(self, isAvailable):
        self.available = isAvailable
