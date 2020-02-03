"""
-----------------------    web框架实现    ---------------------------
教程参考：https://rahmonov.me/posts/write-python-framework-part-one/
"""

import inspect

from parse import parse
from webob import Request, Response


class API(object):

    def __init__(self):
        # 存放所有路由
        self.routes = {}

    # WSGI要求实现的__call__
    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)

        # 将响应状态和header交给WSGI服务器比如gunicorn
        # 同时返回响应正文
        return response(environ, start_response)

    # 找到路由对应的处理对象和参数
    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named
        return None, None

    # 匹配请求路由，分发到不同处理函数
    def handle_request(self, request):

        response = Response()
        handler, kwargs = self.find_handler(request.path)

        if handler is not None:
            # 如果handler是类的话
            if inspect.isclass(handler):
                # 获取类中定义的方法比如get/post
                handler = getattr(handler(), request.method.low(), None)
                # 如果不支持
                if handler is None:
                    raise AttributeError("method not allowed.", request.method)

            handler(request, response, **kwargs)
        else:
            self.default_response(response)
        return response

    def route(self, path):
        if path in self.routes:
            raise AssertionError("route already exists.")

        # bind the route path and handler function
        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper

    # 默认响应
    def default_response(self, response):
        response.status_code = 404
        response.text = "not found."
