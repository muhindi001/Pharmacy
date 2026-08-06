import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import Login from "./pages/auth/login";
import Profile from "./pages/auth/Profile";
import ChangePassword from "./pages/auth/ChangePassword";
import Dashboard from "./pages/dashboard/Dashboard";
import Logout from "./pages/auth/Logout";


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
                <Route path="/profile" element={<Profile />}/> 
                <Route path="/logout" element={<Logout />}/> 

            </Routes>

        </BrowserRouter>
    );
}
export default App;