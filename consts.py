# input greetings to trigger start of convo
GREETINGS = ["hello", "hi"]

INITIAL = ["Dates", "Locations"]

CITIES_AND_DATES = {
    "Guangzhou": ["Oct 24"],
    "Hong Kong": ["Oct 25", "Oct 26", "Oct 27"],
    "Longji":  ["Oct 28", "Oct 29"],
    "Yangshuo": ["Oct 30", "Oct 31"],
    "Guilin": [],
    "Fuzhou": ["Nov 1", "Nov 2", "Nov 3"],
    "Shenzhen": ["Nov 4", "Nov 5"]
}

OPTIONS = ["Sightseeing", "Food", "Lodging"]

TEXT_OUTPUTS = {
    "start": "Hi, how do would you like to search?",
    "search": "What are you searching for?",
    "options": "What would you like to do?",
    "info": "What info would you like?"
}