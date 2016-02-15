

def getNumber(db, reason, mode):
    number = None
    while number is None or number < -1 or number >= len(db):
        try:
            number = int(input("Insert id to "+reason+"(insert -1 to cancel): "))
        except ValueError:
            number = None
    while True and number is not -1:
        if mode == 0:
            y = "Do you want to "+reason+"(" + db[number].firstName + " " + db[number].secondName + ")?"
        if mode == 1 or mode == 2 or mode == 3:
            y = "Do you want to "+reason+"(" + db[number].name + ")?"
        if mode == "removeAG":
            y = "Do you want to "+reason+"(" + str(db[number]) + ")?"
        if yes(y) is True:
            return number
        else:
            break
    return None


def checkBox(text):
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


def yes(text):
    while True:
        yes = input(text+" Y/n: ")
        if yes.lower() == 'y' or yes.lower() == 'yes' or yes == "" or yes == "":
            return True
        elif yes.lower() == 'n' or yes.lower() == 'no':
            return False

