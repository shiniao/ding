from ding import Ding

app = Ding()

app.config["DEBUG"] = True


@app.get("/")
def home():
    return "hello, ding."
    
@app.get("/movies/<name>")
def movie(name):
	return jsonify()


if __name__ == "__main__":
    app.run()
