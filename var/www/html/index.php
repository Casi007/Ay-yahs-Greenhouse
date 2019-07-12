<html>
<head><title>Ay-yah's Greenhouse Automation System Version 1.02</title>
<style>
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}
.the-table-scrollbar {
position: relative;
height: 200px;
overflow: auto;
}
.table-wrapper-scroll-y {
display: block;
}
th, td {
  padding: 10px;
}
</style>
</head>
<body>
 <center>
<h1 align="center">Ay-yah's Greenhouse Automation System</h1>
  <table style="width:30%" align="center">
    <tr>
      <td valign="top">
       <p align="center"><a href="<?php $_SERVER['PHP_SELF']; ?>"><img src="/refresh_icon.png" alt="Refresh Page" height="70" width="70"></a></p>

<?php

$SQLITE_DATABASE_FILE_NAME = "/var/www/html/greenhouse.db";

# linear actuator status file name (Retracted | Extended)
$ACTUATOR_STATUS_FILE_NAME = '/home/pi/Greenhouse/actuator.txt';
# solenoid valve status file name (Open | Closed)
$SOLENOID_STATUS_FILE_NAME = '/home/pi/Greenhouse/solenoid.txt';
# outputs status file name (On | Off)
$OUTPUTS_STATUS_FILE_NAME = '/home/pi/Greenhouse/outputs.txt';

# luminosity graph image web/url file name
$GRAPH_IMAGE_LUMINOSITY_URL_FILE_NAME = "ghouselumi.png";
# temperature graph image web/url file name
$GRAPH_IMAGE_TEMPERATURE_URL_FILE_NAME = "ghousetemp.png";
# humidity graph image web/url file name
$GRAPH_IMAGE_HUMIDITY_URL_FILE_NAME = "/ghousehumi.png";
# soil moisture graph image web/url file name
$GRAPH_IMAGE_SOIL_MOISTURE_URL_FILE_NAME = "ghousesoil.png";

# define table field names to be retrieved from the SQLite database
$current_database_record_identifier = "";
$current_luminosity_value = "";
$current_temperature_value = "";
$current_humidity_value = "";
$current_soilmoisture_value = "";
$current_solenoidstatus_value = "";
$current_actuatorstatus_value = "";
$current_outputonestatus_value = "";
$current_outputtwostatus_value = "";
$current_outputthreestatus_value = "";
$current_record_date_value = "";
$current_record_time_value = "";


# read the current linear actuator status from a text file on disk instead of from the SQLite database file
$linear_actuator_status_file_pointer = fopen($ACTUATOR_STATUS_FILE_NAME, "r") or die("Unable to open file!");
$current_actuatorstatus_value_from_file_not_database = fgets($linear_actuator_status_file_pointer);
fclose($linear_actuator_status_file_pointer);

# read the solenoid valve status from a text file on disk instead of from the SQLite database file
$solenoid_status_file_pointer = fopen($SOLENOID_STATUS_FILE_NAME, "r") or die("Unable to open file!");
$current_solenoidstatus_value_from_file_not_database = fgets($solenoid_status_file_pointer);
fclose($solenoid_status_file_pointer);

# read the outputs status from a text file on disk instead of from the SQLite database file
$current_outputs_status_values_from_file_not_database = file($OUTPUTS_STATUS_FILE_NAME) or die("Unable to open file!");
$current_outputonestatus_value_from_file_not_database = $current_outputs_status_values_from_file_not_database[0];
$current_outputtwostatus_value_from_file_not_database = $current_outputs_status_values_from_file_not_database[1];
$current_outputthreestatus_value_from_file_not_database = $current_outputs_status_values_from_file_not_database[2];

# Open the database and execute a query returning the last row in the table
$db = new SQLite3($SQLITE_DATABASE_FILE_NAME) or print('<h1>Unable to open database!!!</h1>');






$query_results = $db->query('SELECT * FROM greenhouse ORDER BY id DESC LIMIT 1;') or print('<h1>Database select query failed</h1>');

