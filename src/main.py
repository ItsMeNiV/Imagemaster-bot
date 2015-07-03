from flask import Flask, request
import sys
import os
import json

from server import handlers
from data import telegram

__app = Flask(__name__)


@__app.route("/", methods=["POST"])
def main():
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
    if "API_KEY" not in os.environ:
        print("API_KEY env variable has not been set")
        sys.exit(1)

    telegram.init(os.environ["API_KEY"])


setup()
if __name__ == '__main__':
    __app.debug = True
    __app.run(host="0.0.0.0")