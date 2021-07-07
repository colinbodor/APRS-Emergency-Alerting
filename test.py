#!/usr/bin/python3
import requests, json, urllib.request, datetime, psutil, feedparser

#api_key = "40dc6eb10f2a37fd90a8def196fcce21"


#lat = "48.208176"
#lon = "16.373819"



#aprsurl = "https://api.aprs.fi/api/get?name=VA6CCB-4&what=loc&apikey=130248.v9zhPCxvmn45P&format=json"

#response = requests.get(aprsurl)
#aprsdata = json.loads(response.text)
#if aprsdata["found"] == 0:
#  print("not found")
#print(aprsdata)


#from time import gmtime, strftime, now
#import time
#print("\nGMT: "+time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
#print("Local: "+strftime("%a, %d %b %Y %I:%M:%S %p %Z\n"))


#uptime = (str(datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())).split('.')[0])
#print(uptime)

#lat = aprsdata["entries"][0]["lat"]
#long = aprsdata["entries"][0]["lng"]


#wxurl = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, long, api_key)

#response = requests.get(wxurl)
#wxdata = json.loads(response.text)

#current = wxdata["current"]["temp"]
#print(current)



#d = feedparser.parse('http://rss1.naad-adna.pelmorex.com/')
#print(d['feed']['title'])
#print(d['feed']['link'])
#print(len(d['entries']))

#for post in d.entries:
#    print(post.title + ": " + post.link)

# To test it with netcat, start the script and execute:
# 
#    echo "Hello, cat." | ncat.exe 127.0.0.1 12345
#
import socket

HOST = 'rss1.naad-adna.pelmorex.com'   # use '' to expose to all networks
PORT = 80

def incoming(host, port):
  """Open specified port and return file-like object"""
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # set SOL_SOCKET.SO_REUSEADDR=1 to reuse the socket if
  # needed later without waiting for timeout (after it is
  # closed, for example)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  sock.bind((host, port))
  sock.listen(0)   # do not queue connections
  request, addr = sock.accept()
  return request.makefile('r', 0)
# /-- network ---


for line in incoming(HOST, PORT):
  print(line)
