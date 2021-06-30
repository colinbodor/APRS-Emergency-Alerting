#!/usr/bin/python3
# APRS location data from aprs.fi
import aprslib, logging, json, requests, urllib.request, time

api_key = "40dc6eb10f2a37fd90a8def196fcce21"


def callback(packet):
#    if packet['from'] == 'VA6CCB-4':
    replyto = (packet['from'])
    msgnum = (packet['msgNo'])
    print("doing something")
    # send the ack
    AIS.sendall("VA6AEA>APRS,TCPIP*,qAC,::"+replyto+" :ack"+msgnum+"")
#    AIS.sendall("VA6AEA>APRS,TCPIP*,qAC,::"+replyto+" :.-.{"+msgnum+"")

    if "message_text" in packet:
      message = (packet['message_text'])
      if message == 'w' or message == 'W':
        aprsurl = "https://api.aprs.fi/api/get?name="+replyto+"&what=loc&apikey=130248.v9zhPCxvmn45P&format=json"
        response = requests.get(aprsurl)
        aprsdata = json.loads(response.text)
        if aprsdata["found"] == 0:
          AIS.sendall("VA6AEA>APRS,TCPIP*,qAC,::"+replyto+" :No LOC Data{"+msgnum+"")
        else:
          lat = aprsdata["entries"][0]["lat"]
          long = aprsdata["entries"][0]["lng"]
          wxurl = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, long, api_key)
          response = requests.get(wxurl)
          wxdata = json.loads(response.text)
          current = wxdata["current"]["temp"]
          current = str(current)
          AIS.sendall("VA6AEA>APRS,TCPIP*,qAC,::"+replyto+" :"+current+"C{"+msgnum+"")


#logging.basicConfig(level=logging.DEBUG) # level=10

AIS = aprslib.IS("VA6AEA", passwd="22179", port=14580, host="alberta.aprs2.net")
AIS.connect()
fetch = AIS.consumer(callback, lambda x: None, raw=False)
