from flask import Flask
from flask import render_template
import json
from flask import url_for
from flask import request

app = Flask(__name__)


@app.route('/')
def news():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')