while ($row_returned = $query_results->fetchArray())
{
  #print_r($row_returned);
  $current_database_record_identifier = $row_returned['id'];
  $current_luminosity_value = $row_returned['luminosity'];
  $current_temperature_value = $row_returned['temperature'];
  $current_humidity_value = $row_returned['humidity'];
  $current_soilmoisture_value = $row_returned['soilmoisture'];
  $current_solenoidstatus_value = $row_returned['solenoidstatus'];
  $current_actuatorstatus_value = $row_returned['actuatorstatus'];
  $current_outputonestatus_value = $row_returned['outputonestatus'];
  $current_outputtwostatus_value = $row_returned['outputtwostatus'];
  $current_outputthreestatus_value = $row_returned['outputthreestatus'];
  $current_record_date_value = $row_returned['currentdate'];
  $current_record_time_value = $row_returned['currenttime'];

   # display the data in a table 
   print "<h2 align=\"center\" valign=\"center\">Status Information</h2>";
   print "<table style=\"width:20%\" align=\"center\" valign=\"top\">\n";
   print "    <tr>\n";
   print "      <th>Reading Name</th>\n";
   print "      <th>Value</th>\n";
   print "    </tr>\n";
   print "    <tr>\n";
   print "      <td align=\"center\"><img src=\"/luminosity_icon.png\" alt=\"Luminosity Icon\"  height=\"100\" width=\"100\"><br>Luminosity</td>\n";
   print "      <td align=\"center\">$current_luminosity_value V</td>";
   print "    </tr>\n";
   print "    <tr>\n";
   print "      <td align=\"center\"><img src=\"/temperature_icon.png\" alt=\"Temperature Icon\"  height=\"100\" width=\"100\"><br>Temperature</td>\n";
   print "      <td align=\"center\">$current_temperature_value F</td>";
   print "    </tr>\n";
   print "    <tr>\n";
   print "      <td align=\"center\"><img src=\"/humidity_icon.png\" alt=\"Humidity Icon\"  height=\"100\" width=\"100\"><br>Humidity</td>\n";
   print "      <td align=\"center\">$current_humidity_value %</td>";
   print "    </tr>\n";
   print "    <tr>\n";
   print "      <td align=\"center\"><img src=\"/soil_icon.png\" alt=\"Soil Moisture Icon\"  height=\"100\" width=\"100\"><br>Soil Moisture</td>\n";
   print "      <td align=\"center\">$current_soilmoisture_value V</td>";
   print "    </tr>\n";
   print "    <tr>\n";
   print "      <td align=\"center\"><img src=\"/solenoid_icon.png\" alt=\"Solenoid Valve Icon\"  height=\"100\" width=\"100\"><br>Solenoid Valve</td>\n";
   #print "      <td align=\"center\">$current_solenoidstatus_value</td>";
   print "      <td align=\"center\">$current_solenoidstatus_value_from_file_not_database</td>";
   print "    </tr>\n";
   print "    <tr>";
   print "      <td align=\"center\"><img src=\"/actuator_icon.png\" alt=\"Linear Actuator Icon\"  height=\"100\" width=\"100\"><br>Linear Actuator</td>\n";
   #print "      <td align=\"center\">$current_actuatorstatus_value</td>";
   print "      <td align=\"center\">$current_actuatorstatus_value_from_file_not_database</td>";
   print "    </tr>\n";
   print "    <tr>\n";
   print "      <td align=\"center\"><img src=\"/output1_icon.png\" alt=\"Output One Icon\"  height=\"100\" width=\"100\"><br>Output One</td>\n";
   #print "      <td align=\"center\">$current_outputonestatus_value</td>";
   print "      <td align=\"center\">$current_outputonestatus_value_from_file_not_database</td>";
   print "    </tr>\n";
   print "    <tr>\n";
   print "      <td align=\"center\"><img src=\"/output2_icon.png\" alt=\"Output Two Icon\"  height=\"100\" width=\"100\"><br>Output Two</td>\n";
   #print "      <td align=\"center\">$current_outputtwostatus_value</td>";
   print "      <td align=\"center\">$current_outputtwostatus_value_from_file_not_database</td>";
   print "    </tr>\n";
   print "    <tr>\n";
   print "      <td align=\"center\"><img src=\"/output3_icon.png\" alt=\"Output Three Icon\"  height=\"100\" width=\"100\"><br>Output Three</td>\n";
   #print "      <td align=\"center\">$current_outputthreestatus_value</td>";
   print "      <td align=\"center\">$current_outputthreestatus_value_from_file_not_database</td>";
   print "    </tr>\n";
   print "    <tr>\n";
   print "      <td align=\"center\"><img src=\"/date_icon.png\" alt=\"Record Date Icon\"  height=\"100\" width=\"100\"><br>Record Date</td>\n";
   print "      <td align=\"center\">$current_record_date_value</td>";
   print "    </tr>\n";
   print "    <tr>\n";
   print "      <td align=\"center\"><img src=\"/time_icon.png\" alt=\"Record Time Icon\"  height=\"100\" width=\"100\"><br>Record Time</td>\n";
   print "      <td align=\"center\">$current_record_time_value</td>";
   print "    </tr>\n";
   print "  </table>\n";
}









print "      </td>";
print "      <td valign=\"top\">";









$timestamp = date('Y/m/d H:i:s A');
print "<center><h2>\n";
print $timestamp;
print "</h2>\n";
print "<a href=\"/greenhousehigh.jpg\">\n";
print "<img src=\"/greenhouselow.gif\" alt=\"Greenhouse Camera Image - Animated GIF file\"  height=\"240\" width=\"320\" border=\"5\">\n";
print "<br>Click for high resolution</center></a>";
print "<br>\n";

# display graphs generated by greenhouse.py showing the last 24 hours of data

print "<h2 align=\"center\">Graphical Environmental Record<br>(24 Hours)</h2>\n";
print "<table align=\"center\">\n";
print "    <thead>\n";
print "        <tr>\n";
print "         <th>Luminosity</th>\n";
print "         <td><img src=\"$GRAPH_IMAGE_LUMINOSITY_URL_FILE_NAME\" alt=\"Greenhouse Luminosity (Last 24 Hours)\" height=\"240\" width=\"320\"></td>\n";
print "        </tr>\n";
print "        <tr>\n";
print "         <th>Temperature</th>\n";
print "         <td><img src=\"$GRAPH_IMAGE_TEMPERATURE_URL_FILE_NAME\" alt=\"Greenhouse Temperature (Last 24 Hours)\" height=\"240\" width=\"320\"></td>\n";
print "        </tr>\n";
print "        <tr>\n";
print "         <th>Humidity</th>\n";
print "         <td><img src=\"$GRAPH_IMAGE_HUMIDITY_URL_FILE_NAME\" alt=\"Greenhouse Humidity (Last 24 Hours)\" height=\"240\" width=\"320\"></td>\n";
print "        </tr>\n";
print "        <tr>\n";
print "         <th>Soil Mositure</th>\n";
print "         <td><img src=\"$GRAPH_IMAGE_SOIL_MOISTURE_URL_FILE_NAME\" alt=\"Greenhouse Soil Moisture (Last 24 Hours)\" height=\"240\" width=\"320\"></td>\n";
print "        </tr>\n";
print "    </thead>\n";
print "    <tbody>\n";
print "        <tr>\n";
print "        </tr>\n";
print "    <tbody>\n";
print "</table>\n";




