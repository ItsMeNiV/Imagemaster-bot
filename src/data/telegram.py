import requests
import json

__apikey = None
__url = "https://api.telegram.org/bot{0}/{1}"


def init(apikey):
    global __apikey
    __apikey = apikey


def send_message(chat_id,
                 message,
                 reply_id=None,
                 reply_markup=None,
                 disable_preview=True):
    url = __url.format(__apikey, "sendMessage")

    data = {"chat_id": chat_id, "text": message}

    if reply_id is not None:
        data["reply_to_message_id"] = reply_id

    if reply_markup is not None:
        data["reply_markup"] = json.dumps(reply_markup)

    if disable_preview:
        data["disable_web_page_preview"] = "true"

    response = requests.post(url, params=data)
