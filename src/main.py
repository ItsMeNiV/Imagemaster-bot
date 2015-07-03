from flask import Flask, request
import sys
import os
import json

from server import handlers
from data import telegram

__app = Flask(__name__)


@__app.route("/", methods=["POST"])
def hello_world():
    update = request.get_json()
    if "message" in update:
        message = update["message"]
        if "text" in message:
            text = message["text"]
            if text.startswith("/mm_"):
                text = text[4:]
                handlers.handle(text, update)

    return ""


def setup():
    if "SPYFALL_APIKEY" not in os.environ:
        print("SPYFALL_APIKEY env variable has not been set")
        sys.exit(1)

    telegram.init(os.environ["SPYFALL_APIKEY"])


setup()
if __name__ == '__main__':
    __app.debug = True
    __app.run(host="0.0.0.0")