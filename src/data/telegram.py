import requests
import json
import re
import urllib

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

def send_photo(chat_id, image_link, image_name):
    file_extension = None
    m = re.search('^[A-Za-z0-9]*\.(.+?)$', image_name)
    if m:
        file_extension = m.group(1)
    if file_extension == "gif":
        url = __url.format(__apikey, "sendDocument")
        sendname = str("send.{0}").format(file_extension)
        f = open(sendname, 'wb')
        f.write(urllib.request.urlopen(image_link).read())
        f.close()
        document = open(sendname, 'rb')
        data = {'chat_id': chat_id}
        files = {'document': document}
        response = requests.post(url, params=data, files=files)
    elif file_extension == "jpg" or file_extension == "jpeg" or file_extension == "png":
        url = __url.format(__apikey, "sendPhoto")
        sendname = str("send.{0}").format(file_extension)
        f = open(sendname, 'wb')
        f.write(urllib.request.urlopen(image_link).read())
        f.close()
        photo = open(sendname, 'rb')
        files = {'photo': photo}
        data = {'chat_id': chat_id}
        response = requests.post(url, params=data, files=files)
    else:
        pass
