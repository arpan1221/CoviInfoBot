# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

import requests

state_code_dict = {'Andaman and Nicobar Islands':'AN','Andhra Pradesh':'AP', 
'Arunachal Pradesh':'AR','Assam':'AS','Bihar':'BR','Chandigarh':'CH','Chhattisgarh':'CT',
'Dadra and Nagar Haveli':'DN','Daman and Diu':'DD','Delhi':'DL','Goa':'GA','Gujarat':'GJ',
'Haryana':'HR','Himachal Pradesh':'HP','Jammu and Kashmir':'JK','Jharkhand':'JH','Karnataka':'KA',
'Kerala':'KL','Lakshadweep':'LD','Madhya Pradesh':'MP','Maharashtra':'MH','Manipur':'MN','Meghalaya':'ML',
'Mizoram':'MZ','Nagaland':'NL','Odisha':'OR','Puducherry':'PY','Punjab':'PB','Rajasthan':'RJ','Sikkim':'SK',
'Tamil Nadu':'TN','Telangana':'TG','Tripura':'TR','Uttar Pradesh':'UP','Uttarakhand':'UT','West Bengal':'WB'}

class ActionGetLiveData(Action):
    def name(self)-> Text:
        return "action_get_data"

    def run(self, dispatcher,tracker, domain):
        pincode = tracker.get_slot('numpin')
        pincode_data = requests.get('https://api.postalpincode.in/pincode/{}'.format(pincode)).json()
        district = pincode_data[0]['PostOffice'][0]['District']
        state = pincode_data[0]['PostOffice'][0]['State']
        name = pincode_data[0]['PostOffice'][0]['Name']
        sc = state_code_dict.get(state)
        cases = requests.get('https://api.covid19india.org/v4/min/data.min.json').json()
        total = cases[sc]['districts'][district]['total']
        try:
            confirmed = cases[sc]['districts'][district]['total']['confirmed']
        except KeyError:
            confirmed = ""
        try:
            deceased = cases[sc]['districts'][district]['total']['deceased']
        except KeyError:
            deceased = ""
        try:
            other = cases[sc]['districts'][district]['total']['other']
        except KeyError:
            other = ""
        try:
            recovered = cases[sc]['districts'][district]['total']['recovered']
        except KeyError:
            recovered = ""
        try:
            tested = cases[sc]['districts'][district]['total']['tested']
        except KeyError:
            tested = ""
        try:
            vaccinated1 = cases[sc]['districts'][district]['total']['vaccinated1']
        except KeyError:
            vaccinated1 = ""
        try:
            vaccinated2 = cases[sc]['districts'][district]['total']['vaccinated2']
        except KeyError:
            vaccinated2 = ""
        response = """ In {}, {}, {} at pincode {} the Covid cases status is:
Confirmed: {}
Deceased: {}
Other: {}
Recovered: {}
Tested: {}
Vaccinated1: {}
Vaccinated2: {}""".format(state,district,name,pincode,confirmed,deceased,other,recovered,tested,vaccinated1,vaccinated2)
        dispatcher.utter_message(response)
        return [SlotSet('numpin',pincode)]

class ActionGetLiveNews(Action):
    def name(self)-> Text:
        return "action_get_news"
    def run(self, dispatcher,tracker, domain):
        info = requests.get('https://newsapi.org/v2/top-headlines?country=in&apiKey=5b6451226eb74882919e8fed27aa75c6').json()
        substring1 = "covid"
        substring2 = "corona"
        total_results = info['totalResults']
        for i in range (0, int(total_results/2)):
            title = info['articles'][i]['title']
            title1 = title.lower()
            if substring1 in title1 or substring2 in title1:
                output_author = info['articles'][i]['author']
                output_title = info['articles'][i]['title']
                output_url = info['articles'][i]['url']
                result = """ Find latest news here!!!
Author: {}
Title: {}
Link: {}""".format(output_author,output_title,output_url)
                dispatcher.utter_message(result)
        if result=="":
            news_not_found = "No news found :("
            dispatcher.utter_message(news_not_found)