import time

def login():
    return "welcome to our website.......time {}".format(time.ctime())


def register():
    return "register----{}".format(time.ctime())


def profile():
    return  "profile----{}".format(time.ctime())


def application(file_name):
    if file_name=="/login.py":
        return login()
    elif file_name=="/register.py":
        return register()
    elif file_name=="/profile.py":
        return profile()
    else:
        return "not found file"