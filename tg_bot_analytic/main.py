import sqlite3
import logging
import datetime

from flask import render_template, request, make_response, Flask

from db import data, db, cur

app = Flask(__name__)


@app.route("/stat", methods=['GET', 'POST'])
def hello_post():
    if request.method == "POST" and not request.form.get('start_date') is None and not request.form.get(
            'end_date') is None:
        content = data(request.form.get('start_date'), request.form.get('end_date'))
        return render_template('home.html', date=content[3], start_bot=content[0], operator_order=content[1],
                               operator_order_complete=content[2], unique=content[4])
    else:
        content = data(str(datetime.date.today() - datetime.timedelta(days=7)), str(datetime.date.today()))
        return render_template('home.html', date=content[3], start_bot=content[0], operator_order=content[1],
                               operator_order_complete=content[2], unique=content[4], test=content[5])


@app.post("/start")
def helloo_post():
    cur.execute("INSERT INTO statistic(start_bot, date, user_id) VALUES(?, ?, ?)",
                (1, datetime.date.today(), request.get_json()["user_id"]))
    db.commit()
    return make_response("Success", 200)


@app.post("/phone")
def phone():
    cur.execute("INSERT INTO statistic(operator_order, date, user_id) VALUES(?, ?, ?)",
                (1, datetime.date.today(), request.get_json()["user_id"]))
    db.commit()
    return make_response("Success", 200)


@app.post("/order")
def order():
    cur.execute("INSERT INTO statistic(operator_order_complete, date , user_id) VALUES(?, ?, ?)",
                (1, datetime.date.today(), request.get_json()["user_id"]))
    db.commit()
    return make_response("Success", 200)


if __name__ == "__main__":
    app.run()