print "<br><br><h3 align=\"center\">Automation System Wiring Diagram<br><br><a href=\"/wiringhigh.png\"><img src=\"/wiringlow.png\" alt=\"Automation System Wiring Diagram\"><a></h3>";




print "   </td>";
print "   <td>";

?>
<h2 align="center"><p><span class="error">Manual Operations</span></p></h2>
<table style="width:20%" align="center">
  <tr>
    <th>Action Description</th>
    <th>Action Button</th> 
  </tr>
  <tr>
    <td align="right">Open the window manually:</td>
    <td align="center"><br><form action="openwindowmanual.php" method="post">
    <input type="image" src="window_open.png" width="100" height="100" alt="Manually open the window" border="1">
    </form></td>
  </tr>
  <tr>
    <td align="right">Close the window manually:</td>
    <td align="center"><br><form action="closewindowmanual.php" method="post">
    <input type="image" src="window_closed.png" width="100" height="100" alt="Manually close the window" border="1">
    </form></td>
  </tr>
  <tr>
    <td align="right">Open the solenoid valve manually:</td>
    <td align="center"><br><form action="opensolenoidmanual.php" method="post">
    <input type="image" src="solenoid_valve_open.png" width="100" height="100" alt="Manually open the solenoid valve" border="1">
    </form></td>
  </tr>

  <tr>
    <td align="right">Close the solenoid valve manually:</td>
    <td align="center"><br><form action="closesolenoidwmanual.php" method="post">
    <input type="image" src="solenoid_valve_closed.png" width="100" height="100" alt="Manually close the solenoid valve" border="1">
    </form></td>
  </tr>

  <tr>
    <td align="right">Enable output one manually:</td>
    <td align="center"><br><form action="openoutputonemanual.php" method="post">
    <input type="image" src="out_put_on.png" width="100" height="100" alt="Manually enable output one" border="1">
    </form></td>
  </tr>

  <tr>
    <td align="right">Disable output one manually:</td>
    <td align="center"><br><form action="closeoutputonemanual.php" method="post">
    <input type="image" src="out_put_off.png" width="100" height="100" alt="Manually disable output one" border="1">
    </form></td>
  </tr>

  <tr>
    <td align="right">Enable output two manually:</td>
    <td align="center"><br><form action="openoutputtwomanual.php" method="post">
    <input type="image" src="out_put_on.png" width="100" height="100" alt="Manually enable output two" border="1">
    </form></td>
  </tr>

  <tr>
    <td align="right">Disable output two manually:</td>
    <td align="center"><br><form action="closeoutputtwomanual.php" method="post">
    <input type="image" src="out_put_off.png" width="100" height="100" alt="Manually disable output two" border="1">
    </form></td>
  </tr>

  <tr>
    <td align="right">Enable output three manually:</td>
    <td align="center"><br><form action="openoutputthreemanual.php" method="post">
    <input type="image" src="out_put_on.png" width="100" height="100" alt="Manually enable output three" border="1">
    </form></td>
  </tr>

  <tr>
    <td align="right">Disable output three manually:</td>
    <td align="center"><br><form action="closeoutputonemanual.php" method="post">
    <input type="image" src="out_put_off.png" width="100" height="100" alt="Manually disable output three" border="1">
    </form>
   </td>
  </tr>
</table>


<?php





print "<p align=\"center\">Note: Manually performing operations are not reflected anywhere in this system.</p>";

print "   </td>";
print "    </tr>";
print "</table>";



 




print "<br><h2 align=\"center\">Environmental Record (24 Hours)</h2>\n";

# execute a query returning the last 720 records (greenhouse.py is executed every two minutes) = the last 24 hours.
$query_results = $db->query('SELECT * FROM greenhouse ORDER BY id DESC LIMIT 720;') or print('<h1>Greenhouse.db select query failed</h1>');

# make the table scrollable
print "<div class=\"table-wrapper-scroll-y the-table-scrollbar\">\n";

# display a table containing the last 24 hours of the environmental record
print "<table class=\"table table-bordered table-striped mb-0\" align=\"center\">\n";
print "    <thead>\n";
print "        <tr>\n";
print "         <th scope=\"col\">Luminosity</th>\n";
print "         <th scope=\"col\">Temp.</th>\n";
print "         <th scope=\"col\">Humidity</th>\n";
print "         <th scope=\"col\">Soil M.</th>\n";
print "         <th scope=\"col\">Solenoid</th>\n";
print "         <th scope=\"col\">Actuator</th>\n";
print "         <th scope=\"col\">Out. #1</th>\n";
print "         <th scope=\"col\">Out. #2</th>\n";
print "         <th scope=\"col\">Out. #3</th>\n";
print "         <th scope=\"col\">Date</th>\n";
print "         <th scope=\"col\">Time</th>\n";
print "        </tr>\n";
print "    </thead>\n";
print "    <tbody>\n";


