import os
import sys
from datetime import datetime
from brain import Brain
from flask import Flask, request
import requests
import json

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
    # TODO: implement greeting message and get started button

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):  # someone sent us a message

                    # TODO: validate payload
                    # Generate a SHA1 signature using the payload and your app's App Secret.
                    # Compare your signature to the signature in the X-Hub-Signature header (everything after sha1=).
                    # If the signatures match, the payload is genuine.

                    sender_id = messaging_event["sender"]["id"]        # user's facebook ID
                    recipient_id = messaging_event["recipient"]["id"]  # your page's facebook ID

                    if messaging_event["message"].get("text"):  # user sent a text message
                        message = messaging_event["message"].get("text")
                        message_type = "text"

                    elif messaging_event["message"].get("quick_reply"):  # user sent a quick reply
                        # message_payload will be the same as the text
                        message = messaging_event["message"]["quick_reply"]["payload"]
                        message_type = "quick_reply"

                    else:
                        send_message(sender_id, dict(text="Sorry. I currently do not support anything beyond "
                                                          "text and quick reply"))

                    mark_message_read(sender_id)
                    response_in_progress(sender_id)

                    msg_data = process_message(message_type, message)
                    send_message(sender_id, msg_data)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message):
    # Facebook's Send API reference: https://developers.facebook.com/docs/messenger-platform/reference/send-api/
    # message parameter will contain both text and quick response
    bot_text = message.get("text")

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=bot_text))

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
        "message": message
        # {
        #     "text": message,
        #     "quick_replies": [{
        #         "content_type": "text",
        #         "title": "test1",
        #         "payload": "test1"
        #     }, {
        #         "content_type": "text",
        #         "title": "test2",
        #         "payload": "test2"
        #       }
        #     ]
        # }
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


def log(message):  # simple wrapper for logging to stdout on heroku
    print("=== {} DEBUG MSG:: {} ===".format(datetime.now(), message))
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)