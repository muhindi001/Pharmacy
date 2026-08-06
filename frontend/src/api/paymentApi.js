import api from "./axios";

// Payments
export const getPayments = () =>
    api.get("payments/");

export const getPayment = (id) =>
    api.get(`payments/${id}/`);

export const createPayment = (data) =>
    api.post("payments/", data);

export const updatePayment = (id, data) =>
    api.put(`payments/${id}/`, data);

export const deletePayment = (id) =>
    api.delete(`payments/${id}/`);

export const searchPayments = (keyword) =>
    api.get(`payments/?search=${keyword}`);

export const getPaymentsBySale = (saleId) =>
    api.get(`payments/?sale=${saleId}`);

export const refundPayment = (id, data) =>
    api.post(`payments/${id}/refund/`, data);