import re
from scripts.handle_excel import HandleExcel
from scripts.handle_os import cases_path
from datas.random_data import RandomData
from libs.ddt import ddt, data
import unittest
# do_excel = HandleExcel(cases_path, "shop")
# cases = do_excel.get_cases()


class Context:
    shop_name_patten = r"\${shop_name}"

    @classmethod
    def name_replace(cls, data):
        if re.search(cls.shop_name_patten, data):
            shop_name = RandomData().shop_name_data()
            data = re.sub(cls.shop_name_patten, shop_name, data)
        return data

    @classmethod
    def shop_name_param(cls, data):
        """
        店铺名称参数化
        :param data:
        :return: 替换后的参数
        """
        data = cls.name_replace(data)
        return data


class ShopId:

    shop_id_patten = r"\${shop_id}"
    shop_name_patten = r"\${sqlshop_name}"
    @classmethod
    def shop_id_replace(cls, data):
        if re.search(cls.shop_id_patten, data):
            shop_id =str(getattr(Context, "shop_id"))
            data = re.sub(cls.shop_id_patten, shop_id, data)
        return data

    @classmethod
    def shop_name_replace(cls, data):
        if re.search(cls.shop_name_patten, data):
            shop_name = str(getattr(Context, "shop_name"))
            data = re.sub(cls.shop_name_patten, shop_name,data)
        return data

    @classmethod
    def shop_id_param(cls, data):
        data = cls.shop_id_replace(data)
        data = cls.shop_name_replace(data)
        data = Context.name_replace(data)
        return data


