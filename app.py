from api import API

app = API()


@app.route("/home")
def home(request, response):
    response.text = "hello, ding."
    
@app.route("/people/{name}")
def people(req, resp, name):
	resp.text = "hello, {}".format(name) 
