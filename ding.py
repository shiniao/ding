from werkzeug.routing import Rule, Map
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple


class Ding(object):

    def __init__(self):
        self.url_map = Map()
        self.view_func = {}
        self.error_handler = {}
        self.config = Config()

    def __call__(self):
        self.wsgi_app()

    def run(self, host='localhost', port=6666, **options):
        run_simple(host, port, self, **options)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def handle_request(self, request):
        """分发路由到视图函数"""
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return self.view_func[endpoint](**values)
        except HTTPException, e:
            # 接管错误
            handler = self.error_handler(e.code)
            if error_handler is None:
                return e
            handler(e)

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


class Config(object):
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


class Error(object):
    """
    getattr(self, code)
    """

    def __init__(self, code):
        self.code = code
    
    def __get__()

    def not_found(self):
        pass
