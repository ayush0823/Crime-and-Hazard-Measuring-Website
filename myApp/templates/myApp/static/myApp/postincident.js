mapboxgl.accessToken = 'pk.eyJ1IjoidmVuaWwxMCIsImEiOiJjbGd0M3p3MHQxMDVyM3JvMm55Z3hjcjZiIn0.J76tfDJhVMVCDzXqNCpBIA';

var map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/venil10/clgt4gkwl002x01png8jhhn1f',
  center: [72.627819, 23.188915],
  zoom: 5
});

var searchInput = document.getElementById('search-input');
var searchButton = document.getElementById('search-button');
var place = document.getElementById('place');
var err = document.getElementById('err');
var longitude = document.getElementById('longitude');
var latitude = document.getElementById('latitude');
var marker;

searchButton.addEventListener('click', function() {
  geocode(searchInput.value);
});

function geocode(address) {
  var url = 'https://api.mapbox.com/geocoding/v5/mapbox.places/' + encodeURIComponent(address) + '.json?access_token=' + mapboxgl.accessToken;

  fetch(url)
    .then(function(response) {
      return response.json();
    })
    .then(function(data) {

      if (data.features.length === 0) {
        document.getElementsByName('Latitude')[0].value = null;
        document.getElementsByName('Longitude')[0].value = null;
        place.textContent = null;
        err.textContent = "Location not found";
        console.log("Location not found");
        return;
      }
      // if(data==undefined) {
      // console.log(data);
      // console.log("venil");
      // }  
      // else {
      var location = data.features[0].center;
      var name = data.features[0].place_name;
      place.textContent = name;
      console.log(location[1], location[0])
      longitude.textContent = 'Longitude: ' + location[0];
      latitude.textContent = 'Latitude: ' + location[1];
      document.getElementsByName('Latitude')[0].value = (data.features[0].center[1]).toFixed(6);
      document.getElementsByName('Longitude')[0].value = (data.features[0].center[0]).toFixed(6);
      err.textContent = null;
      map.flyTo({
        center: location,
        zoom: 12
      });
      if (marker) {
        marker.remove();
      }
      marker = new mapboxgl.Marker()
        .setLngLat(location)
        .addTo(map);
    });
}

map.on('click', function(e) {
  var coordinates = e.lngLat;
  var url = 'https://api.mapbox.com/geocoding/v5/mapbox.places/' + coordinates.lng + ',' + coordinates.lat + '.json?access_token=' + mapboxgl.accessToken;

  fetch(url)
    .then(function(response) {
      return response.json();
    })
    .then(function(data) {
      var name = data.features[0].place_name;
      place.textContent = name;
      console.log(coordinates.long, coordinates.lat);
      longitude.textContent = 'Longitude: ' + coordinates.lng;
      latitude.textContent = 'Latitude: ' + coordinates.lat;
      document.getElementsByName('Latitude')[0].value = (data.features[0].center[1]).toFixed(6);
      document.getElementsByName('Longitude')[0].value = (data.features[0].center[0]).toFixed(6);
      err.textContent = null;
      if (marker) {
        marker.remove();
      }
      marker = new mapboxgl.Marker()
        .setLngLat(coordinates)
        .addTo(map);
    });
});


function showOptions() {
  // Get the value of the selected radio button
  var crimeOrHazard = document.querySelector('input[name="crime-or-hazard"]:checked').value;

  // Get the dropdown element
  var dropdown = document.getElementById("dropdown");

  // Clear previous options
  dropdown.innerHTML = "";

  // Add new options based on the selected radio button
  if (crimeOrHazard === "crime") {
    var options = ["Murder", "Rape", "Kidnap", "Hit and Run", "Bribe", "CyberCrime", "Smuggling", "Theft", "Money Laundering", "Tax Fraud"];
  } else if (crimeOrHazard === "hazard") {
    var options = ["Fire", "Flood", "Earthquake", "Landslide", "Virus and Bacteria", "Tsunami", "Cyclone", "Drought", "Forest Fire", "Industrial Accident"];
  }

  // Add the options to the dropdown
  for (var i = 0; i < options.length; i++) {
    var option = document.createElement("option");
    option.text = options[i];
    dropdown.add(option);
  }
}

