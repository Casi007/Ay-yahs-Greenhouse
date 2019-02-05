#!/usr/bin/env python
# encoding: utf-8

# greenhousestatuscronttsrfmodem.py
# Copyright (C) 2019 The Groundhog Whisperer
#
# requirements: wget, Ubuntu speech-dispatcher (spd-say), Desktop notification application (notify-send), general-purpose software audio FSK modem (minimodem)
#
# greenhousestatuscronttsrfmodem.py is a Python script that retrieves
# the latest greenhouse environmental data produced by
# /Greenhouse/greenhouse.py in CSV format using the wget
# application. greenhousestatuscronttsrfmodem.py produces text-to-speech
# using the Ubuntu speech-dispatcher containing the current
# greenhouse environmental status. The text-to-speech audio output
# can be connected to a radio in VOX (voice-operated exchange)
# mode allowing for radio frequency transmission of the current
# greenhouse environmental conditions. Before transmitting on any
# channel or frequency the channel should be monitored for at
# least 30 seconds to verify that the channel is clear/available.
# greenhousestatuscronttsrfmodem.py uses the cross-platform command line
# audio manipulation utility sox to achieve verification of the
# current channels availability. Sox is used to record a 60
# second sample of the current channel. Sox is then used to
# generate statistics from the audio recording to establish a
# maximum amplitude value. This maximum amplitude value is used
# to determine if the current broadcast should be deferred due
# to traffic on the channel or frequency. A maximum amplitude
# value > 0.025 is indicative of audio input/channel traffic.
# greenhousestatuscronttsrfmodem.py also produces a notification bubble
# in the desktop GUI using the notify-send application.
# greenhousestatuscronttsrfmodem also produces RTTY audio data
# using the minimodem application. This modem audio is saved as
# a .wav and then played using the sox play command to the 
# default audio output device. 
#
# Execute this script using a crontab
# example executed every 30th minute
# */30 * * * * eval "export $(egrep -z DBUS_SESSION_BUS_ADDRESS /proc/$(pgrep -u $LOGNAME gnome-session)/environ)"; python3 /home/usernamegreenhousealarm/greenhousestatuscronttsrfmodem.py
# The eval command specifies which display notify-send will use to display alerts.

import os
import subprocess
from subprocess import call
import time

# remote CSV file URL (e.g. http://192.168.1.118/index.csv)
REMOTE_FILE_PATH_URL = "http://localhost/index.csv"

# local copy of the remotely fetched greenhouse.csv file
LOCAL_CSV_FILE_NAME = "/home/username/index.csv"

# path and name of the temporary audio sample file
LOCAL_AUDIO_FILE_NAME_RECORDING = '/home/username/recording.wav'

# the maximum amplitude value returned by sox -stats to limit broadcasting on an active channel
MAXIMUM_AMPLITUDE_VALUE_LIMIT = .025

# length of audio sample used to calculate the maximum amplitude value in seconds
#SOX_TRIM_AUDIO_VALUE_STOP = '30'
SOX_TRIM_AUDIO_VALUE_STOP = '10'

# path and name of the temporary RTTY modem audio file
LOCAL_AUDIO_FILE_NAME_RTTY = '/home/username/broadcast.wav'

# path and name of the temporary text file containing the RTTY message content
LOCAL_TEMP_TEXT_FILE = '/home/username/temptext.txt'

# minimodem baud rate speed argument (e.g. 1200, 300, RTTY)
MINIMODEM_SPEED_ARGUMENT = "RTTY"

