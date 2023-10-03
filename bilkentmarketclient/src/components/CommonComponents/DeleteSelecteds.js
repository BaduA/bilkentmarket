import { faXmark } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { useDispatch } from "react-redux";
import { deleteSelecteds } from "../../redux/GroupSlice";
import "./Commons.css"

function DeleteSelecteds() {
  const dispatch = useDispatch();

  return (
    <div className="deleteSelecteds">
      <FontAwesomeIcon
        onClick={() => {
          dispatch(deleteSelecteds());
        }}
        icon={faXmark}
        color="red"
      ></FontAwesomeIcon>
    </div>
  );
}

export default DeleteSelecteds;
