import unittest
from scripts.handle_config import do_config
from scripts.handle_excel import HandleExcel
from scripts.handle_request import HandleRequest
from scripts.handle_os import cases_path
from scripts.handle_mysql import HandleMysql
from scripts.handle_context import Context, ShopId
from libs.ddt import ddt, data


@ddt
class TestAddShop(unittest.TestCase):
    """
    测试新增店铺类
    """
    do_excel = HandleExcel(cases_path, "shop")
    cases = do_excel.get_cases()
    @classmethod
    def setUpClass(cls):
        """
        建立请求
        :return:
        """
        cls.res = HandleRequest()
        cls.token = cls.res.get_token()
        cls.mysql = HandleMysql(host=do_config.get_value("mysql", "host"),
                                user=do_config.get_value("mysql", "user"),
                                pwd=do_config.get_value("mysql", "password"),
                                db=do_config.get_value("mysql", "service_db"),
                                port=do_config.get_int("mysql", "port"))

    @classmethod
    def tearDownClass(cls):
        """
        关闭请求
        :return:
        """
        cls.res.close_session()
        cls.mysql.close_sql()

    @data(*cases)
    def test_insert_shop(self, one_case):
        """
        测试新增店铺接口
        :param one_case:请求数据
        :return:
        """
        # replace_data = one_case["data"]
        # print(replace_data)
        new_data = Context.shop_name_param(one_case["data"]) #参数化后的请求数据
        print(new_data)
        url = do_config.get_value("urlhost", "url") + one_case["url"]
        head = {"access-token": self.token}
        sql = one_case["check_sql"]
        if sql is not None:
            sql_data = self.mysql.run_sql(sql)
            id_before =sql_data["count"]
        result = self.res.do_request(
                                    url=url,
                                    data=new_data,
                                    is_json=True,
                                    head=head)
        expect_result = one_case["expected"]
        msg = one_case["title"]
        success_msg = do_config.get_value("msg", "success_result")
        fail_msg = do_config.get_value("msg", "fail_result")
        try:
            self.assertIn(expect_result, result.text, msg=msg)
            if sql:
                mysql_data = self.mysql.run_sql(sql)
                id = id_before + 1
                id_after =mysql_data["count"]
                self.assertEqual(id, id_after, msg=msg)
            TestAddShop.do_excel.write_excel(one_case["case_id"]+1, result.text, success_msg)
        except AssertionError as e:
            TestAddShop.do_excel.write_excel(one_case["case_id"] + 1, result.text, fail_msg)
            raise e


@ddt
class TestEditShop(unittest.TestCase):
    """
    测试编辑店铺类
    """
    do_excel = HandleExcel(cases_path, "edit")
    cases = do_excel.get_cases()

    @classmethod
    def setUpClass(cls):
        """
        建立接口请求会话
        获取登录token
        建立数据库连接
        :return:
        """
        cls.res = HandleRequest()
        cls.token = cls.res.get_token()
        cls.mysql = HandleMysql(host=do_config.get_value("mysql", "host"),
                                user=do_config.get_value("mysql", "user"),
                                pwd=do_config.get_value("mysql", "password"),
                                db=do_config.get_value("mysql", "service_db"),
                                port=do_config.get_int("mysql", "port"))

    @classmethod
    def tearDownClass(cls):
        """
        关闭接口请求会话；关闭数据库连接
        :return:
        """
        cls.res.close_session()
        cls.mysql.close_sql()

    @data(*cases)
    def test_edit_shop(self, one_case):
        new_data = ShopId.shop_id_param(one_case["data"]) #参数化后的请求数据
        # print(new_data)
        url = do_config.get_value("urlhost", "url") + one_case["url"]
        head = {"access-token": self.token}
        res = self.res.do_request(url=url,
                                  data=new_data,
                                  is_json=True,
                                  head=head)
        if "操作成功" in res.text:
            sql = one_case["check_sql"]
            if sql:
                check_sql =Context.shop_name_param(sql)
                sql_data = self.mysql.run_sql(sql=check_sql)
                # 动态创建类属性
                # 如果第一个为实例对象，将会为这个实例对象创建实例属性
                # 如果第一个为类，将会创建类属性
                # 第二个参数，为属性名的字符串
                # 第三个参数，为具体的属性值
                setattr(Context, "shop_id", sql_data["id"])
                setattr(Context, "shop_name", sql_data["name"])

        expect_result = one_case["expected"]  # 期望结果
        msg = one_case["title"]
        success_msg = do_config.get_value("msg", "success_result")
        fail_msg = do_config.get_value("msg", "fail_result")
        try:
            self.assertIn(expect_result, res.text, msg=msg)
            TestEditShop.do_excel.write_excel(one_case["case_id"] + 1, res.text, success_msg)
        except AssertionError as e:
            TestEditShop.do_excel.write_excel(one_case["case_id"] + 1, res.text, fail_msg)
            raise e


        pass


if __name__ == '__main__':
    unittest.main()