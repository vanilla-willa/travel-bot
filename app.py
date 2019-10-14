import os
import sys
import json
from datetime import datetime
from brain import process_message

import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    # TODO: validate payload
                    # Generate a SHA1 signature using the payload and your app's App Secret.
                    # Compare your signature to the signature in the X-Hub-Signature header (everything after sha1=). If the signatures match, the payload is genuine.

                    sender_id = messaging_event["sender"]["id"]        # user's facebook ID
                    recipient_id = messaging_event["recipient"]["id"]  # your page's facebook ID

                    log(messaging_event)
                    if messaging_event["message"].get("text"):  # user sent a text message
                        message = messaging_event["message"].get("text")
                        message_type = "text"

                    if messaging_event["message"].get("quick_reply"):  # user sent a quick reply
                        message = messaging_event["message"]["quick_reply"]["payload"]
                        message_type = "quick_reply"

                    mark_message_read(sender_id)
                    response_in_progress(sender_id)

                    # responses = process_message(message, message_type)
                    # for resp in responses:
                    # msg = create_quick_reply_options(resp)
                    send_message(sender_id, message)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def create_quick_reply_options(response):

    if type(response) == dict and "quick_replies" in response.keys():
        buttons = [dict(content_type="text", title=b["label"], payload=b["value"]) for b in response["quick_replies"]]
        return dict(text=response["text"], quick_replies=buttons)

    else:
        print(response)
        raise Exception("Don't know how to send a message like that")


def send_message(recipient_id, message_text):
    # Facebook's Send API reference: https://developers.facebook.com/docs/messenger-platform/reference/send-api/

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text,
            "quick_replies": [{
                "content_type": "text",
                "title": "test1",
                "payload": "test1"
            },{
                "content_type":"text",
                "title": "testw",
                "payload": "test2"
              }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def mark_message_read(recipient_id):
    # Facebook's Send API reference: https://developers.facebook.com/docs/messenger-platform/reference/send-api/

    log("Marking message as read")

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "sender_action": "mark_seen"
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def response_in_progress(recipient_id):
    # Facebook's Send API reference: https://developers.facebook.com/docs/messenger-platform/reference/send-api/

    log("Sending ... chat bubble to user")

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "sender_action": "typing_on"
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = unicode(msg).format(*args, **kwargs)
        print(u" === DEBUG {}: {} ===".format(datetime.now(), msg))
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
