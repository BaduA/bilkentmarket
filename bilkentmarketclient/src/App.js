import "./App.css";
import { QueryClientProvider, QueryClient } from "react-query";
import { Route, Routes, Redirect, Navigate } from "react-router-dom";
import Login from "./components/Auth/Login";
import Register from "./components/Auth/Register";
import Loading from "./components/CommonComponents/Loading";
import AppLayout from "./AppLayout";
import Homepage from "./components/Homepage/Homepage";
import AddItem from "./components/Homepage/components/AddItem";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      refetchOnmount: false,
      refetchOnReconnect: false,
      retry: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Routes>
        <Route path="/login" element={<Login></Login>} />
        <Route path="/register" element={<Register></Register>} />
        <Route path="/loading" element={<Loading></Loading>} />
        <Route element={<AppLayout></AppLayout>}>
          <Route path="/" element={<Homepage></Homepage>}></Route>
          <Route path="/additem" element={<AddItem></AddItem>}></Route>
          <Route path="*" element={<Homepage></Homepage>}></Route>
        </Route>
      </Routes>
    </QueryClientProvider>
  );
}

export default App;
