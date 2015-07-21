from flask import Flask, request
import sys
import os
import json
import re
import logging

from server import handlers
from data import telegram

__app = Flask(__name__)
__app.logger.addHandler(logging.StreamHandler(sys.stdout))
__app.logger.setLevel(logging.ERROR)


@__app.route("/", methods=["POST"])
def main():
    pattern = re.compile("^[A-Za-z0-9]*\.(jpg|jpeg|gif|png)$")
    update = request.get_json()
    if "message" in update:
        message = update["message"]
        if "text" in message:
            text = message["text"]
            if pattern.match(text):
                if "username" in message["from"]:
                    handlers.handle_send(update)
                else:
                    telegram.send_message(
                        update["message"]["chat"]["id"],
                        "Smul is a huge faggot! Also: You don't have a username"
                        )
            elif text.startswith("/mm_"):
                retext = None
                m = re.search('^\/mm_(.*?) .*$', text)
                if m:
                    retext = m.group(1)
                else:
                    m = re.search('^\/mm_(.*?)$', text)
                    if m:
                        retext = m.group(1)
                print(retext)
                if "username" in message["from"]:
                    handlers.handle(retext, update)
                else:
                    telegram.send_message(
                        update["message"]["chat"]["id"],
                        "Smul is a huge faggot! Also: You don't have a username"
                        )

    return ""


def setup():
    if "API_KEY" not in os.environ:
        print("API_KEY env variable has not been set")
        sys.exit(1)

    telegram.init(os.environ["API_KEY"])


setup()
if __name__ == '__main__':
    __app.debug = True
    __app.run(host="0.0.0.0")