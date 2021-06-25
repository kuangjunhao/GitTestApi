from configparser import ConfigParser
from scripts.handle_os import config_path


class HandleConfig:

    def __init__(self, filename):
        self.filename = filename
        self.config = ConfigParser()
        self.config.read(self.filename, encoding="utf-8")

    def get_value(self, area, option):
        """
        获取字符串类型数据
        :param area:
        :param option:
        :return:
        """
        return self.config.get(area, option)

    def get_int(self, area, option):
        """
        获取int类型数据
        :param area:
        :param option:
        :return:
        """
        return self.config.getint(area, option)

    def get_folat(self, area, option):
        """
        获取浮点类型数据
        :param area:
        :param option:
        :return:
        """
        return self.config.getfloat(area, option)

    def get_boolean(self, area, option):
        """
        获取布尔值类型数据
        :param area:
        :param option:
        :return:
        """
        return self.config.getboolean(area, option)

    def get_other_data(self, area, option):
        """
        获取其它类型数据
        :param area:
        :param option:
        :return:
        """
        return eval(self.get_value(area, option))

    def write_config(self, datas, filename):
        """
        写入数据到配置文件
        :param datas: 要写入的数据
        :param filename: 文件名
        :return:
        """
        if isinstance(datas, dict):
            for data in datas.values():
                if not isinstance(data, dict):
                    return "写入数据类型错误"
            config = ConfigParser()
            for key in datas:
                config[key] = datas[key]
            with open(filename, mode="w", encoding="utf-8") as file:
                config.write(file)


do_config = HandleConfig(config_path)
if __name__ == '__main__':
    do_config = HandleConfig(config_path)
