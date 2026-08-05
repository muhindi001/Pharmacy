import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import Login from "./pages/auth/login";
import ChangePassword from "./pages/auth/ChangePassword";
import Dashboard from "./pages/dashboard/Dashboard";


function App() {
    return (
        <BrowserRouter>

            {/* <Toaster
                position="top-right"
                reverseOrder={false}
            /> */}

            <Routes>

                {/* Authentication */}

                <Route path="/" element={<Navigate to="/login" replace />}/>
                <Route path="/login" element={<Login />}/>
                <Route path="/change-password" element={<ChangePassword />}/> 
                <Route path="/dashboard" element={<Dashboard />}/> 

            </Routes>

        </BrowserRouter>
    );
}
export default App;