while ($row_returned = $query_results->fetchArray())
{

	print "        <tr>\n";
	print "         <td scope=\"row\">{$row_returned['luminosity']} Volts</td>\n";
	print "         <td>{$row_returned['temperature']} F</td>\n";
	print "         <td>{$row_returned['humidity']} %</td>\n";
	print "         <td>{$row_returned['soilmoisture']} Volts</td>\n";
	print "         <td>{$row_returned['solenoidstatus']}</td>\n";
	print "         <td>{$row_returned['actuatorstatus']}</td>\n";
	print "         <td>{$row_returned['outputonestatus']}</td>\n";
	print "         <td>{$row_returned['outputtwostatus']}</td>\n";
	print "         <td>{$row_returned['outputthreestatus']}</td>\n";
	print "         <td>{$row_returned['currentdate']}</td>\n";
	print "         <td>{$row_returned['currenttime']}</td>\n";
	print "        </tr>\n";

}

print "    <tbody>\n";
print "</table>\n";
print "</div>\n";







# define the variables using during form submission
$LINEAR_ACTUATOR_RUNTIME_VALUE = "";
$MINIMUM_TEMPERATURE_SENSOR_ACTUATOR_RETRACT_VALUE = "";
$MINIMUM_TEMPERATURE_SENSOR_OUTPUT_ONE_OFF_VALUE = "";
$MINIMUM_HUMIDITY_SENSOR_OUTPUT_ONE_OFF_VALUE = "";
$MINIMUM_TEMPERATURE_SENSOR_OUTPUT_TWO_OFF_VALUE = "";
$MINIMUM_LUMINOSITY_SENSOR_OUTPUT_TWO_OFF_VALUE = "";
$MINIMUM_SOIL_MOISTURE_SENSOR_SOLENOID_VALVE_OPEN_VALUE = "";
$OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE = "";

# define the variables used to detect incomplete/unallowed form submission values
$LINEAR_ACTUATOR_RUNTIME_VALUE_Err = "";
$MINIMUM_LUMINOSITY_SENSOR_ACTUATOR_RETRACT_VALUE_Err = "";
$MINIMUM_TEMPERATURE_SENSOR_ACTUATOR_RETRACT_VALUE_Err = "";
$MINIMUM_HUMIDITY_SENSOR_ACTUATOR_RETRACT_VALUE_Err = "";
$MINIMUM_TEMPERATURE_SENSOR_OUTPUT_ONE_OFF_VALUE_Err = "";
$MINIMUM_HUMIDITY_SENSOR_OUTPUT_ONE_OFF_VALUE_Err = "";
$MINIMUM_TEMPERATURE_SENSOR_OUTPUT_TWO_OFF_VALUE_Err = "";
$MINIMUM_LUMINOSITY_SENSOR_OUTPUT_TWO_OFF_VALUE_Err = "";
$MINIMUM_SOIL_MOISTURE_SENSOR_SOLENOID_VALVE_OPEN_VALUE_Err = "";
$OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE_Err = "";

# define the file names of control values stored on disk
$LINEAR_ACTUATOR_RUNTIME_VALUE_FILE_NAME = '/var/www/html/actuatorruntime.txt';
$MINIMUM_TEMPERATURE_SENSOR_ACTUATOR_RETRACT_VALUE_FILE_NAME = '/var/www/html/mintemactretract.txt';
$MINIMUM_TEMPERATURE_SENSOR_OUTPUT_ONE_OFF_VALUE_FILE_NAME = '/var/www/html/mintemoutoneoff.txt';
$MINIMUM_HUMIDITY_SENSOR_OUTPUT_ONE_OFF_VALUE_FILE_NAME = '/var/www/html/minhumoutoneoff.txt';
$MINIMUM_TEMPERATURE_SENSOR_OUTPUT_TWO_OFF_VALUE_FILE_NAME = '/var/www/html/mintemouttwooff.txt';
$MINIMUM_LUMINOSITY_SENSOR_OUTPUT_TWO_OFF_VALUE_FILE_NAME = '/var/www/html/minlumouttwooff.txt';
$MINIMUM_SOIL_MOISTURE_SENSOR_SOLENOID_VALVE_OPEN_VALUE_FILE_NAME = '/var/www/html/minsoilsoleopen.txt';
$OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE_FILE_NAME = '/var/www/html/outtwotemlum.txt';

# read linear actuator runtime value file name (seconds)
$linear_actuator_runtime_file_pointer = fopen($LINEAR_ACTUATOR_RUNTIME_VALUE_FILE_NAME, "r") or die("Unable to open file!");
$LINEAR_ACTUATOR_RUNTIME_VALUE = fgets($linear_actuator_runtime_file_pointer);
fclose($linear_actuator_runtime_file_pointer);

# read minimum temperature sensor actuator retraction value file name (degrees)
$minimum_temperature_actuator_retract_file_pointer = fopen($MINIMUM_TEMPERATURE_SENSOR_ACTUATOR_RETRACT_VALUE_FILE_NAME, "r") or die("Unable to open file!");
$MINIMUM_TEMPERATURE_SENSOR_ACTUATOR_RETRACT_VALUE = fgets($minimum_temperature_actuator_retract_file_pointer);
fclose($minimum_temperature_actuator_retract_file_pointer);

# read minimum temperature sensor output one off value file name (degrees)
$minimum_temperature_output_one_off_file_pointer = fopen($MINIMUM_TEMPERATURE_SENSOR_OUTPUT_ONE_OFF_VALUE_FILE_NAME, "r") or die("Unable to open file!");
$MINIMUM_TEMPERATURE_SENSOR_OUTPUT_ONE_OFF_VALUE = fgets($minimum_temperature_output_one_off_file_pointer);
fclose($minimum_temperature_output_one_off_file_pointer);

