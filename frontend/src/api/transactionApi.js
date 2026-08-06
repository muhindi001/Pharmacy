import api from "./axios";

// Transactions
export const getTransactions = () =>
    api.get("transactions/");

export const getTransaction = (id) =>
    api.get(`transactions/${id}/`);

export const createTransaction = (data) =>
    api.post("transactions/", data);

export const updateTransaction = (id, data) =>
    api.put(`transactions/${id}/`, data);

export const deleteTransaction = (id) =>
    api.delete(`transactions/${id}/`);

export const searchTransactions = (keyword) =>
    api.get(`transactions/?search=${keyword}`);

export const getTransactionsByPayment = (paymentId) =>
    api.get(`transactions/?payment=${paymentId}`);

export const printTransaction = (id) =>
    api.get(`transactions/${id}/print/`, {
        responseType: "blob",
    });