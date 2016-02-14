from birthdayNotify.person import Person
from birthdayNotify.group import Group
from birthdayNotify.event import Event
from birthdayNotify.fakeDb import FakeDb
from birthdayNotify.messages import Messages
from tools import getNumber
import readline
import re


class Shell(object):

    def __init__(self, dbName="database"):
        self.db = FakeDb(dbName)
        self.status = 1
        self.mode = 0
        self.commands = {"help": self.helpMe,
                "add": [self.addPerson, self.addGroup, self.addEvent, self.addMessages],
                "save": self.saveDb,
                "load": self.loadDb,
                "quit": self.quit,
                "exit": self.quit,
                "remgroup": self.removeAssignGroup,
                "assign": [ self.assignGroup, self.assignGroup, self.assignEvent, self.assignPackage],
                "edit": [self.editPerson, self.editGroup, self.editEvent, self.editMessages],
                "list": [self.showDbPerson, self.showDbGroup, self.showDbEvent, self.showDbMessages],
                "table": [self.showTablePerson, self.showTableGroup, self.showTableEvent, self.showTableMessages],
                "Person": self.changeToPerson,
                "Group": self.changeToGroup,
                "Event": self.changeToEvent,
                "Messages": self.changeToMessages,
                "del": [self.deletePerson, self.deleteGroup, self.deleteEvent, self.deleteMessages]}
        self.commandsHelp = ["help\t: show help for commands",
                "Event, Group, Person, Messages\t: switch bettween modes",
                "\tadd\t: add mode in database",
                "\tassign\t: assign mode (Group to Person/Messages to Group)",
                "\tdel\t: delete mode from database",
                "\tedit\t: edit mode in database",
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
                if resArray[i] is not None:
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
        if self.mode == 3:
            return "Messages"

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

    def changeToMessages(self):
        self.mode = 3

    def assignEvent(self):
        pass

    def assignPackage(self):
        self.showTablePackages()
        mes = self.db.messagesDb.db
        mode = self.mode
        self.mode = 3
        pIndex = getNumber(mes, "choose package", self.mode)
        if pIndex is not None:
            while True:
                self.showTableGroup()
                groups = self.db.groupDb.db
                self.mode = 1
                gIndex = getNumber(groups, "choose group", self.mode)
                if gIndex is not None:
                    mes[pIndex].groups.append(groups[gIndex])
                yes = input("\t  More groups? Y/n: ")
                if yes.lower() == 'y' or yes.lower() == 'yes' or yes == "":
                    pass
                elif yes.lower() == 'n' or yes.lower() == 'no':
                    break
        self.mode = mode

    def addGroup(self):
        newGroup = Group("NewGroup")
        newGroup.add(self.db.eventDb)
        self.db.groupDb.add(newGroup)

    def addEvent(self, edit=False):
        name = input("\teventName: ")
        shortcut = input("\teventShortcut: ")
        newEvent = Event(name, shortcut)
        self.db.eventDb.add(newEvent)
        for person in self.db.personDb.db:
            person.date[newEvent.name] = ""

    def addMessages(self, edit=False):
        if edit is False:
            name = input("\tName of the package:\t")
        else:
            oldMessages = self.db.messagesDb.db[edit]
            name = input("\tName of the package("+oldMessages.name+"):\t")

        print("\t  **Use slots as <firstName> or <secondName> for better message")
        mList = []
        x = -1
        while True:
            x += 1
            if edit is False:
                message = input("\t\tmessage("+str(x)+"):\t")
            else:
                message = input("\t\tmessage("+str(x)+")("+oldMessages.mList[0]+"):\t")
            mList.append(message)

            yes = input("\t  More messages? Y/n: ")
            if yes.lower() == 'y' or yes.lower() == 'yes' or yes == "":
                pass
            elif yes.lower() == 'n' or yes.lower() == 'no':
                break

        for message in mList:
            pass
        #REGEX add slots

        newMessages = Messages(name, mList)
        if edit is False:
            self.db.messagesDb.add(newMessages)
        else:
            self.db.messagesDb.edit(edit, newMessages)

    def addPerson(self, edit=False):
        print("    add")
        if edit is False:
            firstName = input("\tfirstName: ")
            secondName = input("\tsecondName: ")
        else:
            oldPerson = self.db.personDb.db[edit]
            firstName = input("\tfirstName("+oldPerson.firstName+"): ")
            secondName = input("\tsecondName("+oldPerson.secondName+"): ")

        if edit is False:
            print("\t**Message slots will help you making better messages")
            dictPrint = ("\tSlots: <firstName> = "+firstName+", <secondName> = "+secondName)
            mSlots = {}
            while True:
                print(dictPrint)
                yes = input("\tMore slots? Y/n: ")
                if yes.lower() == 'y' or yes.lower() == 'yes' or yes == "":
                    pass
                elif yes.lower() == 'n' or yes.lower() == 'no':
                    break
                slotName = "<"+str(input("\tmessageSlotName: "))+">"
                slot = str(input("\tContent of "+slotName+": "))
                mSlots[slotName] = slot
                dictPrint += ", "+slotName+" = "+slot

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
            if re.search(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$", mail) is not None:
                break

        while True:
            if edit is False:
                telNumber = input("\ttelNumber: ")
            else:
                telNumber = input("\ttelNumber("+str(oldPerson.telNumber)+"): ")
            if re.search(r"^((\+\d{3}\ )|\d)?\d{3}\ ?\d{3}\ ?\d{3}$", telNumber) is not None:
                break

        if edit is False:
            facebook = input("\tfacebook: ")
        else:
            facebook = input("\tfacebook("+oldPerson.facebook+"): ")

        newPerson = Person(firstName, secondName, dates, mail, telNumber, facebook, mSlots)

        if edit is False:
            self.db.personDb.add(newPerson)
        else:
            self.db.personDb.edit(edit, newPerson)

    def removeAssignGroup(self):
        pDb = self.db.personDb.db
        self.showTablePerson()
        pIndex = getNumber(pDb, "choose person", 0)
        if pIndex is not None:
            head, content, order = pDb[pIndex].showTableGroup()
            print(head, content)
            self.showTable([head], content, [order])
            gIndex = getNumber(content, "choose group", "removeAG")
            if gIndex is not None:
                pDb[pIndex].removeGroup(content[gIndex][head])

    def assignGroup(self):
        groups = self.db.groupDb.db
        people = self.db.personDb.db
        cycle = True
        pList = []
        self.showTableGroup()
        self.mode = 1
        gIndex = getNumber(groups, "choose group", self.mode)
        self.mode = 0
        if gIndex is not None:
            while cycle is True:
                self.showTablePerson()
                pIndex = getNumber(people, "assign person", self.mode)
                if (pIndex in pList) is False:
                    if pIndex is not None:
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
                people[int(pIndex)].addGroup(groups[gIndex])

    def editMessages(self):
        self.showTablePackages()
        number = getNumber(self.db.messagesDb.db, "edit", self.mode)
        if number is not None:
            self.addMessages(number)

    def editEvent(self):
        self.showTableEvent()
        number = getNumber(self.db.eventDb.db, "edit", self.mode)
        if number is not None:
            oldEvent = self.db.eventDb.db[number]
            name = input("\teventName("+oldEvent.name+"): ")
            shortcut = input("\teventShortcut("+oldEvent.shortcut+"): ")
            newEvent = Event(name, shortcut)
            for person in self.db.personDb.db:
                tmp = person.__dict__
                change = tmp["date"][oldEvent.name]
                del tmp["date"][oldEvent.name]
                tmp["date"][newEvent.name] = change

            for group in self.db.groupDb.db:
                for atr in group.eventsAtr:
                    if group.eventsAtr[atr].event.name == oldEvent.name:
                        group.eventsAtr[atr].event = newEvent

            self.db.eventDb.edit(number, newEvent)

    def editGroup(self):
        self.showTableGroup()
        i = getNumber(self.db.groupDb.db, "edit", self.mode)
        if i is not None:
            group = self.db.groupDb.db[i]
            group.add(self.db.eventDb)

#           for package in self.db.messagesDb.db:
#               if (group.name in package.groups) is True:
#                   package.group.pop(package.group.index(group.name))
#                   package.group.append(newGroup.name)
            self.db.groupDb.edit(i, group)

    def editPerson(self):
        self.showTablePerson()
        number = getNumber(self.db.personDb.db, "edit", self.mode)
        if number is not None:
            self.addPerson(number)

    def deleteMessages(self):
        self.showTableMessages()
        number = getNumber(self.db.messagesDb.db, "delete", self.mode)
        if number is not None:
            self.removeMessages(number)

    def deleteEvent(self):
        self.showTableEvent()
        number = getNumber(self.db.eventDb.db, "delete", self.mode)
        if number is not None:
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
        for package in self.db.messages.db:
            if (group.name in package.groups) is True:
                package.group.pop(package.group.index(group.name))

        self.db.groupDb.remove(number)

    def deleteGroup(self):
        self.showTableGroup()
        number = getNumber(self.db.groupDb.db, "delete", self.mode)
        if number is not None:
            self.removeGroup(number)

    def deletePerson(self):
        self.showTablePerson()
        number = getNumber(self.db.personDb.db, "delete", self.mode)
        if number is not None:
            self.db.personDb.remove(number)

    def showDbMessages(self):
        for package in self.db.messagesDb.db:
            print(package)

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

    def showTablePackages(self):
        head = ["Package name",
                "Groups assigned"]

        content = []
        for package in self.db.messagesDb.db:
            content.append(package.convert())

        self.showTable(head, content, ["name", "groups"])

    def showTableMessages(self):
        self.showTablePackages()
        index = getNumber(self.db.messagesDb.db, "choose package", self.mode)
        if index is not None:
            head, content, order = Messages.showTable(self.db.messagesDb, index)
            self.showTable(head, content, order)

    def showTableEvent(self):
        head, content, order = Event.showTable(self.db.eventDb)
        self.showTable(head, content, order)

    def showTableGroup(self):
        head, content, order = Group.showTable(self.db.groupDb)
        self.showTable(head, content, order)

    def showTablePerson(self):
        head, content, order = Person.showTable(self.db.personDb, self.db.eventDb)
        self.showTable(head, content, order)

    def showTable(self, head, content, order):
        spaceExtra = 1
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
            raw = " ["+str(count)+"]\t|"
            for i in range(len(order)-1):
                raw += str(tmp[order[i]])+" "*(largestStr[head[i]]+spaceExtra-len(str(tmp[order[i]])))+"|"
            raw += str(tmp[order[-1]])
            print(raw)
