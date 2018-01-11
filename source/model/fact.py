from enum import Enum
import model

class factValue(Enum):
    UNKNOWN = 1,
    TRUE = 2,
    FALSE = 3,
    MAYBE = 4

class Fact():
    """
    This class should represent the facts which are contained in rules.
    """

    def __init__(self, name, model):
        self.value = factValue.UNKNOWN  # Possible values: UNKNOWN, TRUE, FALSE, MAYBE
        self.name = name
        self.isConclusion = False
        self.model = model

    
    def setValue(self, val):
        self.value = val

    def getValue(self):
        return self.value


    def setIsConclusion(self, boolean):
        self.isConclusion = boolean

    def isConclusion(self):
        return self.isConclusion

    def __repr__(self):
        return "This is the fact named: " + self.name

    def activate(self):
        pass

'''
# if a decisive fact is set to TRUE it will trigger the elimination of a wood type
class decisiveFact(Fact):
    def __init__(self, name, woodName, model):
        super().__init__(name, model)
        self.woodName = woodName

    def activate(self):
        for wood in self.model.getWoods():
            if (wood.englishName == self.woodName):
                wood.filterOut()
'''

# gives the ordering criterion column with the name prop a weight 
# prop can be: density, price, supply, outsideUse, hardness
class orderingFact(Fact):
    def __init__(self, name, prop, weight, model):
        super().__init__(name, model)
        self.prop = prop
        self.weight = weight

    def activate(self):
        self.model.adjustWeight(self.prop, self.weight)


# filters out all the wood types with the specified prop(erty) set to the specified boolean
class filteringFact(Fact):
    def __init__(self, name, prop, boolean, model):
        super().__init__(name, model)
        self.prop = prop
        self.boolean = boolean

    def activate(self):
        for wood in self.model.getWoods():
            for prop in wood.getProperties():
                if (prop[0] == prop):
                    if (prop[1] == boolean):
                        wood.filterOut(self.prop)
                    else:
                        break
