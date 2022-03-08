# 早期リターンを作成する必要がある
from threading import Lock
from flask import (
    Flask,
    render_template,
    session,
    request,
    copy_current_request_context,
    jsonify,
)
from flask_socketio import (
    SocketIO,
    emit,
    join_room,
    leave_room,
    rooms,
    disconnect,
)
import database_helper
import random
import math
import http.client, urllib.parse
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
async_mode = "threading"
app.debug = True
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


@app.route("/")
def index():
    return render_template("/static/client.html", async_mode=socketio.async_mode)


def create_token():
    letters = "abcdefghiklmnopqrstuvwwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    token = ""
    for i in range(36):
        token = token + letters[math.floor(random.random() * len(letters))]
    return token


def searchLocation(lat, lng):
    conn = http.client.HTTPConnection("geocode.xyz")
    params = urllib.parse.urlencode(
        {
            "locate": lat + "," + lng,
            "json": 1,
        },
    )
    conn.request("GET", "/?{}".format(params))
    res = conn.getresponse()
    data = json.loads(res.read())
    print(data)
    location = {"country": data["country"], "city": data["city"]}
    return location


@app.route("/sign-in", methods=["POST", "GET"])
def sign_in():
    #  we may use these below codes later
    if request.method == "POST":
        json = request.get_json()
        if len(json["email"]) != 0 and len(json["password"]) != 0:
            new_token = create_token()
            res = database_helper.can_sign_in(
                json["email"], json["password"], new_token
            )
            if res["success"]:
                return jsonify(
                    {
                        "success": True,
                        "message": "Successfully signed in.",
                        "data": {"new_token": new_token, "user_info": res["data"]},
                    }
                )
            else:
                return jsonify(
                    {
                        "success": False,
                        "message": "Wrong username or password.",
                    }
                )
    else:
        return jsonify(
            {
                "success": False,
                "message": "Wrong username or password.",
            }
        )


