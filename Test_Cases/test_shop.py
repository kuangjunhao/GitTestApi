import unittest
from scripts.handle_config import do_config
from scripts.handle_excel import HandleExcel
from scripts.handle_request import HandleRequest
from scripts.handle_os import cases_path
from scripts.handle_mysql import HandleMysql
from libs.ddt import ddt, data
do_excel = HandleExcel(cases_path, "shop")
cases = do_excel.get_cases()


@ddt
class TestAddShop(unittest.TestCase):

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
        url = do_config.get_value("urlhost", "url") + one_case["url"]
        head = {"access-token": self.token}
        sql = one_case["check_sql"]
        if sql is not None:
            sql_data = self.mysql.run_sql(sql)
            id_before =sql_data["id"]
        result = self.res.do_request(
                                    url=url,
                                    data=one_case["data"],
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
                id_after =mysql_data["id"]
                self.assertEqual(id, id_after, msg=msg)
            do_excel.write_excel(one_case["case_id"]+1, result.text, success_msg)
        except AssertionError as e:
            do_excel.write_excel(one_case["case_id"] + 1, result.text, fail_msg)
            raise e


if __name__ == '__main__':
    unittest.main()