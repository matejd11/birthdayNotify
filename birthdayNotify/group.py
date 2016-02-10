import json


class Group(object):
    header = ["name",
              "facebook",
              "sms",
              "mail",
              "show"]

    order = ["name",
             "facebook",
             "sms",
             "mail",
             "show"]

    def showTable(dataGroup):
        header = Group.order[:]
        order = Group.order[:]

        content = []
        for group in (dataGroup.db):
            content.append(group.convert())

        return header, content, order

    def __init__(self, name, eventsAtr):
        self.name = name
        self.eventsAtr = eventsAtr

    def convert(self):
        dictionary = {}
        dictionary["name"] = self.name

        for eventAtr in self.eventsAtr:
            markDict = self.eventsAtr[eventAtr].__dict__
            for atr in range(1, len(self.order)):
                if self.order[atr] not in dictionary:
                    dictionary[self.order[atr]] = ""
                if markDict[self.order[atr]] is True:
                    if dictionary[self.order[atr]] != "":
                        dictionary[self.order[atr]] += ", "+self.eventsAtr[eventAtr].event.shortcut
                    else:
                        dictionary[self.order[atr]] = self.eventsAtr[eventAtr].event.shortcut
        return dictionary

    def __str__(self):
        me = self.convert()
        return str(json.dumps(me, sort_keys=True, indent=4))
