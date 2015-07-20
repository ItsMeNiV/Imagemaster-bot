from data import telegram
from doc import filehandler
from data import databasecon
import psycopg2
import re


def handle_help(update):
    telegram.send_message(
        update["message"]["chat"]["id"],
        "Halp iz hia"
        )



def handle_send(update):
    image_name = str(update["message"]["text"])
    link = databasecon.search_image(image_name, update)
    if link != "Not found":
        telegram.send_photo(
            update["message"]["chat"]["id"],
            link,
            image_name
            )
    else:
        telegram.send_message(
        update["message"]["chat"]["id"],
        "Image not found"
        )



def handle_add_image(update):
    name = None
    link = None
    m = re.search('^\/mm_addimage (.+?) [A-Za-z0-9]*', update["message"]["text"]) #Matching the name
    if m:
        name = m.group(1)
    m = re.search('^\/mm_addimage [A-Za-z0-9]*\.[A-Za-z0-9]* (.*?)$', update["message"]["text"]) #Matching the link
    if m:
        link = m.group(1)
    if link is not None and name is not None:
        databasecon.add_image(link, name, update["message"]["from"]["username"], update)
    else:
        telegram.send_message(
        update["message"]["chat"]["id"],
        "Can't find imagename or link. Be sure your message looks like this: \"/mm_addimage <imagename> <imagelink>\" and don't forget the file extension for the imagename"
        )



def handle_add_user(update):
    username = None
    name = None
    m = re.search('^\/mm_adduser (.*?) [A-Za-z0-9_]*', update["message"]["text"]) #Matching the username
    if m:
        username = m.group(1)
    m = re.search('^\/mm_adduser [A-Za-z0-9_]* (.*?)$', update["message"]["text"]) #Matching the user's name
    if m:
        name = m.group(1)
    if username is not None and name is not None:
        databasecon.add_user(username, name, update)
    else:
        telegram.send_message(
        update["message"]["chat"]["id"],
        "Can't find username or user's name. Be sure your message looks like this: \"/mm_adduser <username> <name>\" The second name should be the user's firstname"
        )



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



def handle_list_images(update):
    image_list_string = databasecon.get_all_images(update)
    writestring = "All Images in the Database: {0}".format(image_list_string)
    telegram.send_message(
        update["message"]["chat"]["id"],
        writestring
        )



__handlers = {
    "help": handle_help,
    "about": handle_about,
    "add": handle_add_image,
    "adduser": handle_add_user,
    "addimage": handle_add_image,
    "listimages": handle_list_images,
    "fuckyou": handle_fuckyou
}


def handle(command, update):
    if command in __handlers:
        __handlers[command](update)
    else:
        handle_unknown(update)