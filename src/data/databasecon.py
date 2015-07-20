import psycopg2
import os
import urllib.parse
from data import telegram

__is_connected = False

def connect_to_db():
    global __is_connected
    if "DATABASE_URL" not in os.environ or __is_connected == True:
        print("Environment-variable missing or already connected")
    else:
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
        con = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
            )
        if con != None:
            __is_connected = True
    return con




def disconnect_from_db(db_con, update):
    global __is_connected
    db_con.close()
    __is_connected = False



def search_image(image_name, update):
    db_con = connect_to_db()
    cur = db_con.cursor()
    query = """select link from mm_image where id=%s"""
    cur.execute(query, [image_name])
    result = cur.fetchone()
    if result != None:
        image_link = str(result[0])
        disconnect_from_db(db_con, update)
        return image_link
    else:
        disconnect_from_db(db_con, update)
        return "Not found"



def add_image(image_link, image_name, user_id, update):
    db_con = connect_to_db()
    cur = db_con.cursor()
    query = """select * from mm_user where username=%s"""
    cur.execute(query, [str(update["message"]["from"]["id"])])
    result = cur.fetchone()
    disconnect_from_db(db_con, update)
    if str(update["message"]["from"]["id"]) == str(os.environ["ADMIN_ID"]) or result is not None:
        db_con = connect_to_db()
        cur = db_con.cursor()
        query = """select * from image where image_name=%s"""
        cur.execute(query, (image_name,))
        result = cur.fetchone()
        if result == None:
            query = """insert into image values(%s, %s, %s)"""
            cur.execute(query, (image_name, image_link, user_id))
            db_con.commit()
            disconnect_from_db(db_con)
        else:
            telegram.send_message(
            update["message"]["chat"]["id"],
            "There's already an image with this name in the database"
            )
            disconnect_from_db(db_con)
    else:
        telegram.send_message(
            update["message"]["chat"]["id"],
            "You are not allowed to add users!"
            )



def add_user(user_username, user_name, update):
    db_con = connect_to_db()
    cur = db_con.cursor()
    query = """select * from mm_user where username=%s"""
    cur.execute(query, [str(update["message"]["from"]["id"])])
    result = cur.fetchone()
    disconnect_from_db(db_con, update)
    if str(update["message"]["from"]["id"]) == str(os.environ["ADMIN_ID"]) or result is not None:
        db_con = connect_to_db()
        cur = db_con.cursor()
        query = """select * from mm_user where username=%s"""
        cur.execute(query, [user_username])
        result = cur.fetchone()
        if result == None:
            query = """insert into mm_user values(%s, %s)"""
            cur.execute(query, (user_username, user_name))
            telegram.send_message(
            update["message"]["chat"]["id"],
            "User created!"
            )
            db_con.commit()
            disconnect_from_db(db_con, update)
        else:
            telegram.send_message(
            update["message"]["chat"]["id"],
            "There's already a user with this id in the database"
            )
            disconnect_from_db(db_con, update)
    else:
        telegram.send_message(
            update["message"]["chat"]["id"],
            "You are not allowed to add users!"
            )
