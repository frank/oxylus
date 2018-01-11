from enum import Enum
import csv
from .woodType import WoodType
from .rule import Rule
from .fact import *
from .question import Question


class Model():
    def __init__(self):
        # Listener for model events
        self.listeners = []
        self.woods = []  # list of all the woodtypes
        self.facts = []  # list of all facts
        self.rules = []  # list of all rules
        self.questions = []  # list of all questions
        self.filteredWoods = []
        self.orderingWeights = {"DensityAvg": 0, "Price": 0, "Ease of supply": 0, "Exterior Carpentry": 0, "Hardness": 0}
        self.currentQuestion = None

        self.readFacts()
        self.readRules()
        self.readWoods()
        self.readQuestions()
        self.next_question(self.questions[0])

    def update(self):
        self.forwardChain()
        self.fireRules()
        self.updateWoodTypes()
        self.reorderWoods()
        nextFact = self.nextFactToAskFor()
        self.findQuestionToAskFor(nextFact)

    def updateWoodTypes():
        for fact in self.facts:
            if (fact.value == factValue.TRUE):
                fact.activate()

    # reorders the woods list according to the weights and filters
    def reorderWoods():
        # filter woods first:
        for wood in self.woods:
            if( wood.isAvailable() == False ):
                self.filteredWoods.append(wood)
                self.woods.remove(wood)
            else:
                wood.setRanking(weights)
        # order woods according to ranking:
        woods = sorted(woods, key=lambda wood: wood.getRanking()) 

        

    def fireRules(self):
        i = 0
        while i < len(self.rules):
            if self.rules[i].canFire():
                self.rules[i].fire()
                i = 0

    def addToListWithCount(self, origList, factToAdd):
        i = 0
        for i in range(len(origList)):
            if (origList[i] == factToAdd):
                origList[i + 1] += 1
                return
        origList.append(factToAdd)
        origList.append(1)

    def nextFactToAskFor(self):
        for rule in self.rules:
            ruleCount = 0
            currentPremises = []
            if (rule.isAvailable()):
                for premise in rule.getPremises():
                    if (premise.getValue() == UNKNOWN and not premise.isConclusion() ):
                        ruleCount += 1
                        currentPremises.append(premise)

            # Make a list of all the rules with the minimum number of unknown facts
            if (ruleCount < minRuleCount):
                minRuleCount = ruleCount
                minPremises = []
                for premise in minPremises:
                    addToListWithCount(premise)
            if (ruleCount == minRuleCount):
                for premise in minPremises:
                    addToListWithCount(premise)
        countsOfList = minIndex[range(1, 2, len(minPremises))]
        minIndex = countsOflist.index(min(countsOfList))
        factToAskFor = minPremises[minIndex - 1]
        return factToAskFor

    # Model changing methods (remember to notify()!! )
    # Examples of notifying:
    def __woodTypes_rearranged(self):
        self.notify('woodTypes_rearranged', None)

    def setAnswerToQuestion(self, answer):
        if(self.currentQuestion.getAskedStatus() == False):
            if(answer == "YES"):
                for yesFact in self.currentQuestion.getFacts():
                    yesFact.setValue()
            self.currentQuestion.setAskedStatus()

    def findQuestionToAskFor(self, fact):
        for question in self.questions:
            # Yes/No question:
            if( question[1] == 0):
                factRange = range(3,question[2]).extend(range())
            for yesIdx in range(3,question[2]):
                if( question[yesIdx] == fact.name ):
                    return 


    def readQuestions(self):
        # The Question csv file is structured like such:
        # Question text, question type, questiontype dependent fact data structure
        # Question type is a number that determines what kind of question it is (eg: 0 == YES/NO question)
        # In the case of YES/NO question, fact data structure looks like following:
        # Number of YES facts, yes fact1,..., yes fact n, number of NO facts, no fact 1, ..., no fact n
        readCSV = csv.reader(open('Questions.csv', 'rt'), delimiter=",")
        for question in readCSV:
            if len(question) > 0:
                # Change ';' into ',' by changing the string into a list, then back into a string
                questionText = list(question[0])
                for i in range(len(questionText)):
                    if questionText[i] == ';':
                        questionText[i] = ','
                question[0] = ''.join(questionText)
                # If YES/NO question, creates a list for YES facts and for NO facts
                if int(question[1]) == 0:
                    yesFacts = []
                    for i in range(int(question[2])):
                        yesFacts.append(question[3 + i])
                    noFacts = []
                    for i in range(int(question[2 + int(question[2]) + 1])):
                        noFactsacts.append(question[2 + int(question[2]) + 2 + i])
                    facts = [noFacts, yesFacts]
                    newQuestion = Question(question[0], question[1], facts)
                    self.questions.append(newQuestion)
                if int(question[1]) == 1:
                    pass

    def getQuestions(self):
        return self.questions

    def getNextQuestion(self):
        return self.currentQuestion

    def readWoods(self):
        readCSV = csv.reader(open('Wood_data.csv', 'rt'), delimiter=",")
        propertyNames = next(readCSV)
        for wood in readCSV:
            if (len(wood) > 0):
                newWood = WoodType(wood[0], wood[1], wood[2])
                for prop in range(3, 19):
                    newWood.addProperty(propertyNames[prop], wood[prop])
                self.addWood(newWood)

    def printWoods(self):
        for wood in self.woods:
            wood.print()

    def getWoods(self):
        return self.woods

    def addWood(self, wood):
        self.woods.append(wood)

    def adjustWeight(self, weightName, weightVal):
        self.weights[weightName] = weightVal

    def readFacts(self):
        # Facts need to be formatted in this fashion:
        # normal facts:     normal,factName
        # ordering facts:   order,factName,property,weight(-4 to 4
        # filtering facts:  filter,factName,property,boolean(1 or 0)
        readCSV = csv.reader(open('Facts.csv', 'rt'), delimiter=",")
        for fact in readCSV:
            if len(fact) > 0 and fact[0] != "#":
                if fact[0] == "order":
                    newfact = orderingFact(fact[1], fact[2], fact[3], self)
                elif fact[0] == "filter":
                    newfact = filteringFact(fact[1], fact[2], fact[3], self)
                else:
                    newfact = Fact(fact[1], self)
                self.facts.append(newfact)

    def printFacts(self):
        for fact in self.facts:
            fact.print()

    def addFact(self, fact):
        self.facts.append(fact)

    def findFact(self, name):
        for fact in self.facts:
            if( fact.name == name ):
                return fact  

        print(" ")
        print("ERROR while reading Rules: No fact found with name: ", name)
        print("Rule was dismissed. Please check your Database.")
        print(" ")


    def readRules(self):
        # Rules in CSV file are arranged such that conclusion is the last element in list.
        # Every item before the conclusion is a fact, which can be negated by adding a
        # "!" character in front of it
        readCSV = csv.reader(open('Rules.csv', 'rt'), delimiter=",")
        for rule in readCSV:
            if len(rule) > 0 and rule[0][0] != "#":
                # Create rule with conclusion
                if( rule[0][0] == "!" ):
                    conclusionFact = self.findFact(rule[0][1:])
                else:
                    conclusionFact = self.findFact(rule[0])
                if( conclusionFact == None ):
                    return
                newRule = Rule(conclusionFact)
                # Add premises to rule
                for idx in range(len(rule) - 1):
                    premiseString = rule[idx]
                    if rule[idx][0] == "!":
                        newPremise = self.findFact(premiseString[1:])
                        if( newPremise != None ):
                             newRule.addPremise(newPremise, False)
                        else:
                            return
                    else:
                        newPremise = self.findFact(premiseString)
                        if( newPremise != None ):
                             newRule.addPremise(newPremise, True)
                        else:
                            return
                self.addRule(newRule)

    def addRule(self, rule):
        self.rules.append(rule)

    # MVC related method
    def register_listener(self, listener):
        self.listeners.append(listener)

    def notify(self, event_name, data):
        for listener in self.listeners:
            listener(event_name, data)