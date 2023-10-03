import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import axios from "axios";

const initialState = {
  email: "",
  username: "",
  id: null,
  status: "idle",
};

export const getUser = createAsyncThunk("getUser", async () => {
  const response = await axios.get("http://127.0.0.1:8000/users");
  return response;
});

export const userActions = createSlice({
  name: "user",
  initialState,
  reducers: {
    logout: (state) => {
      window.localStorage.removeItem("token");
      state.email = "";
      state.username = "";
      state.id = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(getUser.pending, (state, action) => {
        state.status = "loading";
      })
      .addCase(getUser.fulfilled, (state, action) => {
        state.status = "success";
        state.email = action.payload.data.email;
        state.username = action.payload.data.username;
        state.id = action.payload.data.id;
      })
      .addCase(getUser.rejected, (state, action) => {
        window.localStorage.removeItem("jwt");
        state.status = "error";
      });
  },
});
export const { logout } = userActions.actions;
export default userActions.reducer;
