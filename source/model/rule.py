from .fact import factValue

class Rule():
    def __init__(self):
        self.premises = []  # list of all the facts that need to be true
        self.truthValues = []  # list of truth values associated to list of facts
        self.available = True
        self.conclusion = None
        self.conclusionTruthValue = None

    def __repr__(self):
        return "rule with concl: "+ self.conclusion.__repr__()


    def addPremise(self, fact, truthValue):
        self.premises.append(fact)
        self.truthValues.append(truthValue)

    def addConclusion(self, fact, truthValue):
        self.conclusion = fact
        self.conclusionTruthValue = truthValue

    def getPremises(self):
        return self.premises

    def canFire(self):
        if( self.available is False ):
            return False
        if( self.conclusion.getValue() is not factValue.UNKNOWN ):
            self.available = False
            return False
        
        canFire = True
        for i in range(len(self.premises)):
            # if a premise has an incorrect truth value, the rule can't fire anymore
            factVal = self.premises[i].getValue()
            truthVal = self.truthValues[i]
            if( factVal == factValue.TRUE and truthVal == factValue.FALSE 
                or factVal == factValue.FALSE and truthVal == factValue.TRUE ):
                print(self, " set to NOT available.")
                self.available = False
                canFire = False
                break
            if( factVal == factValue.UNKNOWN or factVal == factValue.MAYBE):
                canFire = False

        return canFire



    def isAvailable(self):
        return self.available

    def fire(self):
        print(self, " just fired!")
        self.available = False
        if( self.conclusionTruthValue == factValue.TRUE ):
            self.conclusion.setValue(factValue.TRUE)
        else:
            self.conclusion.setValue(factValue.FALSE)
        self.conclusion.activate()  # if conclusion is a decisive fact then activate its consequences

    def setAvailable(self, isAvailable):
        self.available = isAvailable
