import json


class Person(object):
    def __init__(self, firstName, secondName, birthdayDate, namedayDate, mail, telNumber, facebook, group = None):
        if group == None:
            group = []
        self.firstName = firstName
        self.secondName = secondName
        self.birthdayDate = birthdayDate
        self.namedayDate = namedayDate
        self.mail = mail
        self.telNumber = telNumber
        self.facebook = facebook
        self.group = group

    def __str__(self):
        return str(json.dumps(self.__dict__, sort_keys = True, indent = 4))
