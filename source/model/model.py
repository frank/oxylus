import numpy as np
from enum import Enum
import csv
from .woodType import WoodType

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
    i = 0
    while i < len(rules):
      if rules[i].canFire():
        rules[i].fire()
        i = 0
  
  def readWoods(self):
    readCSV = csv.reader(open('Wood_data.csv', 'rt'), delimiter=",")
    propertyNames = next(readCSV)
    for wood in readCSV:
       newWood = WoodType(wood[1], wood[2])
       for prop in range(3,18):
         newWood.addProperty(propertyNames[prop], wood[prop])
       self.addWood(newWood)
    pass

  def printWoods(self):
     for wood in self.woods:
       wood.print()
     


  def readFacts(self):
    readCSV = csv.reader(open('Facts.csv','rt'), delimiter = ",")
    
    for fact in readCSV:
      newFact = Fact(fact[0])
      if(      

      self.facts.append(newFact)

  def readRules(self):
    pass #scans in all the rules from csv file

  def getWoods(self):
    return self.woods

  def addWood(self,wood):
    self.woods.append(wood)
  
  def addRule(self,rule):
    self.rules.append(rule)

  def addFact(self,fact):
    self.facts.append(fact)


