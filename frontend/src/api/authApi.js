import api from "./axios";

// Authentication
// export const register = (data) =>
//     api.post("auth/register/", data);

export const login = (data) =>
    api.post("accounts/login/", data);

export const logout = () =>
    api.post("accounts/logout/");

// Profile
export const getProfile = () =>
    api.get("accounts/profile/");

export const updateProfile = (data) =>
    api.put("accounts/profile/", data);

// Password
export const changePassword = (data) =>
    api.post("accounts/change-password/", data);

export const forgotPassword = (data) =>
    api.post("accounts/forgot-password/", data);

export const resetPassword = (data) =>
    api.post("accounts/reset-password/", data);

// JWT
export const refreshToken = (data) =>
    api.post("accounts/token/refresh/", data);

// Users (Admin)
export const getUsers = () =>
    api.get("users/");

export const getUser = (id) =>
    api.get(`users/${id}/`);

export const createUser = (data) =>
    api.post("users/", data);

export const updateUser = (id, data) =>
    api.put(`users/${id}/`, data);

export const deleteUser = (id) =>
    api.delete(`users/${id}/`);