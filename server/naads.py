#!/usr/bin/python3
import socket, lxml, time, sys, pymysql, pytz
from datetime import datetime
from time import gmtime, strftime
from bs4 import BeautifulSoup as soup
import colorama
from colorama import Fore, Style, init
from os import system, name


from config import *





def clear():
  if name == 'nt':
    _ = system('cls')
  else:
    _ = system('clear')

clear()












init(autoreset=True)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('streaming1.naad-adna.pelmorex.com',8080))



delimiter = "</alert>"
buffer = ""

while True:
    received = s.recv(1024).decode("utf-8", "ignore")
    buffer += received
    if buffer.endswith(delimiter):
        try:
          timezulu = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

          bs_content = soup(buffer, "xml")

          #get identifier and sender first as thats how we relate raw xml, and geolocation tables to the meta information
          identifier = bs_content.find('identifier').get_text()
          sender = bs_content.find('sender').get_text()

          #dump entire raw xml message into the database in case we need it later, but not for heartbeat messages, as we dont care to save those
          if sender != "NAADS-Heartbeat":
            con = pymysql.connect(host = 'localhost',user = dbuser,passwd = dbpass,db = dbname)
            cursor = con.cursor()
            cursor.execute("INSERT INTO naads_xml (identifier, xml) VALUES (%s, %s)", (identifier, bs_content))
            con.commit()
            con.close()


          #start alert header information
          sent = bs_content.find('sent').get_text()
          sent = sent[:-6]
          sent = sent.replace("T", " ")
          status = bs_content.find('status').get_text()

          try:
            msgtype = bs_content.find('msgtype').get_text()
          except:
            msgtype = bs_content.find('msgType').get_text()
          else: msgtype = "no msgtype"

          try:
            source = bs_content.find('source').get_text()
          except:
            source = "no source"

          try:
            scope = bs_content.find('scope').get_text()
          except:
            scope = "no scope"
          #end alert header information




          #no broastcast test messages are sometimes received, there are also broadcast test messages not caught by the below if statement
          if status == "Test":
             print(Fore.YELLOW +identifier+" - Test Message (NO BROADCAST) received from "+sender+" at "+timezulu+" GMT and was sent at "+sent+" GMT -- mark --")
          else:

            if sender == "NAADS-Heartbeat":
              print(Fore.RED + "Heartbeat received from "+source+" at "+timezulu+" GMT and was sent at "+sent+" GMT -- mark --")
              con = pymysql.connect(host = 'localhost',user = dbuser,passwd = dbpass,db = dbname)
              cursor = con.cursor()
              cursor.execute("""UPDATE heartbeat set datetime = %s WHERE task = %s""", (timezulu, "naads.py"))
              con.commit()
              con.close()
            else:


              #this is the main loop through the <info> tags. Splits english and french into separate alerts
              result = bs_content.find_all('info')
              for row in result:

                print("***********************************************************************************************************************************************")
                print(Fore.YELLOW + "Alert received from: "+sender+" sent: "+timezulu+" status: "+status+" msgtype: "+msgtype+" scope: "+scope+" -- mark -- ")
                language = row.find('language').get_text()
                category = row.find('category').get_text()
                event = row.find('event').get_text()




                try:
                  responsetype = row.find('responseType').get_text()
                except:
                  responsetype = "no responseType"



                urgency = row.find('urgency').get_text()

                if urgency == "Past" or urgency == "past":
                  print(Fore.BLUE + "Past urgency found, should these be marked?")

                severity = row.find('severity').get_text()
                certainty = row.find('certainty').get_text()


                try:
                  audience = row.find('audience').get_text()
                except:
                  audience = "no audience"

                try:
                  effective = row.find('effective').get_text()
                  effective = effective[:-6]
                  effective = effective.replace("T", " ")
                except:
                  timezulu = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                  effective = timezulu
                  print(Fore.BLUE + "No effective time? check database.")

                expires = row.find('expires').get_text()
                expires = expires[:-6]
                expires = expires.replace("T", " ")

                sendername = row.find('senderName').get_text()
                headline = row.find('headline').get_text()

                try:
                  description = row.find('description').get_text()
                except:
                  description = "no description"

                try:
                  instruction = row.find('instruction').get_text()
                except:
                  instruction = "no instruction"

                #this loops through all the <area> sections, sometimes many and puts them in separate table linked with the identifier
                result = row.find_all('area')
                for row in result:
                  polygon = row.find('polygon').get_text()
                  #print(polygon)

                  try:
                    areadesc = row.find('areadesc').get_text()
                    #print(areadesc)
                  except:
                    areadesc = row.find('areaDesc').get_text()
                    #print(areadesc)

                  result = row.find_all('geocode')
                  for row in result:
                    if row.find('valueName').get_text() == "layer:EC-MSC-SMC:1.0:CLC":
                      clc = row.find('value').get_text()
                    if row.find('valueName').get_text() == "profile:CAP-CP:Location:0.3":
                      capcp_loc = row.find('value').get_text()



                  con = pymysql.connect(host = 'localhost',user = dbuser,passwd = dbpass,db = dbname)
                  cursor = con.cursor()
                  cursor.execute("INSERT INTO naads_area (identifier, language, areadesc, polygon, clc, capcp_loc) VALUES (%s, %s, %s, %s, %s, %s)", (identifier, language, areadesc, polygon, clc, capcp_loc))
                  con.commit()
                  con.close()

                local_timezone = pytz.timezone('America/Edmonton')
                effective = datetime.fromisoformat(effective)
                expires = datetime.fromisoformat(expires)
                effective_local = str(effective.astimezone(local_timezone))
                expires_local = str(expires.astimezone(local_timezone))
                effective = str(effective)
                expires = str(expires)

                print(Fore.MAGENTA + "Sender Name: " + sendername)
                print(Fore.GREEN + "Headline: " + headline)
                print("Identifier: "+identifier)
                print("Language: "+language)
                print("Category: "+category)
                print("Event: "+event)
                print("Urgency: "+urgency)
                print("Severity: "+severity)
                print("Certainty: "+certainty)
                print("Zulu Effective: "+effective+" / Expires: "+expires)
                print("Local Effective: "+effective_local+" / Expires: "+expires_local)
                print("***********************************************************************************************************************************************")
                print("\n")

                con = pymysql.connect(host = 'localhost',user = dbuser,passwd = dbpass,db = dbname)
                cursor = con.cursor()
                cursor.execute("INSERT INTO naads (identifier, language, category, event, responsetype, urgency, severity, certainty, audience, sendername, headline, effective_gmt, expires_gmt, description, instruction) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (identifier, language, category, event, responsetype, urgency, severity, certainty, audience, sendername, headline, effective, expires, description, instruction))
                con.commit()
                con.close()



        except:
          print("failed parsing")
          raise
        buffer = ""

