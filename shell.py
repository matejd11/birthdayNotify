from person import Person
import readline
import re


def go(db):
    global status
    while status == 1:
        inputText = input("command> ")
        resArray = {}
        for i in commands:
            res = re.search("^" + inputText + ".*", i)
            resArray[i] = res

        candidate = []
        for i in resArray:
            if resArray[i] != None:
                candidate.append(i)

        if len(candidate) == 1:
            commands[candidate[0]](db)
        elif len(candidate) > 1:
            print("do you mean:")
            for can in candidate:
                print("\t", can)
        else:
            print("use h/help for help.")

def helpMe(db):
    print("help:")
    for i in commandsHelp:
        print("\t", i, ":",  commandsHelp[i])

def add(db):
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

    db.add(newPerson)

def showDb(db):
    for index in db.db:
        print(index)

def quit(db):
    global status
    status = 0

status = 1
commands = {"help": helpMe,
            "add": add,
            "quit": quit,
            "exit": quit,
            "list": showDb}
commandsHelp = {"help": "help for command help",
                "add": "help for command add",
                "quit": "help for command quit",
                "list": "help for command list"}
