from person import Person
from group import Group
from atributes import Atribute
from event import Event
from fakeDb import FakeDb
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
                        "edit": [self.editPerson, self.editGroup, self.editEvent],
                        "list": [self.showDbPerson, self.showDbGroup, self.showDbEvent],
                        "table": [self.showTablePerson, self.showTableGroup, self.showTableEvent],
                        "mode": self.changeMode,
                        "del": [self.deletePerson, self.deleteGroup, self.deleteEvent]}

        self.commandsHelp = ["help\t: show help for commands",
                            "mode\t: switch bettween modes",
                            "\tadd\t: add mode in database",
                            "\tdel\t: delete mode from database",
                            "\tdel\t: edit mode in database",
                            "\tlist\t: print mode in database",
                            "\ttable\t: print mode database table",
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
        #self.db = FakeDb(name)

    def helpMe(self):
        print("    help:")
        for command in self.commandsHelp:
            print("\t", command)

    def changeMode(self):
        while True:
            try:
                self.mode = int(input("\tChange mode to 0 = Person or 1 = Group or 2 = Event: "))
                if self.mode == 0 or self.mode == 1 or self.mode == 2:
                    print("\tMode has been changed to ", self.modeName())
                    break
            except ValueError:
                pass

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
            
    def addAtributes(self, event):
        print("\t\tAtributes for "+event.name)
        while True:
            facebook = self.checkBox("\t\t  send by Facebook: ")
            sms = self.checkBox("\t\t  send by sms: ")
            mail = self.checkBox("\t\t  send by e-mail: ")
            show = self.checkBox("\t\t  show message: ")
            if facebook == True or sms == True or mail == True or show == True:
                break
            print("Choose atleast one atribute.")
        return Atribute(event, facebook, sms, mail, show)

    def addEvent(self):
        name = input("\teventName: ")
        shortcut = input("\teventShortcut: ")
        newEvent = Event(name, shortcut)
        self.db.eventDb.add(newEvent)
        for person in self.db.personDb.db:
            person.date[newEvent.name] = ""

    def addGroup(self):
        name = input("    groupName: ")
        print("\t#use 1: yes 0: no")
        print("\tAssign atributes to")
        eventsAtr = []
        while True:
            check =False
            for event in self.db.eventDb.db:
                check = self.checkBox("\t  "+event.name+": ")
                if check == True:
                    eventAtr = self.addAtributes(event)
                    eventsAtr.append(eventAtr)

            if check == True:
                break
            print("Choose atleast one. Atributes can't be assigned to nothing.")

        newGroup = Group(name, eventsAtr)
        self.db.groupDb.add(newGroup)

    def addPerson(self):
        print("    add")

        firstName = input("\tfirstName: ")
        secondName = input("\tsecondName: ")

        dates = {}
        for event in self.db.eventDb.db:
            while True:
                try:
                    date = input("\t"+event.name+" YYYY-MM-DD: ")
                    if str(date) == "NaT":
                        date = ""
                    break    
                except ValueError:
                    pass
            dates[event.name] = date

        while True:
            mail = input("\tmail: ")
            if re.search(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$", mail) != None:
                break

        while True:
            telNumber = input("\ttelNumber: ")
            if re.search(r"^((\+\d{3}\ )|\d)?\d{3}\ ?\d{3}\ ?\d{3}$",telNumber) != None:
                break

        facebook = input("\tfacebook: ")

        newPerson = Person(firstName, secondName, dates, mail, telNumber, facebook)

        self.db.personDb.add(newPerson)

    def getNumber(self, db, reason):
        number = None
        while number == None or number < -1 or number >= len(db):
            try:
                number = int(input("Insert id to "+reason+"(insert -1 to cancel): "))
            except ValueError:
                number = None
        while True and number != -1:
            if self.mode == 0:
                yes = input("Do you want to "+reason+"(" + db[number].firstName + " " + db[number].secondName +") Y/n: ")
            if self.mode == 1 or self.mode == 2:
                yes = input("Do you want to "+reason+"(" + db[number].name + ") Y/n: ")
            if yes.lower() == 'y' or yes.lower() == 'yes' or yes == "":
                return number
            elif yes.lower() == 'n' or yes.lower() == 'no':
                break
        return None
    
    def editEvent(self):
        pass

    def editGroup(self):
        self.showTableGroup()
        number = self.getNumber(self.db.groupDb.db, "edit")
        if number != None:
            self.addGroup()
            self.db.groupDb.remove(number)

    def editPerson(self):
        self.showTablePerson()
        number = self.getNumber(self.db.personDb.db, "edit")
        if number != None:
            self.addPerson()
            self.db.personDb.remove(number)
    
    def deleteEvent(self):
        self.showTableEvent()
        number = self.getNumber(self.db.eventDb.db, "delete")
        if number != None:
            self.db.eventDb.remove(number)

    def deleteGroup(self):
        self.showTableGroup()
        number = self.getNumber(self.db.groupDb.db, "delete")
        if number != None:
            self.db.groupDb.remove(number)

    def deletePerson(self):
        self.showTablePerson()
        number = self.getNumber(self.db.personDb.db, "delete")
        if number != None:
            self.db.personDb.remove(number)

    def showDbEvent(self):
        pass

    def showDbGroup(self):
        for group in self.db.groupDb.db:
            print(group)

    def showDbPerson(self):
        eventDb = self.db.eventDb.db
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
        order = Person.order
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
        largestStr = {}
        length = []
        for x in head:
            largestStr[x] = 0
            length.append(8*((1+len(x))//8)+8)

        for tmp in content:
            for i in range(len(order)):
                if largestStr[head[i]] < len(str(tmp[order[i]])):
                    largestStr[head[i]] = len(str(tmp[order[i]]))

        tabSize = []
        headStr = " ID\t"
        for i in range(len(head)-1):
            tabSize.append(ceil((largestStr[head[i]]+1-length[i])/8))
            if tabSize[i] < 0:
                tabSize[i] = 0
            headStr += "|"+head[i]+ "\t"*tabSize[i] + "\t"
        headStr += "|"+head[-1]
        print(headStr)

        print(" "+"-"*8*17)

        for count, tmp in enumerate(content):
            raw =" ["+str(count)+"]\t|"
            for i in range(len(order)-1):
                raw += str(tmp[order[i]])+"\t"*ceil(((length[i]+ tabSize[i]*8)-1-len(str(tmp[order[i]])))/8)+"|"
            raw += str(tmp[order[-1]])
            print(raw)
