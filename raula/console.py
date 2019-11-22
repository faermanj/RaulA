from .module import Module


class Console(Module):
    dependencies = ["flask"]

    def stand(self):
        from flask import Flask, escape, request
        #app = Flask(__name__)
        self.info("Console module starting")

    #@app.route('/')
    #def hello(self):
    #    name = request.args.get("name", "World")
    #    return f'Hello, {escape(name)}!'
