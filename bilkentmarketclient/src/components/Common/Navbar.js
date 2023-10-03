import React from "react";
import { useNavigate } from "react-router-dom";
import { useQuery } from "react-query";
import axios from "axios";
import Loading from "../CommonComponents/Loading";
import { useSelector } from "react-redux";
import "./Common.css"

function Navbar() {
  let navigate = useNavigate();
  const UserSlice = useSelector((state) => state.user);
  return (
    <div id="classicNavbar">
      <div className="brand">
        <img src={require("./assets/pic.jpg")} alt="" />
        <p>Bilkent Market</p>
      </div>
      <div className="navButtons">
        <a href="/items">ITEMS</a>
        <a href="/profile">PROFILE</a>
      </div>
    </div>
  );
}

export default Navbar;
