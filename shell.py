from person import Person
from group import Group
from atributes import Atribute
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

    def modeName(self):
        if self.mode == 0:
            return "Person"
        if self.mode == 1:
            return "Group"

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
            try:
                self.mode = int(input("\tChange mode to 0 = Person or 1 = Group: "))
                if self.mode == 0 or self.mode == 1:
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
            
    def addAtributes(self, name):
        print("\t\tAtributes for "+name)
        while True:
            facebook = self.checkBox("\t\t  send by Facebook: ")
            sms = self.checkBox("\t\t  send by sms: ")
            mail = self.checkBox("\t\t  send by e-mail: ")
            show = self.checkBox("\t\t  show message: ")
            if facebook == True or sms == True or mail == True or show == True:
                break
            print("Choose atleast one atribute.")
        return Atribute(name, facebook, sms, mail, show)

    def addGroup(self):
        print("    add")
        name = input("    groupName: ")
        print("\t#use 1: yes 0: no")
        print("\tAssign atributes to")
        while True:
            namedayAtr = False
            birthdayAtr = False

            namedayDate = self.checkBox("\t  namedayDate: ")
            if namedayDate == True:
                namedayAtr = self.addAtributes(name+"Nameday")
            birthdayDate = self.checkBox("\t  birthdayDate: ")
            if birthdayDate == True:
                birthdayAtr = self.addAtributes(name+"Birthday")

            if birthdayDate == True or namedayDate == True:
                break
            print("Choose atleast one. Atributes can't be assigned to nothing.")
        newGroup = Group(name, namedayAtr, birthdayAtr)

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

        self.db.add(newPerson)

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
        head = ["firstName",
                "secondName",
                "1234birthdayDate",
                "namedayDate",
                "mail",
                "telNumber",
                "facebook",
                "group"]
        self.showTable(head, self.db.db, Person.order)

    def showTable(self, head, content, order):
        largestStr = {}
        length = []
        for x in head:
            largestStr[x] = 0
            length.append(8*(len(x)//8)+8)

        for person in content:
            tmp = person.__dict__
            for i in range(len(order)):
                if largestStr[head[i]] < len(str(tmp[order[i]])):
                    largestStr[head[i]] = len(str(tmp[order[i]]))

        tabSize = []
        headStr = " ID\t"
        for i in range(len(head)-1):
            tabSize.append(ceil((largestStr[head[i]]-length[i])/8))
            if tabSize[i] < 0:
                tabSize[i] = 0
            headStr += "|"+head[i]+ "\t"*tabSize[i] + "\t"
        headStr += "|"+head[-1]
        print(headStr)

        print(" "+"-"*8*17)

        for count, person in enumerate(content):
            tmp = person.__dict__
            raw =" ["+str(count)+"]\t|"
            for i in range(len(order)-1):
                raw += str(tmp[order[i]])+"\t"*ceil(((length[i]+ tabSize[i]*8)-len(str(tmp[order[i]])))/8)+"|"
            raw += str(tmp[order[-1]])
            print (raw)
