import sys
import consts
from datetime import datetime


def process_message(message_type, message):
    """
    User input of either text or quick reply returns additional text and quick reply
    :param message: either text or payload
    :param message_type: either text or quick_reply
    :return: dict with text and quick_reply
    quick_reply is a list of dicts
    """

    response = {}
    quick_reply_list = []

    # if message in text_outputs.keys():
    #     responses.append(dict(
    #         text=text_outputs[message],
    #         quick_replies=consts.CITIES_AND_DATES.keys()
    #     ))

    if message in consts.GREETINGS:
        response.update(dict(text=consts.TEXT_OUTPUTS["start"]))
        log("Updated to response dict. Currently looks like: {}".format(response))
        quick_reply_list.append(dict(content_type="text", title=opt, payload=opt) for opt in consts.INITIAL)
        response.update(dict(quick_replies=quick_reply_list))
        log("Updated to response dict. Currently looks like: {}".format(response))

    return response


def log(message):  # simple wrapper for logging to stdout on heroku
    print("=== {} DEBUG MSG:: {} ===".format(datetime.now(), message))
    sys.stdout.flush()