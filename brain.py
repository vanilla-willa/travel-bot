import sys
import consts
from datetime import datetime
# from graph import Graph


# def create_graph():
#     test = Graph()

def process_message(message_type, message):
    """
    User input of either text or quick reply returns additional text and quick reply
    Payload from quick reply lets you know which button was clicked
    :param message: either text or payload
    :param message_type: either text or quick_reply
    :return: dict with text and quick_reply
    quick_reply is a list of dicts
    """

    response = {}

    # if message in text_outputs.keys():
    #     responses.append(dict(
    #         text=text_outputs[message],
    #         quick_replies=consts.CITIES_AND_DATES.keys()
    #     ))

    if message in consts.GREETINGS:
        response.update(dict(text=["Helloooo", consts.TEXT_OUTPUTS["start"]]))
        log("Updated to response dict. Currently looks like: {}".format(response))
        quick_reply_list = list(dict(content_type="text", title=opt, payload=opt) for opt in consts.INITIAL)
        response.update(dict(quick_replies=quick_reply_list))
        log("Updated to response dict. Currently looks like: {}".format(response))

    return response


def log(message):  # simple wrapper for logging to stdout on heroku
    print("=== {} DEBUG MSG:: {} ===".format(datetime.now(), message))
    sys.stdout.flush()