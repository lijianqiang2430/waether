# 导包
import os


# 1-定义服务器测试地址
url = "https://restapi.amap.com/v3/weather/weatherInfo?parameters"

params = [{"key": "6e002452dc2ebb227d59e2c960b79883","city":440100,},{"key": "6e002452dc2ebb227d59e2c960b79883","city":440111,}]

# 2-项目根目录(os.path.dirname作用是获取当前项目根目录)
dir_path = os.path.dirname(__file__)
print("项目根目录：{}".format(dir_path))  # .format的作用是将字符串的占位符{}替换为对应的值


