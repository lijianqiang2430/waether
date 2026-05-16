from common.get_log import GetLog
from config import url
import requests
log = GetLog.get_log()

# 定义搜索函数
class WeatherApi:
    @classmethod
    def weather_api(cls,param):
        try:
            # 2. 准备测试数据 行头体
            req_url = url
            # 3. 发送接口请求
            response = requests.get(url=req_url,params= param)
            result = response.json()
            # 4. 查看响应结果
            print("搜索接口响应结果的=", result)
            log.info(f"接口响应结果= {result}")
            # 直接返回
            return result
        except Exception as e:
            # 接口异常也返回error
            print(f"接口请求失败：{str(e)}")
