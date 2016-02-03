
class Group(object):
    order = ["name",
             "facebook",
             "sms",
             "mail",
             "show"]
    def __init__(self, name, namedayAtr, birthdayAtr):
        self.name = name
        self.namedayAtr = namedayAtr
        self.birthdayAtr = birthdayAtr

    def convert(self):
        dictionary = {}
        dictionary["name"] = self.name

        if self.namedayAtr != False:
            markDict = self.namedayAtr.__dict__
            for atr in range(1, len(self.order)): 
                if markDict[self.order[atr]] == True:
                    dictionary[self.order[atr]] = "NameD"
                else:
                    dictionary[self.order[atr]] = ""

        if self.birthdayAtr != False:
            markDict = self.birthdayAtr.__dict__
            for atr in range(1, len(self.order)): 
                if markDict[self.order[atr]] == True:
                    if dictionary[self.order[atr]] != "":
                        dictionary[self.order[atr]] += " & BirthD"
                    else:    
                        dictionary[self.order[atr]] = "BirthD"

        return dictionary

    def __str__(self):
        convert = self.convert()
        string = "\t"
        for key in self.order:
            string+=key+": "+convert[key]+"\n\r\t"
        return string
