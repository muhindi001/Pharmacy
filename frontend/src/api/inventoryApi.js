import api from "./axios";

// Inventory
export const getInventory = () =>
    api.get("inventory/");

export const getInventoryItem = (id) =>
    api.get(`inventory/${id}/`);

export const createInventory = (data) =>
    api.post("inventory/", data);

export const updateInventory = (id, data) =>
    api.put(`inventory/${id}/`, data);

export const deleteInventory = (id) =>
    api.delete(`inventory/${id}/`);

export const searchInventory = (keyword) =>
    api.get(`inventory/?search=${keyword}`);

export const getLowStock = () =>
    api.get("inventory/?stock_status=LOW");

export const getOutOfStock = () =>
    api.get("inventory/?stock_status=OUT");

export const getInventoryByWarehouse = (warehouseId) =>
    api.get(`inventory/?warehouse=${warehouseId}`);

export const getInventoryByMedicine = (medicineId) =>
    api.get(`inventory/?medicine=${medicineId}`);