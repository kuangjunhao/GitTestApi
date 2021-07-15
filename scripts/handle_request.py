import requests
import json
from scripts.handle_config import do_config


class HandleRequest:

    def __init__(self):
        """
        创建会话
        """
        self.one_session = requests.Session()

    def do_request(self, url, method="post", data=None, is_json=False, head=None):
        """
        发起请求方法
        :param url:地址
        :param method: 请求方法
        :param data: 请求数据
        :param is_json: 是否为json数据
        :return: 相应报文
        """
        if isinstance(data, str):
            # 是将json字符串传化为字典
            data = json.loads(data)
        method = method.lower()
        if method == "get":
            res = self.one_session.get(url=url, params=data)
        elif method == "post":
            #判断js_json是否有Ture
            if is_json:
                #判断是否传请求头
                if head is None:
                    res = self.one_session.post(url=url, json=data)
                else:
                    res = self.one_session.post(url=url, json=data, headers=head)
            #判断js_json为None
            else:
                if head is None:
                    res = self.one_session.post(url=url, data=data)
                else:
                    res = self.one_session.post(url=url, data=data, headers=head)
        else:
            res = None
        return res

    def close_session(self):
        """
        关闭接口请求会话
        :return:
        """
        self.one_session.close()

    def get_token(self):
        result = self.do_request(
                        url="http://test2.mg.zhongbaojinfu.com.cn/sm-api/user/login",
                        data={"username": "kaungjh", "password": "abc455318938"},
                        is_json=True)
        return json.loads(result.text)["data"]["accessToken"]
# if __name__ == '__main__':
#     re=HandleRequest()
#     # url = "http://test2.mg.zhongbaojinfu.com.cn/sm-api/user/login"
#     # data = {"username": "kaungjh", "password": "abc455318938","validateCode":None}
#     # value=re.do_request(url=url,method ="post", data=data, is_json=True)
#     # token=json.loads(value.text)["data"]["accessToken"]
#     # co="vue_admin_template_token="+token
#     # print(co)
#     # heads = {"access-token": token}
#
#     tokens=re.get_token()
#     print(tokens)
#     print(type(tokens))
#
#
#     # shop_url="http://test2.mg.zhongbaojinfu.com.cn/sm-api/shop/insert"
#     # shop_data = {"id":None,"name":"自动化店铺","desc":"这是一个描述","code":"ZBJF","exhibitionChannel":"1"}
#     # shop_value = re.do_request(
#     #                             url=shop_url,
#     #                             method="post",
#     #                             data=shop_data,
#     #                             is_json=True,
#     #                             head=heads
#     # )
#     # print(shop_value.text)