// Use a small library to manage, add '; path=/' when setting cookies
// document.cookie = 'login=TBD; path=/';
// Date for cookie that doesn't expire: new Date(9999, 0, 1).toUTCString()
// document.cookie = 'name=vistors; expires=' + new Date(2023, 0, 1).toUTCString()
// Make everyting below expire shortly
// document.cookie = 'user_consent=TBD; expires=' + new Date(2023, 0, 1).toUTCString()
// document.cookie = 'tailw_marketing=allow; expires=' + new Date(2023, 0, 1).toUTCString()
// document.cookie = 'tailw_statistics=denied; expires=' + new Date(2023, 0, 1).toUTCString()
// document.cookie = 'tailw_performance=allowed; expires=' + new Date(2023, 0, 1).toUTCString()
// document.cookie = 'tailw_functional=allowed; expires=' + new Date(2023, 0, 1).toUTCString()

const cookieStorage = {
  getCookie: (name) => {
    // Split cookie string and get individual pairs in an array
    var cookieArr = document.cookie.split(";");
    // Loop through the array
    for (var i = 0; i < cookieArr.length; i++) {
      var cookiePair = cookieArr[i].split("=");
      // Compare cookie name with the given string
      if (name == cookiePair[0].trim()) {
        // Decode the cookie value and return
        return decodeURIComponent(cookiePair[1]);
      }
    }
    // Else return null
    return null;
  },
  setCookie: (name, value, daysToLive) => {
    // Encode value in order to escape semicolons, commas, and whitespace
    var cookie = name + "=" + encodeURIComponent(value);
    if (typeof daysToLive === "number") {
      /* Sets the max-age attribute so that the cookie expires
            after the specified number of days */
      cookie += "; max-age=" + daysToLive * 24 * 60 * 60;
      cookie += "; path=/";
      document.cookie = cookie;
    }
  },
};

const storage = cookieStorage;
const allCookies = "tailw_consent";

const cookiesContainer = document.querySelector(".cookie-container");
const cookieButton = document.querySelector(".cookie-button");
cookieButton.addEventListener("click", () => {
  cookiesContainer.classList.remove("hide");
  storage.setCookie(allCookies, true, 365);
});

setTimeout(() => {
  // change to !storage to check for cookies
  if (!storage.getCookie(allCookies)) {
    cookiesContainer.classList.add("hide");
  }
}, 2000);

// FYI for Terrence:
// Use geoloction API under navigator: navigator.geolocation
// Test in console: navigator.geolocation.getCurrentPosition(console.log, console.log)
const gotLocation = (position) => {
  const latitude = position.coords.latitude;
  const longitude = position.coords.longitude;
  console.log("Current Location:", latitude + ",", longitude);
  //call reverseGeocode function to get user's address based on their coordinates
  reverseGeocode(latitude, longitude);
};

const locationBlocked  = (error) => {
    const errorMessage = error.message;
    // alt. check for error.code === 1
    if (errorMessage === "User denied Geolocation") {
        // allow user to type address in input field (user-address is a placeholder)
        const searchButton = document.querySelector('.search-button');
        searchButton.addEventListener('click', () => {
            const userAddress = document.getElementById("user-address").value;
            console.log("Current Address: ", userAddress);
        });
    };
};

navigator.geolocation.getCurrentPosition(gotLocation, locationBlocked, {
  enableHighAccuracy: true,
  // more accurate position but slower response time
});

function reverseGeocode(lat, long) {
  const address = lat + "," + long;
  //send a GET request to google maps api endpoint for location data on the given coordinates
  axios
    .get("https://maps.googleapis.com/maps/api/geocode/json", {
      params: {
        address: address,
        //api key created in google cloud console
        key: "AIzaSyCOsS_SFOBuAdXiyu_1eVtqRxpssFpig04",
      },
    })
    .then((response) => {
      //convert the reponse JSON string into an object
      const responseObj = JSON.parse(response.request.response);
      //grab the formatted address of nearest detected address e.g. '17507 Central Ave, Upper Marlboro, MD 20774, USA'
      const currentAddress = responseObj.results[0].formatted_address;
      console.log("Current Address: " + currentAddress);
    })
    .catch((error) => console.log(error.message));
}

//creates script tag and imports Google Maps JavaScript library
var script = document.createElement("script");
script.src =
  "https://maps.googleapis.com/maps/api/js?key=AIzaSyCOsS_SFOBuAdXiyu_1eVtqRxpssFpig04&libraries=places&callback=initAutocomplete";
script.async = true;

// Attach your callback function to the `window` object
window.initAutocomplete = function () {
  //create a new Autocomplete service and attatch it to the search input field

  var autocomplete = new google.maps.places.Autocomplete(
    document.getElementById("search_input")
  );

  //update the suggestion list when new input is typed
  autocomplete.addListener("place_changed", function () {
    var near_place = autocomplete.getPlace();
  });
};

// Append the 'script' element to 'head'
document.head.appendChild(script);
