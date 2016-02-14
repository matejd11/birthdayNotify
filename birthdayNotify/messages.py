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

    def __init__(self, name, mList, slots=None, groups=None):
        if groups is None:
            groups = []
        if slots is None:
            slots == []
        self.name = name
        self.mList = mList
        self.groups = groups

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
