from flask import Flask
from flask import session
from flask import render_template
# import json
from flask import url_for
from flask import request
from flask import redirect
from sqlalchemy import create_engine
import sqlalchemy
import random
import os

application = Flask(__name__)
application.secret_key = os.urandom(24)
application.config['TEMPLATES_AUTO_RELOAD'] = False

"""username = "u1729743_artem"
passwd = "84956437929"
db_name = "u1729743_base_1"

engine = create_engine("mysql://" + username + ":" + passwd + "@localhost/" + db_name + "?charset=utf8", pool_size=10,
                       max_overflow=20, echo=True)
"""
"""username = "sql8528062"
passwd = "cwGDW7gFAv"
db_name = "sql8528062
server = "@sql8.freemysqlhosting.net:3306/"
"""

username = "u1729743_artem"
passwd = "84956437929"
db_name = "u1729743_base_1"
server = "@31.31.196.141:3306/"

engine = create_engine(
    "mysql://" + username + ":" + passwd + server + db_name + "?charset=utf8", pool_size=10,
    max_overflow=20, echo=True)


@application.route('/', methods=['GET', 'POST'])  # главная страница
def main(user_id=0):
    session['user_id'] = str(user_id)

    if request.method == "POST":

        if 'stats' in request.form:
            return redirect('/stats/user/' + str(user_id))

        if 'create_class' in request.form:
            return redirect('/create_class/user/' + str(user_id))

        if 'come' in request.form:
            return redirect('/choose_subject/user/' + str(user_id))

        if 'play_game' in request.form:
            session["qu_ind"] = 0
            session['right_kol'] = [0 for x in range(10)]
            session['right'] = 0
            return redirect('/game/user/' + str(user_id))

        if 'read_teor' in request.form:
            return redirect('/subj_theory/user/' + str(user_id))

        if 'instruction' in request.form:
            return render_template("instruction.html")

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


@application.route('/subj_theory/user/<int:user_id>', methods=['GET', 'POST'])  # теория
def choose_subj_theory(user_id=0):
    if request.method == "POST":
        if 'math' in request.form:
            return render_template("math_theory.html")
    return render_template("choose_subject_teor.html", name=user_id)


@application.route('/game/user/<int:user_id>', methods=['GET', 'POST'])  # игра
def game(user_id=0):
    session['quest'] = get_game()
    len_q = len(session["quest"])
    session["len_q"] = len_q
    qu_ind = session["qu_ind"]
    if request.method == "POST":
        if 'next' in request.form:
            session["qu_ind"] = (session["qu_ind"] + 1) % len_q
            session['result'] = ''
            return redirect('/game/user/' + str(user_id))
        if 'return' in request.form:
            session["qu_ind"] = (session["qu_ind"] - 1) % len_q
            session['result'] = ''
            return redirect('/game/user/' + str(user_id))
        if 'end' in request.form:
            return redirect('/user/' + str(user_id))
        if 'enter' in request.form:
            answer = request.form["answer"]
            if len(answer) > 0:
                result = check_answer(answer)
                if result:
                    session['result'] = "Правильно"

                    if session['right_kol'][qu_ind] == 0:
                        session['right'] += 1
                    session['right_kol'][qu_ind] = 1
                else:
                    session['result'] = "Не правильно"
                return redirect('/game/user/' + str(user_id))

    return render_template("game.html", name=user_id, qu_ind=session["qu_ind"])


@application.route('/stats/user/<int:user_id>', methods=['GET', 'POST'])  # статистика пользователя
def stats(user_id=0):
    if session['user_id'] == "0":
        return redirect('/reg')
    stats = get_stats(user_id)
    return render_template("stats.html", name=user_id, stats=stats)


