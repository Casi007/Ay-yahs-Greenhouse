#!/usr/bin/env python3
# encoding: utf-8
#
######################################################################
## Application file name: greenhousegtkcontrol.py		    ##
## Description: A component of Ay-yahs-Greenhouse Automation System ##
## Description: Graphical desktop user interface for greenhouse	    ##
## Description: monitoring and configuration interface application  ##
## Version: 1.03						    ##
## Project Repository: https://git.io/fhhsY			    ##
## Copyright (C) 2019 The Groundhog Whisperer			    ##
######################################################################
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# This is a for-fun project created for the purpose of automating climate
# control and irrigation in a small greenhouse.

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Pango
import time
import requests
import sqlite3
#import sys

# Name of the Sqlite3 database file
SQLITE_DATABASE_FILE = 'greenhouse.db'

# Name of the table to be queried
DATABASE_TABLE_NAME = 'greenhouse'

# Number of historic environmental data rows to display in the history window =< 1500
LIMIT_NUMBER_ROWS_DISPLAYED = '1000'

# text file containing the remote host IP address for the GreenhousePi
IP_GREENHOUSE_PI_FILE_NAME = 'greenhouseip.txt'

# Timeout in seconds before 'requests' fails to fetch the remote URL 
# (e.g. Downloading a file or performing a manual greenhouse operation).
# If this value is less than the linear actuator runtime value this operation
# will timeout before completion while waiting on the linear actuator to
# retract or extend.
URL_FETCH_TIMEOUT_SECONDS = 3

# Create the main GUI window class
class MyWindow(Gtk.Window):
	
	def __init__(self):

		print ("Ready to perform manual operations.")

		# Set the window title
		Gtk.Window.__init__(self, title="Ay-yah's Greenhouse Desktop Interface")

		# Set the window size
		self.set_size_request(400, 300)
		self.set_border_width(10)
		self.move(900, 100)
		# Create a a vertical container box 
		self.box = Gtk.VBox(spacing=0)
		self.add(self.box)
		
		# Construct a Gtk image object
		img = Gtk.Image()
		# Set the image data from the contents of a file
		img.set_from_file("greenhouselow.gif")
		# Make the object visible
		img.show()
		# Add the image to the window
		self.box.pack_start(img, True, True, 10)

		# Create some labels and add the current environmental values below the image in the main window
		label_current_luminosity_sensor_value = Gtk.Label()
		label_current_luminosity_sensor_value.set_text('Luminosity: ' + str(current_luminosity_sensor_value) + 'V')
		label_current_luminosity_sensor_value.set_justify(Gtk.Justification.LEFT)
		self.box.pack_start(label_current_luminosity_sensor_value, True, True, 0)

		label_current_temperature = Gtk.Label()
		label_current_temperature.set_text('Temperature: ' + str(current_temperature) + 'F')
		label_current_temperature.set_justify(Gtk.Justification.LEFT)
		self.box.pack_start(label_current_temperature, True, True, 0)

		label_current_humidity = Gtk.Label()
		label_current_humidity.set_text('Humidity: ' + str(current_humidity) + '%')
		label_current_humidity.set_justify(Gtk.Justification.LEFT)
		self.box.pack_start(label_current_humidity, True, True, 0)

		label_current_soil_moisture_sensor_value = Gtk.Label()
		label_current_soil_moisture_sensor_value.set_text('Soil Moisture: ' + str(current_soil_moisture_sensor_value) + 'V')
		label_current_soil_moisture_sensor_value.set_justify(Gtk.Justification.LEFT)
		self.box.pack_start(label_current_soil_moisture_sensor_value, True, True, 0)

		label_current_solenoid_valve_status = Gtk.Label()
		label_current_solenoid_valve_status.set_text('Solenoid Valve: ' + str(current_solenoid_valve_status))
		label_current_solenoid_valve_status.set_justify(Gtk.Justification.LEFT)
		self.box.pack_start(label_current_solenoid_valve_status, True, True, 0)

		label_current_actuator_extension_status = Gtk.Label()
		label_current_actuator_extension_status.set_text('Actuator: ' + str(current_actuator_extension_status))
		label_current_actuator_extension_status.set_justify(Gtk.Justification.LEFT)
		self.box.pack_start(label_current_actuator_extension_status, True, True, 0)

		label_current_output_one_status = Gtk.Label()
		label_current_output_one_status.set_text('Output One: ' + str(current_output_one_status))
		label_current_output_one_status.set_justify(Gtk.Justification.LEFT)
		self.box.pack_start(label_current_output_one_status, True, True, 0)

		label_current_output_two_status = Gtk.Label()
		label_current_output_two_status.set_text('Output Two: ' + str(current_output_two_status))
		label_current_output_two_status.set_justify(Gtk.Justification.LEFT)
		self.box.pack_start(label_current_output_two_status, True, True, 0)

		label_current_output_three_status = Gtk.Label()
		label_current_output_three_status.set_text('Output Three: ' + str(current_output_three_status))
		label_current_output_three_status.set_justify(Gtk.Justification.LEFT)
		self.box.pack_start(label_current_output_three_status, True, True, 0)

		label_current_time_readable = Gtk.Label()
		label_current_time_readable.set_text('Timestamp: ' + record_time + ' ' + record_date)
		label_current_time_readable.set_justify(Gtk.Justification.LEFT)
		self.box.pack_start(label_current_time_readable, True, True, 0)
	
		label = Gtk.Label("Please select a manual operation to perform")
		self.box.pack_start(label, True, True, 10)
	
		# Add the manual operations buttons
		self.button0 = Gtk.Button(label="Fan On (Output One On)")
		self.button0.connect("clicked", self.on_button0_clicked)
		self.box.pack_start(self.button0, True, True, 1)

		self.button1 = Gtk.Button(label="Fan Off (Output One Off)")
		self.button1.connect("clicked", self.on_button1_clicked)
		self.box.pack_start(self.button1, True, True, 1)

		self.button2 = Gtk.Button(label="Light On (Output Two On)")
		self.button2.connect("clicked", self.on_button2_clicked)
		self.box.pack_start(self.button2, True, True, 1)

		self.button3 = Gtk.Button(label="Light Off (Output Two Off)")
		self.button3.connect("clicked", self.on_button3_clicked)
		self.box.pack_start(self.button3, True, True, 1)

		self.button4 = Gtk.Button(label="Unused (Output Three On)")
		self.button4.connect("clicked", self.on_button4_clicked)
		self.box.pack_start(self.button4, True, True, 1)

		self.button5 = Gtk.Button(label="Unused (Output Three Off)")
		self.button5.connect("clicked", self.on_button5_clicked)
		self.box.pack_start(self.button5, True, True, 1)

		self.button6 = Gtk.Button(label="Open Solenoid Valve")
		self.button6.connect("clicked", self.on_button6_clicked)
		self.box.pack_start(self.button6, True, True, 1)

		self.button7 = Gtk.Button(label="Close Solenoid Valve")
		self.button7.connect("clicked", self.on_button7_clicked)
		self.box.pack_start(self.button7, True, True, 1)

		self.button8 = Gtk.Button(label="Open Window (Extend Actuator)")
		self.button8.connect("clicked", self.on_button8_clicked)
		self.box.pack_start(self.button8, True, True, 1)

		self.button9 = Gtk.Button(label="Close Window (Retract Actuator)")
		self.button9.connect("clicked", self.on_button9_clicked)
		self.box.pack_start(self.button9, True, True, 1)

		# Add some link buttons to the bottom of the main window
		# Linkbutton pointing to the given URI
		button_url0 = Gtk.LinkButton(uri="http://{}".format(IP_GREENHOUSE_PI))
		button_url0.set_label("GreenhousePi Homepage")

		# Add the button to the window
		self.box.pack_start(button_url0, True, True, 0)

		# Linkbutton pointing to the given URI
		button_url1 = Gtk.LinkButton(uri="http://{}/greenhouse.db".format(IP_GREENHOUSE_PI))
		button_url1.set_label("Download historic data .DB (SQLite3)")

		# Add the button to the window
		self.box.pack_start(button_url1, True, True, 0)

		# Linkbutton pointing to the given URI
		button_url3 = Gtk.LinkButton(uri="http://{}/index.csv".format(IP_GREENHOUSE_PI))
		button_url3.set_label("Download historic data .CSV")

		# Add the button to the window
		self.box.pack_start(button_url3, True, True, 0)

		# A linkbutton pointing to the given URI
		button_url4 = Gtk.LinkButton(uri="https://git.io/fhhsY")
		button_url4.set_label("Ay-yah's Greenhouse GitHub Repository")


	# Define the functions performed when a button is selected/clicked
	def on_button0_clicked(self, widget):
		print ("Turning Fan On")
		remote_command_number_option = 0
		fetch_url_trigger_event(remote_command_number_option)

	def on_button1_clicked(self, widget):
		print ("Turning Fan Off")
		remote_command_number_option = 1
		fetch_url_trigger_event(remote_command_number_option)

	def on_button2_clicked(self, widget):
		print ("Turning Light On")
		remote_command_number_option = 2
		fetch_url_trigger_event(remote_command_number_option)

	def on_button3_clicked(self, widget):
		print ("Turning Light Off")
		remote_command_number_option = 3
		fetch_url_trigger_event(remote_command_number_option)

	def on_button4_clicked(self, widget):
		print ("Turning Unused Output Three On")
		remote_command_number_option = 4
		fetch_url_trigger_event(remote_command_number_option)

	def on_button5_clicked(self, widget):
		print ("Turning Unused Output Three Off")
		remote_command_number_option = 5
		fetch_url_trigger_event(remote_command_number_option)

	def on_button6_clicked(self, widget):
		print ("Opening Solenoid Valve")
		remote_command_number_option = 6
		fetch_url_trigger_event(remote_command_number_option)

	def on_button7_clicked(self, widget):
		print ("Closing Solenoid Valve")
		remote_command_number_option = 7
		fetch_url_trigger_event(remote_command_number_option)

	def on_button8_clicked(self, widget):
		print ("Opening Window")
		remote_command_number_option = 8
		fetch_url_trigger_event(remote_command_number_option)

	def on_button9_clicked(self, widget):
		print ("Closing Window")
		remote_command_number_option = 9
		fetch_url_trigger_event(remote_command_number_option)


