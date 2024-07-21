#!/usr/bin/env python3
import sys
import populate
from flask import Flask
from flask import request, jsonify
import pymysql


app = Flask(__name__)
username = "root"
password = "root"
database = "hw5_ex2"


@app.route("/messages", methods=["GET", "POST"])
def messages():
    # Try Except enables the server to send back an
    # error code when parameters are not valid
    try:
        with db.cursor() as cursor:
            sql = "SELECT name,message FROM messages "
            # display all messages
            if request.method == "POST":
                # get the search parameter
                name = request.form["name"]
                sql += "WHERE name LIKE %s "
                cursor.execute(sql, (name))
            else:
                cursor.execute(sql)
            json = [{"name": u, "message": m} for u, m in cursor.fetchall()]
            return jsonify(json), 200
    except Exception as error:
        print(error, file=sys.stderr)
        return "", 500


@app.route("/users", methods=["GET"])
def contact():
    try:
        with db.cursor() as cursor:
            sql = "SELECT name FROM users "
            limit = request.args.get('limit')
            if limit is not None:
                sql += "LIMIT 0, %s "
                print('SQL : %s' % sql, file=sys.stderr)
                cursor.execute(sql, (int(limit)))
            else:
                cursor.execute(sql)

            json = {"users": [row[0] for row in cursor.fetchall()]}
            print(json)
            return jsonify(json), 200
    except Exception as error:
        print(error, file=sys.stderr)
        return "", 500


if __name__ == "__main__":
    db = pymysql.connect(host="localhost",
                         user=username,
                         password=password,
                         database=database,
                         charset="utf8mb4")
    with db.cursor() as cursor:
        populate.populate_db(cursor)
        db.commit()
    print("[+] database populated")

    app.run(host='0.0.0.0', port=80)