# read minimum humidity sensor output one off value file name (percrent)
$minimum_humidity_output_one_off_file_pointer = fopen($MINIMUM_HUMIDITY_SENSOR_OUTPUT_ONE_OFF_VALUE_FILE_NAME, "r") or die("Unable to open file!");
$MINIMUM_HUMIDITY_SENSOR_OUTPUT_ONE_OFF_VALUE = fgets($minimum_humidity_output_one_off_file_pointer);
fclose($minimum_humidity_output_one_off_file_pointer);

# read minimum temperature sensor output two off value file name (degrees)
$minimum_temperature_output_two_off_file_pointer = fopen($MINIMUM_TEMPERATURE_SENSOR_OUTPUT_TWO_OFF_VALUE_FILE_NAME, "r") or die("Unable to open file!");
$MINIMUM_TEMPERATURE_SENSOR_OUTPUT_TWO_OFF_VALUE = fgets($minimum_temperature_output_two_off_file_pointer);
fclose($minimum_temperature_output_two_off_file_pointer);

# read minimum luminosity sensor output two off value file name (volts)
$minimum_luminosity_output_two_off_file_pointer = fopen($MINIMUM_LUMINOSITY_SENSOR_OUTPUT_TWO_OFF_VALUE_FILE_NAME, "r") or die("Unable to open file!");
$MINIMUM_LUMINOSITY_SENSOR_OUTPUT_TWO_OFF_VALUE = fgets($minimum_luminosity_output_two_off_file_pointer);
fclose($minimum_luminosity_output_two_off_file_pointer);

# read minimum soil moisture sensor open solenoid valve value file name (volts)
$minimum_soil_moisture_solenoid_valve_open_file_pointer = fopen($MINIMUM_SOIL_MOISTURE_SENSOR_SOLENOID_VALVE_OPEN_VALUE_FILE_NAME, "r") or die("Unable to open file!");
$MINIMUM_SOIL_MOISTURE_SENSOR_SOLENOID_VALVE_OPEN_VALUE = fgets($minimum_soil_moisture_solenoid_valve_open_file_pointer);
fclose($minimum_soil_moisture_solenoid_valve_open_file_pointer);

# read output two configuration between using temperature or luminosity value file name (Temperature | Luminosity)
$output_two_configure_temperature_or_luminosity_file_pointer = fopen($OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE_FILE_NAME, "r") or die("Unable to open file!");
$OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE = fgets($output_two_configure_temperature_or_luminosity_file_pointer);
fclose($output_two_configure_temperature_or_luminosity_file_pointer);