@application.route('/questions/user/<int:user_id>', methods=['GET', 'POST'])  # вопросы
def questions(user_id=0):
    len_q = len(session["quest"])
    session["len_q"] = len_q
    qu_ind = session["qu_ind"]
    if request.method == "POST":
        if 'next' in request.form:
            session["qu_ind"] = (session["qu_ind"] + 1) % len_q
            session['result'] = ''
            return redirect('/questions/user/' + str(user_id))
        if 'return' in request.form:
            session["qu_ind"] = (session["qu_ind"] - 1) % len_q
            session['result'] = ''
            return redirect('/questions/user/' + str(user_id))
        if 'end' in request.form:
            return redirect('/user/' + str(user_id))
        if 'enter' in request.form:
            answer = request.form["answer"]
            if len(answer) > 0:
                result = check_answer(answer)
                if result:
                    session['result'] = "Правильно"

                    if session['right_kol'][qu_ind] == 0:
                        session['right'] += 1
                    session['right_kol'][qu_ind] = 1
                else:
                    session['result'] = "Не правильно"
                return redirect('/questions/user/' + str(user_id))

    return render_template("go_class.html", name=user_id, qu_ind=session["qu_ind"])


@application.route('/choose_class/user/<int:user_id>', methods=['GET', 'POST']) # выбор класса
def choose_class(user_id=0):
    subject = session['subject']
    result = get_class(subject)

    if request.method == "POST":
        for i in range(len(result)):
            if "button " + str(i) in request.form:
                session['cur_class_id'] = result[i][2]
                session['cur_class_name'] = result[i][1]
                session["qu_ind"] = 0
                session['right'] = 0

                session['quest'] = get_quest(session['cur_class_id'])
                session['right_kol'] = [0 for x in range(len(session["quest"]))]
                return redirect('/questions/user/' + str(user_id))

    return render_template("choose_class.html", name=user_id, class_list=result)


@application.route('/choose_subject/user/<int:user_id>', methods=['GET', 'POST']) # выбор предметов
def choose_subject(user_id=0):
    if request.method == "POST":
        if 'математика' in request.form:
            session['subject'] = 'математика'
            return redirect('/choose_class/user/' + str(user_id))
        if 'русский' in request.form:
            session['subject'] = 'русский'
            return redirect('/choose_class/user/' + str(user_id))
        if 'английский' in request.form:
            session['subject'] = 'английский'
            return redirect('/choose_class/user/' + str(user_id))
        if 'информатика' in request.form:
            session['subject'] = 'информатика'
            return redirect('/choose_class/user/' + str(user_id))
        if 'история' in request.form:
            session['subject'] = 'история'
            return redirect('/choose_class/user/' + str(user_id))

    return render_template("open_choose_subject.html", name=user_id)


@application.route('/reg', methods=['GET', 'POST']) # регистрация
def reg():
    if request.method == "POST":  # Если были переданы данные из формы методом POST
        # if 'enter_button' in request.form:
        #    return "hello"
        if 'enter_button' in request.form:  # Если была нажата кнопка delete_button
            if len(request.form["exampleInputPassword1"]) > 0 and len(request.form["exampleInputEmail1"]) > 0:
                if check_reg(request.form["exampleInputEmail1"], request.form["exampleInputPassword1"]):
                    if check_pass(request.form["exampleInputEmail1"], request.form["exampleInputPassword1"]):
                        user_id = get_id(request.form["exampleInputEmail1"])[0]
                        session['username'] = get_id(request.form["exampleInputEmail1"])[1]
                        session["user_id"] = str(user_id)

                        return redirect('/user/' + str(user_id))
                    else:
                        return "Неправильный пароль"
                else:
                    return "Пользователь с таким email не зарегистрирован"
        elif 'reg_button' in request.form:

            if len(request.form["exampleInputPassword1"]) > 0 and len(request.form["exampleInputEmail1"]) > 0 and len(
                    request.form["username"]) > 0:
                if check_reg(request.form["exampleInputEmail1"], request.form["exampleInputPassword1"]):
                    return "Email занят"
                else:
                    add_user(request.form["exampleInputEmail1"], request.form["exampleInputPassword1"],
                             request.form["username"])
                    user_id = get_id(request.form["exampleInputEmail1"])[0]
                    # session["user_id"] = str(user_id)
                    session['username'] = request.form["username"]
                    return redirect('/user/' + str(user_id))

    return render_template('reg.html', name="") # возвращаем html страницу


