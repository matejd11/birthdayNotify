from person import Person
from personDb import PersonDb
import readline
import re

class Shell(object):
    def __init__(self, dbName = "database"):
        self.db = PersonDb(dbName)
        self.status = 1
        self.commands = {"help": self.helpMe,
                        "add": self.add,
                        "save $": self.saveDb,
                        "load $": self.loadDb,
                        "quit": self.quit,
                        "exit": self.quit,
                        "list": self.showDb,
                        "table": self.showTable}

        self.commandsHelp = {"help": "help for command help",
                            "add": "help for command add",
                            "quit": "help for command quit",
                            "list": "help for command list"}

    def go(self):
        while self.status == 1:
            inputText = input("command> ").strip()
            resArray = {}
            for i in self.commands:
                res = re.search("^" + inputText + ".*", i)
                resArray[i] = res

            candidate = []
            for i in resArray:
                if resArray[i] != None:
                    candidate.append(i)

            if len(candidate) == 1:
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
        for i in self.commandsHelp:
            print("\t", i, ":",  self.commandsHelp[i])

    def add(self):
        print("add")

        firstName = input("\tfirstName: ")
        secondName = input("\tsecondName: ")
        birthdayDate = input("\tbirthdayDate: ")
        namedayDate = input("\tnamedayDate: ")
        mail = input("\tmail: ")
        telNumber = input("\ttelNumber: ")
        facebook = input("\tfacebook: ")
        group = input("\tgroup: ")

        newPerson = Person(firstName, secondName, birthdayDate,namedayDate, mail, telNumber, facebook, group)

        self.db.add(newPerson)

    def showDb(self):
        for person in self.db.db:
            print(person)

    def quit(self):
        self.status = 0

    def showTable(self):
        print("\tfirstName\t|secondName\t|birthdayDate\t|namedayDate\t|mail\t\t|telNumber\t|facebook\t|group")
        print("\t"+"-"*8*16)
        for person in db.db:
            raw = "\t"+str(person.firstName)+"\t"*((16-len(person.firstName))//8+1)+"|"
            raw += str(person.secondName)+"\t"*((16-len(person.secondName))//8+1)+"|"
            raw += str(person.birthdayDate)+"\t"*((16-len(person.birthdayDate))//8+1)+"|"
            raw += str(person.namedayDate)+"\t"*((16-len(person.namedayDate))//8+1)+"|"
            raw += str(person.mail)+"\t"*((16-len(person.mail))//8+1)+"|"
            raw += str(person.telNumber)+"\t"*((16-len(person.telNumber))//8+1)+"|"
            raw += str(person.facebook)+"\t"*((16+len(person.facebook))//8)+"|"
            raw += str(person.group)
            print (raw)

