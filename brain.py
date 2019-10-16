import os
import sys
import consts
from datetime import datetime
import requests
import json
# from graph import Graph


# def create_graph():
#     test = Graph()

class Brain:

    def __init__(self):
        pass

    def determine_message_type(self, user_id, messaging_event):
        if messaging_event["message"].get("text"):  # user sent a text message
            return "text"

        elif messaging_event["message"].get("quick_reply"):  # user sent a quick reply
            return "quick_reply"

        else:
            self.send_message(user_id, dict(text="Sorry. I currently do not support anything beyond "
                                                 "text and quick reply"))
            return None

    def read_message_text(self, user_id, messaging_event):
        if self.determine_message_type(user_id, messaging_event) == "text":
            return messaging_event["message"].get("text")
        else:
            return messaging_event["message"]["quick_reply"]["payload"]

    def process_message(self, message_type, message):
        """
        User input of either text or quick reply returns additional text and quick reply
        Payload from quick reply lets you know which button was clicked
        :param message: either text or payload
        :param message_type: either text or quick_reply
        :return: dict with text and quick_reply
        quick_reply is a list of dicts
        """

        response = {}

        if message in consts.GREETINGS:
            self.log("Updated to response dict. Currently looks like: {}".format(response))
            quick_reply_list = list(dict(content_type="text", title=opt, payload=opt) for opt in consts.INITIAL)
            response.update(dict(quick_replies=quick_reply_list))
            self.log("Updated to response dict. Currently looks like: {}".format(response))

        return response

    def send_message(self, user_id, message):
        # Facebook's Send API reference: https://developers.facebook.com/docs/messenger-platform/reference/send-api/
        # message parameter will contain both text and quick response
        bot_text = message.get("text")

        self.log("sending message to {recipient}: {text}".format(recipient=user_id, text=bot_text))

        params = {
            "access_token": os.environ["PAGE_ACCESS_TOKEN"]
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": user_id
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
            self.log(r.status_code)
            self.log(r.text)

    def mark_message_read(self, user_id):
        # Facebook's Send API reference: https://developers.facebook.com/docs/messenger-platform/reference/send-api/

        self.log("Marking message as read")

        params = {
            "access_token": os.environ["PAGE_ACCESS_TOKEN"]
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": user_id
            },
            "sender_action": "mark_seen"
        })
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
        if r.status_code != 200:
            self.log(r.status_code)
            self.log(r.text)

    def response_in_progress(self, user_id):
        # Facebook's Send API reference: https://developers.facebook.com/docs/messenger-platform/reference/send-api/

        self.log("Sending ... chat bubble to user")

        params = {
            "access_token": os.environ["PAGE_ACCESS_TOKEN"]
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": user_id
            },
            "sender_action": "typing_on"
        })
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
        if r.status_code != 200:
            self.log(r.status_code)
            self.log(r.text)

    @staticmethod
    def log(message):  # simple wrapper for logging to stdout on heroku
        print("=== {} DEBUG MSG:: {} ===".format(datetime.now(), message))
        sys.stdout.flush()
