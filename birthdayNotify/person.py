import json


class Person(object):
    header = ["firstName",
              "secondName",
              "mail",
              "telNumber",
              "facebook"]

    order = ["firstName",
             "secondName",
             "mail",
             "telNumber",
             "facebook"]

    def showTable(dataPerson, dataEvent):
        header = Person.header[:]
        order = Person.order[:]

        for event in dataEvent.db:
            order.append(event.name)
            header.append(event.name)
        order.append("group")
        header.append("group")

        content = []
        for person in dataPerson.db:
            content.append(person.convert())

        return header, content, order

    def __init__(self, firstName, secondName, date, mail, telNumber, facebook, mSlots=None, group=None):
        if group is None:
            group = []
        if mSlots is None:
            mSlots = {}
        if date is None:
            date = {}
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

    def addGroup(self, group):
        if group not in self.group:
            self.group.append(group)

    def removeGroup(self, groupName):
        self.group.remove(groupName)

    def showTableGroup(self):
        content = []
        head = self.firstName + " " + self.secondName
        for group in self.group:
            content.append({head: group.name})
        return head, content, head

    def convert(self):
        dictionary = (self.__dict__).copy()
        del dictionary["date"]

        keys = self.date.keys()
        for name in keys:
            dictionary[name] = str(self.date[name])

        gList = []
        for group in self.group:
            gList.append(group.name)
        dictionary["group"] = gList

        return dictionary

    def __str__(self):
        me = self.convert()
        return str(json.dumps(me, sort_keys=True, indent=4))
