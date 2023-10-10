import { configureStore } from "@reduxjs/toolkit";
import userReducer from "./UserSlice";
import itemReducer from "./ItemSlice";

export const store = configureStore({
  reducer: {
    user: userReducer,
    item: itemReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false,
    }),
});

export default store;
