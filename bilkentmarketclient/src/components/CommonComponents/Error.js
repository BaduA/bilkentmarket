import React, { useEffect } from "react";
import "./Commons.css"

function Error({ error }) {
  useEffect(() => {
    const cont = document.querySelector(".ErrorContainer")
    setTimeout(()=>{
        cont.style.right = (window.innerWidth).toString() + "px"
        cont.style.opacity = 0
    },2000)
    setTimeout(()=>{
        cont.style.display = "none"
    },3000)
  });
  return (
    <div className="ErrorContainer">
      <p>{error}</p>
    </div>
  );
}

export default Error;
