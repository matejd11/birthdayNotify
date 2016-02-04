class Group(object):
    order = ["name",
             "facebook",
             "sms",
             "mail",
             "show"]

    def __init__(self, name, eventsAtr):
        self.name = name
        self.eventsAtr = eventsAtr

    def convert(self):
        dictionary = {}
        dictionary["name"] = self.name

        for eventAtr in self.eventsAtr:
            markDict = eventAtr.__dict__
            for atr in range(1, len(self.order)):
                if self.order[atr] not in dictionary:
                    dictionary[self.order[atr]] = ""
                if markDict[self.order[atr]] is True:
                    if dictionary[self.order[atr]] != "":
                        dictionary[self.order[atr]] += ", "+eventAtr.event.shortcut
                    else:
                        dictionary[self.order[atr]] = eventAtr.event.shortcut
        return dictionary

    def __str__(self):
        convert = self.convert()
        string = "\t"
        for key in self.order:
            string += key+": "+convert[key]+"\n\r\t"
        return string
