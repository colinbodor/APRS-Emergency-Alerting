<?php
require_once("includes/config.inc.php");
require_once("includes/functions.inc.php");

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}


?>


<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4="crossorigin="anonymous"></script>

<script src="https://polyfill.io/v3/polyfill.min.js?features=default"></script>



    <script src="script.js"></script>
    <link rel="stylesheet" href="style.css">

    <title>Hazard Scape</title>

<script>

const fire_out_of_control = [
<?php
$sql = "SELECT * FROM `fedfire` WHERE `stage_of_control` LIKE '%OC%'";
$fedfire_result = $conn->query($sql);

if ($fedfire_result->num_rows > 0) {
  while($row = $fedfire_result->fetch_assoc()) {
    echo "[\"" . $row["firename"]. "\", " . $row["lat"]. ", " . $row["lon"]. ", ". $row["id"]. "],";
  }
}
?>
];

const fire_being_held = [
<?php
$sql = "SELECT * FROM `fedfire` WHERE `stage_of_control` LIKE '%BH%'";
$fedfire_result = $conn->query($sql);

if ($fedfire_result->num_rows > 0) {
  while($row = $fedfire_result->fetch_assoc()) {
    echo "[\"" . $row["firename"]. "\", " . $row["lat"]. ", " . $row["lon"]. ", ". $row["id"]. "],";
  }
}
?>
];

const fire_under_control = [
<?php
$sql = "SELECT * FROM `fedfire` WHERE `stage_of_control` LIKE '%UC%'";
$fedfire_result = $conn->query($sql);

if ($fedfire_result->num_rows > 0) {
  while($row = $fedfire_result->fetch_assoc()) {
    echo "[\"" . $row["firename"]. "\", " . $row["lat"]. ", " . $row["lon"]. ", ". $row["id"]. "],";
  }
}
?>
];





function setMarkers_fire_out_of_control(map) {
  const image = {
    url: "images/fire_out_of_control.png",
    size: new google.maps.Size(20, 32),
    origin: new google.maps.Point(0, 0),
    anchor: new google.maps.Point(0, 32),
  };
  const shape = {
    coords: [1, 1, 1, 32, 20, 32, 20, 1],
    type: "poly",
  };
  for (let i = 0; i < fire_out_of_control.length; i++) {
    const fire = fire_out_of_control[i];
    new google.maps.Marker({
      position: { lat: fire[1], lng: fire[2] },
      map,
      icon: image,
      shape: shape,
      title: fire[0],
      zIndex: fire[3],
    });
  }
}


function setMarkers_fire_being_held(map) {
  const image = {
    url: "images/fire_being_held.png",
    size: new google.maps.Size(20, 32),
    origin: new google.maps.Point(0, 0),
    anchor: new google.maps.Point(0, 32),
  };
  const shape = {
    coords: [1, 1, 1, 32, 20, 32, 20, 1],
    type: "poly",
  };
  for (let i = 0; i < fire_being_held.length; i++) {
    const fire = fire_being_held[i];
    new google.maps.Marker({
      position: { lat: fire[1], lng: fire[2] },
      map,
      icon: image,
      shape: shape,
      title: fire[0],
      zIndex: fire[3],
    });
  }
}

function setMarkers_fire_under_control(map) {
  const image = {
    url: "images/fire_under_control.png",
    size: new google.maps.Size(20, 32),
    origin: new google.maps.Point(0, 0),
    anchor: new google.maps.Point(0, 32),
  };
  const shape = {
    coords: [1, 1, 1, 32, 20, 32, 20, 1],
    type: "poly",
  };
  for (let i = 0; i < fire_under_control.length; i++) {
    const fire = fire_under_control[i];
    new google.maps.Marker({
      position: { lat: fire[1], lng: fire[2] },
      map,
      icon: image,
      shape: shape,
      title: fire[0],
      zIndex: fire[3],
    });
  }
}






</script>





</head>
<body>
<div class="container">

<?php

//this correct list of province/territory? think I am missing some
$sql = "SELECT count(*) as total from fedfire WHERE agency NOT IN ('nrcc')";
$result = $conn->query($sql);
$row = $result->fetch_assoc();
$fedfire_total = $row['total'];

$sql = "SELECT count(*) as total from abroads";
$result = $conn->query($sql);
$row = $result->fetch_assoc();
$abroads_total = $row['total'];

