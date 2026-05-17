# 1-导包
from api.weather import WeatherApi
from common.get_log import GetLog
import pytest
from config import params
logger = GetLog.get_log()


# 2-定义一个测试类
class TestWeather:
    @pytest.mark.parametrize("param", params)
    def test_case(self, param):
        try:
            # 调用天气请求接口传入参数
            result = WeatherApi.weather_api(param = param)
            print(result)
            logger.info(f"接口响应结果 {result}")
        except Exception as e:
            print(e)
            logger.info(e)

