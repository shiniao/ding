# Ding
ding是基于werkzeug的web框架，由python语言编写，目的是用来学习web框架的实现方法，请不要将其用于生产上。

## 特点


## 如何使用

```python
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

```

## TODO
- [] 配置管理
- [] jwt默认支持
- [] 错误处理
- [] 

## License

[木兰宽松许可证](https://license.coscl.org.cn/MulanPSL/)

```
Copyright (c) [2019] [name of copyright holder]
[Software Name] is licensed under the Mulan PSL v1.
You can use this software according to the terms and conditions of the Mulan PSL v1.
You may obtain a copy of Mulan PSL v1 at:
    http://license.coscl.org.cn/MulanPSL
THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR
PURPOSE.
See the Mulan PSL v1 for more details.
```