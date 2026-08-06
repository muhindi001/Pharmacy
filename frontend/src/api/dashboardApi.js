import api from "./axios";

// Dashboard Summary (supports optional filters below)

// Dashboard Statistics
export const getDashboardStats = () =>
    api.get("dashboard/stats/");

// Sales Chart
export const getSalesChart = () =>
    api.get("dashboard/sales-chart/");

// Inventory Chart
export const getInventoryChart = () =>
    api.get("dashboard/inventory-chart/");

// Recent Activities
export const getRecentActivities = () =>
    api.get("dashboard/recent-activities/");

// Top Medicines
export const getTopMedicines = () =>
    api.get("dashboard/top-medicines/");
export const getDashboard = (params = {}) =>
    api.get("dashboard/", {
        params,
    });