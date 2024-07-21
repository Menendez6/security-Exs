#!/usr/bin/env python3
import populate
from flask import Flask
from flask import request, jsonify
import pymysql


app = Flask(__name__)
username = "root"
password = "root"
database = "hw5_ex2"

# This method returns a list of messages in a json format such as
# [
# { "name": <name>, "message": <message> },
# { "name": <name>, "message": <message> },
# ...
# ]
# If this is a POST request and there is a parameter "name" given, then only
# messages of the given name should be returned.
# If the POST parameter is invalid, then the response code must be 500.


@app.route("/messages", methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        with db.cursor() as cursor:
            cursor.execute("SELECT name, message FROM messages")
            messages = cursor.fetchall()

            # Convert the messages into the desired format
            message_list = [{"name": name, "message": message} for name, message in messages]
            
            return jsonify(message_list), 200
    if request.method == "POST":
        name = request.form.get("name")
        with db.cursor() as cursor:
            try:
                cursor.execute("SELECT name, message FROM messages WHERE name = %s",(name))
                messages = cursor.fetchall()

                # Convert the messages into the desired format
                message_list = [{"name": name, "message": message} for name, message in messages]
                
                return jsonify(message_list), 200
            except:
                return "",500


# This method returns the list of users in a json format such as
# { "users": [ <user1>, <user2>, ... ] }
# This methods should limit the number of users if a GET URL parameter is given
# named limit. For example, /users?limit=4 should only return the first four
# users.
# If the paramer given is invalid, then the response code must be 500.
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
