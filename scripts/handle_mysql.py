import pymysql
from scripts.handle_config import do_config


class HandleMysql:

    def __init__(self, host, user, pwd, db, port):
        """
        创建数据库连接实例方法
        :param host: 主机
        :param user: 用户名
        :param pwd: 密码
        :param db: 数据库
        :param port:端口
        """
        self.connect = pymysql.connect(host=host,
                                       user=user,
                                       password=pwd,
                                       db=db,
                                       port=port,
                                       charset="utf8",
                                       # 字典类游标
                                       cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connect.cursor()

    def run_sql(self, sql, args=None, is_more=None):
        """
        执行sql方法
        :param sql: sql语句
        :param args:  sql参数
        :param is_more:是否返回多条结果
        :return:sql执行结果,   返回的是字典类型数据
        """
        self.cursor.execute(sql, args=args)
        self.connect.commit()
        if is_more:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchone()

    def close_sql(self):
        """
        关闭数据库连接方法
        :return:
        """
        self.cursor.close()
        self.connect.close()

if __name__ == '__main__':
    sql='select COUNT(*) as count from service_mall.shop'
    mysql=HandleMysql(host=do_config.get_value("mysql", "host"),  # 地址
                                user=do_config.get_value("mysql", "user"),  # 账号
                                pwd=do_config.get_value("mysql", "password"),  # 密码
                                db=do_config.get_value("mysql", "service_db"),  # 库名
                                port=do_config.get_int("mysql", "port"))
    data=mysql.run_sql(sql=sql)
    mysql.close_sql()
    print(data)
    print(data["count"])
