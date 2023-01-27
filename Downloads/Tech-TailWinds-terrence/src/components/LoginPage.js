import React, { useState } from "react";
import { useLoadScript, GoogleMap } from "@react-google-maps/api";
import Login from "./Login";
import { animated, useTransition } from "@react-spring/web";




export function MapContainer() {


  //Set the margin-top property based on screen size.
  //Currently looking for a different way to do this.
  var marginTop =0;
  if(window.outerHeight > 639 &&  window.outerHeight < 861){
    marginTop = -70;
  }else{marginTop = 150}


  const [showForm, setShowForm] = useState(false);


  //Animations for the log in form transitioning on and off of the screen
  const transition = useTransition(showForm, {
    from: { marginTop: 900, opacity: 0 },
    enter: { marginTop:marginTop, opacity: 1 },
    leave: { marginTop: 900, opacity: 0 },
  });
  const { isLoaded } = useLoadScript({
    googleMapsApiKey: "AIzaSyCOsS_SFOBuAdXiyu_1eVtqRxpssFpig04",
  });


  if (!isLoaded) return <div>Loading...</div>;


  //coordinates to center the map on
  const center = {
    lat: 38.9005542,
    lng: -76.7019744,
  };


  //set map properties so it covers the whole screen
  const mapContainer = {
    width: "100vw",
    height: "100vh",
  };


  //UI options for the map
  const options = {
    disableDefaultUI: true,
    zoomControl: true,
  };


  //The log in icon at the top left from bootstrap
  const loginIcon = (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="32"
      height="30"
      fill="lightBlue"
      className="bi bi-person-badge-fill"
      viewBox="0 0 16 16"
    >
      <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2zm4.5 0a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1h-3zM8 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm5 2.755C12.146 12.825 10.623 12 8 12s-4.146.826-5 1.755V14a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1v-.245z" />
    </svg>
  );


  console.log(window.outerHeight+" ,"+window.outerWidth)
  return (
    <div>
      <div className="login-toggle">
        <button
          onClick={() => setShowForm(!showForm)}
          style={{ boxShadow: "2px 1px 4px black" }}
        >
          {loginIcon}Log In
        </button>
      </div>




      {transition((style, item) =>
        //Ternary operator: if showForm is true, show the
        //Login component, if not show an empty string
        item ? (
          <animated.div className="App" style={style}>
            <Login />
          </animated.div>) : ("")
      )}
      <GoogleMap
        zoom={12}
        options={options}
        center={center}
        mapContainerStyle={mapContainer}
      ></GoogleMap>
    </div>
  );
}
