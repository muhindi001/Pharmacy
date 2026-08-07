import api from "./axios";

// Medicines
export const getMedicines = (params) =>
    api.get("medicines/", { params });

export const getMedicine = (id) =>
    api.get(`medicines/${id}/`);

export const createMedicine = (data) =>
    api.post("medicines/", data);

export const updateMedicine = (id, data) =>
    api.put(`medicines/${id}/`, data);

export const deleteMedicine = (id) =>
    api.delete(`medicines/${id}/`);

// Search
export const searchMedicines = (keyword) =>
    api.get(`medicines/?search=${keyword}`);

// Barcode
export const searchBarcode = (barcode) =>
    api.get(`medicines/?barcode=${barcode}`);

// RFID
export const searchRFID = (rfid) =>
    api.get(`medicines/?rfid_tag=${rfid}`);

// Import Excel
export const importMedicines = (data) =>
    api.post("medicines/import/", data, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });

// Export Excel
export const exportMedicines = () =>
    api.get("medicines/export/", {
        responseType: "blob",
    });