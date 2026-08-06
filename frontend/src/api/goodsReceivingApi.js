import api from "./axios";

// Goods Receiving
export const getGoodsReceiving = () =>
    api.get("goods-receiving/");

export const getGoodsReceivingDetail = (id) =>
    api.get(`goods-receiving/${id}/`);

export const createGoodsReceiving = (data) =>
    api.post("goods-receiving/", data);

export const updateGoodsReceiving = (id, data) =>
    api.put(`goods-receiving/${id}/`, data);

export const deleteGoodsReceiving = (id) =>
    api.delete(`goods-receiving/${id}/`);

export const approveGoodsReceiving = (id) =>
    api.post(`goods-receiving/${id}/approve/`);

export const searchGoodsReceiving = (keyword) =>
    api.get(`goods-receiving/?search=${keyword}`);

export const printGRN = (id) =>
    api.get(`goods-receiving/${id}/print/`, {
        responseType: "blob",
    });