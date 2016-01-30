from person import Person


def go(db):
    global status
    while status == 1:
        inputText = input("command> ")
        for i in commands:
            if inputText == i:
                commands[i](db)

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
commands = {"h": helpMe, 
            "a": add, 
            "q": quit, 
            "l": showDb}
commandsHelp = {"h": "help for command help", 
                "a": "help for command add", 
                "q": "help for command quit",
                "l": "help for command list"}
