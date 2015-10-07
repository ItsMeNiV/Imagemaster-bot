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
    if link:
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
    m = re.search('^\/mm_listimages (.*?)$', update["message"]["text"])
    if m:
        image_list_string = databasecon.get_all_images(update, m.group(1))
    else:
        image_list_string = databasecon.get_all_images(update)
    writestring = "All Images in the Database: {0}".format(image_list_string)
    telegram.send_message(
        update["message"]["chat"]["id"],
        writestring
        )



def handle_update_imagename(update):
    oldname = None
    newname = None
    m = re.search('^\/mm_updateimagename (.*?) [A-Za-z0-9_]*', update["message"]["text"])
    if m:
        oldname = m.group(1)
    m = re.search('^\/mm_updateimagename [A-Za-z0-9_\.]* (.*?)$', update["message"]["text"])
    if m:
        newname = m.group(1)
    if oldname and newname:
        databasecon.update_imagename(oldname, newname, update)
    else:
        telegram.send_message(
        update["message"]["chat"]["id"],
        "Can't find old- or new name. Be sure your message looks like this: \"/mm_updateimagename <oldname> <newname>\""
        )



def handle_delete_image(update):
    imagename = None
    m = re.search('^\/mm_deleteimage (.*?)$', update["message"]["text"])
    if m:
        imagename = m.group(1)
    if imagename:
        databasecon.delete_image(imagename, update)
    else:
        telegram.send_message(
        update["message"]["chat"]["id"],
        "Can't find imagename. Be sure your message looks like this: \"/mm_deleteimage <imagename>\""
        )


def handle_search_image(update):
    searchname = None
    m = re.search('^\/mm_searchimage [A-Za-z0-9_]*', update["message"]["text"])
    if m:
        searchname = m.group(1)
        telegram.send_message(
        update["message"]["chat"]["id"],
        databasecon.search_image(searchname, update)
        )
    else:
        telegram.send_message(
        update["message"]["chat"]["id"],
        "Can't find searchname. Be sure your message looks like this: \"/mm_searchimage <searchname>\""
        )


def handle_get_imageinfo(update):
    imagename = None
    m = re.search('^\/mm_getimageinfo (.*?)$', update["message"]["text"])
    imagename = m.group(1)
    if imagename:
        databasecon.get_image_info(imagename, update)
    else:
        telegram.send_message(
            update["message"]["chat"]["id"],
            "Can't find imagename. Be sure your message looks like this: \"/mm_getimageinfo <imagename>\""
            )


__handlers = {
    "help": handle_help,
    "about": handle_about,
    "adduser": handle_add_user,
    "addimage": handle_add_image,
    "listimages": handle_list_images,
    "updateimagename": handle_update_imagename,
    "deleteimage": handle_delete_image,
    "handleimage": handle_search_image,
    "getimageinfo": handle_get_imageinfo,
    "fuckyou": handle_fuckyou
}


def handle(command, update):
    if command in __handlers:
        __handlers[command](update)
    else:
        handle_unknown(update)