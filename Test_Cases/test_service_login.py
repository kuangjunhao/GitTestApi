import unittest
from scripts.handle_config import do_config
from scripts.handle_excel import HandleExcel
from scripts.handle_request import HandleRequest
from scripts.handle_os import cases_path
from libs.ddt import ddt, data

do_excel = HandleExcel(cases_path, "login")
cases = do_excel.get_cases()


@ddt
class TestLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        建立请求
        :return:
        """
        cls.res = HandleRequest()

    @classmethod
    def tearDownClass(cls):
        """
        关闭请求
        :return:
        """
        cls.res.close_session()

    @data(*cases)
    def test_login(self, one_cases):
        """
        登录接口测试
        :param one_cases: 测试数据
        :return:
        """
        url = do_config.get_value("urlhost", "service_url") + one_cases["url"]
        request_data = one_cases["data"]
        result = self.res.do_request(
                                    url=url,
                                    data=request_data,
                                    method=one_cases["method"],
                                    is_json=True)
        except_result = one_cases["expected"]
        msg = one_cases["title"]
        success_msg = do_config.get_value("msg", "success_result")
        fail_msg = do_config.get_value("msg", "fail_result")
        try:
            self.assertIn(except_result, result.text, msg=msg)
            do_excel.write_excel(one_cases["case_id"]+1, result.text, success_msg)
        except AssertionError as e:
            do_excel.write_excel(one_cases["case_id"]+1, result.text, fail_msg)
            raise e


if __name__ == '__main__':
    unittest.main()

