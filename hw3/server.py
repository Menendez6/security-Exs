from flask import Flask, request, make_response, jsonify
import hmac
import hashlib
import base64
#import requests

app = Flask(__name__)

cookie_name = "LoginCookie"
sk = "12345"

@app.route("/login",methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    

    if username == 'admin' and password == '42':
        cookie_text = 'admin,1489662453,com402,hw3,ex2,admin'
        hmac_obj = hmac.new(sk.encode(),cookie_text.encode(),hashlib.sha256)
        hmac_hex = hmac_obj.hexdigest()
        final_cookie = cookie_text + "," + hmac_hex
        response = make_response("Login successful admin")
    
    else:
        cookie_text = username +',1489662453,com402,hw3,ex2,user'
        hmac_obj = hmac.new(sk.encode(),cookie_text.encode(),hashlib.sha256)
        hmac_hex = hmac_obj.hexdigest()
        final_cookie = cookie_text + "," + hmac_hex
        response = make_response("Login successful user")

    response.set_cookie(cookie_name, base64.b64encode(final_cookie.encode()).decode('utf-8'))

    return response
    # implement here

@app.route("/auth",methods=['GET'])
def auth():
    if cookie_name in request.cookies:
        cookie_encoded = request.cookies.get(cookie_name)
        try:
            cookie = base64.b64decode(cookie_encoded.encode()).decode("utf-8")
        except:
            return jsonify(message='No cookie or cookie temperered'), 403
        cookie_list = cookie.split(",")
        original_message = ",".join(cookie_list[:-1])
        hmac_received = cookie_list[-1]

        hmac_obj = hmac.new(sk.encode(),original_message.encode(),hashlib.sha256)
        hmac_hex = hmac_obj.hexdigest()

        if hmac_received != hmac_hex:
            return jsonify(message='No cookie or cookie temperered'), 403

        else:
            if cookie_list[-2] == "admin":
                return jsonify(message='Admin'),200
            else:
                return jsonify(message='User'),201
            
    else:
        return jsonify(message='No cookie or cookie temperered'), 403


    # implement here

if __name__ == '__main__':
    app.run()