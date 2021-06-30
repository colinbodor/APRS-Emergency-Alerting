#!/usr/bin/python3
import requests, json, urllib.request, datetime

api_key = "40dc6eb10f2a37fd90a8def196fcce21"


#lat = "48.208176"
#lon = "16.373819"



aprsurl = "https://api.aprs.fi/api/get?name=VE6OH&what=loc&apikey=130248.v9zhPCxvmn45P&format=json"

response = requests.get(aprsurl)
aprsdata = json.loads(response.text)
if aprsdata["found"] == 0:
  print("not found")
#print(aprsdata)

#lat = aprsdata["entries"][0]["lat"]
#long = aprsdata["entries"][0]["lng"]


#wxurl = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, long, api_key)

#response = requests.get(wxurl)
#wxdata = json.loads(response.text)

#current = wxdata["current"]["temp"]
#print(current)


