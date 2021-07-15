from libs.HTMLTestRunnerNew import HTMLTestRunner
import unittest


#获取所有的测试用例
test_suit = unittest.defaultTestLoader.discover("C:\PM_project\GitTestApi\datas\cases.xlsx")
#创建测试报告文件
report_file = open(r"C:\PM_project\GitTestApi\reports\report.html", mode="wb")
#创建执行用例的对象
one_runner = HTMLTestRunner(
        stream=report_file,
        title="测试报告",
        verbosity=2,
        description="很牛皮的报告",
        tester="7")
#执行用例
one_runner.run(test_suit)
report_file.close()