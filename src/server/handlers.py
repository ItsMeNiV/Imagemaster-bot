from data import telegram


def handle_help(update):
    telegram.send_message(
        update["message"]["chat"]["id"],
        "Halp iz hia"
        )



def handle_unknown(update):
    print("Unknown command")



__handlers = {
    "help": handle_help
}


def handle(command, update):
    if command in __handlers:
        __handlers[command](update)
    else:
        handle_unknown(update)