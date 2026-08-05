import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
});

// Automatically attach JWT token
API.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

const dashboardService = {
  // Dashboard Summary
  getDashboardSummary: async () => {
    const response = await API.get("dashboard/");
    return response.data;
  },

  // Sales
  getSalesSummary: async () => {
    const response = await API.get("sales/");
    return response.data;
  },

  // Payments
  getPaymentsSummary: async () => {
    const response = await API.get("payments/");
    return response.data;
  },

  // Transactions
  getTransactionsSummary: async () => {
    const response = await API.get("transactions/");
    return response.data;
  },

  // Inventory
  getInventorySummary: async () => {
    const response = await API.get("inventory/");
    return response.data;
  },

  // Low Stock
  getLowStock: async () => {
    const response = await API.get("inventory/?stock_status=LOW");
    return response.data;
  },

  // Expiring Medicines
  getExpiryAlerts: async () => {
    const response = await API.get("alerts/?alert_type=Near Expiry");
    return response.data;
  },

  // Alerts
  getAlerts: async () => {
    const response = await API.get("alerts/");
    return response.data;
  },

  // Goods Receiving
  getGoodsReceiving: async () => {
    const response = await API.get("goods-receiving/");
    return response.data;
  },

  // Warehouses
  getWarehouses: async () => {
    const response = await API.get("warehouses/");
    return response.data;
  },

  // RFID
  getRFIDScans: async () => {
    const response = await API.get("rfid/scans/");
    return response.data;
  },

  // Customers
  getCustomers: async () => {
    const response = await API.get("customers/");
    return response.data;
  },

  // Audit Logs
  getAuditLogs: async () => {
    const response = await API.get("audit/");
    return response.data;
  },

  // Recent Sales
  getRecentSales: async () => {
    const response = await API.get("sales/?ordering=-created_at");
    return response.data;
  },

  // Recent Transactions
  getRecentTransactions: async () => {
    const response = await API.get("transactions/?ordering=-created_at");
    return response.data;
  },
};

export default dashboardService;