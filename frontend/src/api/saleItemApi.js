import api from "./axios";

// Sale Items
export const getSaleItems = () =>
    api.get("sale-items/");

export const getSaleItem = (id) =>
    api.get(`sale-items/${id}/`);

export const createSaleItem = (data) =>
    api.post("sale-items/", data);

export const updateSaleItem = (id, data) =>
    api.put(`sale-items/${id}/`, data);

export const deleteSaleItem = (id) =>
    api.delete(`sale-items/${id}/`);

export const getSaleItemsBySale = (saleId) =>
    api.get(`sale-items/?sale=${saleId}`);

export const searchSaleItems = (keyword) =>
    api.get(`sale-items/?search=${keyword}`);