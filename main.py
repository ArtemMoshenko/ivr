from flask import Flask
from flask import render_template
import json
from flask import url_for
from flask import request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == "POST":
        if 'tren' in request.form:
            return "1"

        if 'create_class' in request.form:
            return render_template("create_class.html")

        if 'come' in request.form:
            return "3"

        if 'play_game' in request.form:
            return "4"

        if 'read_teor' in request.form:
            return "5"

        if 'instruction' in request.form:
            return "6"

        if 'registration' in request.form:
            return render_template("reg.html"
                                   )
        if 'logo' in request.form:
            return render_template("home.html")

        if 'add_picture' in request.form:
            return "add_pic"

        if 'rule' in request.form:
            return "rule"

        if 'delete' in request.form:
            return "delete"

        if 'imp' in request.form:
            return "imp"


    return render_template('home.html')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
