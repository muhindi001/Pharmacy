import api from "./axios";

// RFID Tags
export const getRFIDTags = () =>
    api.get("rfid/");

export const getRFIDTag = (id) =>
    api.get(`rfid/${id}/`);

export const createRFIDTag = (data) =>
    api.post("rfid/", data);

export const updateRFIDTag = (id, data) =>
    api.put(`rfid/${id}/`, data);

export const deleteRFIDTag = (id) =>
    api.delete(`rfid/${id}/`);

export const searchRFIDTags = (keyword) =>
    api.get(`rfid/?search=${keyword}`);

export const scanRFID = (data) =>
    api.post("rfid/scan/", data);

export const assignRFID = (data) =>
    api.post("rfid/assign/", data);

export const unassignRFID = (id) =>
    api.post(`rfid/${id}/unassign/`);