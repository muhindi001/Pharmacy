import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { logout } from "../../api/authApi";

const Logout = () => {
    const navigate = useNavigate();

    useEffect(() => {
        const doLogout = async () => {
            try {
                await logout();
            } catch (error) {
                console.error(error);
            } finally {
                localStorage.removeItem("access_token");
                localStorage.removeItem("refresh_token");
                navigate("/login", { replace: true });
            }
        };

        doLogout();
    }, [navigate]);

    return null;
};

export default Logout;