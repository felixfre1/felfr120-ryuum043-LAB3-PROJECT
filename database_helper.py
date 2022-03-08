import time
import sqlite3
from flask import g

DATABASE_URI = "database.db"


def get_db():
    db = getattr(g, "db", None)
    if db is None:
        db = g.db = sqlite3.connect(DATABASE_URI)
    return db


def disconnect_db():
    db = getattr(g, "db", None)
    if db is not None:
        db.close()
        g.db = None


def check_sign_up_info():
    sign_up_list = get_db().execute("SELECT * FROM sign_up")
    for col in sign_up_list:
        print(col)


def check_user_communication_info():
    sign_up_list = get_db().execute("SELECT * FROM user_communication")
    for col in sign_up_list:
        print(col)


def can_sign_in(email, password, new_token):
    try:
        res = {
            "success": False,
            "data": {},
        }
        # check_sign_up_info()
        cur = get_db().execute(
            "SELECT email, user_password, firstname, familyname, gender, city, country  FROM sign_up WHERE email = ? AND user_password = ?",
            (email, password),
        )
        data = cur.fetchone()
        if data == None:
            print("there is no db")
            disconnect_db()
            return res
        else:
            get_db().execute(
                "UPDATE sign_up SET token = ? WHERE email = ? AND user_password = ?",
                [new_token, email, password],
            )
            get_db().commit()
            disconnect_db()
            res = {
                "success": True,
                "data": {
                    "email": data[0],
                    "firstname": data[2],
                    "familyname": data[3],
                    "gender": data[4],
                    "city": data[5],
                    "country": data[6],
                },
            }
            return res
    except Exception as e:
        print(e)
        return res


def create_sign_up(
    email, password, firstname, familyname, gender, city, country, new_token
):
    try:
        get_db().execute(
            "insert into sign_up values(?, ?, ?, ?, ?, ?, ?, ?)",
            [email, password, firstname, familyname, gender, city, country, new_token],
        )
        get_db().commit()
        # check_sign_up_info()
        disconnect_db()
        return True
    except Exception as e:
        print(e)
        return False


def remove_token(token):
    try:
        # check_sign_up_info()
        cur = get_db().execute(
            "SELECT token FROM sign_up WHERE token = ?",
            [token],
        )
        data = cur.fetchone()
        if data == None:
            disconnect_db()
            return False
        else:
            cur.execute("UPDATE sign_up SET token = '' WHERE token = ?", [token])
            get_db().commit()
            disconnect_db()
            return True
    except Exception as e:
        print(e)
        return False


def update_password(token, old_password, new_password):
    try:
        # check_sign_up_info()
        cur = get_db().execute(
            "SELECT token FROM sign_up WHERE token = ?",
            [token],
        )
        matched_token = cur.fetchone()
        if matched_token == None:
            disconnect_db()
            return "not_sign_in"
        else:
            cur = get_db().execute(
                "SELECT user_password FROM sign_up WHERE user_password = ? AND token = ?",
                [old_password, token],
            )
            matched_old_password = cur.fetchone()
            if matched_old_password == None:
                disconnect_db()
                return "wrong_password"
            else:
                get_db().execute(
                    "UPDATE sign_up SET user_password = ? WHERE user_password = ? AND token = ?",
                    [new_password, old_password, token],
                )
                get_db().commit()
                disconnect_db()
                return "success"
    except Exception as e:
        print(e)
        return False


def fetch_user_data_by_token(token):
    res = {
        "success": False,
        "data": {},
    }
    try:
        cur = get_db().execute(
            "SELECT email, firstname, familyname, gender, city, country FROM sign_up WHERE token = ?",
            [token],
        )
        data = cur.fetchone()
        if data == None:
            disconnect_db()
            return res
        else:
            disconnect_db()
            res = {
                "success": True,
                "data": {
                    "email": data[0],
                    "firstname": data[1],
                    "familyname": data[2],
                    "gender": data[3],
                    "city": data[4],
                    "country": data[5],
                },
            }
            return res
    except Exception as e:
        print(e)
        return res


def fetch_user_data_by_email(token, email):
    res = {
        "status": "not_sign_in",
        "data": {},
    }
    try:
        # check_sign_up_info()
        cur = get_db().execute(
            "SELECT token FROM sign_up WHERE token= ?",
            [token],
        )
        hasUserWithToken = cur.fetchone()
        if hasUserWithToken == None or len(hasUserWithToken) == 0:
            res["status"] = "not_sign_in"
            return res
        data = cur.fetchone()
        cur.execute(
            "SELECT email, firstname, familyname, gender, city, country FROM sign_up WHERE email= ?",
            [email],
        )
        data = cur.fetchone()
        if data == None:
            disconnect_db()
            res["status"] = "wrong_email"
            return res
        else:
            disconnect_db()
            res = {
                "status": "success",
                "data": {
                    "email": data[0],
                    "firstname": data[1],
                    "familyname": data[2],
                    "gender": data[3],
                    "city": data[4],
                    "country": data[5],
                },
            }
            return res
    except Exception as e:
        print(e)
        return res


