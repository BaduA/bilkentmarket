import { faBackward } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { useNavigate } from "react-router-dom";
import "./Commons.css"

function GoBack() {
    let navigate = useNavigate()
  return (
    <>
       <button
        className="goBack"
        onClick={() => {
          navigate(-1);
        }}
      >
        <FontAwesomeIcon icon={faBackward} color="white"></FontAwesomeIcon>
      </button>
    </>
  );
}

export default GoBack;