# execute the wget command to fetch and store the latest index.csv from the automation system
def fetch_csv_file_read_last_environmental_record():

    # define the variable line
    line = None

    wget_command_line = ["wget", "--tries=1","-N", "--no-if-modified-since", REMOTE_FILE_PATH_URL, "-O", LOCAL_CSV_FILE_NAME]
    wget_download_greenhouse_csv_data_run_process = subprocess.Popen(wget_command_line).communicate() 

    # try to read the local file do not die if the file does not exist
    try:
        with open(LOCAL_CSV_FILE_NAME, "r") as f:

            for line in f: pass
            last_line_csv_file = line

    except IOError:
        return 'error'

    if not last_line_csv_file or len(last_line_csv_file) < 1:
        # if the file read failed to read go back to sleep and try again
        exit()

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

    text_to_speech_message_content = '"Begin transmission: Greetings of peace and goodwill to all! This is N: O: C: A: L: L: November: Oscar: Charlie: Alpha: Lima: Lima:   The current greenhouse environmental status is as follows: Light dependent resistor at: %s volts, Temperature at: %s degrees, Humidity at: %s percent, Soil moisture sensor at: %s volts, Solenoid valve is: %s, Linear actuator is: %s, Output one is: %s, Output two is: %s, Output three is: %s, Seconds since the Unix slash Posix epoch: %s. November Oscar Charlie Alpha Lima Lima: End of transmission."' \
                                       % (current_luminosity_sensor_value, current_temperature, current_humidity,
                                          current_soil_moisture_sensor_value, current_solenoid_valve_status,
                                          current_actuator_extension_status, current_output_one_status, current_output_two_status,
                                          current_output_three_status, seconds_since_the_epoch)

    notify_send_message_content = '"Light Dependent Resistor: %s volts, Temperature: %s degrees, Humidity: %s percent, Soil moisture sensor: %s volts, Solenoid valve: %s, Linear actuator: %s, Output one: %s, Output two: %s, Output three: %s, Seconds since the Unix POSIX epoch: %s"' \
                                       % (current_luminosity_sensor_value, current_temperature, current_humidity,
                                          current_soil_moisture_sensor_value, current_solenoid_valve_status,
                                          current_actuator_extension_status, current_output_one_status, current_output_two_status,
                                          current_output_three_status, seconds_since_the_epoch)

    rtty_modem_message_content = '"de NOCALL November Oscar Charlie Alpha Lima Lima de NOCALL November Oscar Charlie Alpha Lima Lima de NOCALL November Oscar Charlie Alpha Lima Lima: Begin transmission: The current greenhouse environmental status is as follows: Light dependent resistor at: %s volts, Temperature at: %s degrees, Humidity at: %s percent, Soil moisture sensor at: %s volts, Solenoid valve is: %s, Linear actuator is: %s, Output one is: %s, Output two is: %s, Output three is: %s, Seconds since the Unix POSIX epoch: %s. de NOCALL November Oscar Charlie Alpha Lima Lima: End of transmission."' \
                                       % (current_luminosity_sensor_value, current_temperature, current_humidity,
                                          current_soil_moisture_sensor_value, current_solenoid_valve_status,
                                          current_actuator_extension_status, current_output_one_status, current_output_two_status,
                                          current_output_three_status, seconds_since_the_epoch)




    # call the subroutine to generate text-to-speech audio and a notify bubble
    audio_notification_text_to_speech(text_to_speech_message_content, notify_send_message_content, rtty_modem_message_content)


