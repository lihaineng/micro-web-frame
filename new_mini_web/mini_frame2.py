"""
显然前面一个框架更新维护起来很麻烦，现在借助装饰器和路由器原理对它进行升级
"""
# 全局变量
import re

import pymysql

file_func_list = []
ERROR_INFO = "<a href='http://www.douyu.com/directory/game/yz'><img src='images/404.jpg'/></a>"
ERROR_LINE = "HTTP/1.1 404 NotFount\r\n"
RIGHT_LINE = "HTTP/1.1 200 OK\r\n"


# 装饰器来制作路由器
def add(file):
    def outer(func):
        file_func_list.append((file, func))
        def inner():
            func()
        return inner
    return outer


@add('/index.html')
def index():
    # 获取页面静态资然
    source_name = './templates'
    file_path = source_name + '/index.html'
    try:
        with open(file_path, 'r') as f:
            data = f.read()
    except:
        return ERROR_LINE, ERROR_INFO
    # 从数据库获取页面动态资然
    # 1 创建连接
    conn = pymysql.connect(host='localhost', user='root', password='lihaineng',
                 database='stock_db', port=3306, charset='utf8')
    # 2 创建游标
    cur = conn.cursor()
    # 3 利用游标执行sql语句获取信息
    cur.execute('select * from info')
    # 4 抓取信息
    info_list = cur.fetchall()

    # 利用数据库获取的数据完善静态页面
    temp = ''
    for i in info_list:
        dynamic_info = """<tr>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td></td>
                        </tr>
                    """ % (i[0],i[1], i[2], i[3], i[4], i[5], i[6], i[7])
        temp += dynamic_info
    data = re.sub(r'{%content%}', temp, data)
    return RIGHT_LINE, data


@add('/center.html')
def center():
    # 获取页面静态资然
    source_name = './templates'
    file_path = source_name + '/center.html'
    try:
        with open(file_path, 'r') as f:
            data = f.read()
    except:
        return ERROR_LINE, ERROR_INFO
    # 从数据库获取页面动态资然
    # 1 创建连接
    conn = pymysql.connect(host='localhost', user='root', password='lihaineng',
                           database='stock_db', port=3306, charset='utf8')
    # 2 创建游标
    cur = conn.cursor()
    # 3 利用游标执行sql语句获取信息
    sql = 'select i.code,i.short,i.chg,i.turnover,i.price,i.highs,f.note_info  from focus as f join info as i on f.info_id = i.id'
    cur.execute(sql)
    # 4 抓取信息
    info_list = cur.fetchall()

    # 利用数据库获取的数据完善静态页面
    temp = ''
    for i in info_list:
        dynamic_info = """<tr>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td></td>
                            <td></td>
                            </tr>
                        """ % (i[0], i[1], i[2], i[3], i[4], i[5], i[6])
        temp += dynamic_info
    data = re.sub(r'{%content%}', temp, data)
    return RIGHT_LINE, data


@add('/update.html')
def update():
    # 获取页面静态资然
    source_name = './templates'
    file_path = source_name + '/update.html'
    try:
        with open(file_path, 'r') as f:
            data = f.read()
    except:
        return ERROR_LINE, ERROR_INFO
    # 从数据库获取页面动态资然
    # 1 创建连接
    conn = pymysql.connect(host='localhost', user='root', password='lihaineng',
                           database='stock_db', port=3306, charset='utf8')
    # 2 创建游标
    cur = conn.cursor()
    # 3 利用游标执行sql语句获取信息
    sql = 'select i.code,i.short,i.chg,i.turnover,i.price,i.highs,f.note_info  from focus as f join info as i on f.info_id = i.id'
    cur.execute(sql)
    # 4 抓取信息
    info_list = cur.fetchall()

    # 利用数据库获取的数据完善静态页面
    # temp = ''
    # for i in info_list:
    #     dynamic_info = """<tr>
    #                            <td>%s</td>
    #                            <td>%s</td>
    #                            <td>%s</td>
    #                            <td>%s</td>
    #                            <td>%s</td>
    #                            <td>%s</td>
    #                            <td>%s</td>
    #                            <td></td>
    #                            <td></td>
    #                            </tr>
    #                        """ % (i[0], i[1], i[2], i[3], i[4], i[5], i[6])
    #     temp += dynamic_info
    # data = re.sub(r'{%content%}', temp, data)
    return RIGHT_LINE, data


def app(info_dict):  # 框架调用接口
    path = info_dict['INFO']  # 获取服务器传来的请求信息
    for file, func in file_func_list:    # 处理请求
        if path == file:
            return func()
    else:
        return ERROR_LINE, ERROR_INFO