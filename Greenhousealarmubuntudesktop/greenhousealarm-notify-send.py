#!/usr/bin/env python
# encoding: utf-8
#
######################################################################
## Application file name: greenhousealarm-notify-send.py			##
## Description: A component of Ay-yahs-Greenhouse Automation System ##
## Description: Performs alarm noitifications on an Ubuntu desktop	##
## Description: 													##
## Version: 1.03													##
## Project Repository: https://git.io/fhhsY							##
## Copyright (C) 2019 The Groundhog Whisperer						##
######################################################################
#
# A Python script that retrieves the latest
# greenhouse environmental data produced by /Greenhouse/greenhouse.py
# in CSV format using the wget application. greenhousealarm.py
# evaluates the last recorded temperature value and sounds an
# audible notification using the Ubuntu speech-dispatcher when
# the temperature value is not between the minimum and maximum
# threshold.

# note: the eval command specifies which display notify-send will use for alerts
# install using crontab
# $ crontab -e
# */2 * * * * eval "export $(egrep -z DBUS_SESSION_BUS_ADDRESS /proc/$(pgrep -u $LOGNAME gnome-session)/environ)"; python3 /home/username/greenhousealarm/greenhousealarm-notify-send.py


import os
import subprocess

# minimum temperature value to sound alarm
MINIMUM_TEMPERATURE_ALARM = 33

# maximum temperature value to sound alarm
MAXIMUM_TEMPERATURE_ALARM = 90

# local copy of the remotely fetched greenhouse.csv file
LOCAL_FILE_NAME = "index.csv"

# remote CSV file URL (e.g. http://192.168.1.118/index.csv)
REMOTE_FILE_PATH_URL = "http://192.168.0.104/index.csv"

# execute the wget command to fetch and store the latest index.csv from the automation system
def fetch_csv_file_read_last_temperature():

	wget_command_line = ["wget", "--tries=1","-N", "--no-if-modified-since", REMOTE_FILE_PATH_URL, "-O", LOCAL_FILE_NAME]
	p = subprocess.Popen(wget_command_line).communicate() 

	# try to read the local file do not die if the file does not exist
	try:
		with open(LOCAL_FILE_NAME, "r") as f:

			for line in f: pass
			last_line_csv_file = line

	except IOError:
		return 'error'
		
	# remove new line char
	last_line_csv_file = last_line_csv_file.replace('\n', '')

	# remove single quotes
	last_line_csv_file = last_line_csv_file.replace("'", "")

	# remove double quotes
	last_line_csv_file = last_line_csv_file.replace('"', '')

	# split at commas
	csv_values = last_line_csv_file.split(",")
	current_greenhouse_temperature = csv_values[1]
	current_greenhouse_temperature = int(float(current_greenhouse_temperature))
	# call the subroutine to evaluate alarm conditions
	compare_temperature_status_minimum_maximum(current_greenhouse_temperature)
	
# call the desktop notification program and the speech-dispatcher for text-to-speech
def audio_notification_text_to_speech(text_to_speech_message_content):

	audio_notification_command_line = ['spd-say', '--wait', text_to_speech_message_content]
	# execute the process on the os
	p = subprocess.Popen(audio_notification_command_line)

	# display a bubble in the gui using notify-send just for fun
	notify_send_command_line = ['notify-send', 'Attention!', text_to_speech_message_content]
	# execute the process on the os
	p = subprocess.Popen(notify_send_command_line)



# evaluate temperature alarm status
def compare_temperature_status_minimum_maximum(current_greenhouse_temperature):

	if (current_greenhouse_temperature < MINIMUM_TEMPERATURE_ALARM and current_greenhouse_temperature is not None):
			alarm_temperature_difference = MINIMUM_TEMPERATURE_ALARM - current_greenhouse_temperature
			text_to_speech_message_content = '"Attention! Attention! Attention! The current greenhouse temperature is: %d degrees. The current minimum temperature alarm is set at: %d degrees. That is a temperature difference of %d degrees. The current temperature is too low! The little plants will freeze!"' % (current_greenhouse_temperature, MINIMUM_TEMPERATURE_ALARM, alarm_temperature_difference)
			audio_notification_text_to_speech(text_to_speech_message_content)

	elif (current_greenhouse_temperature > MAXIMUM_TEMPERATURE_ALARM and current_greenhouse_temperature is not None):
			alarm_temperature_difference = current_greenhouse_temperature - MAXIMUM_TEMPERATURE_ALARM
			text_to_speech_message_content = '"Attention! Attention! Attention! The current greenhouse temperature is: %d degrees. The current maximum temperature alarm is set at: %d degrees. That is a temperature difference of %d degrees. The current temperature is too high! The little plants will wither!"' % (current_greenhouse_temperature, MAXIMUM_TEMPERATURE_ALARM, alarm_temperature_difference)
			audio_notification_text_to_speech(text_to_speech_message_content)

# call the subroutine to fetch the last recorded temperature
# and then evaluate if an audible alarm notification is needed
fetch_csv_file_read_last_temperature()




