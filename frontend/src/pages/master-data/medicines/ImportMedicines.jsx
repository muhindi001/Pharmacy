import { useState } from "react";
import { Upload, FileSpreadsheet, Loader2 } from "lucide-react";
import { toast } from "react-toastify";
import { importMedicines } from "../../../api/medicineApi";

const ImportMedicines = () => {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];

        if (!selectedFile) return;

        const allowedExtensions = [
            ".xlsx",
            ".xls",
            ".csv",
        ];

        const extension = selectedFile.name
            .substring(selectedFile.name.lastIndexOf("."))
            .toLowerCase();

        if (!allowedExtensions.includes(extension)) {
            toast.error("Please select an Excel or CSV file.");
            return;
        }

        setFile(selectedFile);
    };

    const handleImport = async (e) => {
        e.preventDefault();

        if (!file) {
            toast.warning("Please choose a file.");
            return;
        }

        const formData = new FormData();

        formData.append("file", file);

        try {
            setLoading(true);

            await importMedicines(formData);

            toast.success("Medicines imported successfully.");

            setFile(null);

            document.getElementById("medicine-file").value = "";
        } catch (error) {
            toast.error(
                error?.response?.data?.detail ||
                error?.response?.data?.message ||
                "Import failed."
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-3xl mx-auto p-6">

            <div className="bg-white rounded-xl shadow-lg p-8">

                <div className="flex items-center gap-3 mb-6">

                    <FileSpreadsheet
                        className="text-green-600"
                        size={36}
                    />

                    <div>

                        <h1 className="text-2xl font-bold">
                            Import Medicines
                        </h1>

                        <p className="text-gray-500">
                            Upload an Excel (.xlsx/.xls) or CSV file.
                        </p>

                    </div>

                </div>

                <form onSubmit={handleImport}>

                    <div className="border-2 border-dashed rounded-xl p-10 text-center">

                        <Upload
                            size={60}
                            className="mx-auto text-blue-600 mb-4"
                        />

                        <input
                            id="medicine-file"
                            type="file"
                            accept=".xlsx,.xls,.csv"
                            onChange={handleFileChange}
                            className="hidden"
                        />

                        <label
                            htmlFor="medicine-file"
                            className="cursor-pointer bg-blue-600 text-white px-5 py-3 rounded-lg inline-block hover:bg-blue-700"
                        >
                            Choose File
                        </label>

                        <p className="mt-4 text-gray-600">

                            {file
                                ? file.name
                                : "No file selected"}

                        </p>

                    </div>

                    <div className="mt-8 flex justify-end">

                        <button
                            disabled={loading}
                            className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg flex items-center gap-2 disabled:opacity-50"
                        >

                            {loading ? (
                                <>
                                    <Loader2
                                        size={18}
                                        className="animate-spin"
                                    />

                                    Importing...
                                </>
                            ) : (
                                <>
                                    <Upload size={18} />

                                    Import Medicines
                                </>
                            )}

                        </button>

                    </div>

                </form>

            </div>

        </div>
    );
};

export default ImportMedicines;