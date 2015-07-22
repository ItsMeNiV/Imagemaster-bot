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
    query = """select link from mm_image where lower(id)=lower(%s)"""
    cur.execute(query, [image_name])
    result = cur.fetchone()
    if result != None:
        image_link = str(result[0])
        disconnect_from_db(db_con, update)
        return image_link
    else:
        disconnect_from_db(db_con, update)
        return None



def add_image(image_link, image_name, user_id, update):
    db_con = connect_to_db()
    cur = db_con.cursor()
    query = """select * from mm_user where username=%s"""
    cur.execute(query, [str(update["message"]["from"]["username"])])
    result = cur.fetchone()
    disconnect_from_db(db_con, update)
    if str(update["message"]["from"]["id"]) == str(os.environ["ADMIN_ID"]) or result is not None:
        if str(update["message"]["from"]["id"]) == str(os.environ["ADMIN_ID"]):
            if "ADMIN_USERNAME" in os.environ:
                user_id = str(os.environ["ADMIN_USERNAME"])
            else:
                print("Missing ADMIN_USERNAME Environment-variable")
        db_con = connect_to_db()
        cur = db_con.cursor()
        query = """select * from mm_image where lower(id)=lower(%s)"""
        cur.execute(query, (image_name,))
        result = cur.fetchone()
        if result == None:
            query = """insert into mm_image values(%s, %s, %s)"""
            cur.execute(query, (image_name, image_link, user_id))
            db_con.commit()
            disconnect_from_db(db_con, update)
            telegram.send_message(
            update["message"]["chat"]["id"],
            "Image {0} successfully added".format(image_name)
            )
        else:
            telegram.send_message(
            update["message"]["chat"]["id"],
            "There's already an image with this name in the database"
            )
            disconnect_from_db(db_con, update)
    else:
        telegram.send_message(
            update["message"]["chat"]["id"],
            "You are not allowed to add images!"
            )



def add_user(user_username, user_name, update):
    db_con = connect_to_db()
    cur = db_con.cursor()
    query = """select * from mm_user where username=%s"""
    cur.execute(query, [str(update["message"]["from"]["username"])])
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



def get_all_images(update, extension=None):
    db_con = connect_to_db()
    cur = db_con.cursor()
    if extension is None:
        cur.execute("select id from mm_image;")
    else:
        print(extension)
        cur.execute("select id from mm_image where id like %s;", [str("%.{0}").format(extension)])
    result = cur.fetchall()
    disconnect_from_db(db_con, update)

    string_list = [' '.join(item) for item in result]
    retstring = ', '.join(string_list)
    return retstring



def update_imagename(oldname, newname, update):
    db_con = connect_to_db()
    cur = db_con.cursor()
    query = """select * from mm_user where username=%s"""
    cur.execute(query, [str(update["message"]["from"]["username"])])
    result = cur.fetchone()
    disconnect_from_db(db_con, update)
    if str(update["message"]["from"]["id"]) == str(os.environ["ADMIN_ID"]) or result is not None:
        db_con = connect_to_db()
        cur = db_con.cursor()
        cur.execute("update mm_image set id=lower(%s) where lower(id)=lower(%s);", (newname, oldname))
        db_con.commit()
        disconnect_from_db(db_con, update)
        telegram.send_message(
                update["message"]["chat"]["id"],
                "Updated image name {0} to {1}".format(oldname, newname)
                )
    else:
        telegram.send_message(
                update["message"]["chat"]["id"],
                "You are not allowed to do that!"
                )



def update_imagelink(imagename, newlink, update):
    db_con = connect_to_db()
    cur = db_con.cursor()
    query = """select * from mm_image where uploaded_by=%s and id=%s"""
    cur.execute(query, (str(update["message"]["from"]["username"]), imagename))
    result = cur.fetchone()
    disconnect_from_db(db_con, update)
    print(result)
    if str(update["message"]["from"]["id"]) == str(os.environ["ADMIN_ID"]) or result is not None:
        db_con = connect_to_db()
        cur = db_con.cursor()
        cur.execute("update mm_image set link=%s where lower(id)=lower(%s);", (newlink, imagename))
        db_con.commit()
        disconnect_from_db(db_con, update)
        telegram.send_message(
                update["message"]["chat"]["id"],
                "Link updated!"
                )
    else:
        telegram.send_message(
                update["message"]["chat"]["id"],
                "You didn't upload that image so you can't change it!"
                )




def delete_image(imagename, update):
    if str(update["message"]["from"]["id"]) == str(os.environ["ADMIN_ID"]):
        db_con = connect_to_db()
        cur = db_con.cursor()
        cur.execute("delete from mm_image where lower(id)=lower(%s);", [imagename])
        db_con.commit()
        disconnect_from_db(db_con, update)
        telegram.send_message(
                update["message"]["chat"]["id"],
                "Removed image {0}".format(imagename)
                )
    else:
        telegram.send_message(
                update["message"]["chat"]["id"],
                "Only the admin is allowed to remove images!"
                )



def get_image_info(imagename, update):
    db_con = connect_to_db()
    cur = db_con.cursor()
    query = """select * from mm_user where username=%s"""
    cur.execute(query, [str(update["message"]["from"]["username"])])
    result = cur.fetchone()
    disconnect_from_db(db_con, update)
    if str(update["message"]["from"]["id"]) == str(os.environ["ADMIN_ID"]) or result is not None:
        db_con = connect_to_db()
        cur = db_con.cursor()
        cur.execute("select * from mm_image where lower(id)=lower(%s)", [imagename])
        result = cur.fetchone()
        disconnect_from_db(db_con, update)
        if result is not None:
            img_id = str(result[0])
            img_link = str(result[1])
            img_uploaded_by = str(result[2])
            telegram.send_message(
                    update["message"]["chat"]["id"],
                    "The image {0} was:\nUploaded by: {1}\nAnd it points to: {2}".format(img_id, img_uploaded_by, img_link)
                    )
        else:
            telegram.send_message(
                    update["message"]["chat"]["id"],
                    "Couldn't find this image in the Databse"
                    )
    else:
        telegram.send_message(
            update["message"]["chat"]["id"],
            "You are not allowed to do that!"
            )