@application.route('/user/<int:user_id>', methods=['GET', 'POST']) #для зарегестрированного
def main_reg(user_id=0):
    session['user_id'] = str(user_id)

    if request.method == "POST":

        if 'stats' in request.form:
            return redirect('/stats/user/' + str(user_id))

        if 'create_class' in request.form:
            return redirect('/create_class/user/' + str(user_id))

        if 'come' in request.form:
            return redirect('/choose_subject/user/' + str(user_id))

        if 'math' in request.form:
            return render_template("clas.html")

        if 'play_game' in request.form:
            session["qu_ind"] = 0
            session['right_kol'] = [0 for x in range(10)]
            session['right'] = 0
            return redirect('/game/user/' + str(user_id))

        if 'read_teor' in request.form:
            return redirect('/subj_theory/user/' + str(user_id))

        if 'instruction' in request.form:
            return render_template("instruction.html")

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

    return render_template('home.html', name=user_id)


@application.route('/create_class/user/<int:user_id>', methods=['GET', 'POST']) #создаем класс
def create_class_page(user_id=0):
    if session['user_id'] == "0":
        return redirect('/reg')

    if request.method == "POST":

        # redirect('/reg')
        if 'create' in request.form:

            name_class = request.form["name_class"]
            subject = request.form["subject"]
            session['new_subject'] = subject
            session['new_name_class'] = name_class
            if len(name_class) > 0:
                create_class(name_class, subject, user_id)

                return redirect('/add_class/user/' + str(user_id))
    return render_template("create_class.html", name=user_id)


@application.route('/add_class/user/<int:user_id>', methods=['GET', 'POST']) #добавляем класс
def add_class(user_id=0):
    subject = session['new_subject']
    name_class = session['new_name_class']
    if session['user_id'] == "0":
        return redirect('/reg')

    if request.method == "POST":
        if 'next' in request.form:
            question = request.form["question"]
            answer = request.form["answer"]
            if len(question) > 0:
                if len(answer) > 0:
                    add_pair(user_id, question, answer, subject, name_class)
                    return redirect('/add_class/user/' + str(user_id))
        elif 'end' in request.form:
            question = request.form["question"]
            answer = request.form["answer"]
            if len(question) > 0:
                if len(answer) > 0:
                    add_pair(user_id, question, answer, subject, name_class)
                    return redirect('/user/' + str(user_id))
            return redirect('/user/' + str(user_id))

    return render_template("add_class.html", name=user_id, subject=subject, name_class=name_class)


def save_stat(user_id, class_name, subject, result, length): #сохранить статистику
    connection = engine.connect()
    trans = connection.begin()
    connection.execute(
        "INSERT INTO stats(us_id,class_name,subject, result,length)  VALUES (%s, %s, %s, %s, %s)",
        (user_id, class_name, subject, result, length))
    trans.commit()


def get_stats(user_id): #получить теорию
    connection = engine.connect()
    stats = connection.execute("select class_name,subject,result, length from stats where us_id=%s",
                               user_id)
    stats = [dict(row) for row in stats]
    connection.close()
    return stats


def check_answer(answer): #проверяем ответ
    qu_ind = session['qu_ind']
    if session['quest'][qu_ind]['answer'] == answer:
        return True
    return False


