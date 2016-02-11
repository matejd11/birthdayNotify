

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
