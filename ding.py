

class Ding(object):

    def __init__(self):
        self.url_map = {}
        self.view_functions = {}

    def __call__(self):
        self.wsgi_app()
    
    def wsgi_app(self, environ, start_response):
        pass

    def route(self):
        pass

    def add_route(self):
        pass

    def get(self):
        pass
    def post(self):
        pass
