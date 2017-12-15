import numpy as np
from enum import Enum
# import woodType.py

class comparisonType(Enum): # needed for the decisive facts
  HIGHER = 1
  LOWER = 2
  EQUAL = 3


class Model():
    
  def __init__(self):
    self.woods = [] # list of all the woodtypes
    self.facts = [] # list of all facts
    self.rules = [] # list of all rules

    self.readFacts()
    self.readRules()
    self.readWoods()

  def fireRules(self):
    for i in range(0,len(rules)):
      if rules[i].canFire():
        rules[i].fire()
        i = 0
  
  def readWoods(self):
    # readCSV = csv.reader(open('Wood_data.csv', 'rt'), delimiter=",")
    # propertyNames = readCSV[0]
    # for wood in range(1,len(readCSV)):
    #   x = woodType(self, wood[1], wood[2])
    #   for i in range(3,18):
    #     x.addProperty(propertyNames[i], wood[i])
    pass



  def readFacts(self):
    pass #scans in all the facts from csv file

  def readRules(self):
    pass #scans in all the rules from csv file

  def addWood(self,wood):
    self.woods.append(wood)
  
  def addRule(self,rule):
    self.rules.append(rule)

  def addFact(self,fact):
    self.facts.append(fact)


