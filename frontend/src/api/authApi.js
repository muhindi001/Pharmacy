import api from "./axios";


export const login = (data) =>
    api.post("accounts/login/", data);

export const logout = () => {
    const refresh = localStorage.getItem("refresh_token");

    if (!refresh) {
        return Promise.resolve();
    }

    return api.post("accounts/logout/", { refresh });
};

// Profile
export const getProfile = () =>
    api.get("accounts/profile/");

export const updateProfile = (data) =>
    api.put("accounts/profile/", data);

// Password
export const changePassword = (data) =>
    api.post("accounts/change-password/", data);

// JWT
export const refreshToken = (data) =>
    api.post("accounts/token/refresh/", data);
