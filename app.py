import os
import sys
from datetime import datetime
# from brain import process_message
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

                    user_id = messaging_event["sender"]["id"]        # user's facebook ID
                    decision = Brain()

                    message_type = decision.determine_message_type(user_id, messaging_event)
                    if message_type is None:
                        return "ok", 200

                    message = decision.read_message_text(user_id, messaging_event)
                    msg_data = decision.process_message(user_id, message_type, message)
                    decision.send_message(msg_data)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def log(message):
    print("=== {} DEBUG MSG:: {} ===".format(datetime.now(), message))
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)