from enum import Enum
import csv
from .woodType import WoodType
from .fact import *
from .rule import Rule
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
        self.weights = {"DensityAvg": 0, "Price": 0, "Ease of supply": 0, "Exterior Carpentry": 0, "Hardness": 0}
        self.currentQuestion = None

        self.readFacts()
        self.readRules()
        self.readWoods()
        self.readQuestions()
        self.update()

        #self.currentQuestion = self.questions[0]


    def update(self):
        self.fireRules()
        self.fireFacts()
        #print("Fired Facts")
        self.reorderWoods()
        nextFact = self.nextFactToAskFor()
        self.currentQuestion = self.findQuestionToAskFor(nextFact)
        print("Current Question: ",self.currentQuestion)

    def fireFacts(self):
        for fact in self.facts:
            if (fact.value == factValue.TRUE):
                fact.activate()

    # reorders the woods list according to the weights and filters
    def reorderWoods(self):
        # filter woods first:
        for wood in self.woods:
            if( wood.isAdmissible() == False ):
                self.filteredWoods.append(wood)
                self.woods.remove(wood)
            else:
                wood.setRanking(self.weights)
        # order woods according to ranking:
        self.woods = sorted(self.woods, key=lambda wood: wood.getRanking()) 

        

    def fireRules(self):
        i = 0
        numRules = len(self.rules)
        while i < numRules:
            if( self.rules[i].isAvailable() ):
                if( self.rules[i].canFire() ):
                    self.rules[i].fire()
                    i = 0
            i += 1


    def addToListWithCount(self, origList, factToAdd):
        for i in range(len(origList)):
            if (origList[i] == factToAdd):
                origList[i + 1] += 1
                return
        origList.append(factToAdd)
        origList.append(1)

    def nextFactToAskFor(self):
        minRuleCount = 99999
        minPremises = []
        # for all rules that require a minimum number of premises to be fulfilled,
        # collect the facts that they still require to know
        for rule in self.rules:
            unknownFactsInRule = 0
            currentPremises = []
            if ( rule.isAvailable() ):
                print(" One available rule!")
                for premise in rule.getPremises():
                    if (premise.getValue() == factValue.UNKNOWN and premise.canBeAskedFor() ):
                        unknownFactsInRule += 1
                        currentPremises.append(premise)
                        print(" We found one boys!")
            
            if( unknownFactsInRule == 0 ):
                continue

            # Make a list of all the rules with the minimum number of unknown facts
            if (unknownFactsInRule < minRuleCount):
                minRuleCount = unknownFactsInRule
                print("New rule with a minimum number of unkown premises!")
                minPremises = []
                for premise in currentPremises:
                    self.addToListWithCount(minPremises, premise)
            if (unknownFactsInRule == minRuleCount):
                for premise in currentPremises:
                    self.addToListWithCount(minPremises, premise)
        countsOfList = minPremises[1:2:len(minPremises)]
        print(minPremises)

        mostAppearingFactIdx = countsOfList.index(max(countsOfList))
        print(" idx:", mostAppearingFactIdx)
        factToAskFor = minPremises[mostAppearingFactIdx]
        print(factToAskFor)
        return factToAskFor

    # Model changing methods (remember to notify()!! )
    # Examples of notifying:
    def __woodTypes_rearranged(self):
        self.notify('woodTypes_rearranged', None)

    def setAnswerToQuestion(self, answer):
        if(self.currentQuestion.getAskedStatus() == False):
            if(answer == "YES"):
                yesFacts = self.currentQuestion.getFacts()[0]
                yesFactValues = self.currentQuestion.getFactTruthValues()[0]
                for i in range(len(yesFacts)):
                    yesFacts[i].setValue(yesFactValues[i])
            elif(answer == "NO"):
                noFacts = self.currentQuestion.getFacts()[1]
                noFactValues = self.currentQuestion.getFactTruthValues()[1]
                for i in range(len(noFacts)):
                    noFacts[i].setValue(yesFactValues[i])
            #For non-YES/NO question with more than 2 answers
            elif(anser == "ANSWER_3"):
                answer3Facts = self.currentQuestion.getFacts()[2]
                answer3FactValues = self.currentQuestion.getFactTruthValues()[2]
                for i in range(len(answer3Facts)):
                    answer3Facts[i].setValue(answer3FactValues[i])
            self.currentQuestion.setAskedStatus()
            self.update()

    def findQuestionToAskFor(self, nextFact):
        for question in self.questions:
            # Yes/No question:
            if( question.getType() == 0):
                #print(question.getText() , " with the facts: " ,question.getAllFacts())
                for fact in question.getAllFacts():
                    nextFact.getName()
                    fact.getName()
                    if( fact.getName() == nextFact.getName() ):
                        return question


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
                    yesFactValues = []
                    for i in range(int(question[2])):
                        for fact in self.facts:
                            if(fact.getName() == question[3 + i]):
                                yesFacts.append(fact)
                            if question[3+i][0] == "!":
                                yesFactValues.append(factValue.FALSE)
                            else:
                                yesFactValues.append(factValue.TRUE)
                    noFacts = []
                    noFactValues = []
                    for i in range(int(question[2 + int(question[2]) + 1])):
                        for fact in self.facts:
                            if(fact.getName() == question[3 + i]):
                                noFacts.append(fact)
                            if question[2 + int(question[2]) + 2 + i][0] == "!":
                                noFactValues.append(factValue.FALSE)
                            else:
                                noFactValues.append(factValue.TRUE)
                    facts = [yesFacts, noFacts]
                    factValues = [yesFactValues, noFactValues]
                    newQuestion = Question(question[0], question[1], facts, factValues)
                    self.questions.append(newQuestion)
                elif int(question[1]) == 1:
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
                # Create rule
                newRule = Rule()
                conclusionFact = None
                if( rule[0][0] == "!" ):
                    conclusionFact = self.findFact(rule[0][1:])
                    newRule.addConclusion(conclusionFact, factValue.FALSE)
                else:
                    conclusionFact = self.findFact(rule[0])
                    newRule.addConclusion(conclusionFact, factValue.TRUE)

                if( conclusionFact == None ):
                    print(" ")
                    print("Error while reading rule ", rule , ". No conclusion readable!")
                    print(" ")
                    return
                
                # Add premises to rule
                for idx in range(len(rule) - 1):
                    premiseString = rule[idx]
                    if rule[idx][0] == "!":
                        newPremise = self.findFact(premiseString[1:])
                        newRule.addPremise(newPremise, factValue.FALSE)
                       
                    else:
                        newPremise = self.findFact(premiseString)
                        newRule.addPremise(newPremise, factValue.TRUE)
                      
                self.addRule(newRule)

    def addRule(self, rule):
        self.rules.append(rule)

    # MVC related method
    def register_listener(self, listener):
        self.listeners.append(listener)

    def notify(self, event_name, data):
        for listener in self.listeners:
            listener(event_name, data)