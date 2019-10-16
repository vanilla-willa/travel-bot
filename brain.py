import os
import sys
import consts
from datetime import datetime
import requests
import json


class Brain:

    def __init__(self):
        self.is_quick_reply = False
        pass

    def determine_message_type(self, user_id, messaging_event):
        if messaging_event["message"].get("text"):  # user sent a text message
            return "text"

        elif messaging_event["message"].get("quick_reply"):  # user sent a quick reply
            self.is_quick_reply = True
            return "quick_reply"

        else:
            self.send_message(user_id, dict(text="Sorry. I currently do not support anything beyond "
                                                 "text and quick reply"))
            return None

    def read_message_text(self, messaging_event):
        if not self.is_quick_reply:
            message = messaging_event["message"].get("text")
            self.log(message)
            return [message]
        else:
            message = messaging_event["message"]["quick_reply"]["text"]
            payload = messaging_event["message"]["quick_reply"]["payload"]
            self.log("message: {}, payload: {} ".format(message, payload))
            return [message, payload]

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
        if len(message_properties) > 1:
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
