console.log("index.js is running normally")

d3.select("#gyms").on('click', function(){
  console.log("Let's update the display!")  
});


function GET(path) {
  return new Promise(function (resolve, reject) {
      axios.get(path).then((response) => {
          var result = response.data;
          resolve(result);
      }).catch((error) => {
          reject(error);
      });
  });
}

// Function for talking to the server
function POST(path, data) {
  return new Promise(function (resolve, reject) {
      axios.post(path, data).then((response) => {
          var result = response
          resolve(result)
      }).catch((error) => {
          reject(error);
      });
  });
}


// Function to update the individual places elements
function updatePage(places) {
  for (let i=0; i < Object.keys(places).length; i++) {
    d3.select("#LocImg" + i).attr('src', places[i]['image']);
    d3.select("#LocName" + i).text(places[i]['bus_name']);
    d3.select("#LocDes" + i).text("ADDRESS: " + places[i]['address'] + ", " + places[i]['city'] + "  " + places[i]['zip_code'] + "    PHONE: " + places[i]['phone']);
  };
}

// When the Gym Button is clicked:
function myGyms(){
  document.getElementById("headTitle").innerText="GYMs";
  console.log("Gym button clicked.");
  let search = d3.select("#pac-input").property("value");
  let data = {'search': search}
  POST("/Gyms", data).then(response => {
    console.log(response.data);
    updatePage(response.data);    
  });
}

// When the Hotels Button is clicked:
function myHotels(){
  document.getElementById("headTitle").innerText="Hotels";
  console.log("Hotels button clicked.");
  let search = d3.select("#pac-input").property("value");
  let data = {'search': search}
  POST("/Hotels", data).then(response => {
    console.log(response.data);
    updatePage(response.data); 
  });
}

// When the Restaurants Button is clicked:
function myRestaurant(){
  document.getElementById("headTitle").innerText="Restaurants";
  console.log("Restaurantss button clicked.");
  let search = d3.select("#pac-input").property("value");
  let data = {'search': search}
  POST("/Restaurants", data).then(response => {
    console.log(response.data);
    updatePage(response.data); 
  });
}

// When the Entertainment Button is clicked:
function myEntertainment(){
  document.getElementById("headTitle").innerText="Entertainment";
  console.log("Entertainment button clicked.");
  let search = d3.select("#pac-input").property("value");
  let data = {'search': search}
  POST("/Entertainment", data).then(response => {
    console.log(response.data);
    updatePage(response.data); 
  });
}

// When the Attractions Button is clicked:
function myAttraction(){
  document.getElementById("headTitle").innerText="Attractions";
  console.log("Attractions button clicked.");
  let search = d3.select("#pac-input").property("value");
  let data = {'search': search}
  POST("/Attractions", data).then(response => {
    console.log(response.data);
    updatePage(response.data); 
  });
}

// Initialize and add the map
function initMap() {
  // The location of Atlanta, GA
  const myCoords = { lat: 33.7490, lng: -84.3880};
  // The map, centered at Atlanta, GA
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 8,
    center: myCoords,
  });
  
  // The marker, positioned at Atlanta, GA
  const image ="https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png";
  const beachMarker = new google.maps.Marker({
      position: uluru,
      map,
      icon: image
  //const marker = new google.maps.Marker({
    //position: uluru,
    //map: map,
  });
}

//-----------------------------------------------------------------------------------
// This example adds a search box to a map, using the Google Place Autocomplete
// feature. People can enter geographical searches. The search box will return a
// pick list containing a mix of places and predicted search terms.
// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyB41DRUbKWJHPxaFjMAwdrzWzbVKartNGg&libraries=places">
function initAutocomplete() {
    const map = new google.maps.Map(document.getElementById("map"), {
      center: { lat: 33.7490, lng: -84.3880 },
      zoom: 13,
      mapTypeId: "roadmap",
    });
    // Create the search box and link it to the UI element.
    const input = document.getElementById("pac-input");
    const searchBox = new google.maps.places.SearchBox(input);
    console.log(searchBox)
  
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
    // Bias the SearchBox results towards current map's viewport.
    map.addListener("bounds_changed", () => {
      searchBox.setBounds(map.getBounds());
    });
  
    let markers = [];
  
    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    searchBox.addListener("places_changed", () => {
      const places = searchBox.getPlaces();
  
      if (places.length == 0) {
        return;
      }
  
      // Clear out the old markers.
      markers.forEach((marker) => {
        marker.setMap(null);
      });
      markers = [];
  
      // For each place, get the icon, name and location.
      const bounds = new google.maps.LatLngBounds();
  
      places.forEach((place) => {
        if (!place.geometry || !place.geometry.location) {
          console.log("Returned place contains no geometry");
          return;
        }
  
        const icon = {
          url: place.icon,
          size: new google.maps.Size(71, 71),
          origin: new google.maps.Point(0, 0),
          anchor: new google.maps.Point(17, 34),
          scaledSize: new google.maps.Size(25, 25),
        };
  
        // Create a marker for each place.
        markers.push(
          new google.maps.Marker({
            map,
            icon,
            title: place.name,
            position: place.geometry.location,
          })
        );
        if (place.geometry.viewport) {
          // Only geocodes have viewport.
          bounds.union(place.geometry.viewport);
        } else {
          bounds.extend(place.geometry.location);
        }
      });
      map.fitBounds(bounds);
    });
  }


//------------------------------------------------------------------------------------

d3.select("#gyms").on('click', function(){
  console.log("Let's update the display!")  
  let search = d3.select("#pac-input").property("value")
  console.log(search)
    data = {'search': search}
    POST("/api/get_data", data).then(response => {
       console.log(response.data)
    })
});





//-----------------------------------------------------------------------------------------



//------------------------------------------------------------------------------------


// add search button
// button_code = 'id="button" type="submit" value="" style="z-index: 0; position: absolute; margin-left: 220px; margin-right: 25px; top: 20px;"'
// var controls = d3.select(".gmnoprint")
// controls.append("button").text(Search)


//---------Data Set ---------------//




    //console.log(diningData);