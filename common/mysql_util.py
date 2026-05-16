# ==============================================
# 导包区：导入项目需要的所有依赖库，并标注用途
# ==============================================
import pymysql  # Python操作MySQL数据库的核心库
from pymysql.constants import CLIENT  # 用于开启多SQL语句执行权限
from get_log import GetLog  # 项目自定义的日志工具
import traceback  # 用于捕获并打印完整的异常堆栈信息，方便排查bug
from typing import Optional, Union  # 用于类型注解，提升代码可读性和规范性
log = GetLog.get_log()
# ==============================================
# 数据库配置区：集中管理所有连接参数，修改只需改这里
# 【优化点】硬编码配置抽离，方便维护、切换环境
# ==============================================
DB_CONFIG = {
    "host": "121.43.169.97",        # 数据库服务器IP地址
    "port": 3306,                   # 数据库端口号（MySQL默认3306）
    "user": "student",              # 数据库登录用户名
    "password": "P2P_student_2022", # 数据库登录密码
    "database": "czbk_member",      # 要连接的数据库名称
    "charset": "utf8mb4",           # 字符集：utf8mb4支持emoji表情，比utf8更通用
    "autocommit": True,              # 自动提交事务（增删改无需手动commit）
    "client_flag": CLIENT.MULTI_STATEMENTS  # 开启权限：支持同时执行多条SQL语句
}

# ==============================================
# 核心函数：封装SQL执行方法
# 功能：支持查询/增删改/多SQL执行，安全、稳定、易维护
# ==============================================
def execute_sql(sql: str, params: Optional[Union[tuple, list, dict]] = None):
    """
    通用MySQL SQL执行函数
    :param sql: 必传参数，待执行的SQL语句字符串
    :param params: 可选参数，SQL参数（元组/列表/字典），用于参数化查询，【防SQL注入】
    :return: 查询语句返回结果集，增删改语句返回受影响的行数
    """
    # 初始化数据库连接和游标对象，赋值为None，避免未定义报错
    conn = None
    cur = None
    # 初始化结果变量，存储SQL执行的返回值
    result = None

    try:
        # --------------------------
        # 1. 创建数据库连接
        # 【优化点】with上下文管理器：自动创建/关闭连接，无需手动close()，避免资源泄漏
        # **DB_CONFIG：解包字典，直接传入所有连接参数
        # --------------------------
        with pymysql.connect(**DB_CONFIG) as conn:
            # --------------------------
            # 2. 创建数据库游标（用于执行SQL的工具）
            # 【优化点】with自动关闭游标，安全可靠
            # --------------------------
            with conn.cursor() as cur:
                # 日志记录：打印要执行的SQL，方便调试
                log.info(f"执行SQL语句：{sql}")
                # 如果有参数，也打印参数，方便排查问题
                if params:
                    log.info(f"SQL参数：{params}")

                # --------------------------
                # 3. 执行SQL语句
                # 【优化点】参数化执行cur.execute(sql, params)，彻底杜绝SQL注入风险
                # 禁止直接拼接SQL字符串执行！
                # --------------------------
                cur.execute(sql, params)

                # --------------------------
                # 4. 处理SQL执行结果
                # strip()：去除SQL首尾空格；lower()：转为小写，避免大小写判断问题
                # --------------------------
                sql_lower = sql.strip().lower()
                # 判断：如果是查询类语句（select查询、show查看、desc描述表）
                if sql_lower.startswith(("select", "show", "desc")):
                    # 获取查询的所有结果
                    result = cur.fetchall()
                    # 日志记录查询结果
                    log.info(f"SQL查询结果：{result}")
                # 判断：如果是增删改类语句（insert/update/delete）
                else:
                    # 获取受影响的行数（比如新增1条，返回1）
                    result = cur.rowcount
                    # 日志记录受影响行数
                    log.info(f"SQL增删改受影响行数：{result}")

        # 执行完毕，返回结果给调用方
        return result

    # --------------------------
    # 异常捕获：所有执行失败都会进入这里
    # --------------------------
    except Exception as e:
        # 打印完整的异常堆栈信息（最详细的报错信息，定位bug神器）
        log.error(f"执行SQL失败！异常信息：\n{traceback.format_exc()}")
        # 【优化点】安全回滚：只有连接存在且处于打开状态时，才执行回滚，避免空对象报错
        if conn and conn.open:
            # 事务回滚：撤销未提交的增删改操作，保证数据一致性
            conn.rollback()
            log.warning("数据库已执行回滚操作")
        # 抛出异常：让上层代码知道执行失败，可继续捕获处理
        raise

    # --------------------------
    # 【优化点】无需finally手动关闭！
    # with上下文管理器会自动关闭连接和游标，代码更简洁，无资源泄漏风险
    # --------------------------