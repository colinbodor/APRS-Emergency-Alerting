#!/usr/bin/python3
import pymysql, time, aprslib
from math import floor
import datetime

from config import *

def degrees_to_ddm(dd):
    degrees = int(floor(dd))
    minutes = (dd - degrees) * 60
    return (degrees, minutes)


def latitude_to_ddm(dd):
    direction = "S" if dd < 0 else "N"
    degrees, minutes = degrees_to_ddm(abs(dd))

    return "{0:02d}{1:05.2f}{2}".format(
        degrees,
        minutes,
        direction,
        )

def longitude_to_ddm(dd):
    direction = "W" if dd < 0 else "E"
    degrees, minutes = degrees_to_ddm(abs(dd))

    return "{0:03d}{1:05.2f}{2}".format(
        degrees,
        minutes,
        direction,
        )

# connect to MySQL
con = pymysql.connect(host = 'localhost',user = dbuser,passwd = dbpass,db = dbname)
cursor = con.cursor()

# a valid passcode for the callsign is required in order to send
AIS = aprslib.IS("VA6AEA", passwd="22179", port=14580, host="alberta.aprs2.net")
AIS.connect()

# get the current time in UTC and format for APRS
ztime = datetime.datetime.utcnow()
ztime = (ztime.strftime("%d%H%M"))




# qeury, construct and send af fire data to aprs.is
cursor.execute("SELECT * FROM abfire")
result = cursor.fetchall()

for row in result:
  name = (row[1])
  fire_number = (row[5])
  fire_location_latitude = latitude_to_ddm(row[9])
  fire_location_longitude = longitude_to_ddm(row[10])
  general_cause = (row[11])
  fire_status = (row[16])
  area_burned = (row[17])
  # replace some codes with human readable phrases
  fire_status = fire_status.replace("OC", "Out of Control")
  fire_status = fire_status.replace("BH", "Being Held")
  fire_status = fire_status.replace("UC", "Under Control")
  fire_status = fire_status.replace("TO", "Turned Over")

  # sleep 5 seconds so as to not slam APRS
  time.sleep(5)


  # send a single status message
  AIS.sendall("VA6AEA>ABFIRE,TCPIP*:;FR-"+fire_number+"*"+ztime+"z"+fire_location_latitude+"/"+fire_location_longitude+":"+name+", Status: ["+fire_status+"] Cause: ["+general_cause+"] Size: ["+area_burned+"ha]")


# qeury, construct and send af road data to aprs.is, only accidents for now
cursor.execute("SELECT * FROM `abroads` WHERE `eventtype` = 'accidentsAndIncidents'")
result = cursor.fetchall()

for row in result:
  abid = (row[1])
  roadwayname = (row[3])
  description = (row[5])
  latitude = latitude_to_ddm(row[11])
  longitude = longitude_to_ddm(row[12])

  # sleep 5 seconds so as to not slam APRS
  time.sleep(5)

  print(abid)
  # send a single status message
  AIS.sendall("VA6AEA>ABROAD,TCPIP*:;RD-"+roadwayname+"*"+ztime+"z"+latitude+"\\"+longitude+"'"+roadwayname+", Desc: ["+description+"]")



con.commit()
con.close()
