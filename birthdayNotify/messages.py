import json


class Messages(object):
    def __init__(self, name, mList, groups = None):
        if groups == None:
            groups = []
        self.name = name
        self.mList = mList
        self.groups = groups

    def __str__(self):
        me = self.__dict__
        return str(json.dumps(me, sort_keys = True, indent = 4))

