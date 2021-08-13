import socket
import re
import multiprocessing
import time
import mini_frame

class WSGIServer(object):


    def __init__(self):
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server_socket.bind(("", 8080))
        self.tcp_server_socket.listen(128)

    def service_client(self,new_socket):
        request = new_socket.recv(1024).decode("utf-8")
        print(">>"*50)
        # print(request)
        if request:
            request_lines = request.splitlines()
            print("")
            print(">>"*20)
            print(request_lines)

            ret = re.match(r"[^/]+(/[^ ]*)", request_lines[0])
            if ret:
                file_name = ret.group(1)
                print("*"*20,file_name)
                if file_name == "/":
                    file_name += "index.html"


            # 如果请求的资源不是以.py结尾，那么就认为是静态资源(html/css/js/png,jpg等)
            if not file_name.endswith('.py'):
                try:
                    with open("."+file_name,'rb') as f:
                        html_content = f.read()
                except:
                    response = "HTTP/1.1 404 NOT FOUND\r\n"
                    response += "\r\n"
                    response += "<h1>------file not found--------<h1>"
                    new_socket.send(response.encode("utf-8"))
                else:
                    response = "HTTP/1.1 200 OK\r\n"
                    response += "\r\n"
                    new_socket.send(response.encode("utf-8"))
                    new_socket.send(html_content)
            else:
                # 如果是以.py结尾，那么就认为是动态资源的请求
                header = "HTTP/1.1 200 OK\r\n"
                header +="\r\n"

                # body = "hahahah {}".format(time.ctime())
                body = mini_frame.application(file_name)

                response = header+body
                new_socket.send(response.encode('utf-8'))


            # 关闭套接字
            new_socket.close()

    def run_forever(self):
        while True:
            # 等待新客户端的链接
            new_socket, client_addr = self.tcp_server_socket.accept()
            p = multiprocessing.Process(target=self.service_client,args = (new_socket,))
            p.start()
            print(new_socket)
            print(client_addr)
            new_socket.close()
            # 上一步开了一个子进程，复制了主进程的大部分资源包括全局变量和局部变量，
            # 即同时有两个new_socket标记了同一个客户端
            # 当子进程通信关闭，关闭new_close，但是主进程仍有一个new_socket指向客户端
            # 所以该客户端的tcp连接不会启动关闭
            # 所以需在主进程中将new_socket关闭，此时没有指向客户端的变量，启动关闭tcp连接
            # 对于Linux来说，一个客户端即对应一个文件描述符，只有没有指向它的东西时，才会关闭（类似python的引用计数）
            # service_client(new_socket)

        self.tcp_server_socket.close()


def main():
    """控制整体，创建web服务器对象，调用run_forever方法"""
    wsgi_server = WSGIServer()
    wsgi_server.run_forever()


if __name__ == "__main__":
    main()