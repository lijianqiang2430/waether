# 1-导包
import json
from config import dir_path
import os


# 2-定义一个读取json文件的方法
def read_json(filename, keyword):
    """
    :param filename: 代表的是参数化json文件的名称
    :param keyword: 代表json文件中最外层字典的关键字名称（表示1个接口数据源）
    :return: 列表套字典的数据源
    """
    # 定义json文件的完整路径,os.sep方法代表的是/或\，动态适配不同操作系统
    json_path = dir_path + os.sep + "data" + os.sep + filename
    # 2.1-读json文件，获取文件对象
    with open(json_path, "r", encoding="utf-8") as f:  # 读取json文件，以只读的方式，返回文件对象
        # 2.2-将读取的json文件对象转为字典格式的数据
        json_data = json.load(f)
        print("读取的JSON文件数据为：{}".format(json_data))
        # 2.3-通过关键字获取对应接口的参数化数据
        list_data = json_data[keyword]
        # 3-返回列表套字典的数据源
        return list_data


if __name__ == '__main__':
    list_data = read_json("registe.json", "img_code")
    print("测试获取的接口数据源：{}".format(list_data))
