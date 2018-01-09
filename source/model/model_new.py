from enum import Enum
import csv
from .woodType import WoodType
from .rule import Rule
from .fact import *
from .question import Question

class comparisonType(Enum): # needed for the decisive facts
  HIGHER = 1
  LOWER = 2
  EQUAL = 3


class Model_new():
    
  def __init__(self):
    #Listener for model events
    self.listeners = []

    self.woods = [] # list of all the woodtypes
    self.facts = [] # list of all facts
    self.rules = [] # list of all rules
    self.questions = [] #list of all questions
    self.nextQuestion = None

    self.readFacts()
    self.readRules()
    self.readWoods()
    self.readQuestions()
    self.__next_question()


  def fireRules(self):
    i = 0
    while i < len(rules):
      if rules[i].canFire():
        rules[i].fire()
        i = 0

# Model changing methods (remember to notify()!! ) 
#Examples of notifying:
  def __woodTypes_rearranged(self):
    pass
    self.notify('woodTypes_rearranged', None)

  def __next_question(self):
    self.nextQuestion = self.questions[0]
    self.notify(None, None)

  def readQuestions(self):
    #The Question csv file is structured like such:
    # Question text, question type, questiontype dependent fact data strcture
    # Question type is a number that determines what kind of question it is (eg: 0 == YES/NO question)
    # In the case of YES/NO question, fact data structure looks like following:
    # Number of YES facts, yes fact1,..., yes fact n, number of NO facts, no fact 1, ..., no fact n
    readCSV = csv.reader(open('Questions.csv', 'rt'), delimiter=",")
    for question in readCSV:
      if(len(question)>0):
        #Change ';' into ',' by changing the string into a list, then back into a string
        questionText = list(question[0])
        for i in range(len(questionText)):
          if questionText[i] == ';':
            questionText[i] = ','
        question[0] = ''.join(questionText)
        #If YES/NO question, creates a list for YES facts and for NO facts
        if int(question[1]) == 0:
          YESfacts = []
          for i in range(int(question[2])):
            YESfacts.append(question[3+i])
          NOfacts = []
          for i in range(int(question[2+int(question[2])+1])):
            NOfacts.append(question[2+int(question[2])+2+i])
          facts = [YESfacts, NOfacts]
          newQuestion = Question(question[0], question[1], facts)
          self.questions.append(newQuestion)
        if int(question[1]) == 1:
          pass

  def getNextQuestion(self):
    return self.nextQuestion
  
  def readWoods(self):
    readCSV = csv.reader(open('Wood_data.csv', 'rt'), delimiter=",")
    propertyNames = next(readCSV)
    for wood in readCSV:
      if(len(wood)>0):
        newWood = WoodType(wood[0], wood[1], wood[2])
        for prop in range(3,18):
          newWood.addProperty(propertyNames[prop], wood[prop])
        self.addWood(newWood)

  def printWoods(self):
    for wood in self.woods:
      wood.print()

  def getWoods(self):
    return self.woods

  def addWood(self,wood):
    self.woods.append(wood)

  def readFacts(self):
    readCSV = csv.reader(open('Facts.csv','rt'), delimiter = ",")
    for fact in readCSV:
      factName = fact[0]
      if len(fact) > 1:
        propName = fact[1]
        propCompType = fact[2]
        propVal = fact[3]
        newFact = decisiveFact(factName,propName,propCompType,propVal)
      else:
        newFact = Fact(factName)
      self.facts.append(newFact)

  def printFacts(self):
    for fact in self.facts:
      fact.print()

  def addFact(self,fact):
    self.facts.append(fact)

  def readRules(self):
    # Rules in CSV file are arranged such that conclusion is the last element in list.
    # Every item before the conclusion is a fact, which can be negated by adding a 
    # "!" character in front of it
    readCSV = csv.reader(open('Rules.csv', 'rt'), delimiter=",")
    for rule in readCSV:
      newRule = Rule(rule[len(rule)-1])
      for item in range(len(rule)-1):
        if rule[item][0] == "!":
          newRule.addPremise(rule[item], False)
        else:
          newRule.addPremise(rule[item], True)
      self.addRule(newRule)
  
  def addRule(self,rule):
    self.rules.append(rule)

  #MVC related method
  def register_listener(self, listener):
        self.listeners.append(listener)

  def notify(self, event_name, data):
    for listener in self.listeners:
      listener(event_name, data)
