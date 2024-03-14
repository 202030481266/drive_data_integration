from werkzeug.exceptions import HTTPException
from flask import render_template
from flask_restful import marshal_with, fields
import json


API_EXCEPTION_FORMAT = dict(
    msg=fields.String(default='发生异常'),
    code=fields.Integer,
    error_code=fields.Integer
)


class ApiException(HTTPException):
    """
    自定义的异常处理类型，继承了flask的HTTPException类。
    使用于内部的api调试。
    """
    msg = 'Sorry, we made a mistake!'
    code = 500
    error_code = 999

    def __init__(self, msg=None, code=None, error_code=None):
        if msg:
            self.msg = msg
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        super(ApiException, self).__init__(msg, None)


class Success(ApiException):
    code = 201
    msg = 'Ok'
    error_code = 0


class DeleteSuccess(ApiException):
    code = 202
    msg = 'delete ok'
    error_code = 1


class UpdateSuccess(ApiException):
    code = 203
    msg = 'update ok'
    error_code = 2


class ServerError(ApiException):
    code = 500
    msg = 'Sorry, server made a mistake'
    error_code = 999


class ParameterException(ApiException):
    code = 400
    msg = 'Invalid parameter'
    error_code = 1000


class NotFound(ApiException):
    code = 404
    msg = 'Resource not found'
    error_code = 1001


class AuthFailed(ApiException):
    code = 401
    msg = 'authorization failed'
    error_code = 1005


class Forbidden(ApiException):
    code = 403
    msg = 'forbidden, not in space'
    error_code = 1004


@marshal_with(API_EXCEPTION_FORMAT)
def handle_api_exception(e):
    """
    处理自定义的ApiException，由于是自己内部调试使用，不需要模板
    :param e: 异常
    :return: 返回异常对象
    """
    return e

def handle_http_exception(e):
    """
    处理HTTP异常函数
    :param e: exception异常
    :return: 返回异常处理数据
    """
    if isinstance(e, ApiException):
        return e
    print(e)
    if e.code == 400:
        return render_template('/HTTPError/400.html')
    return render_template('/HTTPError/404.html')


def handle_all_exception(e):
    """
    处理所有的Exception
    :param e: 异常
    :return: 异常处理数据
    """
    if isinstance(e, HTTPException):
        return e
    print(e)
    return render_template('/HTTPError/500.html')