import React from "react";
import "./Homepage.css";
import { useNavigate } from "react-router-dom";

function Homepage() {
  let navigate = useNavigate();
  return (
    <div id="homepageContainer">
      <div className="topButtons">
        <button
          onClick={() => {
            navigate("/addItem");
          }}
        >
          Add Item
        </button>
      </div>
    </div>
  );
}

export default Homepage;
