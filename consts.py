# input greetings to trigger start of convo
GREETINGS = ["hello", "hi"]

INITIAL = ["Guangzhou"]

BOT_MSGS = {
    "start": "Hi, I'm here to retrieve information about your lodging plans.",
    "location": "Select your location.",
    "info": "What info would you like?",
    "selection": "You selected ____.",
    "more_info": "Is there more info you'd like?",
    "stop": "Thank you for chatting with me! Hope to talk to you soon! :) "
}

DATA = {
    "Guangzhou": {
        "Name": "Lazy Gaga Hostel",
        "Dates": ["Oct 24"],
        "Address": "215 Haizhu Zhong Road, YueXiu District, Guangzhou, China",
        "Check-in Time": "13:00-18:00",
        "Check-out Time": "Flexible(?)",
        "Url": "https://www.hostelworld.com/hosteldetails.php/Lazy-Gaga-Hostel/Guangzhou/77286?dateFrom=2019-10-24&dateTo=2019-10-25&number_of_guests=2&sc_pos=1",
        "Summary": "No co-ed dorms, near Shangxiajiu Pedestrian Street, near Ximenkou Metro Station, free luggage storage",
        "Phone Number": "+86 20 8192 3232",
        "Visited": False
    },
    "Hong Kong": {
        "Name": "YHA Mei Ho House",
        "Dates": ["Oct 25", "Oct 26"],
        "Address": "Block 41 Shek Kip Mei Estate, Sham Shui Po, Hong Kong, Hong Kong China",
        "Check-in Time": "16:00",
        "Check-out Time": "11:00",
        "Url": "https://www.hostelworld.com/hosteldetails.php/YHA-Mei-Ho-House/Hong-Kong/82044?dateFrom=2019-10-25&dateTo=2019-10-26&number_of_guests=2&sc_pos=3",
        "Summary": "Near Sham Shui Po Night Markets, mixed dorms, coin-operated laundry",
        "Phone Number": "+852 3728 3500",
        "Visited": False
    },
    "Longsheng": {
        "Name": "Rice View Villa",
        "Dates": ["Oct 28", "Oct 29"],
        "Address": "[FILL IN HERE]",
        "Check-in Time": "14:00",
        "Check-out Time": "12:00",
        "Url": "https://www.booking.com/hotel/cn/long-yi-xuan.en-us.html?aid=1550129;label=postbooking_confpage;sid=e27e0ff387b9fce17a0ec3dacc438e69;checkin=2019-11-01;checkout=2019-11-02;dest_id=-1916500;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=1;hpos=1;no_rooms=1;room1=A%2CA;sb_price_type=total;soh=1;sr_order=popularity;srepoch=1571551947;srpvid=fe702ba52bd2006f;type=total;ucfs=1&#no_availability_msg",
        "Summary": "5 miles from Jinkeng Rice Terrace, 12 miles from Pingan Rice Terrace, private bathroom, available gym and laundry",
        "Phone Number": "+86 182 0773 3701",
        "Visited": False
    },
    "Yangshuo": {
        "Name": "Yangshuo Travelling With Hostel (West Street)",
        "Dates": ["Oct 30", "Oct 31"],
        "Address": "3F Zone A, Business Street, Cheng Zhong Cheng, Diecui Road, Yangshuo, 541900 Yangshuo, China",
        "Check-in time": "12:00 PM",
        "Check-out time": "12:00 PM",
        "Url": "https://www.booking.com/hotel/cn/green-forest-hostel-yangshuo.html?aid=356980;label=gog235jc-1DCAsoMUIcZ3JlZW4tZm9yZXN0LWhvc3RlbC15YW5nc2h1b0gzWANolQKIAQGYATG4AQfIAQzYAQPoAQH4AQKIAgGoAgO4Atj56-wFwAIB;sid=43194d254e520695bea5001b2cd6de23;all_sr_blocks=50048412_125412330_0_2_0;checkin=2019-10-30;checkout=2019-11-01;dest_id=-1935586;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=1;highlighted_blocks=50048412_125412330_0_2_0;hpos=1;no_rooms=1;room1=A%2CA;sb_price_type=total;sr_order=popularity;srepoch=1570679760;srpvid=47d21ba79c4500d4;type=total;ucfs=1&#hotelTmpl",
        "Summary": "5 minute walk from West Street",
        "Phone Number": "+86 773 888 2686",
        "Visited": False
    }
}