$sql = "SELECT * FROM naads_heartbeat";
$result = $conn->query($sql);
if ($result->num_rows > 0) {
  while($row = $result->fetch_assoc()) {
    $heartbeat_naads_sent =  $row["sent"];
  }
}


?>
<br />
<div class="alert alert-danger" role="alert">
This is a work in progress, not to be used for any critical decision making. Data may be inaccurate.
</div>
<br />
<div class="alert alert-info" role="alert">
Currently seeking contributors who would want to help with the code as well as testers who can provide feedback. Please contact <a href="mailto:colin@imperium.ca">colin@imperium.ca</a> if interested.
</div>


<h1>Situation Report</h1>
<?php echo "<strong>Generated</strong>: (" . date("Y-m-d H:i:s T") . ") (" . gmdate("Y-m-d H:i:s T") . ")";?>

<br /><br />


<h3>Current Weather</h3>
<?php
$url = "https://api.openweathermap.org/data/2.5/forecast?q=Edmonton&APPID=0dfddd0c3196246da61a909e1beb82d6&units=metric";
$json=file_get_contents($url);
$data=json_decode($json);

$wind_direction = wind_cardinals($data->list[0]->wind->deg);

echo '<strong>Current Temp:</strong> ', $data->list[0]->main->temp, ' &deg;C (Min: ', $data->list[0]->main->temp_min, ' &deg;C - Max: ', $data->list[0]->main->temp_max, ' &deg;C)<br />';
echo '<strong>Conditions:</strong> ', $data->list[0]->weather[0]->main, ' <strong>Pressure:</strong> ', $data->list[0]->main->pressure, 'kpa <strong>Humidity:</strong> ', $data->list[0]->main->humidity, '% <strong>Wind Speed:</strong> ', $data->list[0]->wind->speed, 'kt <strong>Wind Direction:</strong> '.$wind_direction. '<br />';

?>


Current <strong>Location</strong>: <span id="jslat"></span>, <span id="jslong"></span>






<br /><br />

<h3>Dataset Metrics</h3>
Number of <strong>Wildfires</strong> being tracked in <strong>Canada</strong>: <?php echo $fedfire_total; ?><br />
Number of road <strong>Accidents</strong> and <strong>Incidents</strong> in <strong>Alberta</strong>: <?php echo $abroads_total; ?><br />
Last <strong>Heartbeat</strong> from NAADS: <?php echo $heartbeat_naads_sent; ?> GMT<br />

<br /><br />

<div class="row">
  <div class="col-sm-2 col-12">
    <h4>Wildfire map</h4>
  </div>
  <div class="col-sm-10 col-12">
    <img src="images/fire_out_of_control.png"> = Out of Control <img src="images/fire_being_held.png"> = Being Held <img src="images/fire_under_control.png"> = Under Control
  </div>
</div>
<div id="map_wildfire"></div>

<br /><br />

<h4>National Alert Aggregation & Dissemination System Map</h4>
<div id="map_naads"></div>




<br /><br />
<h4>10 most recent NAADS alerts</h4>
<table class="table">
  <thead>
    <tr>
      <th scope="col">Category</th>
      <th scope="col">Event</th>
      <th scope="col">Urgency</th>
      <th scope="col">Severity</th>
      <th scope="col">Certainty</th>
      <th scope="col">Headline</th>
      <th scope="col">Description<td>
    </tr>
  </thead>
  <tbody>

<?php
$sql = "SELECT * FROM `naads` ORDER BY timestamp DESC LIMIT 10;";
$result = $conn->query($sql);
if ($result->num_rows > 0) {
  while($row = $result->fetch_assoc()) {
    echo "<tr><th scope=\"row\">" . $row["category"]. "</th><td>" . $row["event"]. "</td><td>" . $row["urgency"]. "</td><td>". $row["severity"]. "</td><td>". $row["certainty"]. "</td><td>". $row["headline"]. "</td><td><a href=\"/naadsdesc?event=\"id\">View</td>";
  }
}

?>
  </tbody>
</table>

<br /><br />



</div>

<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAZiG2K0Jy2jEYUA2Y3l18nAyl_CLlITSM&callback=initMap&libraries=&v=weekly" async></script>

</body>

</html>
<?php
$conn->close();
?>
