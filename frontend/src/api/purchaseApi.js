import api from "./axios";

// Purchases
export const getPurchases = () =>
    api.get("purchases/");

export const getPurchase = (id) =>
    api.get(`purchases/${id}/`);

export const createPurchase = (data) =>
    api.post("purchases/", data);

export const updatePurchase = (id, data) =>
    api.put(`purchases/${id}/`, data);

export const deletePurchase = (id) =>
    api.delete(`purchases/${id}/`);

export const approvePurchase = (id) =>
    api.post(`purchases/${id}/approve/`);

export const receivePurchase = (id) =>
    api.post(`purchases/${id}/receive/`);

export const searchPurchases = (keyword) =>
    api.get(`purchases/?search=${keyword}`);