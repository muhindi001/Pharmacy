import api from "./axios";

// Customers
export const getCustomers = () =>
    api.get("customers/");

export const getCustomer = (id) =>
    api.get(`customers/${id}/`);

export const createCustomer = (data) =>
    api.post("customers/", data);

export const updateCustomer = (id, data) =>
    api.put(`customers/${id}/`, data);

export const deleteCustomer = (id) =>
    api.delete(`customers/${id}/`);

export const searchCustomers = (keyword) =>
    api.get(`customers/?search=${keyword}`);

export const getCustomerSales = (customerId) =>
    api.get(`customers/${customerId}/sales/`);

export const getCustomerPayments = (customerId) =>
    api.get(`customers/${customerId}/payments/`);

export const getCustomerInvoices = (customerId) =>
    api.get(`customers/${customerId}/invoices/`);