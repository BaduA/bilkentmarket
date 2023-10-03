import axios from "axios";
import React, { useEffect, useState } from "react";
import "./Auth.css";
import AuthNavbar from "./AuthNavbar";
import { useMutation } from "react-query";
function Register() {
  const [creds, setCreds] = useState({});
  function setInputFilter(textbox, inputFilter, errMsg) {
    [
      "input",
      "keydown",
      "keyup",
      "mousedown",
      "mouseup",
      "select",
      "contextmenu",
      "drop",
      "focusout",
    ].forEach(function (event) {
      textbox.addEventListener(event, function (e) {
        if (inputFilter(this.value)) {
          // Accepted value.
          if (["keydown", "mousedown", "focusout"].indexOf(e.type) >= 0) {
            this.classList.remove("input-error");
            this.setCustomValidity("");
          }

          this.oldValue = this.value;
          this.oldSelectionStart = this.selectionStart;
          this.oldSelectionEnd = this.selectionEnd;
        } else if (this.hasOwnProperty("oldValue")) {
          // Rejected value: restore the previous one.
          this.classList.add("input-error");
          this.setCustomValidity(errMsg);
          this.reportValidity();
          this.value = this.oldValue;
          this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
        } else {
          // Rejected value: nothing to restore.
          this.value = "";
        }
      });
    });
  }
  useEffect(() => {
    setInputFilter(
      document.querySelector(".phoneNum"),
      function (value) {
        return /^\d*\.?\d*$/.test(value); // Allow digits and '.' only, using a RegExp.
      },
      "Only digits are allowed"
    );
    setInputFilter(
      document.querySelector(".bilkentId"),
      function (value) {
        return /^\d*\.?\d*$/.test(value); // Allow digits and '.' only, using a RegExp.
      },
      "Only digits are allowed"
    );
  });
  const Register = useMutation({
    mutationFn: (data) => {
      console.log(data)
      return axios.post("http://127.0.0.1:8000/users", data);
    },
    onSuccess: (res) => {
      console.log(res.data)
      // Login.mutate();
    },
  });

  const handleSubmit = (event) => {
    event.preventDefault();
    var new_obj = {};
    var isEmpty = [];
    document.querySelectorAll("#registerForm input").forEach((element) => {
      var type = element.getAttribute("data-type");
      new_obj[type] = element.value;
      if (element.value === "" || element.value === null) {
        isEmpty.push(true);
      } else {
        isEmpty.push(false);
      }
    });
    if (isEmpty.includes(true)) {
    } else {
      Register.mutate(new_obj);
    }
  };
  return (
    <>
      <AuthNavbar></AuthNavbar>
      <div id="registerContainer">
        <div id="registerFormContainer">
          <h2>Bilkent Market'e Kayıt ol</h2>
          <p>
            Zaten bir hesabın var mı? <a href="/login">Giriş Yap</a>
          </p>
          <form action="" onSubmit={handleSubmit} id="registerForm">
            <input
              placeholder="Phone Number"
              className="phoneNum onlynum"
              type="text"
              data-type="phone_num"
            />
            <input
              placeholder="Bilkent ID"
              className="bilkentId onlynum"
              type="text"
              data-type="id"
            />
            <input type="text" data-type="email" placeholder="Email" />
            <input type="text" data-type="username" placeholder="Username" />
            <input type="text" data-type="name" placeholder="Name" />
            <input type="text" data-type="surname" placeholder="Surname" />
            <input type="text" data-type="city" placeholder="City" />
            <input type="text" data-type="subcity" placeholder="Subcity" />
            <input type="text" data-type="school" placeholder="School" />
            <input
              type="text"
              data-type="department"
              placeholder="Department"
            />
            <input type="text" data-type="grade" placeholder="Grade" />
            <input type="text" data-type="password" placeholder="Password" />
            <button type="submit">KAYDOL</button>
          </form>
        </div>
      </div>
    </>
  );
}

export default Register;