# process form submission data
if ($_SERVER["REQUEST_METHOD"] == "POST") {

# clean the form input data values using test_input(), verify the data values are not blank, 
# and verify the data values contain only allowed characters
if (empty($_POST["LINEAR_ACTUATOR_RUNTIME_VALUE"])) {
  $LINEAR_ACTUATOR_RUNTIME_VALUE_Err = "LINEAR_ACTUATOR_RUNTIME_VALUE is required";
} else {
  $LINEAR_ACTUATOR_RUNTIME_VALUE = test_input($_POST["LINEAR_ACTUATOR_RUNTIME_VALUE"]);
  // check if LINEAR_ACTUATOR_RUNTIME_VALUE only contains letters and whitespace
  if (!preg_match("/^[0-9\.]*$/",$LINEAR_ACTUATOR_RUNTIME_VALUE)) {
    $LINEAR_ACTUATOR_RUNTIME_VALUE_Err = "Only numbers allowed";
}
}

if (empty($_POST["MINIMUM_TEMPERATURE_SENSOR_ACTUATOR_RETRACT_VALUE"])) {
  $MINIMUM_TEMPERATURE_SENSOR_ACTUATOR_RETRACT_VALUE_Err = "MINIMUM_TEMPERATURE_SENSOR_ACTUATOR_RETRACT_VALUE is required";
} else {
  $MINIMUM_TEMPERATURE_SENSOR_ACTUATOR_RETRACT_VALUE = test_input($_POST["MINIMUM_TEMPERATURE_SENSOR_ACTUATOR_RETRACT_VALUE"]);
  // check if MINIMUM_TEMPERATURE_SENSOR_ACTUATOR_RETRACT_VALUE only contains letters and whitespace
  if (!preg_match("/^[0-9\.]*$/",$MINIMUM_TEMPERATURE_SENSOR_ACTUATOR_RETRACT_VALUE)) {
    $MINIMUM_TEMPERATURE_SENSOR_ACTUATOR_RETRACT_VALUE_Err = "Only numbers allowed";
}
}

if (empty($_POST["MINIMUM_TEMPERATURE_SENSOR_OUTPUT_ONE_OFF_VALUE"])) {
  $MINIMUM_TEMPERATURE_SENSOR_OUTPUT_ONE_OFF_VALUE_Err = "MINIMUM_TEMPERATURE_SENSOR_OUTPUT_ONE_OFF_VALUE is required";
} else {
  $MINIMUM_TEMPERATURE_SENSOR_OUTPUT_ONE_OFF_VALUE = test_input($_POST["MINIMUM_TEMPERATURE_SENSOR_OUTPUT_ONE_OFF_VALUE"]);
  // check if MINIMUM_TEMPERATURE_SENSOR_OUTPUT_ONE_OFF_VALUE only contains letters and whitespace
  if (!preg_match("/^[0-9\.]*$/",$MINIMUM_TEMPERATURE_SENSOR_OUTPUT_ONE_OFF_VALUE)) {
    $MINIMUM_TEMPERATURE_SENSOR_OUTPUT_ONE_OFF_VALUE_Err = "Only numbers allowed";
}
}

if (empty($_POST["MINIMUM_HUMIDITY_SENSOR_OUTPUT_ONE_OFF_VALUE"])) {
  $MINIMUM_HUMIDITY_SENSOR_OUTPUT_ONE_OFF_VALUE_Err = "MINIMUM_HUMIDITY_SENSOR_OUTPUT_ONE_OFF_VALUE is required";
} else {
  $MINIMUM_HUMIDITY_SENSOR_OUTPUT_ONE_OFF_VALUE = test_input($_POST["MINIMUM_HUMIDITY_SENSOR_OUTPUT_ONE_OFF_VALUE"]);
  // check if MINIMUM_HUMIDITY_SENSOR_OUTPUT_ONE_OFF_VALUE only contains letters and whitespace
  if (!preg_match("/^[0-9\.]*$/",$MINIMUM_HUMIDITY_SENSOR_OUTPUT_ONE_OFF_VALUE)) {
    $MINIMUM_HUMIDITY_SENSOR_OUTPUT_ONE_OFF_VALUE_Err = "Only numbers allowed";
}
}

if (empty($_POST["MINIMUM_TEMPERATURE_SENSOR_OUTPUT_TWO_OFF_VALUE"])) {
  $MINIMUM_TEMPERATURE_SENSOR_OUTPUT_TWO_OFF_VALUE_Err = "MINIMUM_TEMPERATURE_SENSOR_OUTPUT_TWO_OFF_VALUE is required";
} else {
  $MINIMUM_TEMPERATURE_SENSOR_OUTPUT_TWO_OFF_VALUE = test_input($_POST["MINIMUM_TEMPERATURE_SENSOR_OUTPUT_TWO_OFF_VALUE"]);
  // check if MINIMUM_TEMPERATURE_SENSOR_OUTPUT_TWO_OFF_VALUE only contains letters and whitespace
  if (!preg_match("/^[0-9\.]*$/",$MINIMUM_TEMPERATURE_SENSOR_OUTPUT_TWO_OFF_VALUE)) {
    $MINIMUM_TEMPERATURE_SENSOR_OUTPUT_TWO_OFF_VALUE_Err = "Only numbers allowed";
}
}

if (empty($_POST["MINIMUM_LUMINOSITY_SENSOR_OUTPUT_TWO_OFF_VALUE"])) {
  $MINIMUM_LUMINOSITY_SENSOR_OUTPUT_TWO_OFF_VALUE_Err = "TEMPLATE is required";
} else {
  $MINIMUM_LUMINOSITY_SENSOR_OUTPUT_TWO_OFF_VALUE = test_input($_POST["MINIMUM_LUMINOSITY_SENSOR_OUTPUT_TWO_OFF_VALUE"]);
  // check if MINIMUM_LUMINOSITY_SENSOR_OUTPUT_TWO_OFF_VALUE only contains letters and whitespace
  if (!preg_match("/^[0-9\.]*$/",$MINIMUM_LUMINOSITY_SENSOR_OUTPUT_TWO_OFF_VALUE)) {
    $MINIMUM_LUMINOSITY_SENSOR_OUTPUT_TWO_OFF_VALUE_Err = "Only letters and white space allowed";
}
}

if (empty($_POST["MINIMUM_SOIL_MOISTURE_SENSOR_SOLENOID_VALVE_OPEN_VALUE"])) {
  $MINIMUM_SOIL_MOISTURE_SENSOR_SOLENOID_VALVE_OPEN_VALUE_Err = "MINIMUM_SOIL_MOISTURE_SENSOR_SOLENOID_VALVE_OPEN_VALUE is required";
} else {
  $MINIMUM_SOIL_MOISTURE_SENSOR_SOLENOID_VALVE_OPEN_VALUE = test_input($_POST["MINIMUM_SOIL_MOISTURE_SENSOR_SOLENOID_VALVE_OPEN_VALUE"]);
  // check if MINIMUM_SOIL_MOISTURE_SENSOR_SOLENOID_VALVE_OPEN_VALUE only contains letters and whitespace
  if (!preg_match("/^[0-9\.]*$/",$MINIMUM_SOIL_MOISTURE_SENSOR_SOLENOID_VALVE_OPEN_VALUE)) {
    $MINIMUM_SOIL_MOISTURE_SENSOR_SOLENOID_VALVE_OPEN_VALUE_Err = "Only numbers allowed";
}
}

if (empty($_POST["OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE"])) {
  $OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE_Err = "OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE is required";
} else {
  $OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE = test_input($_POST["OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE"]);
  // check if OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE only contains letters and whitespace
  if (!preg_match("/^[a-zA-Z]*$/",$OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE)) {
    $OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE_Err = "Only letters allowed";
}
}

if ($_SERVER["REQUEST_METHOD"] == "POST" &&
    empty($LINEAR_ACTUATOR_RUNTIME_VALUE_Err) &&
    empty($MINIMUM_TEMPERATURE_SENSOR_ACTUATOR_RETRACT_VALUE_Err) &&
    empty($MINIMUM_TEMPERATURE_SENSOR_OUTPUT_ONE_OFF_VALUE_Err) &&
    empty($MINIMUM_HUMIDITY_SENSOR_OUTPUT_ONE_OFF_VALUE_Err) &&
    empty($MINIMUM_TEMPERATURE_SENSOR_OUTPUT_TWO_OFF_VALUE_Err) &&
    empty($MINIMUM_LUMINOSITY_SENSOR_OUTPUT_TWO_OFF_VALUE_Err) &&
    empty($MINIMUM_SOIL_MOISTURE_SENSOR_SOLENOID_VALVE_OPEN_VALUE_Err) &&
    empty($OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE_Err))

{

# display a saved values confirmation message when successful
print "<br><br><br>\n<h2 align=\"center\" style=\"color:blue;\">Automation system configuration values saved!</h2>\n";

}

# write linear actuator runtime value file name (seconds)
$linear_actuator_runtime_file_pointer = fopen($LINEAR_ACTUATOR_RUNTIME_VALUE_FILE_NAME, "w") or die("Unable to open file!");
fwrite($linear_actuator_runtime_file_pointer, $LINEAR_ACTUATOR_RUNTIME_VALUE);
fclose($linear_actuator_runtime_file_pointer);

# write minimum temperature sensor actuator retraction value file name (degrees)
$minimum_temperature_actuator_retract_file_pointer = fopen($MINIMUM_TEMPERATURE_SENSOR_ACTUATOR_RETRACT_VALUE_FILE_NAME, "w") or die("Unable to open file!");
fwrite($minimum_temperature_actuator_retract_file_pointer, $MINIMUM_TEMPERATURE_SENSOR_ACTUATOR_RETRACT_VALUE);
fclose($minimum_temperature_actuator_retract_file_pointer);

# write minimum temperature sensor output one off value file name (degrees)
$minimum_temperature_output_one_off_file_pointer = fopen($MINIMUM_TEMPERATURE_SENSOR_OUTPUT_ONE_OFF_VALUE_FILE_NAME, "w") or die("Unable to open file!");
fwrite($minimum_temperature_output_one_off_file_pointer, $MINIMUM_TEMPERATURE_SENSOR_OUTPUT_ONE_OFF_VALUE);
fclose($minimum_temperature_output_one_off_file_pointer);

# write minimum humidity sensor output one off value file name (percrent)
$minimum_humidity_output_one_off_file_pointer = fopen($MINIMUM_HUMIDITY_SENSOR_OUTPUT_ONE_OFF_VALUE_FILE_NAME, "w") or die("Unable to open file!");
fwrite($minimum_humidity_output_one_off_file_pointer, $MINIMUM_HUMIDITY_SENSOR_OUTPUT_ONE_OFF_VALUE);
fclose($minimum_humidity_output_one_off_file_pointer);

# write minimum temperature sensor output two off value file name (degrees)
$minimum_temperature_output_two_off_file_pointer = fopen($MINIMUM_TEMPERATURE_SENSOR_OUTPUT_TWO_OFF_VALUE_FILE_NAME, "w") or die("Unable to open file!");
fwrite($minimum_temperature_output_two_off_file_pointer, $MINIMUM_TEMPERATURE_SENSOR_OUTPUT_TWO_OFF_VALUE);
fclose($minimum_temperature_output_two_off_file_pointer);

# write minimum luminosity sensor output two off value file name (volts)
$minimum_luminosity_output_two_off_file_pointer = fopen($MINIMUM_LUMINOSITY_SENSOR_OUTPUT_TWO_OFF_VALUE_FILE_NAME, "w") or die("Unable to open file!");
fwrite($minimum_luminosity_output_two_off_file_pointer, $MINIMUM_LUMINOSITY_SENSOR_OUTPUT_TWO_OFF_VALUE);
fclose($minimum_luminosity_output_two_off_file_pointer);

# write minimum soil moisture sensor open solenoid valve value file name (volts)
$minimum_soil_moisture_solenoid_valve_open_file_pointer = fopen($MINIMUM_SOIL_MOISTURE_SENSOR_SOLENOID_VALVE_OPEN_VALUE_FILE_NAME, "w") or die("Unable to open file!");
fwrite($minimum_soil_moisture_solenoid_valve_open_file_pointer, $MINIMUM_SOIL_MOISTURE_SENSOR_SOLENOID_VALVE_OPEN_VALUE);
fclose($minimum_soil_moisture_solenoid_valve_open_file_pointer);

# write output two configuration between using temperature or luminosity value file name (Temperature | Luminosity)
$output_two_configure_temperature_or_luminosity_file_pointer = fopen($OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE_FILE_NAME, "w") or die("Unable to open file!");
fwrite($output_two_configure_temperature_or_luminosity_file_pointer, $OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE);
fclose($output_two_configure_temperature_or_luminosity_file_pointer);

}

