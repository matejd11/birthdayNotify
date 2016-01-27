import pickle


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
        for group in person:
        tmp.append(person)
        self.groups = tmp

    def save(data, fileName = 'database'):
        filen = fileExtension(fileName)
        with open(filen,"wb") as pickleOut:
            pickle.dump(data, pickleOut)

    def load(fileName = 'database'):
        filen = fileExtension(fileName)
        with open(filen, "rb") as pickleIn:
            data = pickle.load(pickleIn)
        return data

    def fileExtension(fileName):
        result = fileName.strip()
        if '.json' not in result:
            result += '.json'
        return result
