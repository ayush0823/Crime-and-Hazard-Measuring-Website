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
// var longitude = document.getElementById('longitude');
// var latitude = document.getElementById('latitude');
var marker;

searchButton.addEventListener('click', function() {
  geocode(searchInput.value);
});

// Listen for the "keydown" event on the input element
searchInput.addEventListener("keydown", function(event) {
  if (event.keyCode === 13) { // Check if the key pressed is the enter key
    geocode(searchInput.value);
  }
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
         document.getElementsByName('City')[0].value = null;
       document.getElementsByName('State')[0].value = null;
      document.getElementsByName('Country')[0].value = null;
      document.getElementsByName('Pincode')[0].value = null;
        place.textContent = null;
        err.textContent = "Location not found";
        console.log("Location not found");
        return;
      }

      var location = data.features[0].center;
      var name = data.features[0].place_name;
      place.textContent = name;
      // console.log(location[1], location[0])
      // longitude.textContent = 'Longitude: ' + location[0];
      // latitude.textContent = 'Latitude: ' + location[1];

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

      document.getElementsByName('Latitude')[0].value = (data.features[0].center[1]).toFixed(6);
      document.getElementsByName('Longitude')[0].value = (data.features[0].center[0]).toFixed(6);
      err.textContent = null;

      document.getElementsByName('City')[0].value = null;
      document.getElementsByName('State')[0].value = null;
      document.getElementsByName('Country')[0].value = null;
      document.getElementsByName('Pincode')[0].value = null;


      // Extract city, state, country, and pincode from the response
      var context = data.features[0].context;
      var city, state, country, pincode;

      for (var i = 0; i < context.length; i++) {
        var c = context[i];
        if (c.id.startsWith('district')) {
          city = c.text;
        } else if (c.id.startsWith('region')) {
          state = c.text;
        } else if (c.id.startsWith('country')) {
          country = c.text;
        } else if (c.id.startsWith('postcode')) {
          pincode = c.text;
        }
      }

      // Display the city, state, country, and pincode

      if (city) {

        document.getElementsByName('City')[0].value = city;
      }
      if (state) {
        document.getElementsByName('State')[0].value = state;
      }
      if (country) {
        document.getElementsByName('Country')[0].value = country;
      }
      if (pincode) {
        document.getElementsByName('Pincode')[0].value = pincode;
      }


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
      // console.log(coordinates.long, coordinates.lat);
      // longitude.textContent = 'Longitude: ' + coordinates.lng;
      // latitude.textContent = 'Latitude: ' + coordinates.lat;
      document.getElementsByName('Latitude')[0].value = (data.features[0].center[1]).toFixed(6);
      document.getElementsByName('Longitude')[0].value = (data.features[0].center[0]).toFixed(6);
      err.textContent = null;


      document.getElementsByName('City')[0].value = null;
      document.getElementsByName('State')[0].value = null;
      document.getElementsByName('Country')[0].value = null;
      document.getElementsByName('Pincode')[0].value = null;

      // Extract city, state, country, and pincode from the response
      var context = data.features[0].context;
      var city, state, country, pincode;

      for (var i = 0; i < context.length; i++) {
        var c = context[i];
        if (c.id.startsWith('district')) {
          city = c.text;
        } else if (c.id.startsWith('region')) {
          state = c.text;
        } else if (c.id.startsWith('country')) {
          country = c.text;
        } else if (c.id.startsWith('postcode')) {
          pincode = c.text;
        }
      }

      // Display the city, state, country, and pincode

      if (city) {

        document.getElementsByName('City')[0].value = city;
      }
      if (state) {
        document.getElementsByName('State')[0].value = state;
      }
      if (country) {
        document.getElementsByName('Country')[0].value = country;
      }
      if (pincode) {
        document.getElementsByName('Pincode')[0].value = pincode;
      }

      if (marker) {
        marker.remove();
      }
      marker = new mapboxgl.Marker()
        .setLngLat(coordinates)
        .addTo(map);
    });
});