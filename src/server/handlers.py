from data import telegram
from doc import filehandler
from data import databasecon
import psycopg2


def handle_help(update):
    telegram.send_message(
        update["message"]["chat"]["id"],
        "Halp iz hia"
        )



def handle_send(update):
    telegram.send_message(
        update["message"]["chat"]["id"],
        "I'd send the requested image now.. If I could!"
        )
    #SEND IMAGE



def handle_add_image(update):
    #con = databasecon.connect_to_db()
    name = "testname, please ignore" #Parse from text
    link = "testlink, please ignore" #Parse from text
    #databasecon.add_image(link, name, update["message"]["from"]["id"],con, update)
    #databasecon.disconnect_from_db(con)
    pass #ADD IMAGE TO DB



def handle_add_user(update):
    #con = databasecon.connect_to_db()
    #databasecon.add_user(update["message"]["from"]["id"],update["message"]["from"]["username"],con, update) #Need to parse id and name from text!
    #databasecon.disconnect_from_db(con)
    pass #ADD USER TO DB



def handle_about(update):
    telegram.send_message(
        update["message"]["chat"]["id"],
        filehandler.get_doc(filehandler.Document.about)
        )



def handle_unknown(update):
    print("Unknown command")



def handle_fuckyou(update):
    telegram.send_message(
        update["message"]["chat"]["id"],
        "Fuck you too!"
        )



def handle_db_config(update):
    con = databasecon.connect_to_db(update)
    cur = con.cursor()
    query = "create table mm_user(ID INT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL)"
    cur.execute(query)
    query = " create table mm_image(ID TEXT PRIMARY KEY NOT NULL, LINK TEXT NOT NULL, UPLOADED_BY INT NOT NULL references user(ID))"
    cur.execute(query)
    databasecon.disconnect_from_db(con)



__handlers = {
    "help": handle_help,
    "about": handle_about,
    "add": handle_add_image,
    "adduser": handle_add_user,
    "dbconfig": handle_db_config,
    "fuckyou": handle_fuckyou
}


def handle(command, update):
    if command in __handlers:
        __handlers[command](update)
    else:
        handle_unknown(update)