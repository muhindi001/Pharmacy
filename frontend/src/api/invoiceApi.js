import api from "./axios";

// Invoices
export const getInvoices = () =>
    api.get("invoices/");

export const getInvoice = (id) =>
    api.get(`invoices/${id}/`);

export const createInvoice = (data) =>
    api.post("invoices/", data);

export const updateInvoice = (id, data) =>
    api.put(`invoices/${id}/`, data);

export const deleteInvoice = (id) =>
    api.delete(`invoices/${id}/`);

export const searchInvoices = (keyword) =>
    api.get(`invoices/?search=${keyword}`);

export const printInvoice = (id) =>
    api.get(`invoices/${id}/print/`, {
        responseType: "blob",
    });

export const downloadInvoicePDF = (id) =>
    api.get(`invoices/${id}/pdf/`, {
        responseType: "blob",
    });