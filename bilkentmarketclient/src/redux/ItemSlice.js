import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import axios from "axios";

const initialState = {
  isAddItem: false,
};

export const itemActions = createSlice({
  name: "item",
  initialState,
  reducers: {
    addItem: (state) => {
      state.isAddItem = !state.isAddItem;
    },
  },
  extraReducers: (builder) => {
  },
});
export const { addItem } = itemActions.actions;
export default itemActions.reducer;
