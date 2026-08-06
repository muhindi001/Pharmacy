import api from "./axios";

// Audit Logs
export const getAuditLogs = () =>
    api.get("audit/");

export const getAuditLog = (id) =>
    api.get(`audit/${id}/`);

export const searchAuditLogs = (keyword) =>
    api.get(`audit/?search=${keyword}`);

export const filterAuditLogs = (params) =>
    api.get("audit/", {
        params,
    });

export const exportAuditLogs = () =>
    api.get("audit/export/", {
        responseType: "blob",
    });

export const getUserAuditLogs = (userId) =>
    api.get(`audit/?user=${userId}`);