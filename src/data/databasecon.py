import psycopg2
import os
import urllib.parse
from data import telegram

__is_connected = False
__con = None

def connect_to_db():
    global __is_connected
    global __con
    if "DATABASE_URL" not in os.environ or __is_connected == True:
        print("Environment-variable missing or already connected")
    else:
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
        __con = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
            )
        if __con != None:
            __is_connected = True




def disconnect_from_db():
    global __is_connected
    global __con
    __con.close()
    __is_connected = False
    __con = None



def search_image(image_name, update):
    global __con
    connect_to_db()
    cur = __con.cursor()
    query = """select link from mm_image where id=%s"""
    cur.execute(query, (image_name))
    result = cur.fetchone()
    if result != None:
        image_link = str(result[0])
        disconnect_from_db()
        return image_link
    else:
        disconnect_from_db()
        return "Not found"



def add_image(image_link, image_name, user_id, update):
    global __con
    connect_to_db()
    cur = __con.cursor()
    query = """select * from image where image_name=%s"""
    cur.execute(query, (image_name,))
    result = cur.fetchone()
    if result == None:
        query = """insert into image values(%s, %s, %s)"""
        cur.execute(query, (image_name, image_link, user_id))

        __con.commit()
        disconnect_from_db()
    else:
        telegram.send_message(
        update["message"]["chat"]["id"],
        "There's already an image with this name in the database"
        )
        disconnect_from_db()



def add_user(user_id, user_name, update):
    global __con
    connect_to_db()
    cur = __con.cursor()
    query = """select * from user where user_id=%s"""
    cur.execute(query, (str(user_id),))
    result = cur.fetchone()
    if result == None:
        query = """insert into user values(%s, %s)"""
        cur.execute(query, (user_id, user_name))
        print("User created!")
        __con.commit()
        disconnect_from_db()
    else:
        telegram.send_message(
        update["message"]["chat"]["id"],
        "There's already a user with this id in the database"
        )
        disconnect_from_db()
