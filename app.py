import os
import sys
from datetime import datetime
from brain import Brain
from flask import Flask, request
import json
import requests

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
    log(data)

    if data["object"] == "page":
        print("HI!!")
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                messaging_event = json.dumps(messaging_event)
                print("converted messaging event: ", messaging_event)
                if messaging_event.get("message"):  # someone sent us a message

                    # TODO: validate payload
                    # Generate a SHA1 signature using the payload and your app's App Secret.
                    # Compare your signature to the signature in the X-Hub-Signature header (everything after sha1=).
                    # If the signatures match, the payload is genuine.

                    user_id = messaging_event["sender"]["id"]        # user's facebook ID
                    decision = Brain()

                    message_properties = decision.read_message_text(messaging_event)
                    if message_properties is None:
                        decision.send_message(user_id, dict(text="Sorry. I currently do not support anything beyond "
                                                                 "text and quick reply"))
                        return "ok", 200
                    print("What is message_properties?: ", message_properties)
                    msg_data = decision.process_message(user_id)
                    decision.send_message(user_id, msg_data)

                    # DEBUGGING
                    # if messaging_event["message"].get("text"):
                    #     send_message(user_id, dict(text="hello"))

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200

# DEBUGGING
# def send_message(user_id, message):
#     # Facebook's Send API reference: https://developers.facebook.com/docs/messenger-platform/reference/send-api/
#     # message parameter will contain both text and quick response
#     bot_text = message.get("text")
#
#     log("sending message to {recipient}: {text}".format(recipient=user_id, text=bot_text))
#
#     params = {
#         "access_token": os.environ["PAGE_ACCESS_TOKEN"]
#     }
#     headers = {
#         "Content-Type": "application/json"
#     }
#     data = json.dumps({
#         "recipient": {
#             "id": user_id
#         },
#         "message": message
#     })
#     r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
#     if r.status_code != 200:
#         log(r.status_code)
#         log(r.text)


def log(message):
    print("=== {} DEBUG MSG:: {} ===".format(datetime.now(), message))
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)