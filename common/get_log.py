# 1-导包
import logging
from logging import handlers
from config import dir_path
import os


# 2-定义一个日志封装类（为了替代原生的logging模块，让它看起来和原本的一样一样的）
class GetLog:

    log = None  # 初始化日志器对象(解决警告问题)
    _initialized = False  # 标志位

    # 3-封装日志获取方法
    @classmethod  # 将定义的方法声明为一个类方法，方便直接通过类名调用，不需要实例化
    def get_log(cls):
        # 如果尚未初始化，则进行初始化
        if not cls._initialized:
            # 3.1-定义1个日志器
            cls.log = logging.getLogger()  # 获取日志器对象
            cls.log.setLevel(logging.INFO)  # 设置日志记录的基本info及以上
            log_path = dir_path + os.sep + "log" + os.sep + "test_log.log"  # 设置日志存储的路径和文件名称，os.sep方法代表的是/或\
            # 3.2-定义1个处理器
            fh = handlers.TimedRotatingFileHandler(
                filename=log_path,  # 日志的存放位置和文件名
                when="midnight",   # 设置按天存储
                interval=1,   # 设置按照每1天存储1份日志文件
                backupCount=3,  # 设置备份的日志文件数量，超出后会覆盖最旧的一份日志
                encoding="utf8"  # 设置日志编码
            )
            # 3.3-定义1个格式器
            fmt = "%(asctime)s %(levelname)s [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s"  # 定义日志显示的格式
            ft = logging.Formatter(fmt=fmt)
            # 3.4-将格式器装载到处理器
            fh.setFormatter(ft)
            # 3.5-再将处理器装载到日志器
            cls.log.addHandler(fh)

            # 设置已初始化标志为True
            cls._initialized = True

        # 4-返回日志器对象
        return cls.log



