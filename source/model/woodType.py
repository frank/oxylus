class WoodType():
    def __init__(self, spanishName, englishName, latinName):
        self.englishName = englishName  # name of the wood
        self.latinName = latinName  # name of wood in latin
        self.spanishName = spanishName
        # self.image = loadImage..
        self.properties = []  # list of properties associated to the wood type
        # each property has a value and a boolean to indicate if that property
        # still fulfills the criteria set by the user
        # a property also has a name
        # The fourth boolean in a property indicates whether the property
        # is represented by a boolean value itself
        self.appliedFilterInfo = []  # Applying filters will cause the wood to have non-matching
        # properties to the model's prototype. These are represented
        # as strings and are listed in this variable
        self.admissible = True
        self.ranking = 0
 
    def setRanking(self, weights):
        self.ranking = 0
        for weightName in weights:
             for prop in self.properties:
                if( prop[1] == None):
                    #print(prop[0])
                    continue
                if( weightName == prop[0] ):
                    self.ranking += weights[weightName] * prop[1]

    def getRanking(self):
        return self.ranking

    def isAdmissible(self):
        return self.admissible

    def setAdmissible(self, value):
        self.admissible = value

    def getEnglishName(self):
        return self.englishName

    def getLatinName(self):
        return self.latinName

    def getSpanishName(self):
        return self.spanishName

    def getInfo_from_appliedFilters(self):
        return self.appliedFilterInfo

    def filterOut(self, prop):
        self.admissible = False
        self.addAppliedFilterInfo("Filtered out because the " + prop + " of the wood did not fit your preferences.")

    def getProperties(self):
        return self.properties

    def addProperty(self, name, value):
        print(name)
        print(value)
        if( value == "" ):
            value = None
        elif( value != "TRUE" and value != "FALSE" ):
            value = float(value)
        
        self.properties.append([name, value])

    def addAppliedFilterInfo(self, string):
        self.appliedFilterInfo.append(string)

    def __repr__(self):
        return self.englishName
