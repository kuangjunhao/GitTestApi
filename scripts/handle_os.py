import os

BaseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#datas路径
DataDir = os.path.join(BaseDir, "datas")
#配置文件路径
config_path = os.path.join(DataDir, "testcases.conf")
#用例路径
cases_path = os.path.join(DataDir, "cases.xlsx")

#报告文件夹路径
ReportDir = os.path.join(BaseDir, "reports")
#报告文件路径
report_file = os.path.join(ReportDir, "report.html")
