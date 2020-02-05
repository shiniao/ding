from werkzeug.routing import Rule, Map
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from werkzeug.local import LocalStack, LocalProxy


_request_context = LocalStack()
request = LocalProxy(lambda: _request_context.top.request)
c = LocalProxy(lambda: _request_context.top.c)


class RequestGlobals(object):
    pass


class RequestContext(object):
    def __init__(self, app, environ):
        self.app = app
        self.url_adapter = app.url_map.bind_to_environ(environ)
        self.request = app.request_class(environ)
        self.c = RequestGlobals()

    def __enter__(self):
        _request_context.push(self)

    def _exit__(self):
        if not self.app.debug:
            _request_context.pop()


class Ding(object):

    def __init__(self):
        self.url_map = Map() # 路由map
        self.view_func = {} # 视图函数
        self.error_handler = {} # 错误handler
        self.config = Config # 配置
        self.response = Response # 响应

    def __call__(self):
        self.wsgi_app()

    def run(self, host='localhost', port=6666, **options):
        run_simple(host, port, self, **options)

    def wsgi_app(self, environ, start_response):
        with RequestContext(environ):
            rv = self.handle_request()
            response = self.make_response(rv)
            return response(environ, start_response)

    def handle_request(self):
        """分发路由到视图函数"""
        try:
            endpoint, values = _request_context.top.url_adapter.match()
            request.endpoint = endpoint
            request.values = values
            # 返回对应的视图函数
            return self.view_func[endpoint](**values)
        except HTTPException, e:
            # 接管错误
            handler = self.error_handler(e.code)
            if error_handler is None:
                return e
            handler(e)
        except Exception, e:
            # TODO 500
            pass

    def make_response(self, rv):
        """"响应
        如果是 Response类型，直接返回
        """
        if isinstance(rv, self.response):
            return rv
        if isinstance(rv, basestring):
            return self.response(rv)
        if isinstance(rv, tuple):
            return self.response(*rv)
        return self.response.force_type(rv, request.environ)

    def error(self, code):
        def wrapper(func):
            self.error_handler[code] = func
            return func
        return wrapper

    def add_route(self, rule, handler, method, **options):
        """添加路由规则"""
        options['endpoint'] = handler
        options['methods'] = (method, )
        self.url_map.add(Rule(rule, **options))

    # The http function #
    def get(self, rule):
        """GET 方法"""

        def wrapper(func):
            self.add_route(rule, func.__name__, 'GET')
            self.view_func[func.__name__] = func
            return func

        return wrapper

    def post(self, rule):
        """POST 方法"""

        def wrapper(func):
            self.add_route(rule, func.__name__, 'POST')
            self.view_func[func.__name__] = func
            return func

        return wrapper

    def put(self, rule):
        """PUT 方法"""

        def wrapper(func):
            self.add_route(rule, func.__name__, 'PUT')
            self.view_func[func.__name__] = func
            return func

        return wrapper

    def delete(self, rule):
        """DELETE 方法"""

        def wrapper(func):
            self.add_route(rule, func.__name__, 'DELETE')
            self.view_func[func.__name__] = func
            return func

        return wrapper

    # The response #
    def html(self, status=200, message):
        return self.response(response=message, status=status, mimetype='text/html')

    def json(self, status=200, message):
        return self.response(response=message, status=status, mimetype='text/html')

    def data(sel, status=200, message):
        return self.response(response=message, status=status, mimetype='text/html')


class Config(object):
    """
    配置管理，Config类表现的像字典
    在Ding类中，self.config = Config()
    可以这样使用：
    app = Ding()
    app.config["DEBUG"] = True

    """

    def __init__(self):
        self.__config__ = {}

    def __getitem__(self, key):
        return self.__config__[key]

    def __setitem__(self, key, value):
        self.__config__[key] = value


class ConfigAttribute(object):
    def __init__(self, name):
        self.name = name

    def __get__(self, obj):
        if obj is None:
            return self
        return obj.config[self.name]

    def __set__(self, obj, value):
        obj.config[self.name] = value


class Error(object):
    """
    app.err.not_found()
    """

    def __init__(self):
        self.code = code

    def __get__()

    def not_found(self):
        pass
