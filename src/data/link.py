import src.data.error as error
import src.data.user as user
import typing

link = {
    user.User : user,
    "User" : user,
}

def get(type : typing.Union[str, type]):
    return link.get(type, error)
