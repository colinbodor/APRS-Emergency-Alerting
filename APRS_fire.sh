#!/bin/bash

# APRS Emergency Alert
# Jared Miconi & Colin Bodor

#Data source
#https://wildfire.alberta.ca/reports/activedd.csv


APRS_CALL="VA6AEA"
APRS_PASS="22179"
APRS_SERVER="alberta.aprs2.net"

APRS_PORT="14580"
Counter="0"


#Collects the data and preps it for parsing
cd /opt/APRS
wget https://wildfire.alberta.ca/reports/activedd.csv

#removes the title line from the CSV file
sed -i '1d' activedd.csv




INPUT=activedd.csv
OLDIFS=$IFS
IFS=,
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }

while read name yesterday_datetime location description fire_number year fire_num_yr assessment_datetime fire_location_latitude fire_location_longitude general_cause cr_id id id percent_contained fire_status area_burned no_of_wfu no_of_manpower no_of_ag no_of_aircraft no_of_equipment no_of_ac_rw_light no_of_ac_rw_medium no_of_ac_rw_inter no_of_veq_truck no_of_veq_truck_wt no_of_veq_skidder no_of_veq_bus no_of_veq_dozer no_of_fl_eq_pump cr_group_name report_creation_date eco_zone_flag modified_action_flag web_general_cause fire_type group_type group_sort_1 fire_complex_number fire_complex_name fire_complex_year

do

	#Extracts, coverts & formats the LAT/Long into DMS as per APRS requirnments.

	LatD=${fire_location_latitude%%.*}
	LatM="$(echo "$fire_location_latitude-$LatD" | bc)"
	LatM="$(echo "$LatM*60" | bc)"
	LatS=$LatM
	LatM=${LatM%%.*}
	LatS="$(echo "$LatS-$LatM" | bc)"
	LatS="$(echo "$LatS*60" | bc)"
	LatS=${LatS%%.*}

	LONGITUDE="$(echo "$fire_location_longitude*-1" | bc)"
	LongD=${LONGITUDE%%.*}
	LongM="$(echo "$LONGITUDE-$LongD" | bc)"
	LongM="$(echo "$LongM*60" | bc)"
	LongS=$LongM
	LongM=${LongM%%.*}
	printf -v LongM "%02d" $LongM
	LongS="$(echo "$LongS-$LongM" | bc)"
	LongS="$(echo "$LongS*60" | bc)"
	LongS=${LongS%%.*}
	printf -v LongS "%02d" $LongS

	if [ $fire_status == "OC" ];
	then
	  fire_status="Out of Control"
	fi

	if [ $fire_status == "BH" ];
	then
	  fire_status="Being Held"
	fi

	if [ $fire_status == "UC" ];
	then
	  fire_status="Under Control"
	fi

	if [ $fire_status == "TO" ];
	then
	  fire_status="Turned Over"
	fi


	#Plugs the extracted information into the APRS update variables.
	OBJ_NAME="FR-$fire_number"
	OBJ_LAT="$LatD$LatM.$LatS""N"
	OBJ_LONG="$LongD$LongM.$LongS""W"
	OBJ_OVERLAY="/"
	OBJ_SYMBOL=":"
	OBJ_COMMENT="$name, Status: [$fire_status] Cause: [$general_cause] Size: [$area_burned ha]"

	# Dither beaconing to not slam APRS network on the top of the interval
	sleep 20

	# Generate Beacon text and inject into APRS-IS backbone
	TIMESTAMP="`date -u +%d%H%M`z"
	OBJ_STRING=";${OBJ_NAME}*${TIMESTAMP}${OBJ_LAT}${OBJ_OVERLAY}${OBJ_LONG}${OBJ_SYMBOL}${OBJ_COMMENT}"

	BEACON_LOGIN="user ${APRS_CALL} pass ${APRS_PASS}"
	BEACON_TEXT="${APRS_CALL}>ABFIRE,TCPIP*:${OBJ_STRING}"

	printf "%s\n" "user VA6AEA pass 22179" "${BEACON_TEXT}" | ncat $APRS_SERVER $APRS_PORT

	echo "${BEACON_TEXT}"

	Counter="$(echo "$Counter+1" | bc)"




done < $INPUT
IFS=$OLDIFS

rm activedd.csv

#Would be nice to echo into a log file some stats like how many fires present etc from here down....
echo "There are $Counter active fires in Alberta presently...   :'("

echo "`date +%T`,`date +%d`,`date +%m`,`date +%Y`,$Counter" >> log.txt

