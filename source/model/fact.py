from enum import Enum


class factValue(Enum):
    UNKNOWN = 1,
    TRUE = 2,
    FALSE = 3,
    MAYBE = 4


class Fact:
    """
    This class should represent the facts which are contained in rules.
    """

    def __init__(self, name, model):
        self.value = factValue.UNKNOWN  # Possible values: UNKNOWN, TRUE, FALSE, MAYBE
        self.name = name
        self.numQuestions = 0
        self.model = model

    def isType(self):
        return "Normal"

    def getName(self):
        return self.name

    def setValue(self, val):
        # print(self, " was adjusted to ", val)
        self.value = val

    def getValue(self):
        return self.value

    def addQuestion(self):
        self.numQuestions += 1

    def deleteQuestion(self):
        self.numQuestions -= 1

    def canBeAskedFor(self):
        return self.numQuestions > 0

    def getNumQuestions(self):
        return self.numQuestions

    def __repr__(self):
        return "FactName: " + self.name + "| FactVal: " + repr(self.value)

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
    def __init__(self, name, prop, description, weight, model):
        super().__init__(name, model)
        self.prop = prop
        self.description = description
        self.weight = int(weight)

    def activate(self):
        # print("Ordering of ", self.prop, " was given the weight ", self.weight)
        self.model.adjustWeight(self.prop, self.weight)

    def getDescription(self):
        return self.description

    def isType(self):
        return "Order"


# filters out all the wood types with the specified prop(erty) set to the specified boolean
class filteringFact(Fact):
    def __init__(self, name, prop, boolean, model):
        super().__init__(name, model)
        self.prop = prop
        self.boolean = boolean

    def isType(self):
        return "Filter"

    def activate(self):
        # print("Filtering of ", self.prop, " activated.")
        cnt = 0
        for wood in self.model.getWoods():
            for prop in wood.getProperties():
                # print("|", prop[0], "|", self.prop, "|")
                if prop[0] == self.prop:

                    # print(prop[1], " and ", self.boolean)
                    if prop[1] == self.boolean:
                        cnt += 1
                        # print("Filtering ", wood.getEnglishName(), " because of ", prop[0], " is set to ", prop[1])
                        wood.filterOut(self.prop)

                    break
        # print(cnt, " woods were filtered out.")