# display a form containing the system configuration values
?>
<br><br>
<h2 align="center">Automation System Configuration Values<br>
<span class="error">* required field</span></h2>
<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
 <table style="width:50%" align="center">
  <tr>
    <th style="width:80%;">Value Description</th>
    <th style="width:20%;">Value</th> 
  </tr>
  <tr>
    <td align="right">LINEAR_ACTUATOR_RUNTIME_VALUE: =</td>
    <td align="left"><br><input type="text" name="LINEAR_ACTUATOR_RUNTIME_VALUE" size="5" value="<?php echo $LINEAR_ACTUATOR_RUNTIME_VALUE;?>">
  <span class="error">Seconds * <?php echo $LINEAR_ACTUATOR_RUNTIME_VALUE_Err;?></span>
  <br><br>
    </td>
  </tr>
  <tr>
    <td align="right">MINIMUM_TEMPERATURE_SENSOR_ACTUATOR_RETRACT_VALUE: <=<br><br>
		      Logic: When the temperature reaches the minimum specified value retract the actuator (Close Window)
    </td>
    <td align="left"><input type="text" name="MINIMUM_TEMPERATURE_SENSOR_ACTUATOR_RETRACT_VALUE" size="5" value="<?php echo $MINIMUM_TEMPERATURE_SENSOR_ACTUATOR_RETRACT_VALUE;?>"
  <span class="error">Degrees F * <?php echo $MINIMUM_TEMPERATURE_SENSOR_ACTUATOR_RETRACT_VALUE_Err;?></span><br><br><br>
   <br>
    </td>
  </tr>
  <tr>
    <td align="right">MINIMUM_TEMPERATURE_SENSOR_OUTPUT_ONE_OFF_VALUE: <=<br>
		      AND MINIMUM_HUMIDITY_SENSOR_OUTPUT_ONE_OFF_VALUE: <=<br><br>
		      Logic: When the temperature reaches the minimum specified value AND when the humidity reaches the minimum specified value turn off output #1 (Fan).
    </td>
    <td align="left"><input type="text" name="MINIMUM_TEMPERATURE_SENSOR_OUTPUT_ONE_OFF_VALUE" size="5" value="<?php echo $MINIMUM_TEMPERATURE_SENSOR_OUTPUT_ONE_OFF_VALUE;?>">
  <span class="error">Degrees F * <?php echo $MINIMUM_TEMPERATURE_SENSOR_OUTPUT_ONE_OFF_VALUE_Err;?></span>
   <br><input type="text" name="MINIMUM_HUMIDITY_SENSOR_OUTPUT_ONE_OFF_VALUE" size="5" value="<?php echo $MINIMUM_HUMIDITY_SENSOR_OUTPUT_ONE_OFF_VALUE;?>">
  <span class="error">% 0-100 * <?php echo $MINIMUM_HUMIDITY_SENSOR_OUTPUT_ONE_OFF_VALUE_Err;?></span><br><br><br><br>
    </td>
  </tr>
  <tr>
    <td align="right">OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE:</td>
    <td align="left"><br>
  <input type="radio" name="OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE" <?php if (isset($OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE) && trim($OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE) == "Temperature") echo "checked";?> value="Temperature">Temperature*<br>
  <input type="radio" name="OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE" <?php if (isset($OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE) && trim($OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE) == "Luminosity") echo "checked";?> value="Luminosity">Luminosity
  <span class="error">* <?php echo $OUTPUT_TWO_CONFIGURATION_BETWEEN_TEMPERATURE_OR_LUMINOSITY_VALUE_Err;?></span>
  <br>
    </td>
  </tr>
  <tr>
    <td align="right">MINIMUM_TEMPERATURE_SENSOR_OUTPUT_TWO_OFF_VALUE: <=<br><br>
		      Logic: When the temperature reaches the minimum specified value turn off output two.
    </td>
    <td align="left"><br><input type="text" name="MINIMUM_TEMPERATURE_SENSOR_OUTPUT_TWO_OFF_VALUE" size="5" value="<?php echo $MINIMUM_TEMPERATURE_SENSOR_OUTPUT_TWO_OFF_VALUE;?>">
  <span class="error">Degrees F * <?php echo $MINIMUM_TEMPERATURE_SENSOR_OUTPUT_TWO_OFF_VALUE_Err;?></span><br><br>
  <br><br>
    </td>
  </tr>
  <tr>
    <td align="right">MINIMUM_LUMINOSITY_SENSOR_OUTPUT_TWO_OFF_VALUE: <=<br><br>
		      Logic: When the luminosity reaches the minimum specified value turn off output two.
    </td>
    <td align="left"><br><input type="text" name="MINIMUM_LUMINOSITY_SENSOR_OUTPUT_TWO_OFF_VALUE" size="5" value="<?php echo $MINIMUM_LUMINOSITY_SENSOR_OUTPUT_TWO_OFF_VALUE;?>">
  <span class="error">Volts 0-5 * <?php echo $MINIMUM_LUMINOSITY_SENSOR_OUTPUT_TWO_OFF_VALUE_Err;?></span><br><br>
  <br><br>
    </td>
  </tr>
  <tr>
    <td align="right">MINIMUM_SOIL_MOISTURE_SENSOR_SOLENOID_VALVE_OPEN_VALUE: >=</td>
    <td align="left"><br><input type="text" name="MINIMUM_SOIL_MOISTURE_SENSOR_SOLENOID_VALVE_OPEN_VALUE" size="5" value="<?php echo $MINIMUM_SOIL_MOISTURE_SENSOR_SOLENOID_VALVE_OPEN_VALUE;?>">
  <span class="error">Volts 0-5 * <?php echo $MINIMUM_SOIL_MOISTURE_SENSOR_SOLENOID_VALVE_OPEN_VALUE_Err;?></span>
  <br><br>
    </td>
  </tr>
 </table>
  <center>
    <input type="image" src="save_settings.png" width="100" height="100" alt="Save automation system configuration values">
</form>
</center>
<br><br>

<?php

print "<br><br>\n<center>This page generated: ";
print $timestamp = date('Y/m/d H:i:s A');
print "</center>";


function test_input($data) {
  $data = trim($data);
  $data = stripslashes($data);
  $data = htmlspecialchars($data);
  return $data;
}




?>
 </center>
</body>
</html>

