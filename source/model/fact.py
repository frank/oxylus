from enum import Enum


class factValue(Enum):
    UNKNOWN = 1,
    TRUE = 2,
    FALSE = 3,
    MAYBE = 4


class Fact():
    '''
    This class should represent the facts which are contained in rules.
    '''

    def __init__(self, name):
        self.value = factValue.UNKNOWN  # Possible values: UNKNOWN, TRUE, FALSE, MAYBE
        self.name = name
        self.isConclusion = False

    def isConclusion(boolean):
        self.isConclusion = boolean

    def print(self):
        print("This is the fact named: ", self.name)


# if a decisive fact is set to TRUE it will trigger the elimination of a wood type
class decisiveFact(Fact):
    def __init__(self, name, woodName):
        super().__init__(name)
        self.woodName = woodName
        pass

# gives the ordering criterion column with the name prop a weight 
class orderingFact(Fact):
  
    def __init__(self, name, prop, weight):
        super().__init__(name)
        self.prop = prop
        self.weight = weight

# filters out all the wood types with the specified prop(erty) set to the specified boolean
class filteringFact(Fact):

    def __init__(self, name, prop, boolean):
        super().__init__(name)
        self.prop = prop
        self.boolean = boolean
