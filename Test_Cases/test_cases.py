import unittest
from libs.ddt import ddt, data
from scripts.handle_config import do_config
from scripts.handle_excel import HandleExcel
from scripts.handle_os import cases_path
from scripts.handle_request import HandleRequest


do_excel = HandleExcel(cases_path, "login")
cases = do_excel.get_cases()
@ddt
class TestLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.res = HandleRequest()

    @classmethod
    def tearDownClass(cls):
        cls.res.close()

    @data(*cases)
    def test_login_t(self, one_case):
        url = do_config.get_value("urlhost", "url")+one_case["url"]
        request_data = one_case["data"]
        result = self.res.do_request(url=url,
                                     method=one_case['method'],
                                     data=request_data,
                                     is_json=True)
        expect_result = one_case["expected"]
        msg = one_case["title"]
        success_msg = do_config.get_value("msg", "success_result")
        fail_msg = do_config.get_value("msg", "fail_result")
        try:
            self.assertIn(expect_result, result.text, msg=msg)
            do_excel.write_excel(one_case["case_id"]+1, result.text, success_msg)
        except AssertionError as e:
            do_excel.write_excel(one_case["case_id"]+1, result.text, fail_msg)
            raise e


    # def test_login_f(self):
    #     res=requests.Session()
    #     url = "http://test.mg.zhongbaojinfu.com.cn/api/login"
    #     data = {"username": "kaungjh", "password": "abc45531893"}
    #     result = res.post(url=url, json=data)
    #     code=result.status_code
    #     res.close()
    #     self.assertEqual(201,code,msg="登录成功")

if __name__ == '__main__':
    unittest.main()