# Define the function called after the button selection function performing the remote URL fetch (manual operation)
def fetch_url_trigger_event(remote_command_number_option):

	print ("Fetching URL triggering event: ", REMOTE_CONTROL_URLS[remote_command_number_option])

	try: 
		object_containing_the_output_response_page = requests.get(REMOTE_CONTROL_URLS[remote_command_number_option], timeout=URL_FETCH_TIMEOUT_SECONDS)
		print ("Operation successful!")
		print ("URL fetch results: ", object_containing_the_output_response_page.text)

		if object_containing_the_output_response_page.status_code is not 200:
			print ("An error has occurred. Error code: ", object_containing_the_output_response_page.status_code)
			exit()

	except requests.ConnectionError as e:
		print ("Connection Error: ", e)

	except requests.HTTPError as e:
		print ("HTTP Error: ", e)
		raise requests.HTTPError(e.response.text, response=e.response)



# Create the history data GUI window class
class DialogWindow(Gtk.Window):

	def __init__(self):

		# Define the column header values
		columns = [	"Record",
				"LDR",
				"Temp.",
				"Humidity",
				"Soil",
				"Solenoid",
				"Actuator",
				"Output #1",
				"Output #2",
				"Output #3",
				"Date",
				"Time"]

		# Create a window, set the title, set the window size, and set the border width
		Gtk.Window.__init__(self, title="Historic Environmental Record")
		self.set_default_size(975, 350)
		self.set_border_width(10)
		self.move(200, 500)
		# Make the window scrollable
		scrolled_window = Gtk.ScrolledWindow()
		scrolled_window.set_border_width(10)
		scrolled_window.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)

		# Define the listmodel used by the ListStore
		listmodel = Gtk.ListStore(int, float, float, float, float, str, str, str, str, str, str, str)

		# Append the values in the model
		for i in range(len(list_of_greenhouse_table_rows)):
			listmodel.append(list(list_of_greenhouse_table_rows[i]))

		# Create a TreeView to see the data stored in the model
		view = Gtk.TreeView(model=listmodel)
		# For each column
		for i, column in enumerate(columns):
			# Cellrenderer to render the text
			cell = Gtk.CellRendererText()
			# The text in all of the columns should be in boldface
			if i is not None:
				cell.props.weight_set = True
				cell.props.weight = Pango.Weight.BOLD
				# Create the column
				col = Gtk.TreeViewColumn(column, cell, text=i)
				# Appended the column to the TreeView
				view.append_column(col)

		# Create a grid to attach the widgets to
		grid = Gtk.Grid()
		grid.attach(view, 0, 0, 1, 1)
	
		# Add the image to the scrolledwindow
		scrolled_window.add_with_viewport(grid)

		# Add the scrolledwindow to the window
		self.add(scrolled_window)

# Define the function that downloads the image files and greenhouse.db file the queries the greenhouse.db file
def fetch_greenhouse_data():

	print ("Downloading the low resolution animated .GIF image file.")

	try:

		filedata = requests.get("http://{}/greenhouselow.gif".format(IP_GREENHOUSE_PI))
		if filedata.status_code == 200:
			with open('greenhouselow.gif', 'wb') as f:
				f.write(filedata.content)

		# catch any error I cannot successfully catch using requests.HTTPError as e:
		if filedata.status_code is not 200:
			print ("An error has occurred. Error code: ", filedata.status_code)
			exit()

	except requests.ConnectionError as e:
		print ("Connection Error: ", e)

	except requests.HTTPError as e:
		print ("HTTP Error: ", e)
		raise requests.HTTPError(e.response.text, response=e.response)


	print ("Downloading the high resolution .JPG image file.")

	try:

		filedata = requests.get("http://{}/greenhousehigh.jpg".format(IP_GREENHOUSE_PI))
		if filedata.status_code == 200:
			with open('greenhousehigh.jpg', 'wb') as f:
				f.write(filedata.content)

		# catch any error I cannot successfully catch using requests.HTTPError as e:
		if filedata.status_code is not 200:
			print ("An error has occurred. Error code: ", filedata.status_code)
			exit()

	except requests.ConnectionError as e:
		print ("Connection Error: ", e)

	except requests.HTTPError as e:
		print ("HTTP Error: ", e)
		raise requests.HTTPError(e.response.text, response=e.response)


	print ("Downloading the historic environmental record greenhouse.db file.")

	try:


		filedata = requests.get("http://{}/greenhouse.db".format(IP_GREENHOUSE_PI))
		if filedata.status_code == 200:
			with open('greenhouse.db', 'wb') as f:
				f.write(filedata.content)

		# catch any error I cannot successfully catch using requests.HTTPError as e:
		if filedata.status_code is not 200:
			print ("An error has occurred. Error code: ", filedata.status_code)
			exit()

	except requests.ConnectionError as e:
		print ("Connection Error: ", e)

	except requests.HTTPError as e:
		print ("HTTP Error: ", e)
		raise requests.HTTPError(e.response.text, response=e.response)



	# Define global variable accessible in other functions
	global current_luminosity_sensor_value
	global current_luminosity_sensor_value
	global current_temperature
	global current_humidity
	global current_soil_moisture_sensor_value
	global current_solenoid_valve_status
	global current_actuator_extension_status
	global current_output_one_status
	global current_output_two_status
	global current_output_three_status
	global record_time
	global record_date
	global list_of_greenhouse_table_rows

	# Connecting to the Sqlite3 database file
	conn = sqlite3.connect(SQLITE_DATABASE_FILE)
	database_cursor = conn.cursor()

	# Return the last n number of rows from the greenhouse table
	database_cursor.execute("SELECT * FROM " + DATABASE_TABLE_NAME + " ORDER BY id DESC LIMIT " + LIMIT_NUMBER_ROWS_DISPLAYED.format(tn=DATABASE_TABLE_NAME, cn=id))
	list_of_greenhouse_table_rows = database_cursor.fetchall()

	# Return the last row in the greenhouse table
	database_cursor.execute("SELECT * FROM " + DATABASE_TABLE_NAME + " ORDER BY id DESC LIMIT 1;".format(tn=DATABASE_TABLE_NAME, cn=id))
	last_row_exists = database_cursor.fetchone()

	if last_row_exists:

		# print ('(Record Returned): {}'.format(last_row_exists))
		last_row_greenhouse_table_sqlite3 = last_row_exists
		current_database_record_id = last_row_greenhouse_table_sqlite3[0]
		current_luminosity_sensor_value = last_row_greenhouse_table_sqlite3[1]
		current_temperature = last_row_greenhouse_table_sqlite3[2]
		current_humidity = last_row_greenhouse_table_sqlite3[3]
		current_soil_moisture_sensor_value = last_row_greenhouse_table_sqlite3[4]
		current_solenoid_valve_status = last_row_greenhouse_table_sqlite3[5]
		current_actuator_extension_status = last_row_greenhouse_table_sqlite3[6]
		current_output_one_status = last_row_greenhouse_table_sqlite3[7]
		current_output_two_status = last_row_greenhouse_table_sqlite3[8]
		current_output_three_status = last_row_greenhouse_table_sqlite3[9]
		record_date = last_row_greenhouse_table_sqlite3[10]
		record_time = last_row_greenhouse_table_sqlite3[11]

	else:
		print ("Error: No last row returned!")

	# Closing the connection to the database file
	conn.close()



