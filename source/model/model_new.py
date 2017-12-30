from enum import Enum
import csv
from .woodType import WoodType
from .rule import Rule
from .fact import *

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

    self.readFacts()
    self.readRules()
    self.readWoods()


  def fireRules(self):
    i = 0
    while i < len(rules):
      if rules[i].canFire():
        rules[i].fire()
        i = 0

# Model changing methods (remember to notify()!! ) 
#Examples of notifying:
  def __woodTypes_rearranged():
    pass
    self.notify('woodTypes_rearranged', None)

  def __next_question():
    pass
    self.notify('next_question', None)
################
  
  def readWoods(self):
    readCSV = csv.reader(open('Wood_data.csv', 'rt'), delimiter=",")
    propertyNames = next(readCSV)
    for wood in readCSV:
      if(len(wood)>0):
        newWood = WoodType(wood[1], wood[2])
        for prop in range(3,18):
          newWood.addProperty(propertyNames[prop], wood[prop])
        self.addWood(newWood)


  def printWoods(self):
     for wood in self.woods:
       wood.print()

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

  def getWoods(self):
    return self.woods

  def addWood(self,wood):
    self.woods.append(wood)
  
  def addRule(self,rule):
    self.rules.append(rule)

  def addFact(self,fact):
    self.facts.append(fact)

  #MVC related method
  def register_listener(self, listener):
        self.listeners.append(listener)

  def notify(self, event_name, data):
    for listener in self.listeners:
      listener(event_name, data)
