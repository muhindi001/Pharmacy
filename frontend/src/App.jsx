import { HashRouter, Routes, Route, Navigate, BrowserRouter } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import Login from "./pages/auth/login";
import Profile from "./pages/auth/Profile";
import ChangePassword from "./pages/auth/ChangePassword";
import Dashboard from "./pages/dashboard/Dashboard";
import Logout from "./pages/auth/Logout";
import MainLayout from "./pages/layouts/MainLayout";
import PagePlaceholder from "./pages/layouts/PagePlaceholder";
import MedicineList from "./pages/master-data/medicines/MedicineList";
import MedicineForm from "./pages/master-data/medicines/MedicineForm";
import ImportMedicines from "./pages/master-data/medicines/ImportMedicines";

function App() {
    return (
        <BrowserRouter>

            {/* <Toaster
                position="top-right"
                reverseOrder={false}
            /> */}

            <Routes>

                {/* Authentication */}

                <Route path="/" element={<Navigate to="/login" replace />} />
                <Route path="/login" element={<Login />} />
                <Route path="/change-password" element={<ChangePassword />} />

                <Route element={<MainLayout />}>
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/profile" element={<Profile />} />
                    <Route path="/categories" element={<PagePlaceholder />} />
                    <Route path="/suppliers" element={<PagePlaceholder />} />
                    <Route path="/manufacturers" element={<PagePlaceholder />} />
                    <Route path="/medicines" element={<MedicineList />} />
                    <Route path="/medicines/create" element={<MedicineForm />} />
                    <Route path="/medicines/edit/:id" element={<MedicineForm />} />
                    <Route path="/medicines/import" element={<ImportMedicines />} />
                    <Route path="/customers" element={<PagePlaceholder />} />
                    <Route path="/inventory" element={<PagePlaceholder />} />
                    <Route path="/inventory/batches" element={<PagePlaceholder />} />
                    <Route path="/inventory/goods-receiving" element={<PagePlaceholder />} />
                    <Route path="/inventory/stock-adjustment" element={<PagePlaceholder />} />
                    <Route path="/inventory/rfid" element={<PagePlaceholder />} />
                    <Route path="/sales/pos" element={<PagePlaceholder />} />
                    <Route path="/sales" element={<PagePlaceholder />} />
                    <Route path="/sales/payments" element={<PagePlaceholder />} />
                    <Route path="/sales/transactions" element={<PagePlaceholder />} />
                    <Route path="/sales/invoices" element={<PagePlaceholder />} />
                </Route>

                <Route path="/logout" element={<Logout />} />

            </Routes>

        </BrowserRouter>
    );
}
export default App;