import api from "./axios";

// Reports
export const getSalesReport = (params) =>
    api.get("reports/sales/", {
        params,
    });

export const getInventoryReport = (params) =>
    api.get("reports/inventory/", {
        params,
    });

export const getPurchaseReport = (params) =>
    api.get("reports/purchases/", {
        params,
    });

export const getCustomerReport = (params) =>
    api.get("reports/customers/", {
        params,
    });

export const getSupplierReport = (params) =>
    api.get("reports/suppliers/", {
        params,
    });

export const getExpiryReport = (params) =>
    api.get("reports/expiry/", {
        params,
    });

export const getProfitReport = (params) =>
    api.get("reports/profit/", {
        params,
    });

export const exportSalesReport = (params) =>
    api.get("reports/sales/export/", {
        params,
        responseType: "blob",
    });

export const exportInventoryReport = (params) =>
    api.get("reports/inventory/export/", {
        params,
        responseType: "blob",
    });

export const exportPurchaseReport = (params) =>
    api.get("reports/purchases/export/", {
        params,
        responseType: "blob",
    });

export const exportCustomerReport = (params) =>
    api.get("reports/customers/export/", {
        params,
        responseType: "blob",
    });