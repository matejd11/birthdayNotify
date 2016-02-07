from birthdayNotify.person import Person
from birthdayNotify.group import Group
from birthdayNotify.atributes import Atribute
from birthdayNotify.event import Event
from birthdayNotify.fakeDb import FakeDb
from math import ceil
import numpy as np
import readline
import re


class Shell(object):

    def __init__(self, dbName="database"):
        self.db = FakeDb(dbName)
        self.status = 1
        self.mode = 0
        self.commands = {"help": self.helpMe,
                        "add": [self.addPerson, self.addGroup, self.addEvent],
                        "save": self.saveDb,
                        "load": self.loadDb,
                        "quit": self.quit,
                        "exit": self.quit,
                        "group": self.groupPeople,
                        "edit": [self.editPerson, self.editGroup, self.editEvent],
                        "list": [self.showDbPerson, self.showDbGroup, self.showDbEvent],
                        "table": [self.showTablePerson, self.showTableGroup, self.showTableEvent],
                        "Person": self.changeToPerson,
                        "Group": self.changeToGroup,
                        "Event": self.changeToEvent,
                        "del": [self.deletePerson, self.deleteGroup, self.deleteEvent]}

        self.commandsHelp = ["help\t: show help for commands",
                            "Event, Group, Person\t: switch bettween modes",
                            "\tadd\t: add mode in database",
                            "\tdel\t: delete mode from database",
                            "\tedit\t: edit mode in database",
                            "\tlist\t: print mode in database",
                            "\ttable\t: print mode database table",
                            "group\t: start grouping people",
                            "save\t: save changes in database",
                            "load\t: load database",
                            "quit\t: quit shell",
                            "exit\t: quit shell"]

    def go(self):
        while self.status == 1:
            inputText = input("command(" + self.db.dbName + "/" + str(self.modeName()) + ")> ").strip()
            resArray = {}
            for i in self.commands:
                res = re.search("^" + inputText + ".*", i)
                resArray[i] = res

            candidate = []
            for i in resArray:
                if resArray[i] != None:
                    candidate.append(i)

            if len(candidate) == 1:
                if type(self.commands[candidate[0]]) == list:
                    self.commands[candidate[0]][int(self.mode)]()
                else:
                    self.commands[candidate[0]]()
            elif len(candidate) > 1 and not(not inputText):
                print("do you mean:")
                for can in candidate:
                    print("\t", can)
            elif not(not inputText):
                print("use h/help for help.")

    def modeName(self):
        if self.mode == 0:
            return "Person"
        if self.mode == 1:
            return "Group"
        if self.mode == 2:
            return "Event"

    def getDbName(self):
        name = input("\tEnter name of DB(leave blank for `" + self.db.dbName + "`): ")
        if not name:
            name = self.db.dbName
        return name

    def saveDb(self):
        name = self.getDbName()
        self.db.save(name)

    def loadDb(self):
        name = self.getDbName()
        self.db.load(name)

    def helpMe(self):
        print("    help:")
        for command in self.commandsHelp:
            print("\t", command)
    
    def changeToPerson(self):
        self.mode = 0

    def changeToGroup(self):
        self.mode = 1

    def changeToEvent(self):
        self.mode = 2
        
    def checkBox(self, text):
        while True:
            check = input(text)
            try:
                check = int(check)
                if check == 0:
                    return False
                if check == 1:
                    return True
            except ValueError:
                if check == "":
                    return False
            
    def addAtributes(self, event, edit = False):
        print("\t\tAtributes for "+event.name)
        while True:
            if edit is False or (event.name in self.db.groupDb.db[edit].eventsAtr) is False:
                facebook = self.checkBox("\t\t  send by Facebook:\t")
                sms = self.checkBox("\t\t  send by sms:\t\t")
                mail = self.checkBox("\t\t  send by e-mail:\t")
                show = self.checkBox("\t\t  show message:\t\t")
            else:
                oldAtr = self.db.groupDb.db[edit].eventsAtr[event.name]
                facebook = self.checkBox("\t\t  send by Facebook("+str(int(oldAtr.facebook))+"):\t")
                sms = self.checkBox("\t\t  send by sms("+str(int(oldAtr.sms))+"):\t")
                mail = self.checkBox("\t\t  send by e-mail("+str(int(oldAtr.mail))+"):\t")
                show = self.checkBox("\t\t  show message("+str(int(oldAtr.show))+"):\t")

            if facebook == True or sms == True or mail == True or show == True:
                break
            print("Choose atleast one atribute.")
        return Atribute(event, facebook, sms, mail, show)

    def addEvent(self, edit = False):
        if edit is False:
            name = input("\teventName: ")
            shortcut = input("\teventShortcut: ")
        else:
            oldEvent = self.db.eventDb.db[edit]
            name = input("\teventName("+oldEvent.name+"): ")
            shortcut = input("\teventShortcut("+oldEvent.shortcut+"): ")

        newEvent = Event(name, shortcut)

        if edit is False:
            self.db.eventDb.add(newEvent)
            for person in self.db.personDb.db:
                person.date[newEvent.name] = ""
        else:
            for person in self.db.personDb.db:
                tmp = person.__dict__
                change = tmp["date"][oldEvent.name]
                del tmp["date"][oldEvent.name]
                tmp["date"][newEvent.name] = change

            for group in self.db.groupDb.db:
                for atr in group.eventsAtr:
                    if group.eventsAtr[atr].event.name == oldEvent.name:
                        group.eventsAtr[atr].event = newEvent

            self.db.eventDb.edit(edit, newEvent)

    def addGroup(self, edit = False):
        if edit is False:
            name = input("    groupName: ")
        else:    
            name = input("    groupName("+self.db.groupDb.db[edit].name+"): ")

        print("\t#use 1: yes 0: no")
        print("\tAssign atributes to")
        eventsAtr = {}
        while True:
            check =False
            for event in self.db.eventDb.db:
                check = self.checkBox("\t  "+event.name+": ")
                if check == True:
                    eventAtr = self.addAtributes(event, edit)
                    eventsAtr[event.name] = eventAtr
                    atleastOne = True

            if atleastOne == True:
                break
            print("Choose atleast one. Atributes can't be assigned to nothing.")

        newGroup = Group(name, eventsAtr)
        if edit is False:
            self.db.groupDb.add(newGroup)
        else:
            group = self.db.groupDb.db[edit]
            for person in self.db.personDb.db:
                if (group.name in person.group) is True:
                    person.group.pop(person.group.index(group.name))
                    person.group.append(newGroup.name)
            
            self.db.groupDb.edit(edit, newGroup)

    def addPerson(self, edit = False):
        print("    add")
        if edit is False:
            firstName = input("\tfirstName: ")
            secondName = input("\tsecondName: ")
        else:
            oldPerson = self.db.personDb.db[edit]
            firstName = input("\tfirstName("+oldPerson.firstName+"): ")
            secondName = input("\tsecondName("+oldPerson.secondName+"): ")

        dates = {}
        for event in self.db.eventDb.db:
            while True:
                try:
                    if edit is False:
                        date = input("\t"+event.name+" YYYY-MM-DD: ")
                    else:
                        date = input("\t"+event.name+" YYYY-MM-DD("+str(oldPerson.date[event.name])+"): ")
                    if str(date) == "NaT":
                        date = ""
                    break    
                except ValueError:
                    pass
            dates[event.name] = date

        while True:
            if edit is False:
                mail = input("\tmail: ")
            else:
                mail = input("\tmail("+oldPerson.mail+"): ")
            if re.search(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$", mail) != None:
                break

        while True:
            if edit is False:
                telNumber = input("\ttelNumber: ")
            else:
                telNumber = input("\ttelNumber("+str(oldPerson.telNumber)+"): ")
            if re.search(r"^((\+\d{3}\ )|\d)?\d{3}\ ?\d{3}\ ?\d{3}$",telNumber) != None:
                break

        if edit is False:
            facebook = input("\tfacebook: ")
        else:
            facebook = input("\tfacebook("+oldPerson.facebook+"): ")

        newPerson = Person(firstName, secondName, dates, mail, telNumber, facebook)

        if edit is False:
            self.db.personDb.add(newPerson)
        else:
            self.db.personDb.edit(edit, newPerson)

    def getNumber(self, db, reason):
        number = None
        while number == None or number < -1 or number >= len(db):
            try:
                number = int(input("Insert id to "+reason+"(insert -1 to cancel): "))
            except ValueError:
                number = None
        while True and number != -1:
            if self.mode == 0:
                yes = input("Do you want to "+reason+"(" + db[number].firstName + " " + db[number].secondName +")? Y/n: ")
            if self.mode == 1 or self.mode == 2:
                yes = input("Do you want to "+reason+"(" + db[number].name + ")? Y/n: ")
            if yes.lower() == 'y' or yes.lower() == 'yes' or yes == "":
                return number
            elif yes.lower() == 'n' or yes.lower() == 'no':
                break
        return None

    def groupPeople(self):
        groups = self.db.groupDb.db
        people = self.db.personDb.db
        cycle = True
        pList = []
        self.showTableGroup()
        self.mode = 1
        gIndex = self.getNumber(groups, "choose group")
        self.mode = 0
        if gIndex != None:
            while cycle is True:
                self.showTablePerson()
                pIndex = self.getNumber(people, "assign person")
                if (pIndex in pList) is False:
                    if pIndex != None:
                        pList.append(pIndex)
                else:
                    print("This person is already choosen.")
                    
                while True:    
                    yes = input("Do you wish to choose another person? Y/n: ")
                    if yes.lower() == 'y' or yes.lower() == 'yes' or yes == "":
                        break
                    elif yes.lower() == 'n' or yes.lower() == 'no':
                        cycle = False
                        break
            for pIndex in pList:
                people[int(pIndex)].group=[]
                people[int(pIndex)].group.append(groups[gIndex].name)

    
    def editEvent(self):
        self.showTableEvent()
        number = self.getNumber(self.db.eventDb.db, "edit")
        if number != None:
            self.addEvent(number)

    def editGroup(self):
        self.showTableGroup()
        number = self.getNumber(self.db.groupDb.db, "edit")
        if number != None:
            self.addGroup(number)

    def editPerson(self):
        self.showTablePerson()
        number = self.getNumber(self.db.personDb.db, "edit")
        if number != None:
            self.addPerson(number)
    
    def deleteEvent(self):
        self.showTableEvent()
        number = self.getNumber(self.db.eventDb.db, "delete")
        if number != None:
            oldEvent = self.db.eventDb.db[number]
            for person in self.db.personDb.db:
                tmp = person.__dict__
                del tmp["date"][oldEvent.name]

            for group in self.db.groupDb.db:
                for atr in group.eventsAtr:
                    if group.eventsAtr[atr].event.name == oldEvent.name:
                        del group.eventsAtr[atr]
                        break
                if len(group.eventsAtr) == 0:
                    print("Group("+group.name+") has been removed for having no atributes!")
                    self.removeGroup(self.db.groupDb.db.index(group))
            self.db.eventDb.remove(number)

    def removeGroup(self, number):
        group = self.db.groupDb.db[number]
        for person in self.db.personDb.db:
            if (group.name in person.group) is True:
                person.group.pop(person.group.index(group.name))
        self.db.groupDb.remove(number)

    def deleteGroup(self):
        self.showTableGroup()
        number = self.getNumber(self.db.groupDb.db, "delete")
        if number != None:
            self.removeGroup(number)

    def deletePerson(self):
        self.showTablePerson()
        number = self.getNumber(self.db.personDb.db, "delete")
        if number != None:
            self.db.personDb.remove(number)

    def showDbEvent(self):
        for event in self.db.eventDb.db:
            print(event)

    def showDbGroup(self):
        for group in self.db.groupDb.db:
            print(group)

    def showDbPerson(self):
        for person in self.db.personDb.db:
            print(person)

    def quit(self):
        self.status = 0

    def showTableEvent(self):
        head = ["Event name",
                "Shortcut",]
        
        content = []
        for event in self.db.eventDb.db:
            content.append(event.__dict__)

        self.showTable(head, content, Event.order)

    def showTableGroup(self):
        head = ["Group name",
                "Facebook",
                "Sms",
                "Mail",
                "Show"]
        
        content = []
        for group in (self.db.groupDb.db):
            content.append(group.convert())

        self.showTable(head, content, Group.order)

    def showTablePerson(self):
        head = ["firstName",
                "secondName",
                "mail",
                "telNumber",
                "facebook"]
        order = Person.order[:]
        for event in self.db.eventDb.db:
            order.append(event.name)
            head.append(event.name)
        order.append("group")
        head.append("group")

        content = []
        for person in self.db.personDb.db:
            content.append(person.convert())

        self.showTable(head, content, order)

    def showTable(self, head, content, order):
        spaceExtra = 2
        largestStr = {}
        length = []
        for x in head:
            largestStr[x] = len(x)
            length.append(1+len(x))

        for tmp in content:
            for i in range(len(order)):
                if largestStr[head[i]] < len(str(tmp[order[i]])):
                    largestStr[head[i]] = len(str(tmp[order[i]]))

        headStr = " ID\t"
        for i in range(len(head)-1):
            tabSize = (largestStr[head[i]]+1+spaceExtra-length[i])
            headStr += "|"+head[i]+(" "*tabSize)
        headStr += "|"+head[-1]
        print(headStr)

        print(" "+"-"*8*17)

        for count, tmp in enumerate(content):
            raw =" ["+str(count)+"]\t|"
            for i in range(len(order)-1):
                raw += str(tmp[order[i]])+" "*(largestStr[head[i]]+spaceExtra-len(str(tmp[order[i]])))+"|"
            raw += str(tmp[order[-1]])
            print(raw)
