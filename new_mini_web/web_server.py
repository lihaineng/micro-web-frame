"""
利用多进程来维护效率
"""
import socket

import time

import sys

import os

from mini_frame2 import app


class HttpSever(object):
    def __init__(self, port):   # 初始化，创建特产品连接
        # 创建客户端socket,并复用端口
        self.sever_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sever_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        # 绑定端口
        self.sever_socket.bind(('',int(port)))
        # 设置监听
        self.sever_socket.listen(5)

    @staticmethod
    def get_msg(new_socket):
        info = new_socket.recv(1024)
        info_list = info.decode().split("\r\n")
        file_name_list = info_list[0].split(" ")
        try:
            file_name = file_name_list[1]
            return file_name
        except:
            return None         # 当关闭网页时会收到空消息,不处理会报错

    @staticmethod
    def send_msg(new_socket, file_name):
        sources_path = './static'
        t_now = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        if file_name == '/':
            file_name = '/index.html'
        path = sources_path + file_name
        response_line = 'HTTP/1.1 200 OK\r\n'
        response_header = 'Server: Tengine\r\n'
        response_header += 'Content-Type: text/css,text/html; charset=UTF-8\r\n' # 为什么text/css加在这里，思考下！！
        response_header += 'Connection: keep-alive\r\n'
        response_header += 'Date: %s\r\n' % t_now
        try:
            with open(path,'rb') as f:
                response_body = f.read()
        except:
            response_line = 'HTTP/1.1 404 Not Found\r\n'
            response_body = "<a href='http://www.douyu.com/directory/game/yz'><img src='images/404.jpg'/></a>".encode()
        finally:
            send_data = response_line + response_header + '\r\n'
            new_socket.send(send_data.encode() + response_body)

    @staticmethod
    def send_dynamic_msg(new_socket, file_name):
        # 动态消息要通过第三放框架获取
        info_dict = {'INFO': file_name}   # 当作一种与框架通讯的默认协议
        t_now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        response_header = 'Server: Tengine\r\n'
        response_header += 'Content-Type: text/html; charset=UTF-8\r\n'
        response_header += 'Connection: keep-alive\r\n'
        response_header += 'Date: %s\r\n' % t_now
        response_line, response_body = app(info_dict)
        send_data = response_line + response_header + '\r\n'
        data = send_data + response_body
        new_socket.send(data.encode())

    def startup(self):
        while True:  # 因为服务器启动后要一直工作所以用死循环
            new_socket, client_addr = self.sever_socket.accept()
            # 服务器作用是发消息，和接收消息
            file_name = HttpSever.get_msg(new_socket)  # 接收消息,调用类方法
            if file_name != None:  # 判断情况发送消息
                if file_name.endswith('.html'): # 如果是'.html',怎要发送的是动态消息
                    HttpSever.send_dynamic_msg(new_socket, file_name)
                else:
                    HttpSever.send_msg(new_socket, file_name)
            new_socket.close()

    def __del__(self):
        self.sever_socket.close()


def main():
    # 创建Http对象
    if len(sys.argv) < 2:
        print("请输入正确的端口号:")
        print("参考如下: python3 xxx.py 8888")
        return
    try:
        port = sys.argv[1]
    except:
        print("请输入正确的端口号:")
        print("参考如下: python3 xxx.py 8888")
    http_sever = HttpSever(port)   # 创建对象
    print("这是进程%s" % os.getpid())
    http_sever.startup()        # 启动服务
    


if __name__ == '__main__':
   main()
