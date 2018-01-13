from enum import Enum
import csv
from .woodType import WoodType
from .fact import *
from .rule import Rule
from .question import Question



class Model():
    def __init__(self):
        self.questionCount = 0 #number of questions posed so far
        self.end = False
        # Listener for model events
        self.listeners = []
        self.woods = []  # list of all the woodtypes
        self.facts = []  # list of all facts
        self.rules = []  # list of all rules
        self.questions = []  # list of all questions
        self.askedQuestions = [] # list of questions that have been asked
        self.filteredWoods = []
        self.weights = {"DensityAvg": 0, "Price": 0, "Ease of supply": 0, "Exterior Carpentry": 0, "Hardness": 0}
        self.currentQuestion = None

        self.readFacts()
        self.readRules()
        self.readWoods()
        self.readQuestions()
        self.update()


    def update(self):
        print("")
        print("Round number ", self.questionCount)
        self.fireRules()
        self.reorderWoods()
        nextFact = self.nextFactToAskFor()
        self.currentQuestion = self.findQuestionToAskFor(nextFact)
        self.printActivatedFilterFacts()
        print("Current Question: ",self.currentQuestion)
        print("   ")
        #fact = self.findFact("Glued")
        #print(fact, " noQuestions: ", fact.getNumQuestions())
        
        self.questionCount += 1
        self.notify(None)

    def fireFacts(self):
        for fact in self.facts:
            if( fact.value == factValue.TRUE ):
                fact.activate()

    # reorders the woods list according to the weights and filters
    def reorderWoods(self):
        print("Filtering woods...")
        # filter woods first:
        removeWoods = []
        for wood in self.woods:
            if( wood.isAdmissible() == False ):
                print("-")
                print( wood, " was filtered out.")
                print("-")
                self.filteredWoods.append(wood)
                removeWoods.append(wood)
            else:
                wood.setRanking(self.weights)


        for filteredWood in removeWoods:
            for wood in self.woods:
                if filteredWood == wood:
                    self.woods.remove(wood)
                    break

        # order woods according to ranking:#
        print("Reordering woods...")
        
        self.woods = sorted(self.woods, key=lambda wood: wood.getRanking(), reverse = True) 

    def fireRules(self):
        i = 0
        numRules = len(self.rules)
        while i < numRules:
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
        #print("")
        #print("Available rules: ")
        #print("")
        #print("NEXT FACT TO ASK FOR:")
        for rule in self.rules:
            unknownFactsInRule = 0
            currentPremises = []
            #print(rule ," is available:", rule.isAvailable())

            if ( rule.isAvailable() ):
                for premise in rule.getPremises():
                    if( premise.getValue() == factValue.UNKNOWN and premise.canBeAskedFor() ):
                        unknownFactsInRule += 1
                        currentPremises.append(premise)
            
            if( unknownFactsInRule == 0 ):
                continue

            # Make a list of all the rules with the minimum number of unknown facts
            if (unknownFactsInRule < minRuleCount):
                minRuleCount = unknownFactsInRule
                minPremises = []
                for premise in currentPremises:
                    self.addToListWithCount(minPremises, premise)
            if (unknownFactsInRule == minRuleCount):
                for premise in currentPremises:
                    self.addToListWithCount(minPremises, premise)
        print(" minPremises :" , minPremises)
        if( minPremises == [] ):
            return None
        countsOfList = minPremises[1:2:len(minPremises)]
        mostAppearingFactIdx = countsOfList.index(max(countsOfList))
        factToAskFor = minPremises[mostAppearingFactIdx]
        print("fact that we want to know: ", factToAskFor)
        return factToAskFor

    def setAnswerToQuestion(self, answer):
        if(self.currentQuestion.getAskedStatus() == True):
            print("ERROR: question has been asked before!")

        self.currentQuestion.setTruthValuesToAnsweredFacts(answer)
        self.askedQuestions.append(self.currentQuestion)
        self.update()

    def findQuestionToAskFor(self, nextFact):
        if( nextFact == None ):
            self.end = True
            return None

        maxQuestionCnt = 0
        for question in self.questions:
            questionCnt = 0
            #print("")
            #print(question)
            #print("question type: " ,question.getType())
            # Yes/No question:
            if( question.getType() == 0) :
                #print(question.getText() , " with the facts: " ,question.getAllFacts())
                #print("number of facts in this question: ", len(question.getAllFacts()))
                if( question.getAskedStatus() == False ):
                    for fact in question.getAllFacts():
                        if( fact.getName() == nextFact.getName() ):
                            questionCnt += 1
                            if( questionCnt > maxQuestionCnt ):
                                maxQuestionCnt = questionCnt
                                questionToAskFor = question
        
        return questionToAskFor



            #print("")

    def getEnd(self):
        return self.end

    def addFactsToQuestion(self, newQuestion, questionScan, numFacts, start, button): 
        for i in range(numFacts):
            factString = questionScan[start+i]
            factAdded = False
            for fact in self.facts:
                currentFact = fact.getName()

                if( currentFact == factString or currentFact == factString[1:] ):
                    factAdded = True
                    if( factString[0] == "!" ):
                        newQuestion.addFact(fact, factValue.FALSE, button)
                    else:
                        newQuestion.addFact(fact, factValue.TRUE, button)

            if not factAdded:
                print("ERROR! ", factString , " could not be added to question ", newQuestion)


    def readQuestions(self):
        # The Question csv file is structured like such:
        # Question text, question type, questiontype dependent fact data structure
        # Question type is a number that determines what kind of question it is (eg: 0 == YES/NO question)
        # In the case of YES/NO question, fact data structure looks like following:
        # Number of YES facts, yes fact1,..., yes fact n, number of NO facts, no fact 1, ..., no fact n
        readCSV = csv.reader(open('Questions.csv', 'rt'), delimiter=",")
        for question in readCSV:
            if len(question) > 0 and question[0][0] != "#":
                questionText = question[0]
                questionType = int(question[1])
                #print(questionText)
                # Change ';' into ',' by changing the string into a list, then back into a string
                questionText = list(questionText)
                for i in range(len(questionText)):
                    if questionText[i] == ';':
                        questionText[i] = ','
                questionText = ''.join(questionText)
        
                newQuestion = Question(questionText, questionType)
                # Yes/No question:
                if questionType == 0:
                    numPositives = int(question[2])
                    positiveStart = 3
                    numNegatives = int(question[3 + numPositives])
                    negativeStart = 4 + numPositives
                    self.addFactsToQuestion(newQuestion, question, numPositives, positiveStart, 0)
                    self.addFactsToQuestion(newQuestion, question, numNegatives, negativeStart, 1)
                # Other type of question:
                elif int(question[1]) == 1:
                    pass

                self.questions.append(newQuestion)


    def getQuestions(self):
        return self.questions

    def getAskedQuestions(self):
        return self.askedQuestions

    def getRoundNumber(self):
        return self.questionCount

    def getNextQuestion(self):
        return self.currentQuestion

    def readWoods(self):
        readCSV = csv.reader(open('Wood_data.csv', 'rt'), delimiter=",")
        propertyNames = next(readCSV)
        for wood in readCSV:
            if (len(wood) > 0):
                newWood = WoodType(wood[0], wood[1], wood[2])
                for prop in range(3, len(wood)):
                    newWood.addProperty(propertyNames[prop], wood[prop])
                self.addWood(newWood)

    def printWoods(self):
        for wood in self.woods:
            wood.print()

    def printActivatedFilterFacts(self):
        print("")
        print("Printing all Filter/Order Facts set to TRUE:")
        for fact in self.facts:
            if( fact.isType() != "Normal" and fact.getValue() == factValue.TRUE ):
                print(fact, end = " ")
        print("")

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

    def findQuestion(self, name):
        for question in self.questions:
            if( question.getText() == name ):
                return question
        print("")
        print("ERROR: Question with name ", name , " could not be found!")
        print("")


    def findFact(self, name):
        for fact in self.facts:
            if( fact.name == name ):
                return fact  

        print(" ")
        print("ERROR while looking for fact. No fact found with name: ", name)
        print("Please check your Database.")
        quit()
        print(" ")


    def readRules(self):
        # Rules in CSV file are arranged such that conclusion is the last element in list.
        # Every item before the conclusion is a fact, which can be negated by adding a
        # "!" character in front of it
        readCSV = csv.reader(open('Rules.csv', 'rt'), delimiter=",")
        print("SCANNED RULES:")
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
                    print("Error while reading rule ", rule , ". CHECK YOUR DATABASE - RULES ARE FAULTY")
                    print(" ")
                    quit()
                    return
                
                # Add premises to rule
                for idx in range(1, len(rule) ):
                    premiseString = rule[idx]
                    if rule[idx][0] == "!":
                        newPremise = self.findFact(premiseString[1:])
                        newRule.addPremise(newPremise, factValue.FALSE)
                       
                    else:
                        newPremise = self.findFact(premiseString)
                        newRule.addPremise(newPremise, factValue.TRUE)
                      
                self.addRule(newRule)
                print(newRule)

    def addRule(self, rule):
        self.rules.append(rule)

    # MVC related method
    def register_listener(self, listener):
        self.listeners.append(listener)

    def notify(self, event_name):
        for listener in self.listeners:
            listener(event_name)