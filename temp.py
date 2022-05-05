from bot import *

class test():
    def __init__(self):
        self.coucou = " salut "

class Test(test):

    def salut(self):
        print(self.coucou)

Test().salut()






validator = Validator()
validator.set_user(0).add_user(1)
print(validator.check())
validator.set_server(0).add_server(0)
print(validator.check())
