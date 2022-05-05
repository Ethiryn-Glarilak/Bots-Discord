from bot import *

validator = Validator()
validator.set_user(0).add_user(1)
print(validator.check())
validator.set_server(0).add_server(0)
print(validator.check())
