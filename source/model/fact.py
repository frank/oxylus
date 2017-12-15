from enum import Enum

class factValue(Enum):
  UNKNOWN = 1
  TRUE = 2
  FALSE = 3
  MAYBE = 4

class Fact():
  '''
  This class should represent the facts which are contained in rules.
  '''
  def __init__(self, name, text):
    self.value = UNKNOWN # Possible values: UNKNOWN, TRUE, FALSE, MAYBE
    self.text = text;
    self.name = name
	

# if a decisive fact is set to TRUE it will trigger the elimination of certain wood types
class decisiveFact(Fact):
  def __init__(self, compType, value, prop):
    self.compType = compType # HIGHER, LOWER or EQUAL
    self.property = prop # name of the property of woods that will be affected
    self.numValue = value
    pass
  
