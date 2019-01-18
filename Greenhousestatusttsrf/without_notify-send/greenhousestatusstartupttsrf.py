#!/usr/bin/env python
# encoding: utf-8

# greenhousestatusstartupttsrf.py
# Copyright (C) 2019 The Groundhog Whisperer
# greenhousestatusstartupttsrf.py is a Python script that retrieves
# the latest greenhouse environmental data produced by
# /Greenhouse/greenhouse.py in CSV format using the wget
# application. greenhousestatusstartupttsrf.py produces text-to-speech
# using the Ubuntu speech-dispatcher containing the current
# greenhouse environmental status. The text-to-speech audio output
# can be connected to a radio in VOX (voice-operated exchange)
# mode allowing for radio frequency transmission of the current
# greenhouse environmental conditions.
#
# Execute this script once using the Ubuntu Startup Applications
# GUI. This script runs in an infinite loop.

import os
import subprocess
import time

# local copy of the remotely fetched greenhouse.csv file
LOCAL_FILE_NAME = "/home/username/greenhousealarm/index.csv"

# remote CSV file URL (e.g. http://192.168.1.118/index.csv)
REMOTE_FILE_PATH_URL = "http://localhost/index.csv"

# time in seconds between notifications
TIME_BETWEEN_NOTIFICATIONS = 10  # ten minutes
#TIME_BETWEEN_NOTIFICATIONS = 3600  # one hour
#TIME_BETWEEN_NOTIFICATIONS = 7200  # two hour
#TIME_BETWEEN_NOTIFICATIONS = 14400 # four hours
#TIME_BETWEEN_NOTIFICATIONS = 21600 # six hours
#TIME_BETWEEN_NOTIFICATIONS = 28800 # eight hours
#TIME_BETWEEN_NOTIFICATIONS = 43200 # twelve hours

# execute the wget command to fetch and store the latest index.csv from the automation system
def fetch_csv_file_read_last_environmental_record():

    # define the variable line
    line = None

    wget_command_line = ["wget", "--tries=1","-N", "--no-if-modified-since", REMOTE_FILE_PATH_URL, "-O", LOCAL_FILE_NAME]
    p = subprocess.Popen(wget_command_line).communicate() 
    print("attempting fetch")

    # try to read the local file do not die if the file does not exist
    try:
        with open(LOCAL_FILE_NAME, "r") as f:

            for line in f: pass
            last_line_csv_file = line

    except IOError:
        return 'error'

    if not last_line_csv_file or len(last_line_csv_file) < 1:
        # if the file read failed to read go back to sleep and try again
        main_subroutine()
    print(last_line_csv_file)

    # remove new line char
    last_line_csv_file = last_line_csv_file.replace('\n', '')

    # remove single quotes
    last_line_csv_file = last_line_csv_file.replace("'", "")

    # remove double quotes
    last_line_csv_file = last_line_csv_file.replace('"', '')

    # split at commas
    csv_values = last_line_csv_file.split(",")

    current_luminosity_sensor_value = csv_values[0]
    current_temperature = csv_values[1]
    current_humidity = csv_values[2]
    current_soil_moisture_sensor_value = csv_values[3]
    current_solenoid_valve_status = csv_values[4]
    current_actuator_extension_status = csv_values[5]
    current_output_one_status = csv_values[6]
    current_output_two_status = csv_values[7]
    current_output_three_status = csv_values[8]
    seconds_since_the_epoch = csv_values[9]

    text_to_speech_message_content = '"Begin transmission: Greetings of peace and goodwill to all! This is N: O: C: A: L: L: November: Oscar: Charlie: Alpha: Lima: Lima:   The current greenhouse environmental status is as follows: Light dependent resistor at: %s volts, Temperature at: %s degrees, Humidity at: %s percent, Soil moisture sensor at: %s volts, Solenoid valve is: %s, Linear actuator is: %s, Output one is: %s, Output two is: %s, Output three is: %s, Seconds since the epoch: %s. November Oscar Charlie Alpha Lima Lima: End of transmission."' \
                                       % (current_luminosity_sensor_value, current_temperature, current_humidity,
                                          current_soil_moisture_sensor_value, current_solenoid_valve_status,
                                          current_actuator_extension_status, current_output_one_status, current_output_two_status,
                                          current_output_three_status, seconds_since_the_epoch)

    # call the subroutine to generate text-to-speech audio and a notify bubble
    audio_notification_text_to_speech(text_to_speech_message_content)


# call the speech-dispatcher for text-to-speech
def audio_notification_text_to_speech(text_to_speech_message_content):

    audio_notification_command_line = ['spd-say', '--wait', text_to_speech_message_content]
    # execute the process on the os
    p = subprocess.Popen(audio_notification_command_line)

    # call the main subroutine again and sleep
    main_subroutine()


# the main subroutine...
def main_subroutine():
    # call the subroutine to fetch the last recorded temperature
    # and then play the audio notification
    time.sleep(TIME_BETWEEN_NOTIFICATIONS)
    fetch_csv_file_read_last_environmental_record()

# call the main subroutine
main_subroutine()

