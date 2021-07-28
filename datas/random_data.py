from faker import Faker


class RandomData:

    def shop_name_data(self):
        name = Faker(locale="zh_CN").company_prefix()
        return name

# if __name__ == '__main__':
#     a=RandomData().shop_name()
#     print(a)