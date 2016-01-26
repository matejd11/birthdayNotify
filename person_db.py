import pickle


class person_db(object):
    def __init__(self, db_name, autoload = True):
        self.db_name = db_name
        if autoload:
        self.setup()

    def setup(self):
        self.db = person_db.load(self.db_name)
        self.get_groups()

    def get_groups(self):
        tmp = set()
        for person in self.db:
        for group in person:
        tmp.append(person)
        self.groups = tmp

    def save(data, file_name = 'database'):
        filen = file_extension(file_name)
        with open(filen,"wb") as pickle_out:
            pickle.dump(data, pickle_out)

    def load(file_name = 'database'):
        filen = file_extension(file_name)
        with open(filen, "rb") as pickle_in: 
            data = pickle.load(pickle_in)
        return data

    def file_extension(file_name):
        result = file_name.strip()
        if '.json' not in result:
            result += '.json'
        return result
