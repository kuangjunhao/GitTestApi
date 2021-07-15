import re
from faker import Faker


fake=Faker(locale="zh_CN")
shop_name=fake.company_prefix()


# class Context:
#     shop_name_patten = r"\${shop_name}"
#
#     @classmethod
#     def name_replace(cls):
#         if