import pytest

from api import API


@pytest.fixture
def api():
    return API()


def test_basic_route(api):
    @api.route("/home")
    def home(req, resp):
        resp.text = "ding"

    with pytest.raises(AssertionError):
        @api.route("/home")
        def home2(req, resp):
            resp.text = "ding"
