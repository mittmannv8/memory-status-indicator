#!/bin/bash

function uninstall {
	APP_FOLDER="/usr/lib/memory_status_indicator"
	CONF_FILE="~/.config/memory_status_indicator.conf"
	LAUNCHER="~/.config/autostart/memory_status_indicator.desktop"
	
	if [ -e /tmp/memory_status_indicator.pid ]
	then
	    PID=`cat /tmp/memory_status_indicator.pid`
	fi
	
	if [ -d $APP_FOLDER ]
	then
		rm -fr $APP_FOLDER > /dev/null
	fi
	if [ -e $CONF_FILE ]
	then
		rm $CONF_FILE > /dev/null
	fi
	if [ -e $LAUNCHER ]
	then
		rm  > /dev/null
	fi
	
	kill -9 $PID
	
	echo "Memory Status Indicator uninstalled successful"
	exit
}

while :
do
	read -p "You really would like to proceed? (y/n)" -n1 CONTINUE
	echo
	case "$CONTINUE" in
		y) uninstall;;
		n) break 2;; 
		*) echo "Please, press y for YES or n for NO";;
	esac
done
	