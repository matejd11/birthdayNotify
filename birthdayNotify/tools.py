

def getNumber(db, reason, mode):
    number = None
    while number is None or number < -1 or number >= len(db):
        try:
            number = int(input("Insert id to "+reason+"(insert -1 to cancel): "))
        except ValueError:
            number = None
    while True and number is not -1:
        if mode == 0:
            yes = input("Do you want to "+reason+"(" + db[number].firstName + " " + db[number].secondName + ")? Y/n: ")
        if mode == 1 or mode == 2 or mode == 3:
            yes = input("Do you want to "+reason+"(" + db[number].name + ")? Y/n: ")
        if mode == "removeAG":
            yes = input("Do you want to "+reason+"(" + str(db[number]) + ")? Y/n: ")
        if yes.lower() == 'y' or yes.lower() == 'yes' or yes == "":
            return number
        elif yes.lower() == 'n' or yes.lower() == 'no':
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
