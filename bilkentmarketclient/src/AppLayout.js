import axios from "axios";
import { useQuery } from "react-query";
import { Navigate, Outlet } from "react-router-dom";
import Navbar from "./components/Common/Navbar";
import Loading from "./components/CommonComponents/Loading";
import { useDispatch, useSelector } from "react-redux";
import { getUser } from "./redux/UserSlice";
import { useEffect } from "react";

axios.interceptors.request.use((config) => {
  const token = window.localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

function AppLayout() {
  const UserSlice = useSelector((state) => state.user);
  const dispatch = useDispatch();
  useEffect(() => {
    dispatch(getUser());
  }, []);
  if (UserSlice.status === "loading") {
    return (
      <div className="flexAllContainer">
        <Loading></Loading>
      </div>
    );
  } else if (UserSlice.status === "error") {
    return <Navigate to="/login"></Navigate>;
  } else if (UserSlice.status === "success") {

  }
  return (
    <>
      <div className="app-container">
        <Navbar></Navbar>
        <Outlet></Outlet>
      </div>
    </>
  );
}

export default AppLayout;
