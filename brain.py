import os
import sys
import consts
from datetime import datetime
import requests
import json


class Brain:

    def __init__(self):
        self.is_quick_reply = None
        pass

    def determine_message_type(self, messaging_event):
        # Set is_quick_reply to either True or False. If not compatible, defaulted to None
        if messaging_event["message"].get("quick_reply"):  # user sent a quick reply
            print("User sent quick reply. Setting is_quick_reply to True")
            self.is_quick_reply = True

        elif messaging_event["message"].get("text"):  # user sent a text
            print("User sent quick reply. Setting is_quick_reply to False")
            self.is_quick_reply = False

    def read_message_text(self, messaging_event):
        self.determine_message_type(messaging_event)

        if self.is_quick_reply is None:
            return None

        if self.is_quick_reply:
            message = messaging_event["message"].get("text")
            payload = messaging_event["message"]["quick_reply"].get("payload")
            return [message, payload]
        else:
            message = messaging_event["message"].get("text")
            self.log(message)
            return [message]

    def process_message(self, user_id, message_properties):
        """
        User input of either text or quick reply returns additional text and quick reply
        Payload from quick reply lets you know which button was clicked
        :param user_id: string
        :param message_properties: list of length 1 or 2, depending on text or quick reply, respectively
        :return: dict with text and quick_reply
        quick_reply is a list of dicts
        """
        self.typing(user_id)
        response = {}
        print("This is a quick reply: ", self.is_quick_reply)

        message = message_properties[0]
        if self.is_quick_reply:
            payload = message_properties[1]

        if message in consts.GREETINGS:
            response.update(dict(text=consts.BOT_MSGS["start"]))
            # self.log("Updated to response dict. Currently looks like: {}".format(response))
            quick_reply_list = list(dict(content_type="text", title=city, payload="city") for city in consts.DATA.keys())
            response.update(dict(quick_replies=quick_reply_list))
            # self.log("Updated to response dict. Currently looks like: {}".format(response))

        elif self.is_quick_reply:
            self.log("this is a freaking quick reply")
            if payload is "city":
                self.log("i just clicked on a freaking city")
                response.update(dict(text=consts.BOT_MSGS["info"]))
                self.log("Updated to response dict. Currently looks like: {}".format(response))
                quick_reply_list = list(dict(content_type="text", title=info, payload = "info")
                                        for city in consts.DATA.keys() for info in consts.DATA[city].keys())
                response.update(dict(quick_replies=quick_reply_list))

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

    def typing(self, user_id):
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
    def log(message):
        print("=== {} DEBUG MSG:: {} ===".format(datetime.now(), message))
        sys.stdout.flush()
