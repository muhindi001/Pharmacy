import api from "./axios";

// Warehouses
export const getWarehouses = () =>
    api.get("warehouses/");

export const getWarehouse = (id) =>
    api.get(`warehouses/${id}/`);

export const createWarehouse = (data) =>
    api.post("warehouses/", data);

export const updateWarehouse = (id, data) =>
    api.put(`warehouses/${id}/`, data);

export const deleteWarehouse = (id) =>
    api.delete(`warehouses/${id}/`);

export const searchWarehouses = (keyword) =>
    api.get(`warehouses/?search=${keyword}`);