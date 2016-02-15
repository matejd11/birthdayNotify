from tools import yes
import json


class Messages(object):
    header = ["Messages from 'NONE' package"]
    order = ["mList"]

    def showTable(dataMessage, index):
        package = dataMessage.db[index]
        header = ["Messages from '" + package.name + "' package"]
        order = Messages.order

        content = []
        for message in package.mList:
            dicti = {}
            dicti["mList"] = message
            content.append(dicti)

        return header, content, order

    def __init__(self, name, mList=None, slots=None, groups=None):
        if groups is None:
            groups = []
        if slots is None:
            slots == {}
        if mList is None:
            mList = []
        self.name = name
        self.mList = mList
        self.groups = groups

    def add(self):
        name = input("\tName of the package("+self.name+"):\t")
        print("\t----------------------------------------------------------------")
        print("\t  **Usable slots: ")
        mList = []
        x = -1
        while True:
            x += 1
            try:
                print("\t\toldMessage:\t"+self.mList[x])
                message = input("\t\tmessage["+str(x)+"]:\t")
            except IndexError:
                message = input("\t\tmessage["+str(x)+"]:\t")
            mList.append(message)
            #regex slots
            #self.slots[x] = slots
            if yes("\t  More messages?") is False:
                break
        self.name = name
        self.mList = mList

    def convert(self):
        dicti = {}
        dicti["name"] = self.name
        groups = []
        for group in self.groups:
            groups.append(group.name)
        dicti["groups"] = groups
        return dicti

    def __str__(self):
        me = self.__dict__
        return str(json.dumps(me, sort_keys=True, indent=4))
