$(document).ready(function(){
    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(showLocation);
    }else{
        $('#location').html('Geolocation is not supported by this browser.');
    }
});


function showLocation(position){
    var latitude = position.coords.latitude;
    var longitude = position.coords.longitude;
    document.getElementById("jslat").innerHTML = latitude;
    document.getElementById("jslong").innerHTML = longitude;
}

function initMap() {
  const map_wildfire = new google.maps.Map(document.getElementById("map_wildfire"), {
    zoom: 5,
    mapTypeId: "terrain",
  });

  map_naads = new google.maps.Map(document.getElementById("map_naads"), {
    zoom: 5,
    mapTypeId: "terrain",
  });

  setMarkers_fire_out_of_control(map_wildfire);
  setMarkers_fire_being_held(map_wildfire);
  setMarkers_fire_under_control(map_wildfire);

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function (position) {
      initialLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
      map_wildfire.setCenter(initialLocation);
      map_naads.setCenter(initialLocation);
    });
  }


  const triangleCoords = [
    { lat: 25.774, lng: -80.19 },
    { lat: 18.466, lng: -66.118 },
    { lat: 32.321, lng: -64.757 },
  ];
  // Construct the polygon.
  const bermudaTriangle = new google.maps.Polygon({
    paths: triangleCoords,
    strokeColor: "#FF0000",
    strokeOpacity: 0.8,
    strokeWeight: 3,
    fillColor: "#FF0000",
    fillOpacity: 0.35,
  });
  bermudaTriangle.setMap(map_naads);
  // Add a listener for the click event.
  bermudaTriangle.addListener("click", showArrays);
  infoWindow = new google.maps.InfoWindow();

}


function showArrays(event) {
  // Since this polygon has only one path, we can call getPath() to return the
  // MVCArray of LatLngs.
  const polygon = this;
  const vertices = polygon.getPath();
  let contentString =
    "<b>Bermuda Triangle polygon</b><br>" +
    "Clicked location: <br>" +
    event.latLng.lat() +
    "," +
    event.latLng.lng() +
    "<br>";

  // Iterate over the vertices.
  for (let i = 0; i < vertices.getLength(); i++) {
    const xy = vertices.getAt(i);
    contentString +=
      "<br>" + "Coordinate " + i + ":<br>" + xy.lat() + "," + xy.lng();
  }
  // Replace the info window's content and position.
  infoWindow.setContent(contentString);
  infoWindow.setPosition(event.latLng);
  infoWindow.open(map_naads);
}

