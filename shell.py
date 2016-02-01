from person import Person
from personDb import PersonDb
from math import ceil
import numpy as np
import readline
import re

class Shell(object):
    def __init__(self, dbName = "database"):
        self.db = PersonDb(dbName)
        self.status = 1
        self.mode = 0
        self.commands = {"help": self.helpMe,
                        "add": [self.addPerson, self.addGroup],
                        "save": self.saveDb,
                        "load": self.loadDb,
                        "quit": self.quit,
                        "exit": self.quit,
                        "list": [self.showDbPerson, self.showDbGroup],
                        "table": [self.showTablePerson, self.showTableGroup],
                        "mode": self.changeMode,
                        "del": [self.deletePerson, self.deleteGroup]}

        self.commandsHelp = ["help\t: show help for commands",
                            "mode 0/1\t: 0 for person 1 for group",
                            "\tadd\t: add mode in database",
                            "\tdel\t: delete mode from database",
                            "\tlist\t: print mode in database",
                            "\ttable\t: print mode database table",
                            "save\t: save changes in database",
                            "load\t: load database",
                            "quit\t: quit shell",
                            "exit\t: quit shell"]

    def go(self):
        while self.status == 1:
            inputText = input("command(" + self.db.dbName + ")> ").strip()
            resArray = {}
            for i in self.commands:
                res = re.search("^" + inputText + ".*", i)
                resArray[i] = res

            candidate = []
            for i in resArray:
                if resArray[i] != None:
                    candidate.append(i)

            if len(candidate) == 1:
                try:
                    type(self.commands[candidate[0]])
                    self.commands[candidate[0]][int(self.mode)]()
                except TypeError:
                    self.commands[candidate[0]]()
            elif len(candidate) > 1 and not(not inputText):
                print("do you mean:")
                for can in candidate:
                    print("\t", can)
            elif not(not inputText):
                print("use h/help for help.")

    def getDbName(self):
        name = input("\tEnter name of DB(leave blank for `" + self.db.dbName + "`): ")
        if not name:
            name = self.db.dbName
        return name

    def saveDb(self):
        name = self.getDbName()
        PersonDb.save(self.db.db, name)

    def loadDb(self):
        name = self.getDbName()
        self.db = PersonDb(name)

    def helpMe(self):
        print("    help:")
        for command in self.commandsHelp:
            print("\t", command)

    def changeMode(self):
        while True:
            self.mode = (input("\tChange mode to 0 = Person or 1 = Group: "))
            if self.mode == "0":
                print("Mode has been changed to Person")
                break
            if self.mode == "1":
                print("Mode has been changed to Group")
                break

    def addGroup(self):
        pass

    def addPerson(self):
        print("    add")

        firstName = input("\tfirstName: ")
        secondName = input("\tsecondName: ")
        while True:
            try:
                birthdayDate = (np.datetime64(input("\tbirthdayDate YYYY-MM-DD: ")))
                if str(birthdayDate) != "NaT":
                    break
            except ValueError:
                pass
                
        while True:
            try:
                namedayDate = (np.datetime64(input("\tnamedayDate: ")))
                if str(namedayDate) != "NaT":
                    break
            except ValueError:
                pass

        while True:
            mail = input("\tmail: ")
            if re.search(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$", mail) != None:
                break

        while True:
            telNumber = input("\ttelNumber: ")
            if re.search(r"^((\+\d{3}\ )|\d)?\d{3}\ ?\d{3}\ ?\d{3}$",telNumber) != None:
                break

        facebook = input("\tfacebook: ")

        newPerson = Person(firstName, secondName, birthdayDate, namedayDate, mail, telNumber, facebook)

        self.db.addPerson(newPerson)

    def getNumber(self):
        number = None
        while number == None or number < -1 or number >= len(self.db.db):
            try:
                number = int(input("Insert id to delete(insert -1 to cancel): "))
            except ValueError:
                number = None
        while True and number != -1:
            yes = input("Do you want to delete(" + self.db.db[number].firstName + " " + self.db.db[number].secondName +") Y/n: ")
            if yes.lower() == 'y' or yes.lower() == 'yes' or yes == "":
                return number
            elif yes.lower() == 'n' or yes.lower() == 'no':
                break
        return None

    def deleteGroup(self):
        pass

    def deletePerson(self):
        self.showTablePerson()
        number = self.getNumber()
        if number != None:
            self.db.db.pop(number)

    def showDbGroup(self):
        pass

    def showDbPerson(self):
        for person in self.db.db:
            print(person)

    def quit(self):
        self.status = 0

    def showTableGroup(self):
        pass

    def showTablePerson(self):
        largestStr = {"firstName": 0, 
                    "secondName": 0,
                    "birthdayDate": 0,
                    "namedayDate": 0,
                    "mail": 0,
                    "telNumber": 0,
                    "facebook": 0,
                    "group": 0}
        for person in self.db.db:
            tmp = person.__dict__
            for index in tmp:
                if largestStr[index] < len(str(tmp[index])):
                    largestStr[index] = len(str(tmp[index]))

        tabSize = []
        tabSize.append(ceil((largestStr["firstName"]-16)/8))
        tabSize.append(ceil((largestStr["secondName"]-16)/8))
        tabSize.append(ceil((largestStr["birthdayDate"]-16)/8))
        tabSize.append(ceil((largestStr["namedayDate"]-16)/8))
        tabSize.append(ceil((largestStr["mail"]-8)/8))
        tabSize.append(ceil((largestStr["telNumber"]-16)/8))
        tabSize.append(ceil((largestStr["facebook"]-16)/8))

        for x in range(len(tabSize)):
            if tabSize[x] < 0:
                tabSize[x] = 0

        head = " ID\t|firstName" + "\t"*tabSize[0] + "\t"
        head += "|secondName" + "\t"*tabSize[1] + "\t"
        head += "|birthdayDate"+"\t"*tabSize[2] +"\t"
        head += "|namedayDate"+"\t"*tabSize[3] +"\t"
        head += "|mail"+"\t"*tabSize[4] +"\t"
        head += "|telNumber"+"\t"*tabSize[5] +"\t"
        head += "|facebook"+"\t"*tabSize[6] +"\t"
        head += "|group"
        print(head)

        print("  "+"-"*8*16)

        space = " "
        for count, person in enumerate(self.db.db):
            raw =" ["+str(count)+"]\t|"+str(person.firstName)+"\t"*ceil(((16+ tabSize[0]*8)-len(person.firstName))/8)+"|"
            raw += str(person.secondName)+"\t"*ceil(((16+ tabSize[1]*8)-len(person.secondName))/8)+"|"
            raw += str(person.birthdayDate)+"\t"*ceil(((16+ tabSize[2]*8)-len(str(person.birthdayDate)))/8)+"|"
            raw += str(person.namedayDate)+"\t"*ceil(((16+ tabSize[3]*8)-len(str(person.namedayDate)))/8)+"|"
            raw += str(person.mail)+"\t"*ceil(((8+ tabSize[4]*8)-len(person.mail))/8)+"|"
            raw += str(person.telNumber)+"\t"*ceil(((16+ tabSize[5]*8)-len(str(person.telNumber)))/8)+"|"
            raw += str(person.facebook)+"\t"*ceil(((16+ tabSize[6]*8)-len(person.facebook))/8)+"|"
            raw += str(person.group)
            print (raw)
