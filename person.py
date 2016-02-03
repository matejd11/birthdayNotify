import json
import numpy as np

class Person(object):
    order = ["firstName",
            "secondName",
            "birthdayDate",
            "namedayDate",
            "mail",
            "telNumber",
            "facebook",
            "group"]
    def __init__(self, firstName, secondName, birthdayDate, namedayDate, mail, telNumber, facebook, group = None):
        if group == None:
            group = "None"
        self.firstName = firstName
        self.secondName = secondName
        self.birthdayDate = np.dtype(np.datetime64)
        self.birthdayDate = birthdayDate
        self.namedayDate = np.dtype(np.datetime64)
        self.namedayDate = namedayDate
        self.mail = mail
        self.telNumber = telNumber
        self.facebook = facebook
        self.group = group

    def __str__(self):
        me = self.__dict__
        me["birthdayDate"] = str(me["birthdayDate"])
        me["namedayDate"] = str(me["namedayDate"])
        return str(json.dumps(me, sort_keys = True, indent = 4))
