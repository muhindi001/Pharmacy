import api from "./axios";

// Sales
export const getSales = () =>
    api.get("sales/");

export const getSale = (id) =>
    api.get(`sales/${id}/`);

export const createSale = (data) =>
    api.post("sales/", data);

export const updateSale = (id, data) =>
    api.put(`sales/${id}/`, data);

export const deleteSale = (id) =>
    api.delete(`sales/${id}/`);

export const searchSales = (keyword) =>
    api.get(`sales/?search=${keyword}`);

export const printReceipt = (id) =>
    api.get(`sales/${id}/receipt/`, {
        responseType: "blob",
    });

export const printInvoice = (id) =>
    api.get(`sales/${id}/invoice/`, {
        responseType: "blob",
    });