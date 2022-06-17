from src.composant.user import User

def to_json(user : User):
    return {
        "__type__": "User",
        "id": user.id,
    }

def from_json(user : dict):
    user_obj = User()
    user_obj.id = user.get("id")
    return user_obj
