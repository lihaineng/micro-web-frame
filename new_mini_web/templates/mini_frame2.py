"""
前面一个框架当要更新时显然维护起来比较麻烦，利用装饰器原理，结合路由器该连对它进行改造
"""
# 全局变量
import re
import pymysql

ERROR_INFO = "<a href='http://www.douyu.com/directory/game/yz'><img src='images/404.jpg'/></a>"
ERROR_LINE = "HTTP/1.1 404 NotFount\r\n"
RIGHT_LINE = "HTTP/1.1 200 OK\r\n"


def index(path):
    # 获取页面静态资然
    source_name = './templates'
    file_path = source_name + path
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


def center(path):
    # 获取页面静态资然
    source_name = './templates'
    file_path = source_name + path
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


def update(path):
    # 获取页面静态资然
    source_name = './templates'
    file_path = source_name + path
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
    if path == '/index.html':  # 处理请求
        return index(path)
    elif path == '/center.html':
        return center(path)
    elif path == '/update.html':
        return update(path)
    else:
        return ERROR_LINE, ERROR_INFO