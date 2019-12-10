# -*- coding:utf-8 -*-

from pyramid.response import Response
from pyramid.httpexceptions import HTTPClientError
from pyramid.view import view_config


@view_config(route_name="api", context=Exception, renderer="json")
class HandleException(object):
    """Handle and exception and return a json object in the jsend message spec format"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    status = "error"
    default_message = "Server Error"

    @property
    def message(self):
        context_message = getattr(self.context, "jsend_message", None)
        if context_message:
            message = context_message
        elif self.code == 404:
            message = "Not found"
        elif self.code == 403:
            message = "Forbidden"
        else:
            message = self.default_message
        return message

    @property
    def code(self):
        if isinstance(self.context, Response):
            return getattr(self.context, "code", None) or 500
        else:
            return 500


    @property
    def data(self):
        return getattr(self.context, "jsend_data", None)

    def __call__(self):
        self.request.response.status_code = self.code
        jsend = {
            "status": self.status,
            "data": self.data,
            "message": self.message,
            "code": self.code,
        }
        return jsend


@view_config(route_name="api", context=HTTPClientError, renderer="json")
class HandleClientError(HandleException):
    """Handle a client error and return a json object in the jsend message spec format"""

    status = "fail"
    default_message = "Client Error"
