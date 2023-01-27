import { animated, useTransition } from "@react-spring/web";
import React, { useState } from "react";
import { SocialIcon } from "react-social-icons";
import axios from "axios";



const Login = (props) => {
  const [email, setEmail] = useState();
  const [pass, setPass] = useState();
  //State that keeps track of whether the 'log in' button was clicked
  const [loggedIn, setLoggedIn] = useState(false);
  const [coords, setCoords] = useState({})




  //log in form's transitipn in and out of the screen.
  const transition = useTransition(loggedIn, {
    from: { opacity: 0 },
    enter: { opacity: 1 },
    leave: { opacity: 0 },
    trail: 0,
  });


  //'enter your address' input form's transitions in and out of the screen
  const searchFieldTransition = useTransition(loggedIn, {
    from: { marginTop: -200, opacity: 0 },
    enter: { marginTop: 180, opacity: 1 },
    leave: { opacity: 0 },
    trail: 300,
  });


  //location icon for button from bootstrap
  const locationIcon = (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="15"
      height="21"
      fill="white"
      className="bi bi-cursor-fill"
      viewBox="-2 -3 16 16"
    >
      <path d="M14.082 2.182a.5.5 0 0 1 .103.557L8.528 15.467a.5.5 0 0 1-.917-.007L5.57 10.694.803 8.652a.5.5 0 0 1-.006-.916l12.728-5.657a.5.5 0 0 1 .556.103z" />
    </svg>
  );


  //Get user's coordinates and use them for reverse geocoding
  const gotLocation = (position) => {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
    console.log("Current Location:", latitude + ",", longitude);
    //call reverseGeocode function to get user's address based on their coordinates
    reverseGeocode(latitude, longitude);
  };


//Allow users to type in address if don't want to be tracked  
const locationBlocked  = (error) => {
    const errorMessage = error.message;
    // alt. check for error.code === 1
    if (errorMessage === "User denied Geolocation") {
        // allow user to type address in input field (user-address is a placeholder)
        const searchButton = document.getElementById('submit-address');
        searchButton.addEventListener('click', () => {
            const userAddress = document.getElementById("search_input").value;
            console.log("Current Address: ", userAddress);
        });
    };
};


  //Autofill input field with the user's address
  document.getElementById("autofill-address")?.addEventListener("click", () => {
    navigator.geolocation.getCurrentPosition(gotLocation, locationBlocked, {
      enableHighAccuracy: true,
    });
  });


  //use latitude and longitude to get user's address
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
        document
          .getElementById("search_input")
          ?.setAttribute("value", currentAddress);
        console.log(responseObj);
      })
      .catch((error) => console.log(error.message));
  }


  //Use users address to get their coordinates
  async function geocode(address) {
    //replace all white spaces with a "+" symbol
    address = address.replace(/\s/g,"+")
     await axios
      .get("https://maps.googleapis.com/maps/api/geocode/json", {
        params: {
          address: address,
          //api key created in google cloud console
          key: "AIzaSyCOsS_SFOBuAdXiyu_1eVtqRxpssFpig04",
        },
      })
      .then(async (response) => {
        //convert the reponse JSON string into an object
        const responseObj = JSON.parse(response.request.response);
        //grab the formatted address of nearest detected address e.g. '17507 Central Ave, Upper Marlboro, MD 20774, USA'
        const userCoords = responseObj.results[0].geometry.location;
        await axios
    .get("https://maps.googleapis.com/maps/api/place/search/json", {
      params: {
        //display all gyms in a 7000m radius to test that request are working
        location: userCoords.lat + "," + userCoords.lng,
        radius: 7000,
        types: "gym",
        //api key created in google cloud console
        key: "AIzaSyCOsS_SFOBuAdXiyu_1eVtqRxpssFpig04",
      },
    })
    .then(async (response) => {
      //convert the reponse JSON string into an object
      const responseObj = JSON.parse(response.request.response);
      //grab the formatted address of nearest detected address e.g. '17507 Central Ave, Upper Marlboro, MD 20774, USA'
      responseObj.results.forEach(x=>console.log(x.name))
    })
    .catch((error) => console.log(error.message));
       
      })
      .catch((error) => console.log(error.message));
  }
 


  const handleSubmit = async () => {
    let userLocation =  document.getElementById("search_input").value
     geocode(userLocation);  }


  return (
    <div>
      {searchFieldTransition((style, item) =>
      //If loggedIn == true, this will show,
      //if not an empty string will show in its place
        item ? (
          <animated.div style={style}>
            <div>
              <input
                id="search_input"
                className="input"
                style={{ width: "15vw", marginRight: "8px" }}
                type="text"
                placeholder="Enter your Current Location's Address"
              />
              <button onClick={handleSubmit} id="submit-address">Submit</button>
            </div>
            <div>
              <button id="autofill-address">
                Or click here to autofill using location services {locationIcon}
              </button>
            </div>
          </animated.div> ) : ( "")
      )}


      {transition((style, item) =>
      //if Logged in is true, an empty string will show,
      //if not the log in form will be displayed
        item ? (
          ""
        ) : (
          <animated.header style={style} className="App-header">
            <div>
              <br></br>
              <br></br>
              <br></br>
            </div>
            <div className="auth-form-container">
              <p style={{ fontWeight: "bolder" }}>Log In</p>
              <div className="login-form">
                <label htmlFor="email">Email</label>
                <input
                  className="input"
                  type="email"
                  placeholder={String(loggedIn)}
                  id="email"
                  name="Email"
                />
                <label htmlFor="password">Password</label>
                <input
                  className="input"
                  type="password"
                  placeholder="password"
                  id="password"
                  name="password"
                />
                <button
                  className="login-btn"
                  onClick={() => {
                    setLoggedIn((prev) => !prev);
                  }}
                >
                  Log In
                </button>
              </div>
              <div>
                <p className="or">OR</p>
                <div
                  style={{
                    paddingTop: 15,
                    marginRight: "auto",
                    marginLeft: "auto",
                  }}
                >
                  <SocialIcon
                    network="google"
                    bgColor="#db4437"
                    style={{ height: 25, width: 25 }}
                  />
                  <SocialIcon
                    network="facebook"
                    bgColor="#3b5998"
                    style={{ height: 25, width: 25 }}
                  />
                  <SocialIcon
                    network="linkedin"
                    bgColor="#0072b1"
                    style={{ height: 25, width: 25 }}
                  />
                </div>
                <button className="link-btn" onClick={() => props}>
                  Don't have an account? <span>Register</span>
                </button>
              </div>
            </div>
          </animated.header>
        )
      )}
    </div>
  );
                };
export default Login;



