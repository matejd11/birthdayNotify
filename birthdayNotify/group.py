from birthdayNotify.atributes import Atribute
from tools import checkBox
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

    def add(eventDb, edit=False):
        text = ""
        if edit is not False:
            text = "("+edit.name+")"
        name = input("    groupName"+text+": ")
        print("\t#use 1: yes 0: no")
        print("\tAssign atributes to")
        eventsAtr = {}
        while True:
            check = False
            for event in eventDb.db:
                check = checkBox("\t  "+event.name+": ")
                if check is True:
                    print("\t\tAtributes for "+event.name)
                    if edit is False or (event.name in edit.eventsAtr) is False:
                        facebook, sms, mail, show = Atribute.addAtr(event)
                    else:
                        oldAtr = edit.eventsAtr[event.name]
                        facebook, sms, mail, show = oldAtr.editAtr(event)
                    eventAtr = Atribute(event, facebook, sms, mail, show)
                    eventsAtr[event.name] = eventAtr
                    atleastOne = True

            if atleastOne is True:
                break
            print("Choose atleast one. Atributes can't be assigned to nothing.")
        return name, eventsAtr

    def __str__(self):
        me = self.convert()
        return str(json.dumps(me, sort_keys=True, indent=4))
