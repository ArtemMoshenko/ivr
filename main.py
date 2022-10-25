from flask import Flask
from flask import session
from flask import render_template
# import json
from flask import url_for
from flask import request
from flask import redirect
from sqlalchemy import create_engine
import random

application = Flask(__name__)
application.config['TEMPLATES_AUTO_RELOAD'] = False
username = "sql8528062"
passwd = "cwGDW7gFAv"
db_name = "sql8528062"

global flag_reg
flag_reg = False

engine = create_engine(
    "mysql://" + username + ":" + passwd + "@sql8.freemysqlhosting.net:3306/" + db_name + "?charset=utf8", pool_size=10,
    max_overflow=20, echo=True)


@application.route('/', methods=['GET', 'POST'])
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
            return redirect('/reg')

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


@application.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == "POST":  # Если были переданы данные из формы методом POST
        # if 'enter_button' in request.form:
        #    return "hello"
        if 'enter_button' in request.form:  # Если была нажата кнопка delete_button
            if len(request.form["exampleInputPassword1"]) > 0 and len(request.form["exampleInputEmail1"]) > 0:
                if check_reg(request.form["exampleInputEmail1"], request.form["exampleInputPassword1"]):
                    if check_pass(request.form["exampleInputEmail1"], request.form["exampleInputPassword1"]):
                        user_id = get_id(request.form["exampleInputEmail1"])
                        # session["user_id"] = user_id
                        global flag_reg, name
                        flag_reg = True
                        name = request.form["exampleInputPassword1"]
                        return redirect('/user/' + str(user_id))
                    else:
                        return "Неправильный пароль"
                else:
                    return "Пользователь с таким email не зарегистрирован"
        elif 'reg_button' in request.form:

            if len(request.form["exampleInputPassword1"]) > 0 and len(request.form["exampleInputEmail1"]) > 0:
                if check_reg(request.form["exampleInputEmail1"], request.form["exampleInputPassword1"]):
                    return "Email занят"
                else:
                    add_user(request.form["exampleInputEmail1"], request.form["exampleInputPassword1"])
                    user_id = get_id(request.form["exampleInputEmail1"])
                    # session["user_id"] = user_id

                    return redirect('/user/' + str(user_id))

    return render_template('reg.html', flag_reg=flag_reg, name="")


@application.route('/user/<int:user_id>', methods=['GET', 'POST'])
def main_reg(user_id):
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
            return redirect('/reg')

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


def check_pass(email, passw):
    connection = engine.connect()  # Подключаемся к базе
    user_table = connection.execute("select password from user where email=%s",
                                    email)  # Выполняем запрос и получаем таблицу с результатов
    connection.close()  # Закрываем подключение к базе

    user = [dict(row) for row in user_table]

    if user[0]['password'] == passw:
        return True
    else:
        return False


def check_reg(email, passw):
    connection = engine.connect()
    user_table = connection.execute("select email from user where email=%s",
                                    email)  # Выполняем запрос и получаем таблицу с результатов
    user = [dict(row) for row in user_table]

    connection.close()
    if len(user) == 0:
        return False
    else:
        return True


def get_id(email):
    connection = engine.connect()  # Подключаемся к базе
    user_table = connection.execute("select id from user where email=%s",
                                    email)  # Выполняем запрос и получаем таблицу с результатов
    connection.close()  # Закрываем подключение к базе
    user = [dict(row) for row in user_table]
    return user[0]['id']


def add_user(email, passw):
    connection = engine.connect()
    trans = connection.begin()
    connection.execute("INSERT INTO user(email, password)  VALUES ( %s, %s)", (email, passw))
    trans.commit()
    connection.close()


if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
