# 1-导包
from pygments.lexers import dsls

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
        except Exception as e:
            print(e)
            logger.info(e)

