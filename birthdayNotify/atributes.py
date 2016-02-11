from tools import checkBox


class Atribute(object):

    header = ["facebook",
              "sms",
              "mail",
              "show"]

    order = ["facebook",
             "sms",
             "mail",
             "show"]

    def __init__(self, event, facebook=False, sms=False, mail=False, show=False):
        self.event = event
        self.facebook = facebook
        self.sms = sms
        self.mail = mail
        self.show = show

    def addAtr(event):
        while True:
            facebook = checkBox("\t\t  send by Facebook:\t")
            sms = checkBox("\t\t  send by sms:\t\t")
            mail = checkBox("\t\t  send by e-mail:\t")
            show = checkBox("\t\t  show message:\t\t")
            if facebook is True or sms is True or mail is True or show is True:
                return facebook, sms, mail, show
            print("Choose atleast one atribute.")

    def editAtr(self, event):
        while True:
            facebook = checkBox("\t\t  send by Facebook("+str(int(self.facebook))+"):\t")
            sms = checkBox("\t\t  send by sms("+str(int(self.sms))+"):\t")
            mail = checkBox("\t\t  send by e-mail("+str(int(self.mail))+"):\t")
            show = checkBox("\t\t  show message("+str(int(self.show))+"):\t")
            if facebook is True or sms is True or mail is True or show is True:
                return facebook, sms, mail, show
            print("Choose atleast one atribute.")

