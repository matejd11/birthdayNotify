import json
import numpy as np


class Person(object):
    order = ["firstName",
            "secondName",
            "mail",
            "telNumber",
            "facebook"]

    def __init__(self, firstName, secondName, date, mail, telNumber, facebook, mSlots = {}, group = []):
        if group == None:
            group = "None"
        self.firstName = firstName
        self.secondName = secondName
        self.date = date
        self.mail = mail
        self.telNumber = telNumber
        self.facebook = facebook
        self.mSlots = mSlots
        self.mSlots['firstName'] = firstName
        self.mSlots['secondName'] = secondName
        self.group = group

    def convert(self):
        dictionary = (self.__dict__).copy()
        del dictionary["date"]
        keys = self.date.keys()
        for name in keys:
            dictionary[name] = str(self.date[name])
        return dictionary

    def __str__(self):
        me = self.convert()
        return str(json.dumps(me, sort_keys = True, indent = 4))