@app.route("/sign-up", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        json = request.get_json()
        if (
            len(json["email"]) != 0
            and len(json["password"]) >= 6
            and len(json["firstname"]) != 0
            and len(json["familyname"]) != 0
            and len(json["gender"]) != 0
            and len(json["city"]) != 0
            and len(json["country"]) != 0
        ):
            new_token = create_token()
            res = database_helper.create_sign_up(
                json["email"],
                json["password"],
                json["firstname"],
                json["familyname"],
                json["gender"],
                json["city"],
                json["country"],
                new_token,
            )
            if res:
                return jsonify(
                    {
                        "success": True,
                        "message": "Successfully created a new user.",
                        "data": new_token,
                    }
                )
            else:
                return jsonify(
                    {
                        "success": False,
                        "message": "User already exists.",
                    }
                )
        else:
            return jsonify(
                {"success": False, "message": "Form data missing or incorrect type."}
            )
    else:
        return jsonify(
            {"success": False, "message": "Form data missing or incorrect type."}
        )


@app.route("/sign-out", methods=["POST", "GET"])
def sign_out():
    if request.method == "POST":
        token = request.headers.get("token")
        if len(token) > 0:
            res = database_helper.remove_token(token)
            if res:
                return jsonify({"success": True, "message": "Successfully signed out."})
            else:
                return jsonify({"success": False, "message": "You are not signed in."})
        else:
            return jsonify({"success": False, "message": "You are not signed in."})


@app.route("/change-password", methods=["PUT", "GET"])
def change_password():
    if request.method == "PUT":
        token = request.headers.get("token")
        json = request.get_json()
        if (
            len(token) > 0
            and len(json["old_password"]) >= 6
            and len(json["new_password"]) >= 6
        ):
            res = database_helper.update_password(
                token, json["old_password"], json["new_password"]
            )
            if res == "success":
                return jsonify({"success": True, "message": "Password changed."})
            elif res == "wrong_password":
                return jsonify({"success": False, "message": "Wrong password."})
            elif res == "not_sign_in":
                return jsonify({"success": False, "message": "You are not sign in."})
        else:
            return jsonify(
                {
                    "success": False,
                    "message": "You are not sign in or the passwords are the lack of length",
                }
            )


@app.route("/get-user-data-by-token", methods=["GET"])
def get_user_data_by_token():
    if request.method == "GET":
        token = request.headers.get("token")
        if len(token) == 0:
            return jsonify(
                {
                    "success": False,
                    "message": "You are not signed in.",
                }
            )
        res = database_helper.fetch_user_data_by_token(token)
        if res["success"]:
            return jsonify(
                {
                    "success": True,
                    "message": "User data retrieved.",
                    "data": res["data"],
                }
            )
        else:
            return jsonify(
                {
                    "success": False,
                    "message": "You are not signed in.",
                }
            )


@app.route("/get-user-data-by-email/<email>", methods=["GET"])
def get_user_data_by_email(email):
    if request.method == "GET":
        token = request.headers.get("token")
        if len(token) == 0 or len(email) == 0:
            return jsonify(
                {
                    "success": False,
                    "message": "You are not signed in.",
                }
            )
        res = database_helper.fetch_user_data_by_email(token, email)
        if res["status"] == "success":
            return jsonify(
                {
                    "success": True,
                    "message": "User data retrieved.",
                    "data": res["data"],
                }
            )
        elif res["status"] == "wrong_email":
            return jsonify(
                {
                    "success": False,
                    "message": "No such user.",
                }
            )
        elif res["status"] == "not_sign_in":
            return jsonify(
                {
                    "success": False,
                    "message": "You are not signed in.",
                }
            )
            # else 追加


@app.route("/get-user-messages-by-token", methods=["GET"])
def get_user_messages_by_token():
    if request.method == "GET":
        token = request.headers.get("token")
        if len(token) == 0:
            return jsonify(
                {
                    "success": False,
                    "message": "You are not signed in.",
                }
            )
        res = database_helper.fetch_user_messages_by_token(token)
        if res["status"] == "success":
            return jsonify(
                {
                    "success": True,
                    "message": "User messages retrieved.",
                    "data": res["data"],
                }
            )
        elif res["status"] == "no_message":
            return jsonify(
                {
                    "success": False,
                    "message": "No message yet.",
                }
            )
        elif res["status"] == "not_sign_in":
            return jsonify(
                {
                    "success": False,
                    "message": "You are not signed in.",
                }
            )


@app.route("/get-user-messages-by-email/<email>", methods=["GET"])
def get_user_messages_by_email(email):
    try:
        if request.method == "GET":
            token = request.headers.get("token")
            if len(token) == 0 or len(email) == 0:
                return jsonify(
                    {
                        "success": False,
                        "message": "You are not signed in.",
                    }
                )
            res = database_helper.fetch_user_messages_by_email(token, email)
            if res["status"] == "success":
                return jsonify(
                    {
                        "success": True,
                        "message": "User messages retrieved.",
                        "data": res["data"],
                    }
                )
            elif res["status"] == "no_message_or_no_user":
                return jsonify(
                    {
                        "success": False,
                        "message": "No message yet or no such user.",
                    }
                )
            elif res["status"] == "not_sign_in":
                return jsonify(
                    {
                        "success": False,
                        "message": "You are not signed in.",
                    }
                )
    except Exception as e:
        print(e)
        return "no_receiver"


@app.route("/post-message", methods=["POST", "GET"])
def post_message():
    if request.method == "POST":
        json = request.get_json()
        token = request.headers.get("token")
        if len(token) != 0 and "message" in json and "email" in json:
            location = searchLocation(json["lat"], json["lng"])
            res = database_helper.post_message(
                token,
                json["message"],
                json["email"],
                location["country"],
                location["city"],
            )

            if res == "success":
                return jsonify({"success": True, "message": "Message posted"})
            elif res == "no_receiver":
                return jsonify({"success": False, "message": "No such user."})
            elif res == "not_sign_in":
                return jsonify({"success": False, "message": "You are not signed in."})
        else:
            return jsonify({"success": False, "message": "You are not signed in."})


@app.route("/leave-only-latest-user", methods=["GET"])
def leave_only_latest_user():
    if request.method == "GET":
        # ANNOTATION:this token has slightly different meaning from the other token variables.
        token = request.headers.get("token")
        if len(token) != 0:
            res = database_helper.is_match_token(
                token,
            )
            if res == "must_sign_out":
                return jsonify({"success": True, "message": "You must sign out"})
            elif res == "can_stay":
                return jsonify({"success": False, "message": "You can stay."})
            elif res == False:
                return jsonify({"success": False, "message": "Something wrong."})
        else:
            return jsonify({"success": False, "message": "Something wrong."})


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit("my_response", {"data": "Server generated event", "count": count})


@socketio.event
def my_event(message):
    session["receive_count"] = session.get("receive_count", 0) + 1
    emit("my_response", {"data": message["data"], "count": session["receive_count"]})


@socketio.event
def join(message):
    try:
        join_room(message["room"])
        session["receive_count"] = session.get("receive_count", 0) + 1
        emit(
            "my_response",
            {
                "data": "In rooms: " + ", ".join(rooms()),
                "count": session["receive_count"],
            },
        )
    except Exception as e:
        print(e)
        return False


@socketio.event
def leave(message):
    leave_room(message["room"])
    session["receive_count"] = session.get("receive_count", 0) + 1
    emit(
        "my_response",
        {"data": "In rooms: " + ", ".join(rooms()), "count": session["receive_count"]},
    )


@socketio.event
def my_room_event(message):
    session["receive_count"] = session.get("receive_count", 0) + 1
    emit(
        "my_response",
        {"data": message["data"], "count": session["receive_count"]},
        to=message["room"],
        #   To test, just comment out including_self
        # include_self=False,
    )


@socketio.event
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session["receive_count"] = session.get("receive_count", 0) + 1
    emit(
        "my_response",
        {"data": "Disconnected!", "count": session["receive_count"]},
        callback=can_disconnect,
    )


@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit("my_response", {"data": "Connected", "count": 0})


if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=5500)
