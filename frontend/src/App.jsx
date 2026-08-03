import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import Login from "./pages/auth/Login";


function App() {
    return (
        <BrowserRouter>

            {/* <Toaster
                position="top-right"
                reverseOrder={false}
            /> */}

            <Routes>

                {/* Authentication */}

                <Route
                    path="/"
                    element={<Navigate to="/login" replace />}
                />

                <Route
                    path="/login"
                    element={<Login />}
                />

            </Routes>

        </BrowserRouter>
    );
}
export default App;