def get_game(): #начинаем игру
    connection = engine.connect()
    count = connection.execute("SELECT qu_id FROM questions")
    count = [dict(row) for row in count]
    count = [x['qu_id'] for x in count]
    count = [int(x) for x in count]

    ind = random.sample(count, k=10)

    query = sqlalchemy.text('select qu_id,text,answer from questions where qu_id in :id_list')
    # qu_lst = connection.execute("select qu_id,text,answer from questions where qu_id in :s",
    #                           s=ind)
    qu_lst = connection.execute(query, id_list=tuple(ind))
    connection.close()
    qu_lst = [dict(row) for row in qu_lst]
    random.shuffle(qu_lst)
    return qu_lst


def get_quest(class_id): #задаем вопрос
    class_id = int(class_id)
    connection = engine.connect()
    qu_lst = connection.execute("select qu_id,text,answer from questions where class_id=%s",
                                class_id)
    connection.close()
    qu_lst = [dict(row) for row in qu_lst]
    return qu_lst


def get_class(subject): #работа с классом
    connection = engine.connect()
    class_lst = connection.execute("select id from class where subject=%s",
                                   subject)
    name_lst = connection.execute("select name from class where subject=%s",
                                  subject)
    class_lst = [dict(row) for row in class_lst]
    class_lst = [x["id"] for x in class_lst]
    name_lst = [dict(row) for row in name_lst]
    name_lst = [x["name"] for x in name_lst]
    ind_list = [str(x) for x in range(len(name_lst))]
    connection.close()
    return list(zip(ind_list, name_lst, class_lst))


def add_pair(user_id, question, answer, subject, name_class): #добавляемк классу вопросы
    connection = engine.connect()

    class_id = session['new_class_id']
    trans = connection.begin()
    qu_id = 0
    connection.execute(
        "INSERT INTO questions(user_id,qu_id, text, subject,class_name,class_id,answer)  VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (user_id, qu_id, question, subject, name_class, class_id, answer))
    trans.commit()

    last_inc = connection.execute('SELECT LAST_INSERT_ID()')
    last_inc = [dict(row) for row in last_inc]
    session['new_ans_id'] = last_inc[0]["LAST_INSERT_ID()"]
    last_inc = session['new_ans_id']

    trans = connection.begin()
    connection.execute(f"UPDATE questions SET ans_id = {last_inc} WHERE qu_id = {last_inc}")
    trans.commit()

    # trans = connection.begin()
    # connection.execute("INSERT INTO questions(user_id, ans_id, text, subject,class_name,class_id)  VALUES (%s, %s, %s, %s, %s, %s)", (user_id, last_inc,question,subject,name_class,class_id))
    # trans.commit()

    connection.close()


def create_class(name, subject, us_id): #создаем класс
    connection = engine.connect()
    trans = connection.begin()
    connection.execute("INSERT INTO class(us_id, name, subject)  VALUES ( %s, %s, %s)", (us_id, name, subject))
    trans.commit()
    last_inc = connection.execute('SELECT LAST_INSERT_ID()')
    last_inc = [dict(row) for row in last_inc]
    session['new_class_id'] = last_inc[0]["LAST_INSERT_ID()"]
    # print("YYYYYYY", session['new_class_id'])
    connection.close()


def check_pass(email, passw): #проверяем пароль
    connection = engine.connect()  # Подключаемся к базе
    user_table = connection.execute("select password from user where email=%s",
                                    email)  # Выполняем запрос и получаем таблицу с результатов
    connection.close()  # Закрываем подключение к базе

    user = [dict(row) for row in user_table]

    if user[0]['password'] == passw:
        return True
    else:
        return False


def check_reg(email, passw): #проверяем регистра
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
    user_table = connection.execute("select id,name from user where email=%s",
                                    email)  # Выполняем запрос и получаем таблицу с результатов
    connection.close()  # Закрываем подключение к базе
    user = [dict(row) for row in user_table]
    return [user[0]['id'], user[0]['name']]


def add_user(email, passw, name):
    connection = engine.connect()
    trans = connection.begin()
    connection.execute("INSERT INTO user(email, password,name)  VALUES ( %s, %s, %s)", (email, passw, name))
    trans.commit()
    connection.close()


if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
