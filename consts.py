# input greetings to trigger start of convo
GREETINGS = ["hello", "hi"]

INITIAL = ["Guangzhou"]

CITIES_AND_DATES = {
    "Guangzhou": ["Oct 24"],
    "Hong Kong": ["Oct 25", "Oct 26", "Oct 27"],
    "Longsheng":  ["Oct 28", "Oct 29"],
    "Yangshuo": ["Oct 30", "Oct 31"],
    "Fuzhou": ["Nov 1", "Nov 2", "Nov 3"],
    "Shenzhen": ["Nov 4", "Nov 5"]
}

TEXT_OUTPUTS = {
    "start": "Hi, my name is {}. I'm here to retrieve information "
             "about your lodging plans.".format(u'流浪狗'),
    "location": "Select your location.",
    "info": "What info would you like?",
    "selection": "You selected ____.",
    "more_info": "Is there more info you'd like?",
    "stop": "Thank you for chatting with me! Hope to talk to you soon! :) "
}

nodes = {
    "Guangzhou": {
        "month": "Oct",
        "dates": [24],
        "lodging": {
            "name": "hostel",
            "address": "[FILL IN HERE]",
            "check-in time": "[FILL IN HERE]",
            "check-out time": "[FILL IN HERE]",
            "url": "[FILL IN HERE]",
            "summary": "near ___ and ___",
        }
    }

}