# Create the high resolution camera image GUI window class
class Large_Image_Window(Gtk.Window):

	def __init__(self):

		# Create the window object, set the title, and set the size
		Gtk.Window.__init__(self, title="High Resolution Camera Image")
		self.set_default_size(640, 480)
		self.move(150, 100)
		# Create a scrollable window
		scrolled_window = Gtk.ScrolledWindow()
		scrolled_window.set_border_width(10)
		# There is always the scrollbar automaticaly or none if not needed
		scrolled_window.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)

		# Construct a Gtk image object
		img = Gtk.Image() 
		# Set the image data from the contents of a file
		img.set_from_file("greenhousehigh.jpg") 

		# Add the image to the scrolledwindow
		scrolled_window.add_with_viewport(img)

		# Add the scrolledwindow to the window
		self.add(scrolled_window)


# Create the high resolution camera image GUI window class
class System_Configuration_Window(Gtk.Window):

	def __init__(self):


		# define the variable containg the remote host IP address
		global IP_GREENHOUSE_PI

		try: 
			# read the current GreenhousePi remote IP address from file
			ip_greenhouse_pi_file_handle = open(IP_GREENHOUSE_PI_FILE_NAME, 'r')
			IP_GREENHOUSE_PI = ip_greenhouse_pi_file_handle.readline().rstrip()
			print ("Read remote host address IP_GREENHOUSE_PI from file", IP_GREENHOUSE_PI)
			ip_greenhouse_pi_file_handle.close()
	
		except OSError:
	
			print ("An error occurred reading file name: ", IP_GREENHOUSE_PI_FILE_NAME)
			quit()

		# the list of remote URLs that trigger manual operations
		global REMOTE_CONTROL_URLS

		# Action selection input number to remote control function list
		# 0/1 Turn on/off the greenhouse fan
		# 2/3 Turn on/off the greenhouse light
		# 4/5 Turn on/off output three
		# 6/7 Open/close the water solenoid valve
		# 8/9 Open/close the window

		REMOTE_CONTROL_URLS = ["http://{}/openoutputonemanual.php".format(IP_GREENHOUSE_PI),
					"http://{}/closeoutputonemanual.php".format(IP_GREENHOUSE_PI),
					"http://{}/openoutputtwomanual.php".format(IP_GREENHOUSE_PI),
					"http://{}/closeoutputtwomanual.php".format(IP_GREENHOUSE_PI),
					"http://{}/openoutputthreemanual.php".format(IP_GREENHOUSE_PI),
					"http://{}/closeoutputthreemanual.php".format(IP_GREENHOUSE_PI),
					"http://{}/openwatermanual.php".format(IP_GREENHOUSE_PI),
					"http://{}/closewatermanual.php".format(IP_GREENHOUSE_PI),
					"http://{}/openwindowmanual.php".format(IP_GREENHOUSE_PI),
					"http://{}/closewindowmanual.php".format(IP_GREENHOUSE_PI)]

		# remote text files containing system configuration values
		global REMOTE_VARIABLE_URLS

		REMOTE_VARIABLE_URLS = ["http://{}/actuatorruntime.txt".format(IP_GREENHOUSE_PI),
					"http://{}/mintemactretract.txt".format(IP_GREENHOUSE_PI),
					"http://{}/mintemoutoneoff.txt".format(IP_GREENHOUSE_PI),
					"http://{}/minhumoutoneoff.txt".format(IP_GREENHOUSE_PI),
					"http://{}/mintemouttwooff.txt".format(IP_GREENHOUSE_PI),
					"http://{}/minlumouttwooff.txt".format(IP_GREENHOUSE_PI),
					"http://{}/minsoilsoleopen.txt".format(IP_GREENHOUSE_PI),
					"http://{}/outtwotemlum.txt".format(IP_GREENHOUSE_PI),
					"http://{}/soleoffsensch.txt".format(IP_GREENHOUSE_PI),
					"http://{}/solschtimesel.txt".format(IP_GREENHOUSE_PI),
					"http://{}/solschruntim.txt".format(IP_GREENHOUSE_PI)]

		global LINEAR_ACTUATOR_RUNTIME_VALUE_REMOTE
		global MINIMUM_TEMPERATURE_SENSOR_ACTUATOR_RETRACT_VALUE_REMOTE
		global MINIMUM_TEMPERATURE_SENSOR_OUTPUT_ONE_OFF_VALUE_REMOTE
		global MINIMUM_HUMIDITY_SENSOR_OUTPUT_ONE_OFF_VALUE_REMOTE
		global MINIMUM_TEMPERATURE_SENSOR_OUTPUT_TWO_OFF_VALUE_REMOTE
		global MINIMUM_LUMINOSITY_SENSOR_OUTPUT_TWO_OFF_VALUE_REMOTE
		global MINIMUM_SOIL_MOISTURE_SENSOR_SOLENOID_VALVE_OPEN_VALUE_REMOTE
		global OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE_REMOTE
		global SOLENOID_VALVE_CONFIGURATION_BETWEEN_OFF_SENSOR_SCHEDULE_VALUE_REMOTE
		global SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE
		global SOLENOID_VALVE_SCHEDULED_OPEN_RUNTIME_VALUE_REMOTE


		remote_control_values_list = []
		temporary_counter_variable = 0

		while (temporary_counter_variable < 11):
			print ("Fetching automation system control values")
			print ("Fetching URL: ", REMOTE_VARIABLE_URLS[temporary_counter_variable])

			try: 
				temporary_remote_response_value = requests.get(REMOTE_VARIABLE_URLS[temporary_counter_variable])
				remote_control_values_list.insert(temporary_counter_variable, temporary_remote_response_value.text) 
				print ("Operation successful!")
				print ("URL fetch results: ", remote_control_values_list[temporary_counter_variable])

				# catch any error I cannot successfully catch using requests.HTTPError as e:
				if temporary_remote_response_value.status_code is not 200:
					print ("An error has occurred. Error code: ", temporary_remote_response_value.status_code)
					exit()

			except requests.ConnectionError as e:
				print ("Connection Error: ", e)
			except requests.HTTPError as e:
				print ("HTTP Error: ", e)
				raise requests.HTTPError(e.response.text, response=e.response)

			temporary_counter_variable = temporary_counter_variable + 1	

		LINEAR_ACTUATOR_RUNTIME_VALUE_REMOTE = remote_control_values_list[0]
		MINIMUM_TEMPERATURE_SENSOR_ACTUATOR_RETRACT_VALUE_REMOTE = remote_control_values_list[1]
		MINIMUM_TEMPERATURE_SENSOR_OUTPUT_ONE_OFF_VALUE_REMOTE = remote_control_values_list[2]
		MINIMUM_HUMIDITY_SENSOR_OUTPUT_ONE_OFF_VALUE_REMOTE = remote_control_values_list[3]
		MINIMUM_TEMPERATURE_SENSOR_OUTPUT_TWO_OFF_VALUE_REMOTE = remote_control_values_list[4]
		MINIMUM_LUMINOSITY_SENSOR_OUTPUT_TWO_OFF_VALUE_REMOTE = remote_control_values_list[5]
		MINIMUM_SOIL_MOISTURE_SENSOR_SOLENOID_VALVE_OPEN_VALUE_REMOTE = remote_control_values_list[6]
		OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE_REMOTE = remote_control_values_list[7]
		SOLENOID_VALVE_CONFIGURATION_BETWEEN_OFF_SENSOR_SCHEDULE_VALUE_REMOTE = remote_control_values_list[8]
		SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE = remote_control_values_list[9]
		SOLENOID_VALVE_SCHEDULED_OPEN_RUNTIME_VALUE_REMOTE = remote_control_values_list[10]

		# Create the window object, set the title, and set the size
		Gtk.Window.__init__(self, title="Automation System Configuration")
		self.set_default_size(100, 200)
		self.set_hexpand(False)
		self.move(100, 50)
		# Create a a vertical container box 
		self.box = Gtk.VBox(spacing=0)
		self.add(self.box)

		# Create a scrollable window
		scrolled_window = Gtk.ScrolledWindow()
		scrolled_window.set_border_width(10)
		# There is always the scrollbar automaticaly or none if not needed
		scrolled_window.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)

		label_entry_actuator_runtime = Gtk.Label(xalign=1)
		label_entry_actuator_runtime.set_text('Linear Actuator Runtime: ')
		label_entry_actuator_runtime.set_justify(Gtk.Justification.LEFT)

		self.entry_actuator_runtime = Gtk.Entry()
		self.entry_actuator_runtime.set_text(str(LINEAR_ACTUATOR_RUNTIME_VALUE_REMOTE))
		self.entry_actuator_runtime.set_activates_default(True)
		self.entry_actuator_runtime.set_width_chars(5)

		label_entry_actuator_runtime_description_unit = Gtk.Label(xalign=0)
		label_entry_actuator_runtime_description_unit.set_text('Seconds')
		label_entry_actuator_runtime_description_unit.set_justify(Gtk.Justification.LEFT)

		label_entry_minimum_temperature_sensor_actuator_retract_value_remote = Gtk.Label(xalign=1)
		label_entry_minimum_temperature_sensor_actuator_retract_value_remote.set_text('Minimum Temperature Actuator Retract:')
		label_entry_minimum_temperature_sensor_actuator_retract_value_remote.set_justify(Gtk.Justification.LEFT)

		self.entry_minimum_temperature_sensor_actuator_retract_value_remote = Gtk.Entry()
		self.entry_minimum_temperature_sensor_actuator_retract_value_remote.set_text(str(MINIMUM_TEMPERATURE_SENSOR_ACTUATOR_RETRACT_VALUE_REMOTE))
		self.entry_minimum_temperature_sensor_actuator_retract_value_remote.set_activates_default(True)

		label_entry_minimum_temperature_sensor_actuator_retract_value_remote_description_unit = Gtk.Label(xalign=0)
		label_entry_minimum_temperature_sensor_actuator_retract_value_remote_description_unit.set_text('Degrees F')
		label_entry_minimum_temperature_sensor_actuator_retract_value_remote_description_unit.set_justify(Gtk.Justification.LEFT)

		label_entry_minimum_temperature_sensor_output_one_off_value_remote = Gtk.Label(xalign=1)
		label_entry_minimum_temperature_sensor_output_one_off_value_remote.set_text('Minimum Temperature Output #1 Off:')
		label_entry_minimum_temperature_sensor_output_one_off_value_remote.set_justify(Gtk.Justification.LEFT)

		self.entry_minimum_temperature_sensor_output_one_off_value_remote = Gtk.Entry()
		self.entry_minimum_temperature_sensor_output_one_off_value_remote.set_text(str(MINIMUM_TEMPERATURE_SENSOR_OUTPUT_ONE_OFF_VALUE_REMOTE))
		self.entry_minimum_temperature_sensor_output_one_off_value_remote.set_activates_default(True)

		label_entry_minimum_temperature_sensor_output_one_off_value_remote_description_unit = Gtk.Label(xalign=0)
		label_entry_minimum_temperature_sensor_output_one_off_value_remote_description_unit.set_text('Degrees F')
		label_entry_minimum_temperature_sensor_output_one_off_value_remote_description_unit.set_justify(Gtk.Justification.LEFT)

		label_entry_minimum_humidity_sensor_output_one_off_value_remote = Gtk.Label(xalign=1)
		label_entry_minimum_humidity_sensor_output_one_off_value_remote.set_text('AND Minimum Humidity Output #1 Off:')
		label_entry_minimum_humidity_sensor_output_one_off_value_remote.set_justify(Gtk.Justification.LEFT)

		self.entry_minimum_humidity_sensor_output_one_off_value_remote = Gtk.Entry()
		self.entry_minimum_humidity_sensor_output_one_off_value_remote.set_text(str(MINIMUM_HUMIDITY_SENSOR_OUTPUT_ONE_OFF_VALUE_REMOTE))
		self.entry_minimum_humidity_sensor_output_one_off_value_remote.set_activates_default(True)

		label_entry_minimum_humidity_sensor_output_one_off_value_remote_description_unit = Gtk.Label(xalign=0)
		label_entry_minimum_humidity_sensor_output_one_off_value_remote_description_unit.set_text('% 0-100')
		label_entry_minimum_humidity_sensor_output_one_off_value_remote_description_unit.set_justify(Gtk.Justification.LEFT)

		label_entry_minimum_temperature_sensor_output_two_off_value_remote = Gtk.Label(xalign=1)
		label_entry_minimum_temperature_sensor_output_two_off_value_remote.set_text('Minimum Temperature Output #2 Off:')
		label_entry_minimum_temperature_sensor_output_two_off_value_remote.set_justify(Gtk.Justification.LEFT)

		self.entry_minimum_temperature_sensor_output_two_off_value_remote = Gtk.Entry()
		self.entry_minimum_temperature_sensor_output_two_off_value_remote.set_text(str(MINIMUM_TEMPERATURE_SENSOR_OUTPUT_TWO_OFF_VALUE_REMOTE))
		self.entry_minimum_temperature_sensor_output_two_off_value_remote.set_activates_default(True)

		label_entry_minimum_temperature_sensor_output_two_off_value_remote_description_unit = Gtk.Label(xalign=0)
		label_entry_minimum_temperature_sensor_output_two_off_value_remote_description_unit.set_text('Degrees F')
		label_entry_minimum_temperature_sensor_output_two_off_value_remote_description_unit.set_justify(Gtk.Justification.LEFT)

		label_entry_minimum_luminosity_sensor_output_two_off_value_remote = Gtk.Label(xalign=1)
		label_entry_minimum_luminosity_sensor_output_two_off_value_remote.set_text('Minimum Luminosity Outout #2 Off:')
		label_entry_minimum_luminosity_sensor_output_two_off_value_remote.set_justify(Gtk.Justification.LEFT)

		self.entry_minimum_luminosity_sensor_output_two_off_value_remote = Gtk.Entry()
		self.entry_minimum_luminosity_sensor_output_two_off_value_remote.set_text(str(MINIMUM_LUMINOSITY_SENSOR_OUTPUT_TWO_OFF_VALUE_REMOTE))
		self.entry_minimum_luminosity_sensor_output_two_off_value_remote.set_activates_default(True)

		label_entry_minimum_luminosity_sensor_output_two_off_value_remote_description_unit = Gtk.Label(xalign=0)
		label_entry_minimum_luminosity_sensor_output_two_off_value_remote_description_unit.set_text('Volts 0-5')
		label_entry_minimum_luminosity_sensor_output_two_off_value_remote_description_unit.set_justify(Gtk.Justification.LEFT)

		label_entry_minimum_soil_moisture_sensor_solenoid_valve_open_value_remote = Gtk.Label(xalign=1)
		label_entry_minimum_soil_moisture_sensor_solenoid_valve_open_value_remote.set_text('Minimum Moisture Sensor Open Solenoid:')
		label_entry_minimum_soil_moisture_sensor_solenoid_valve_open_value_remote.set_justify(Gtk.Justification.LEFT)

		self.entry_minimum_soil_moisture_sensor_solenoid_valve_open_value_remote = Gtk.Entry()
		self.entry_minimum_soil_moisture_sensor_solenoid_valve_open_value_remote.set_text(str(MINIMUM_SOIL_MOISTURE_SENSOR_SOLENOID_VALVE_OPEN_VALUE_REMOTE))
		self.entry_minimum_soil_moisture_sensor_solenoid_valve_open_value_remote.set_activates_default(True)

		label_entry_minimum_soil_moisture_sensor_solenoid_valve_open_value_remote_description_unit = Gtk.Label(xalign=0)
		label_entry_minimum_soil_moisture_sensor_solenoid_valve_open_value_remote_description_unit.set_text('Volts 0-5')
		label_entry_minimum_soil_moisture_sensor_solenoid_valve_open_value_remote_description_unit.set_justify(Gtk.Justification.LEFT)

		label_radio_buttons_output_two_configuration_between_temperature_or_luminosity_value_remote = Gtk.Label(xalign=1)
		label_radio_buttons_output_two_configuration_between_temperature_or_luminosity_value_remote.set_text('Output #2 Mode Temperature OR Luminosity:')
		label_radio_buttons_output_two_configuration_between_temperature_or_luminosity_value_remote.set_justify(Gtk.Justification.LEFT)

		temperature_radio_button = Gtk.RadioButton.new_with_label_from_widget(None, "Temperature")
		temperature_radio_button.connect("toggled", self.on_button_toggled_1, "0")

		if OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE_REMOTE == 'Temperature': temperature_radio_button.set_active(True)

		luminosity_radio_button = Gtk.RadioButton.new_from_widget(temperature_radio_button)
		luminosity_radio_button.set_label("Luminosity")

		if OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE_REMOTE == 'Luminosity': luminosity_radio_button.set_active(True)

		luminosity_radio_button.connect("toggled", self.on_button_toggled_1, "1")






		label_radio_buttons_solenoid_valve_configuration_between_off_schedule_sensor_value_remote = Gtk.Label(xalign=1)
		label_radio_buttons_solenoid_valve_configuration_between_off_schedule_sensor_value_remote.set_text('Solenoid Valve Off OR Schedule OR Sensor:')
		label_radio_buttons_solenoid_valve_configuration_between_off_schedule_sensor_value_remote.set_justify(Gtk.Justification.LEFT)

		solenoid_valve_configuration_off_radio_button = Gtk.RadioButton.new_with_label_from_widget(None, "Off")

		solenoid_valve_configuration_off_radio_button.connect("toggled", self.on_button_toggled_2, "0")

		if SOLENOID_VALVE_CONFIGURATION_BETWEEN_OFF_SENSOR_SCHEDULE_VALUE_REMOTE == 'Off': solenoid_valve_configuration_off_radio_button.set_active(True)

		solenoid_valve_configuration_schedule_radio_button = Gtk.RadioButton.new_from_widget(solenoid_valve_configuration_off_radio_button)

		solenoid_valve_configuration_schedule_radio_button.set_label("Schedule")

		if SOLENOID_VALVE_CONFIGURATION_BETWEEN_OFF_SENSOR_SCHEDULE_VALUE_REMOTE == 'Schedule': solenoid_valve_configuration_schedule_radio_button.set_active(True)

		solenoid_valve_configuration_schedule_radio_button.connect("toggled", self.on_button_toggled_2, "1")

		solenoid_valve_configuration_sensor_radio_button = Gtk.RadioButton.new_from_widget(solenoid_valve_configuration_off_radio_button)
		solenoid_valve_configuration_sensor_radio_button.set_label("Sensor")

		if SOLENOID_VALVE_CONFIGURATION_BETWEEN_OFF_SENSOR_SCHEDULE_VALUE_REMOTE == 'Sensor': solenoid_valve_configuration_sensor_radio_button.set_active(True)

		solenoid_valve_configuration_sensor_radio_button.connect("toggled", self.on_button_toggled_2, "2")


		label_radio_buttons_solenoid_valve_scheduled_time_value_remote = Gtk.Label(xalign=1)
		label_radio_buttons_solenoid_valve_scheduled_time_value_remote.set_text('Solenoid Valve Scheduled Time Selection:')
		label_radio_buttons_solenoid_valve_scheduled_time_value_remote.set_justify(Gtk.Justification.LEFT)


		label_entry_solenoid_valve_scheduled_open_runtime_value_remote = Gtk.Label(xalign=1)
		label_entry_solenoid_valve_scheduled_open_runtime_value_remote.set_text('Solenoid Valve Scheduled Open Runtime:')
		label_entry_solenoid_valve_scheduled_open_runtime_value_remote.set_justify(Gtk.Justification.LEFT)

		self.entry_solenoid_valve_scheduled_open_runtime_value_remote = Gtk.Entry()
		self.entry_solenoid_valve_scheduled_open_runtime_value_remote.set_text(str(SOLENOID_VALVE_SCHEDULED_OPEN_RUNTIME_VALUE_REMOTE))
		self.entry_solenoid_valve_scheduled_open_runtime_value_remote.set_activates_default(True)

		label_entry_solenoid_valve_scheduled_open_runtime_value_description_unit = Gtk.Label(xalign=0)
		label_entry_solenoid_valve_scheduled_open_runtime_value_description_unit.set_text('Minutes')
		label_entry_solenoid_valve_scheduled_open_runtime_value_description_unit.set_justify(Gtk.Justification.LEFT)




		label_empty_spacer_for_table_local_0 = Gtk.Label(xalign=1)
		label_empty_spacer_for_table_local_0.set_text(' ')
		label_empty_spacer_for_table_local_0.set_justify(Gtk.Justification.LEFT)

		label_empty_spacer_for_table_local_1 = Gtk.Label(xalign=1)
		label_empty_spacer_for_table_local_1.set_text(' ')
		label_empty_spacer_for_table_local_1.set_justify(Gtk.Justification.LEFT)

		label_empty_spacer_for_table_local_2 = Gtk.Label(xalign=1)
		label_empty_spacer_for_table_local_2.set_text(' ')
		label_empty_spacer_for_table_local_2.set_justify(Gtk.Justification.LEFT)

		label_empty_spacer_for_table_local_3 = Gtk.Label(xalign=1)
		label_empty_spacer_for_table_local_3.set_text(' ')
		label_empty_spacer_for_table_local_3.set_justify(Gtk.Justification.LEFT)

		label_empty_spacer_for_table_local_4 = Gtk.Label(xalign=1)
		label_empty_spacer_for_table_local_4.set_text(' ')
		label_empty_spacer_for_table_local_4.set_justify(Gtk.Justification.LEFT)

		label_empty_spacer_for_table_local_5 = Gtk.Label(xalign=1)
		label_empty_spacer_for_table_local_5.set_text(' ')
		label_empty_spacer_for_table_local_5.set_justify(Gtk.Justification.LEFT)

		### Need a list and a while loop that produces a radio button for each element
		# define the descriptions of the crontab configuration values for opening the solenoid valve
		list_of_predefined_crontab_configuration_descriptions = [
					"Water Daily Every Two Minutes",
					"Water Daily @ 12AM",
					"Water Daily @ 6AM",
					"Water Daily @ 12PM",
					"Water Daily @ 6PM",
					"Water Twice Daily @ 12AM & 12PM",
					"Water Thrice Daily @ 8AM & 4PM & 12AM",
					"Water Every Two Days @ 12AM",
					"Water Every Two Days @ 6AM",
					"Water Every Two Days @ 12PM",
					"Water Every Two Days @ 6PM",
					"Water Every Three Days @ 12AM",
					"Water Every Three Days @ 6AM",
					"Water Every Three Days @ 12PM",
					"Water Every Three Days @ 6PM",
					"Water Weekly Sunday @ Midnight",
					]

		solenoid_valve_scheduled_time_value_remote_radio_button_0 = Gtk.RadioButton.new_with_label_from_widget(None, list_of_predefined_crontab_configuration_descriptions[0])
		solenoid_valve_scheduled_time_value_remote_radio_button_0.connect("toggled", self.on_button_toggled_3, "0")
		if SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE == '0': solenoid_valve_scheduled_time_value_remote_radio_button_0.set_active(True)

		solenoid_valve_scheduled_time_value_remote_radio_button_1 = Gtk.RadioButton.new_from_widget(solenoid_valve_scheduled_time_value_remote_radio_button_0)
		solenoid_valve_scheduled_time_value_remote_radio_button_1.set_label(list_of_predefined_crontab_configuration_descriptions[1])
		if SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE == '1': solenoid_valve_scheduled_time_value_remote_radio_button_1.set_active(True)
		solenoid_valve_scheduled_time_value_remote_radio_button_1.connect("toggled", self.on_button_toggled_3, "1")

		solenoid_valve_scheduled_time_value_remote_radio_button_2 = Gtk.RadioButton.new_from_widget(solenoid_valve_scheduled_time_value_remote_radio_button_0)
		solenoid_valve_scheduled_time_value_remote_radio_button_2.set_label(list_of_predefined_crontab_configuration_descriptions[2])
		if SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE == '2': solenoid_valve_scheduled_time_value_remote_radio_button_2.set_active(True)
		solenoid_valve_scheduled_time_value_remote_radio_button_2.connect("toggled", self.on_button_toggled_3, "2")

		solenoid_valve_scheduled_time_value_remote_radio_button_3 = Gtk.RadioButton.new_from_widget(solenoid_valve_scheduled_time_value_remote_radio_button_0)
		solenoid_valve_scheduled_time_value_remote_radio_button_3.set_label(list_of_predefined_crontab_configuration_descriptions[3])
		if SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE == '3': solenoid_valve_scheduled_time_value_remote_radio_button_3.set_active(True)
		solenoid_valve_scheduled_time_value_remote_radio_button_3.connect("toggled", self.on_button_toggled_3, "3")

		solenoid_valve_scheduled_time_value_remote_radio_button_4 = Gtk.RadioButton.new_from_widget(solenoid_valve_scheduled_time_value_remote_radio_button_0)
		solenoid_valve_scheduled_time_value_remote_radio_button_4.set_label(list_of_predefined_crontab_configuration_descriptions[4])
		if SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE == '4': solenoid_valve_scheduled_time_value_remote_radio_button_4.set_active(True)
		solenoid_valve_scheduled_time_value_remote_radio_button_4.connect("toggled", self.on_button_toggled_3, "4")

		solenoid_valve_scheduled_time_value_remote_radio_button_5 = Gtk.RadioButton.new_from_widget(solenoid_valve_scheduled_time_value_remote_radio_button_0)
		solenoid_valve_scheduled_time_value_remote_radio_button_5.set_label(list_of_predefined_crontab_configuration_descriptions[5])
		if SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE == '5': solenoid_valve_scheduled_time_value_remote_radio_button_5.set_active(True)
		solenoid_valve_scheduled_time_value_remote_radio_button_5.connect("toggled", self.on_button_toggled_3, "5")

		solenoid_valve_scheduled_time_value_remote_radio_button_6 = Gtk.RadioButton.new_from_widget(solenoid_valve_scheduled_time_value_remote_radio_button_0)
		solenoid_valve_scheduled_time_value_remote_radio_button_6.set_label(list_of_predefined_crontab_configuration_descriptions[6])
		if SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE == '6': solenoid_valve_scheduled_time_value_remote_radio_button_6.set_active(True)
		solenoid_valve_scheduled_time_value_remote_radio_button_6.connect("toggled", self.on_button_toggled_3, "6")

		solenoid_valve_scheduled_time_value_remote_radio_button_7 = Gtk.RadioButton.new_from_widget(solenoid_valve_scheduled_time_value_remote_radio_button_0)
		solenoid_valve_scheduled_time_value_remote_radio_button_7.set_label(list_of_predefined_crontab_configuration_descriptions[7])
		if SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE == '7': solenoid_valve_scheduled_time_value_remote_radio_button_7.set_active(True)
		solenoid_valve_scheduled_time_value_remote_radio_button_7.connect("toggled", self.on_button_toggled_3, "7")

		solenoid_valve_scheduled_time_value_remote_radio_button_8 = Gtk.RadioButton.new_from_widget(solenoid_valve_scheduled_time_value_remote_radio_button_0)
		solenoid_valve_scheduled_time_value_remote_radio_button_8.set_label(list_of_predefined_crontab_configuration_descriptions[8])
		if SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE == '8': solenoid_valve_scheduled_time_value_remote_radio_button_8.set_active(True)
		solenoid_valve_scheduled_time_value_remote_radio_button_8.connect("toggled", self.on_button_toggled_3, "8")

		solenoid_valve_scheduled_time_value_remote_radio_button_9 = Gtk.RadioButton.new_from_widget(solenoid_valve_scheduled_time_value_remote_radio_button_0)
		solenoid_valve_scheduled_time_value_remote_radio_button_9.set_label(list_of_predefined_crontab_configuration_descriptions[9])
		if SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE == '9': solenoid_valve_scheduled_time_value_remote_radio_button_9.set_active(True)
		solenoid_valve_scheduled_time_value_remote_radio_button_9.connect("toggled", self.on_button_toggled_3, "9")

		solenoid_valve_scheduled_time_value_remote_radio_button_10 = Gtk.RadioButton.new_from_widget(solenoid_valve_scheduled_time_value_remote_radio_button_0)
		solenoid_valve_scheduled_time_value_remote_radio_button_10.set_label(list_of_predefined_crontab_configuration_descriptions[10])
		if SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE == '10': solenoid_valve_scheduled_time_value_remote_radio_button_10.set_active(True)
		solenoid_valve_scheduled_time_value_remote_radio_button_10.connect("toggled", self.on_button_toggled_3, "10")

		solenoid_valve_scheduled_time_value_remote_radio_button_11 = Gtk.RadioButton.new_from_widget(solenoid_valve_scheduled_time_value_remote_radio_button_0)
		solenoid_valve_scheduled_time_value_remote_radio_button_11.set_label(list_of_predefined_crontab_configuration_descriptions[11])
		if SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE == '11': solenoid_valve_scheduled_time_value_remote_radio_button_11.set_active(True)
		solenoid_valve_scheduled_time_value_remote_radio_button_11.connect("toggled", self.on_button_toggled_3, "11")

		solenoid_valve_scheduled_time_value_remote_radio_button_12 = Gtk.RadioButton.new_from_widget(solenoid_valve_scheduled_time_value_remote_radio_button_0)
		solenoid_valve_scheduled_time_value_remote_radio_button_12.set_label(list_of_predefined_crontab_configuration_descriptions[12])
		if SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE == '12': solenoid_valve_scheduled_time_value_remote_radio_button_12.set_active(True)
		solenoid_valve_scheduled_time_value_remote_radio_button_12.connect("toggled", self.on_button_toggled_3, "12")

		solenoid_valve_scheduled_time_value_remote_radio_button_13 = Gtk.RadioButton.new_from_widget(solenoid_valve_scheduled_time_value_remote_radio_button_0)
		solenoid_valve_scheduled_time_value_remote_radio_button_13.set_label(list_of_predefined_crontab_configuration_descriptions[13])
		if SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE == '13': solenoid_valve_scheduled_time_value_remote_radio_button_13.set_active(True)
		solenoid_valve_scheduled_time_value_remote_radio_button_13.connect("toggled", self.on_button_toggled_3, "13")

		solenoid_valve_scheduled_time_value_remote_radio_button_14 = Gtk.RadioButton.new_from_widget(solenoid_valve_scheduled_time_value_remote_radio_button_0)
		solenoid_valve_scheduled_time_value_remote_radio_button_14.set_label(list_of_predefined_crontab_configuration_descriptions[14])
		if SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE == '14': solenoid_valve_scheduled_time_value_remote_radio_button_14.set_active(True)
		solenoid_valve_scheduled_time_value_remote_radio_button_14.connect("toggled", self.on_button_toggled_3, "14")

		solenoid_valve_scheduled_time_value_remote_radio_button_15 = Gtk.RadioButton.new_from_widget(solenoid_valve_scheduled_time_value_remote_radio_button_0)
		solenoid_valve_scheduled_time_value_remote_radio_button_15.set_label(list_of_predefined_crontab_configuration_descriptions[15])
		if SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE == '15': solenoid_valve_scheduled_time_value_remote_radio_button_15.set_active(True)
		solenoid_valve_scheduled_time_value_remote_radio_button_15.connect("toggled", self.on_button_toggled_3, "15")



		button_post_form_values = Gtk.Button.new_with_label("Save Settings")
		button_post_form_values.connect("clicked", self.on_button_post_form_values_clicked)

		layout_table = Gtk.Table(39, 3, False)
		self.box.add(layout_table)
		layout_table.set_border_width(10)
		layout_table.attach(label_entry_actuator_runtime, 0, 1, 0, 1)
		layout_table.attach(self.entry_actuator_runtime, 1, 2, 0, 1)
		layout_table.attach(label_entry_actuator_runtime_description_unit, 2, 3, 0, 1)
		layout_table.attach(label_entry_minimum_temperature_sensor_actuator_retract_value_remote, 0, 1, 1, 2)
		layout_table.attach(self.entry_minimum_temperature_sensor_actuator_retract_value_remote, 1, 2, 1, 2)
		layout_table.attach(label_entry_minimum_temperature_sensor_actuator_retract_value_remote_description_unit, 2, 3, 1, 2)
		layout_table.attach(label_entry_minimum_temperature_sensor_output_one_off_value_remote, 0, 1, 2, 3)
		layout_table.attach(self.entry_minimum_temperature_sensor_output_one_off_value_remote, 1, 2, 2, 3)
		layout_table.attach(label_entry_minimum_temperature_sensor_output_one_off_value_remote_description_unit, 2, 3, 2, 3)
		layout_table.attach(label_entry_minimum_humidity_sensor_output_one_off_value_remote, 0, 1, 3, 4)
		layout_table.attach(self.entry_minimum_humidity_sensor_output_one_off_value_remote, 1, 2, 3, 4)
		layout_table.attach(label_entry_minimum_humidity_sensor_output_one_off_value_remote_description_unit, 2, 3, 3, 4)

		layout_table.attach(label_empty_spacer_for_table_local_0, 0, 1, 4, 5)

		layout_table.attach(label_radio_buttons_output_two_configuration_between_temperature_or_luminosity_value_remote, 0, 1, 5, 6)
		layout_table.attach(temperature_radio_button, 1, 2, 5, 6)
		layout_table.attach(luminosity_radio_button, 1, 2, 6, 7)

		layout_table.attach(label_empty_spacer_for_table_local_1, 0, 1, 9, 10)

		layout_table.attach(label_entry_minimum_temperature_sensor_output_two_off_value_remote, 0, 1, 10, 11)
		layout_table.attach(self.entry_minimum_temperature_sensor_output_two_off_value_remote, 1, 2, 10, 11)
		layout_table.attach(label_entry_minimum_temperature_sensor_output_two_off_value_remote_description_unit, 2, 3, 10, 11)

		layout_table.attach(label_entry_minimum_luminosity_sensor_output_two_off_value_remote, 0, 1, 11, 12)
		layout_table.attach(self.entry_minimum_luminosity_sensor_output_two_off_value_remote, 1, 2, 11, 12)
		layout_table.attach(label_entry_minimum_luminosity_sensor_output_two_off_value_remote_description_unit, 2, 3, 11, 12)



		layout_table.attach(label_empty_spacer_for_table_local_2, 0, 1, 12, 13)

		layout_table.attach(label_radio_buttons_solenoid_valve_configuration_between_off_schedule_sensor_value_remote, 0, 1, 13, 14)
		layout_table.attach(solenoid_valve_configuration_off_radio_button, 1, 2, 13, 14)
		layout_table.attach(solenoid_valve_configuration_schedule_radio_button, 1, 2, 14, 15)
		layout_table.attach(solenoid_valve_configuration_sensor_radio_button, 1, 2, 15, 16)

		layout_table.attach(label_empty_spacer_for_table_local_3, 0, 1, 16, 17)





		layout_table.attach(label_radio_buttons_solenoid_valve_scheduled_time_value_remote, 0, 1, 17, 18)

		layout_table.attach(solenoid_valve_scheduled_time_value_remote_radio_button_0, 1, 2, 17, 18)
		layout_table.attach(solenoid_valve_scheduled_time_value_remote_radio_button_1, 1, 2, 18, 19)
		layout_table.attach(solenoid_valve_scheduled_time_value_remote_radio_button_2, 1, 2, 20, 21)
		layout_table.attach(solenoid_valve_scheduled_time_value_remote_radio_button_3, 1, 2, 21, 22)
		layout_table.attach(solenoid_valve_scheduled_time_value_remote_radio_button_4, 1, 2, 22, 23)
		layout_table.attach(solenoid_valve_scheduled_time_value_remote_radio_button_5, 1, 2, 23, 24)
		layout_table.attach(solenoid_valve_scheduled_time_value_remote_radio_button_6, 1, 2, 24, 25)
		layout_table.attach(solenoid_valve_scheduled_time_value_remote_radio_button_7, 1, 2, 25, 26)
		layout_table.attach(solenoid_valve_scheduled_time_value_remote_radio_button_8, 1, 2, 26, 27)
		layout_table.attach(solenoid_valve_scheduled_time_value_remote_radio_button_9, 1, 2, 27, 28)
		layout_table.attach(solenoid_valve_scheduled_time_value_remote_radio_button_10, 1, 2, 28, 29)
		layout_table.attach(solenoid_valve_scheduled_time_value_remote_radio_button_11, 1, 2, 29, 30)
		layout_table.attach(solenoid_valve_scheduled_time_value_remote_radio_button_12, 1, 2, 30, 31)
		layout_table.attach(solenoid_valve_scheduled_time_value_remote_radio_button_13, 1, 2, 31, 32)
		layout_table.attach(solenoid_valve_scheduled_time_value_remote_radio_button_14, 1, 2, 32, 33)
		layout_table.attach(solenoid_valve_scheduled_time_value_remote_radio_button_15, 1, 2, 33, 34)

		layout_table.attach(label_empty_spacer_for_table_local_4, 0, 1, 34, 35)

		layout_table.attach(label_entry_solenoid_valve_scheduled_open_runtime_value_remote, 0, 1, 35, 36)
		layout_table.attach(self.entry_solenoid_valve_scheduled_open_runtime_value_remote, 1, 2, 35, 36)
		layout_table.attach(label_entry_solenoid_valve_scheduled_open_runtime_value_description_unit, 2, 3, 35, 36)

		layout_table.attach(label_entry_minimum_soil_moisture_sensor_solenoid_valve_open_value_remote, 0, 1, 36, 37)
		layout_table.attach(self.entry_minimum_soil_moisture_sensor_solenoid_valve_open_value_remote, 1, 2, 36, 37)
		layout_table.attach(label_entry_minimum_soil_moisture_sensor_solenoid_valve_open_value_remote_description_unit, 2, 3, 36, 37)

		layout_table.attach(label_empty_spacer_for_table_local_5, 0, 1, 37, 38)

		layout_table.attach(button_post_form_values, 0, 3, 38, 39)


	def on_button_toggled_1(self, button, name):

		# define the global variable
		global OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE_REMOTE

		if button.get_active():

			state = "on"
		else:
			state = "off"

		if (name == '0') and (state == 'on'): OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE_REMOTE = 'Temperature'
		if (name == '1') and (state == 'on'): OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE_REMOTE = 'Luminosity'


	def on_button_toggled_2(self, button, name):

		# define the variable
		global SOLENOID_VALVE_CONFIGURATION_BETWEEN_OFF_SENSOR_SCHEDULE_VALUE_REMOTE

		if button.get_active():

			state = "on"
		else:
			state = "off"

		if (name == '0') and (state == 'on'): SOLENOID_VALVE_CONFIGURATION_BETWEEN_OFF_SENSOR_SCHEDULE_VALUE_REMOTE = 'Off'
		if (name == '1') and (state == 'on'): SOLENOID_VALVE_CONFIGURATION_BETWEEN_OFF_SENSOR_SCHEDULE_VALUE_REMOTE = 'Schedule'
		if (name == '2') and (state == 'on'): SOLENOID_VALVE_CONFIGURATION_BETWEEN_OFF_SENSOR_SCHEDULE_VALUE_REMOTE = 'Sensor'


	def on_button_toggled_3(self, button, name):

		# define the variable
		global SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE

		if button.get_active():

			state = "on"
		else:
			state = "off"

		if (name == '0') and (state == 'on'): SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE = 0
		if (name == '1') and (state == 'on'): SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE = 1
		if (name == '2') and (state == 'on'): SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE = 2
		if (name == '3') and (state == 'on'): SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE = 3
		if (name == '4') and (state == 'on'): SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE = 4
		if (name == '5') and (state == 'on'): SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE = 5
		if (name == '6') and (state == 'on'): SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE = 6
		if (name == '7') and (state == 'on'): SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE = 7
		if (name == '8') and (state == 'on'): SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE = 8
		if (name == '9') and (state == 'on'): SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE = 9
		if (name == '10') and (state == 'on'): SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE = 10
		if (name == '11') and (state == 'on'): SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE = 11
		if (name == '12') and (state == 'on'): SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE = 12
		if (name == '13') and (state == 'on'): SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE = 13
		if (name == '14') and (state == 'on'): SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE = 14
		if (name == '15') and (state == 'on'): SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE = 15
		if (name == '16') and (state == 'on'): SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE = 16


	# Define the functions performed when a button is selected/clicked
	def on_button_post_form_values_clicked(self, widget):

		LINEAR_ACTUATOR_RUNTIME_VALUE_REMOTE = self.entry_actuator_runtime.get_text()
		MINIMUM_TEMPERATURE_SENSOR_ACTUATOR_RETRACT_VALUE_REMOTE = self.entry_minimum_temperature_sensor_actuator_retract_value_remote.get_text()
		MINIMUM_TEMPERATURE_SENSOR_OUTPUT_ONE_OFF_VALUE_REMOTE = self.entry_minimum_temperature_sensor_output_one_off_value_remote.get_text()
		MINIMUM_HUMIDITY_SENSOR_OUTPUT_ONE_OFF_VALUE_REMOTE = self.entry_minimum_humidity_sensor_output_one_off_value_remote.get_text()
		MINIMUM_TEMPERATURE_SENSOR_OUTPUT_TWO_OFF_VALUE_REMOTE = self.entry_minimum_temperature_sensor_output_two_off_value_remote.get_text()
		MINIMUM_LUMINOSITY_SENSOR_OUTPUT_TWO_OFF_VALUE_REMOTE = self.entry_minimum_luminosity_sensor_output_two_off_value_remote.get_text()
		MINIMUM_SOIL_MOISTURE_SENSOR_SOLENOID_VALVE_OPEN_VALUE_REMOTE = self.entry_minimum_soil_moisture_sensor_solenoid_valve_open_value_remote.get_text()
		SOLENOID_VALVE_SCHEDULED_OPEN_RUNTIME_VALUE_REMOTE = self.entry_solenoid_valve_scheduled_open_runtime_value_remote.get_text()

		print ("Saving Settings...")

		remote_post_form_url = "http://{}/index.php".format(IP_GREENHOUSE_PI)

		post_form_values = {	'LINEAR_ACTUATOR_RUNTIME_VALUE' : LINEAR_ACTUATOR_RUNTIME_VALUE_REMOTE,
					'MINIMUM_TEMPERATURE_SENSOR_ACTUATOR_RETRACT_VALUE' : MINIMUM_TEMPERATURE_SENSOR_ACTUATOR_RETRACT_VALUE_REMOTE,
					'MINIMUM_TEMPERATURE_SENSOR_OUTPUT_ONE_OFF_VALUE' : MINIMUM_TEMPERATURE_SENSOR_OUTPUT_ONE_OFF_VALUE_REMOTE,
					'MINIMUM_HUMIDITY_SENSOR_OUTPUT_ONE_OFF_VALUE' : MINIMUM_HUMIDITY_SENSOR_OUTPUT_ONE_OFF_VALUE_REMOTE,
					'MINIMUM_TEMPERATURE_SENSOR_OUTPUT_TWO_OFF_VALUE' : MINIMUM_TEMPERATURE_SENSOR_OUTPUT_TWO_OFF_VALUE_REMOTE,
					'MINIMUM_LUMINOSITY_SENSOR_OUTPUT_TWO_OFF_VALUE' : MINIMUM_LUMINOSITY_SENSOR_OUTPUT_TWO_OFF_VALUE_REMOTE,
					'MINIMUM_SOIL_MOISTURE_SENSOR_SOLENOID_VALVE_OPEN_VALUE' : MINIMUM_SOIL_MOISTURE_SENSOR_SOLENOID_VALVE_OPEN_VALUE_REMOTE,
					'OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE' : OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE_REMOTE,
					'SOLENOID_VALVE_CONFIGURATION_BETWEEN_OFF_SENSOR_SCHEDULE_VALUE' : SOLENOID_VALVE_CONFIGURATION_BETWEEN_OFF_SENSOR_SCHEDULE_VALUE_REMOTE,
					'SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE' : SOLENOID_VALVE_SCHEDULED_TIME_SELECTION_VALUE_REMOTE,
					'SOLENOID_VALVE_SCHEDULED_OPEN_RUNTIME_VALUE' :  SOLENOID_VALVE_SCHEDULED_OPEN_RUNTIME_VALUE_REMOTE }

		print ("Submitting configuration values:")
		print (post_form_values)
		session = requests.session()
		object_containing_the_output_response_page = requests.post(remote_post_form_url, data=post_form_values)
		print (object_containing_the_output_response_page)



win = System_Configuration_Window()
win.show_all()

win = Large_Image_Window()
win.show_all()

fetch_greenhouse_data()

win = DialogWindow()
win.show_all()

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