# call the desktop notification program and the speech-dispatcher for text-to-speech
def audio_notification_text_to_speech(text_to_speech_message_content, notify_send_message_content, rtty_modem_message_content):


    # record 60 seconds of audio using sox
    # use arecord command with -l or -L to locate values for the hw:#,# option
    # sox_record_audio_command = '/usr/bin/sox -b 32 -r 96000 -c 2 -t alsa hw:0,0 /home/usernamegreenhousettsrf/recording.wav trim 0 5'
    sox_command = '/usr/bin/sox'
    sox_bit_option = '-b'
    sox_bit_value = '32'
    sox_sample_rate_option = '-r'
    sox_sample_rate_value = '96000'
    sox_channels_audio_option = '-c'
    sox_channels_value = '2'
    sox_file_type_option = '-t'
    sox_file_type_value0 = 'alsa'
    sox_file_type_value1 = 'hw:0,0'
    sox_output_file_name = LOCAL_AUDIO_FILE_NAME_RECORDING
    sox_trim_audio_option = 'trim'
    sox_trim_audio_value_start = '0'


    record_process = subprocess.Popen([sox_command, sox_bit_option, sox_bit_value, sox_sample_rate_option, sox_sample_rate_value, sox_channels_audio_option, sox_channels_value, sox_file_type_option, sox_file_type_value0, sox_file_type_value1, sox_output_file_name, sox_trim_audio_option, sox_trim_audio_value_start, SOX_TRIM_AUDIO_VALUE_STOP])
    # sleep until sox has finished recording before calculating statistics on the audio data
    time.sleep(int(SOX_TRIM_AUDIO_VALUE_STOP) + 3)

    # use sox to calculate the maximum amplitude value
    # maximum amplitude value > 0.025 = audio detected 
    sox_calculate_midline_amplitude_command = "sox %s -n stat 2>&1" % LOCAL_AUDIO_FILE_NAME_RECORDING
    command_output = subprocess.getoutput([sox_calculate_midline_amplitude_command])

    maximum_amplitude_command_output_split_once = command_output.split(':')
    maximum_amplitude_command_output_split_twice = maximum_amplitude_command_output_split_once[4].split('\n')
    maximum_amplitude_command_output_split_twice = maximum_amplitude_command_output_split_twice[0]
    maximum_amplitude_value = float(maximum_amplitude_command_output_split_twice.replace(' ', ''))
    print('Maximum amplitude calculated at: %s' % str(maximum_amplitude_value))

    if maximum_amplitude_value is None:
        # display a bubble in the GUI
        notify_send_message_content = '"Broadcast deferred! Unable to estimate maximum amplitude from an audio sample of the current channel."' 
        notify_send_command_line = ['notify-send', 'Broadcast deferred!', notify_send_message_content]
        print("Exiting due to lack of sample data")
        # execute the process on the os
        notify_send_GUI_no_data_run_process = subprocess.Popen(notify_send_command_line)
        exit()

    if maximum_amplitude_value >= MAXIMUM_AMPLITUDE_VALUE_LIMIT:
        # display a bubble in the GUI
        notify_send_message_content = '"Broadcast deferred! Incoming transmission detected!"' 
        notify_send_command_line = ['notify-send', 'Broadcast deffered!', notify_send_message_content]
        print("Exiting due to channel traffic")
        # execute the process on the os
        notify_send_GUI_channel_traffic_run_process = subprocess.Popen(notify_send_command_line)
        exit()

    else:

        # display a bubble in the gui using notify-send just for fun
        # notify_send_command_line = ['notify-send', '--urgency=critical', 'Current Greenhouse Conditions', notify_send_message_content]
        notify_send_command_line = ['notify-send', 'Current Greenhouse Conditions', notify_send_message_content]
        # execute the process on the os
        notify_send_GUI_current_conditions_run_process = subprocess.Popen(notify_send_command_line)

        # generate the text-to-speech audio notification
        audio_notification_command_line = ['/usr/bin/spd-say', '--wait', text_to_speech_message_content]
        # execute the process on the os
        text_to_speech_current_conditions_run_process = subprocess.Popen(audio_notification_command_line).communicate()


        # write the RTTY message content to a text file sent to minimodem using cat
        file_handle = open(LOCAL_TEMP_TEXT_FILE, 'w') 
        file_handle.write(rtty_modem_message_content)
        file_handle.close()

        minimodem_command = "/usr/bin/minimodem"
        minimodem_read_write_argument = "--write"
        minimodem_file_argument = "-f"
        minimodem_command = "%s %s %s %s %s" % (minimodem_command, minimodem_read_write_argument, MINIMODEM_SPEED_ARGUMENT, minimodem_file_argument, LOCAL_AUDIO_FILE_NAME_RTTY)
        cat_command_binary = "/bin/cat"
        cat_content_text_file = LOCAL_TEMP_TEXT_FILE
        cat_command_redirect = "|"
        cat_command = "%s %s %s" % (cat_command_binary, cat_content_text_file, cat_command_redirect)
        minimodem_command_line = "%s %s" % (cat_command, minimodem_command)

        # execute the process on the os
        call(minimodem_command_line, shell=True)

        audio_notification_command_line = ['/usr/bin/play', LOCAL_AUDIO_FILE_NAME_RTTY]
        # execute the process on the os
        play_modem_rtty_file_current_conditions_run_process = subprocess.Popen(audio_notification_command_line)


# the main subroutine...
def main_subroutine():
    # call the subroutine to fetch the last recorded temperature
    # and then play the audio notification
    fetch_csv_file_read_last_environmental_record()

# call the main subroutine
main_subroutine()

