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


# a valid passcode for the callsign is required in order to send
AIS = aprslib.IS(aprs_call, passwd=aprs_pass, port=aprs_port, host=aprs_server)
AIS.connect()

# get the current time in UTC and format for APRS
ztime = datetime.datetime.utcnow()
ztime = (ztime.strftime("%d%H%M"))




# qeury, construct and send af fire data to aprs.is for alberta
con = pymysql.connect(host = 'localhost',user = dbuser,passwd = dbpass,db = dbname)
cursor = con.cursor()
cursor.execute("SELECT * FROM abfire")
result = cursor.fetchall()
con.commit()
con.close()

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
  AIS.sendall("VA6AEA>ABFIRE,TCPIP*:;FR-"+fire_number+"*"+ztime+"z"+fire_location_latitude+"/"+fire_location_longitude+":"+name+", Status: ["+fire_status+"] Cause: ["+general_cause+"] Size: ["+area_burned+"ha] hazardscape.ca")






# qeury, construct and send af road data to aprs.is, only accidents for now
con = pymysql.connect(host = 'localhost',user = dbuser,passwd = dbpass,db = dbname)
cursor = con.cursor()
cursor.execute("SELECT * FROM `abroads` WHERE `eventtype` = 'accidentsAndIncidents'")
result = cursor.fetchall()
con.commit()
con.close()

for row in result:
  abid = (row[1])
  # padd the object name to make it 9 characters, APRS expects object names to be 9 characters only, do some other formatting
  abid = abid.strip()
  abid = abid.replace("-", "")
  abid = abid.ljust(9, ' ')
  roadwayname = (row[3])
  description = (row[5])
  latitude = latitude_to_ddm(row[11])
  longitude = longitude_to_ddm(row[12])

  # sleep 10 seconds so as to not slam APRS, or trigger "location changes too fast"
  time.sleep(10)

  # send a single status message
  AIS.sendall("VA6AEA>ABROAD,TCPIP*:;"+abid+"*"+ztime+"z"+latitude+"A"+longitude+"'"+roadwayname+", Desc: ["+description+"] hazardscape.ca")




# qeury, construct and send af fire data to aprs.is for sask
con = pymysql.connect(host = 'localhost',user = dbuser,passwd = dbpass,db = dbname)
cursor = con.cursor()
cursor.execute("SELECT * FROM `fedfire` WHERE `agency` = 'SK' ")
result = cursor.fetchall()
con.commit()
con.close()

for row in result:
  firename = (row[2]).strip()
  aprs_firename = firename
  aprs_firename = aprs_firename.replace("-", "")
  aprs_firename = aprs_firename[2:8]
  aprs_firename = aprs_firename.ljust(6, ' ')

  lat = latitude_to_ddm(row[3]).strip()
  lon = longitude_to_ddm(row[4]).strip()
  stage_of_control = (row[7]).strip()
  hectares = (row[6]).strip()
  # replace some codes with human readable phrases
  stage_of_control = stage_of_control.replace("OC", "Out of Control")
  stage_of_control = stage_of_control.replace("BH", "Being Held")
  stage_of_control = stage_of_control.replace("UC", "Under Control")
  stage_of_control = stage_of_control.replace("TO", "Turned Over")

  # sleep 5 seconds so as to not slam APRS
  time.sleep(5)

  # send a single status message
  AIS.sendall("VA6AEA>SKFIRE,TCPIP*:;FR-"+aprs_firename+"*"+ztime+"z"+lat+"/"+lon+":"+firename+", Status: ["+stage_of_control+"] Size: ["+hectares+"ha] hazardscape.ca")