def fetch_user_messages_by_token(token):
    res = {
        "status": "not_sign_in",
        "data": [],
    }
    list = []
    try:
        # check_sign_up_info()
        # check_user_communication_info()
        cur = get_db().execute(
            "SELECT email FROM sign_up WHERE token= ?",
            [token],
        )
        sender_email = cur.fetchone()
        if sender_email == None:
            disconnect_db()
            res["status"] = "not_sign_in"
            return res
        else:
            cur.execute(
                "SELECT sender_email, post_message,post_timestamp,country, city FROM user_communication WHERE sender_email= ?",
                [sender_email[0]],
            )
            messages_data = cur.fetchall()
            if messages_data == None or len(messages_data) == 0:
                res["status"] = "no_message"
                return res
            else:
                for message_data in messages_data:
                    list.append(
                        {
                            "writer": message_data[0],
                            "content": message_data[1],
                            "timestamp": message_data[2],
                            "country": message_data[3],
                            "city": message_data[4],
                        }
                    )
                sorted_list = sorted(list, key=lambda x: x["timestamp"])
                disconnect_db()
                res = {
                    "status": "success",
                    "data": sorted_list,
                }
                return res
    except Exception as e:
        print(e)
        return res


def fetch_user_messages_by_email(token, email):
    res = {
        "status": "not_sign_in",
        "data": [],
    }
    list = []
    try:
        # check_sign_up_info()
        # check_user_communication_info()
        cur = get_db().execute(
            "SELECT token FROM sign_up WHERE token= ?",
            [token],
        )
        token = cur.fetchone()
        if token == None:
            disconnect_db()
            res["status"] = "not_sign_in"
            return res
        else:
            cur.execute(
                "SELECT sender_email, post_message,post_timestamp, country, city FROM user_communication WHERE receiver_email = ?",
                [email],
            )
            messages_data = cur.fetchall()
            if messages_data == None or len(messages_data) == 0:
                res["status"] = "no_message_or_no_user"
                return res
            else:
                for message_data in messages_data:
                    list.append(
                        {
                            "writer": message_data[0],
                            "content": message_data[1],
                            "timestamp": message_data[2],
                            "country": message_data[3],
                            "city": message_data[4],
                        }
                    )
                sorted_list = sorted(list, key=lambda x: x["timestamp"])
                disconnect_db()
                res = {
                    "status": "success",
                    "data": sorted_list,
                }
                return res
    except Exception as e:
        print(e)
        return False


def post_message(token, message, receiver_email, country, city):
    try:
        check_sign_up_info()
        # check_user_communication_info()
        cur = get_db().execute(
            "SELECT email FROM sign_up WHERE token = ?",
            [token],
        )
        data = cur.fetchone()
        if data == None:
            disconnect_db()
            return "not_sign_in"
        else:
            sender_email = data[0]
            timestamp = str(int(time.time()))
            cur.execute(
                "INSERT INTO user_communication(sender_email, receiver_email, post_message, post_timestamp, country, city) values(?,?,?,?,?,?)",
                [sender_email, receiver_email, message, timestamp, country, city],
            )
            get_db().commit()
            disconnect_db()
            return "success"
    except Exception as e:
        print(e)
        return "no_receiver"


def is_match_token(token):
    try:
        check_sign_up_info()
        # check_user_communication_info()
        cur = get_db().execute(
            "SELECT token FROM sign_up WHERE token = ?",
            [token],
        )
        data = cur.fetchone()
        if data == None:
            disconnect_db()
            return "must_sign_out"
        else:
            disconnect_db()
            return "can_stay"
    except Exception as e:
        print(e)
        return False

        # get_db().execute(
        #     "CREATE TABLE sign_up (email STRING NOT NULL UNIQUE, user_password STRING NOT NULL, firstname STRING  NOT NULL, familyname STRING NOT NULL, gender STRING NOT NULL, city STRING NOT NULL, country STRING NOT NULL, token STRING NOT NULL,primary key(email))"
        # )
        # get_db().commit()
        # get_db().execute(
        #     "CREATE TABLE user_communication (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, sender_email STRING NOT NULL, receiver_email STRING NOT NULL, post_message STRING NOT NULL, post_timestamp STRING NOT NULL, country STRING NOT NULL, city STRING NOT NULL)"
        # )
        # get_db().commit()
