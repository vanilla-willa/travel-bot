# input greetings to trigger start of convo
GREETINGS = ["hello", "hi"]

INITIAL = ["Guangzhou"]

TEXT_OUTPUTS = {
    "start": "Hi, I'm here to retrieve information about your lodging plans.",
    "location": "Select your location.",
    "info": "What info would you like?",
    "selection": "You selected ____.",
    "more_info": "Is there more info you'd like?",
    "stop": "Thank you for chatting with me! Hope to talk to you soon! :) "
}

DATA = {
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
    },
    "Hong Kong": {
        "month": "Oct",
        "dates": [25, 26],
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