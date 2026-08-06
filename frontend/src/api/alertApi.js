import api from "./axios";

// Alerts
export const getAlerts = () =>
    api.get("alerts/");

export const getAlert = (id) =>
    api.get(`alerts/${id}/`);

export const createAlert = (data) =>
    api.post("alerts/", data);

export const updateAlert = (id, data) =>
    api.put(`alerts/${id}/`, data);

export const deleteAlert = (id) =>
    api.delete(`alerts/${id}/`);

export const searchAlerts = (keyword) =>
    api.get(`alerts/?search=${keyword}`);

export const getUnreadAlerts = () =>
    api.get("alerts/?status=New");

export const markAlertRead = (id) =>
    api.patch(`alerts/${id}/`, {
        status: "Read",
    });

export const getLowStockAlerts = () =>
    api.get("alerts/?alert_type=Low Stock");

export const getExpiryAlerts = () =>
    api.get("alerts/?alert_type=Expiry");