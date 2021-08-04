#!/usr/bin/python3
# APRS location data from aprs.fi
import aprslib, logging, json, requests, urllib.request, time, pymysql, time, os, psutil, threading
from datetime import datetime
from time import gmtime, strftime
from config import *

if debug == "yes":
  logging.basicConfig(level=logging.INFO)


def heartbeat():
  threading.Timer(60.0, heartbeat).start()
  now = datetime.utcnow()
  formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
  con = pymysql.connect(host = 'localhost',user = dbuser,passwd = dbpass,db = dbname)
  cursor = con.cursor()
  cursor.execute("""UPDATE heartbeat set datetime = %s WHERE task = %s""", (now, "listen.py"))
  con.commit()
  con.close()

heartbeat()



def callback(packet):
  try:
    if packet['format'] == 'message':
      replyto = (packet['from'])
      msgnum = (packet['msgNo'])
      now = datetime.now()
      formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')


      if packet['addresse'] == 'VA6AEA':
        response = 0
        # send an ack so they know we got the packet
        AIS.sendall("VA6AEA>APRS,TCPIP*,qAC,::"+replyto+" :ack"+msgnum+"")

        if "message_text" in packet:
          message = (packet['message_text'])
          # connect to MySQL
          con = pymysql.connect(host = 'localhost',user = dbuser,passwd = dbpass,db = dbname)
          cursor = con.cursor()
          cursor.execute("INSERT INTO aprs_log (timestamp, direction, callsign, message) VALUES (%s, 'inbound', %s, %s)", (formatted_date, replyto, message))
          con.commit()
          con.close()

          if message[0] == 'w' or message[0] == 'W' and len(message) <=1:
            aprsurl = "https://api.aprs.fi/api/get?name="+replyto+"&what=loc&apikey="+aprs_api_key+"&format=json"
            response = requests.get(aprsurl)
            aprsdata = json.loads(response.text)
            if aprsdata["found"] == 0:
              AIS.sendall("VA6AEA>APRS,TCPIP*,qAC,::"+replyto+" :Error: [No location data found]{"+msgnum+"")
              response = 1
            else:
              lat = aprsdata["entries"][0]["lat"]
              long = aprsdata["entries"][0]["lng"]
              wxurl = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, long, wx_api_key)
              response = requests.get(wxurl)
              wxdata = json.loads(response.text)
              currenttemp = str(wxdata["current"]["temp"])
              currenthumidity = str(wxdata["current"]["humidity"])
              currentpressure = str(wxdata["current"]["pressure"])

              AIS.sendall("VA6AEA>APRS,TCPIP*,qAC,::"+replyto+" :Current Temperature: ["+currenttemp+"C]{"+msgnum+"")
              AIS.sendall("VA6AEA>APRS,TCPIP*,qAC,::"+replyto+" :Current Humidity: ["+currenthumidity+"%]{"+msgnum+"")
              AIS.sendall("VA6AEA>APRS,TCPIP*,qAC,::"+replyto+" :Current Pressure: ["+currentpressure+"atm]{"+msgnum+"")
              response = 1

          if message[0] == 's' or message[0] == 'S' and len(message) <=1:
            pid = os.getpid()
            scriptpid = psutil.Process(pid)
            memusage = scriptpid.memory_info()[0]/2.**30
            memusage = str(round(memusage, 2))
            cpuusage = str(psutil.cpu_percent())
            uptime = (str(datetime.now() - datetime.fromtimestamp(psutil.boot_time())).split('.')[0])
            AIS.sendall("VA6AEA>APRS,TCPIP*,qAC,::"+replyto+" :Mem Usage: ["+memusage+"]GB{"+msgnum+"")
            AIS.sendall("VA6AEA>APRS,TCPIP*,qAC,::"+replyto+" :CPU Usage: ["+cpuusage+"]%{"+msgnum+"")
            AIS.sendall("VA6AEA>APRS,TCPIP*,qAC,::"+replyto+" :Uptime: ["+uptime+"]{"+msgnum+"")
            response = 1

          if message[0] == 't' or message[0] == 'T' and len(message) <=1:
            timezulu = ("Zulu: "+time.strftime("%a, %d %b %Y %H:%M:%S %p", time.gmtime()))
            timelocal = ("Local: "+strftime("%a, %d %b %Y %H:%M:%S %p"))
            AIS.sendall("VA6AEA>APRS,TCPIP*,qAC,::"+replyto+" :["+timelocal+"]{"+msgnum+"")
            AIS.sendall("VA6AEA>APRS,TCPIP*,qAC,::"+replyto+" :["+timezulu+"]{"+msgnum+"")
            response = 1

          # if nothing caught to do, send instructions back
          if response != 1:
            AIS.sendall("VA6AEA>APRS,TCPIP*,qAC,::"+replyto+" :Send:{"+msgnum+"")
            time.sleep(1)
            AIS.sendall("VA6AEA>APRS,TCPIP*,qAC,::"+replyto+" :w = weather{"+msgnum+"")
            AIS.sendall("VA6AEA>APRS,TCPIP*,qAC,::"+replyto+" :t = time{"+msgnum+"")
            AIS.sendall("VA6AEA>APRS,TCPIP*,qAC,::"+replyto+" :s = system{"+msgnum+"")
    else:
      print("received a packet without a format field / invalid?")
      print(packet)

  except:
    logging.exception('')

AIS = aprslib.IS(aprs_call, passwd=aprs_pass, port=aprs_port, host="rotate.aprs.net")
AIS.connect()
fetch = AIS.consumer(callback, lambda x: None, raw=False, immortal=True)
