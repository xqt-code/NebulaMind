import logging
import os
from logging.handlers import TimedRotatingFileHandler

from app.utils.trace_id_util import get_trace_id


class TraceIDFilter(logging.Filter):
    """日志过滤器，自动从 contextvars 中读取 trace_id 注入到日志记录"""

    def filter(self, record: logging.LogRecord) -> bool:
        record.trace_id = get_trace_id() or "-"
        return True


# 日志格式
LOG_FORMAT = "%(asctime)s | %(levelname)-5s | %(trace_id)s | [%(name)s] | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# 确保 logs 目录存在
os.makedirs("logs", exist_ok=True)


def _setup_root_logger():
    """初始化根日志配置"""
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    trace_id_filter = TraceIDFilter()

    # 控制台输出（开发环境使用）
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
    console_handler.addFilter(trace_id_filter)
    root_logger.addHandler(console_handler)

    # 按天滚动文件日志（所有级别）
    file_handler = TimedRotatingFileHandler(
        filename="logs/app.log",
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
    file_handler.addFilter(trace_id_filter)
    root_logger.addHandler(file_handler)

    # ERROR 级别单独文件
    error_handler = TimedRotatingFileHandler(
        filename="logs/error.log",
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8",
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
    error_handler.addFilter(trace_id_filter)
    root_logger.addHandler(error_handler)


# 模块初始化时自动配置日志
_setup_root_logger()


def get_logger(name: str) -> logging.Logger:
    """获取指定名称的 Logger 实例"""
    return logging.getLogger(name)