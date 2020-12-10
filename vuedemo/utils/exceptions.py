# _*_ coding:utf-8 _*_

__author__ = "super.gyk"

from rest_framework.views import exception_handler as drf_exception_handler
import logging
from rest_framework.response import Response
from rest_framework import status
from django.db import DatabaseError

# 获取在配置文件中定义的logger，用来记录日志
logger = logging.getLogger('django')


def exception_handler(exc, context):

    response = drf_exception_handler(exc, context)
    if response is None:
        view = context['view']
        if isinstance(exc, DatabaseError):
            # 数据库异常
            logger.error('[%s] %s' % (view, exc))
            response = Response({'message': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return response



