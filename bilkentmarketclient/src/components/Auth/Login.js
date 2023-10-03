import React, { useState } from "react";
import "./Auth.css"; // Import CSS file for styling
import { useMutation } from "react-query";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import Error from "../CommonComponents/Error";
import AuthNavbar from "./AuthNavbar";
import { getFormData } from "../../utils";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [borderColor, setBColor] = useState("none");
  let navigate = useNavigate();
  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };
  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };
  const Login = useMutation({
    mutationFn: () => {
      return axios
        .post(
          "http://127.0.0.1:8000/login",
          getFormData({
            username: email,
            password: password,
          })
        )
        .then((res) => {
          const token = res.data.access_token;
          //set JWT token to local
          localStorage.setItem("token", token);
        });
    },
    onSuccess: () => {
      navigate("/");
    },
    onError: () => {
      setBColor("red");
    },
  });

  const handleSubmit = (event) => {
    event.preventDefault();
    let isError = false;
    document.querySelectorAll("input").forEach((element) => {
      if (element.value === "") {
        element.style.border = "1px solid red";
        isError = true;
      }
    });
    if (!isError) {
      Login.mutate();
    }
  };

  return (
    <>
      <AuthNavbar></AuthNavbar>
      <div id="loginContainer">
        <div id="loginFormContainer">
          <h2>Bilkent Market'e Giriş</h2>
          <div id="loginFormBottom">
            <div className="imageBrand">
              <img src={require("./assets/pic.jpg")} alt="" />
            </div>
            <form action="" id="loginForm" onSubmit={handleSubmit}>
              <input
                type="text"
                placeholder="Email / Phone Number / Bilkent ID"
                onChange={handleEmailChange}
                style={{ borderColor: borderColor }}
              />
              <input
                type="text"
                placeholder="Password"
                onChange={handlePasswordChange}
                style={{ borderColor: borderColor }}
              />
              <button type="submit">Giriş Yap</button>
              <div id="loginLinks">
                <a href="/register">Kaydol</a>
                <a href="/">Şifrenizi mi unuttunuz?</a>
              </div>
            </form>
          </div>
        </div>
      </div>
    </>
  );
};

export default Login;
