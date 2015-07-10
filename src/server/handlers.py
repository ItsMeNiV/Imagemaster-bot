from data import telegram
from doc import filehandler


def handle_help(update):
    telegram.send_message(
        update["message"]["chat"]["id"],
        "Halp iz hia"
        )



def handle_send(update):
    pass #SEND IMAGE



def handle_add(update):
    pass #ADD IMAGE TO DB



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



__handlers = {
    "help": handle_help,
    "about": handle_about,
    "add": handle_add,
    "fuckyou": handle_fuckyou
}


def handle(command, update):
    if command in __handlers:
        __handlers[command](update)
    else:
        handle_unknown(update)