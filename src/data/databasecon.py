import psycopg2
import os
import urllib.parse
from data import telegram

def connect_to_db(update):
    if "DATABASE_URL" not in os.environ:
        print("Environment-variable missing")
    else:
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
        
        telegram.send_message(
        update["message"]["chat"]["id"],
        "Trying to connect to db")

        con = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
            )
        
        telegram.send_message(
        update["message"]["chat"]["id"],
        "DB-connection succesful")

        return con




def disconnect_from_db(db_con):
    db_con.close()



def search_image(image_name, db_con):
    cur = db_con.cursor()
    query = """select image_link from image where image_name=%s"""
    cur.execute(query, (image_name))
    result = cur.fetchone()
    if result != None:
        image_link = result[0]
        return image_link
    else:
        return "Not found"



def add_image(image_link, image_name, user_id, db_con, update):
    cur = db_con.cursor()
    query = """select * from image where image_name=%s"""
    cur.execute(query, (image_name,))
    result = cur.fetchone()
    if result == None:
        query = """insert into image values(%s, %s, %s)"""
        cur.execute(query, (image_name, image_link, user_id))

        db_con.commit()
    else:
        telegram.send_message(
        update["message"]["chat"]["id"],
        "There's already an image with this name in the database"
        )



def add_user(user_id, user_name, db_con, update):
    cur = db_con.cursor()
    query = """select * from user where user_id=%s"""
    cur.execute(query, (str(user_id),))
    result = cur.fetchone()
    if result == None:
        query = """insert into user values(%s, %s)"""
        cur.execute(query, (user_id, user_name))
        print("User created!")
        db_con.commit()
    else:
        telegram.send_message(
        update["message"]["chat"]["id"],
        "There's already a user with this id in the database"
        )
