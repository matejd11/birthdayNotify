

class Atribute(object):

    order = ["facebook",
            "sms",
            "mail",
            "show"]
    def __init__(self, event, facebook = False, sms = False, mail = False, show = False):
        self.event = event
        self.facebook = facebook
        self.sms = sms
        self.mail = mail
        self.show = show

