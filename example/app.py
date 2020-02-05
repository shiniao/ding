from ding import Ding

app = Ding()

app.config["DEBUG"] = True


@app.get("/")
def hello():
    return app.data("hello, ding. :)")


@app.get("/movies")
def movies(name):
    return app.json({
        'movies': [
            'name': '天注定',
            'director': '贾樟柯',
        ]
    })


if __name__ == "__main__":
    app.run()
