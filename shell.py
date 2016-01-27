from person import Person


def go(db):
    global status
    while status == 1:
        inputText = input("command>")
        for i in commands:
            if inputText == i:
                commands[i](db)

def helpMe(db):
    print("help:")
    for i in commandsHelp:
        print(i, ":",  commandsHelp[i])

def add(db):
    print("add")

    firstName = input("firstName:")
    secondName = input("secondName:")
    birthdayDate = input("birthdayDate:")
    namedayDate = input("namedayDate:")
    mail = input("mail:")
    telNumber = input("telNumber:")
    facebook = input("facebook:")
    group = input("group:")

    newPerson = Person(firstName, secondName, birthdayDate,namedayDate, mail, telNumber, facebook, group)

    db.add(newPerson)

def showDb(db):
    for index in db.db:
        print(index)

def quit(db):
    global status
    status = 0

status = 1
commands = {"h": helpMe, "a": add, "q": quit, "l": showDb}
commandsHelp = {"h": "help for command help", "a": "help for command add", "q": "help for command quit"}
