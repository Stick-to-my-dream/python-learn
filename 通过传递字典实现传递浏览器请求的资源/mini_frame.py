def login():
    # return '这里是登录界面'
    with open("../index.html",encoding='utf-8') as f:
        content = f.read()
    return content

def register():
    # return "register"
    with open('./HTMLsite-master/HTMLsite/index.html',encoding='utf-8') as f:
        content = f.read()
    return content

def other():
    with open("./HTMLsite-master/HTMLsite/立方体.html",encoding="utf-8") as f:
        content = f.read()
    return content


def application(environ,start_response):
    start_response('200 OK',[('Content-Type','text/html;charset=utf-8')])
    file_name = environ['PATH']

    if file_name == "/register.py":
        return register()
    elif file_name == "/login.py":
        return login()
    else:
        return other()