import pickle
import os


class PersonDb(object):
    def __init__(self, dbName, autoload = True):
        self.dbName = dbName
        self.db = None
        if autoload:
            self.setup()

    def setup(self):
        self.db = PersonDb.load(self.dbName)
        self.getGroups()

    def getGroups(self):
        tmp = set()
        for person in self.db:
            for group in person.group:
                tmp.add(person)
        self.groups = tmp

    def add(self, person):
        self.db.append(person)

    def save(data, fileName = None):
        if fileName == None:
            fileName = self.dbName
        filen = PersonDb.fileExtension(fileName)
        with open(filen,"wb") as pickleOut:
            pickle.dump(data, pickleOut)

    def load(fileName = None):
        if fileName == None:
            fileName = self.dbName
        filen = PersonDb.fileExtension(fileName)
        try:
            with open(filen, "rb") as pickleIn:
                data = pickle.load(pickleIn)
            return data
        except FileNotFoundError:
            return []

    def fileExtension(fileName):
        result = fileName.strip()
        if '.json' not in result:
            result += '.json'
        return result
