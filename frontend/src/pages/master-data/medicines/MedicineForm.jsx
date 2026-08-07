import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Save, ArrowLeft } from "lucide-react";
import { toast } from "react-toastify";

import {
    createMedicine,
    updateMedicine,
    getMedicine,
} from "../../../api/medicineApi";

import { getCategories } from "../../../api/categoryApi";

const UNIT_OPTIONS = [
    "Tablet",
    "Capsule",
    "Bottle",
    "Box",
    "Tube",
    "Injection",
    "Syrup",
    "Sachet",
    "Piece",
];

const MedicineForm = () => {
    const navigate = useNavigate();
    const { id } = useParams();
    const isEdit = Boolean(id);

    const [loading, setLoading] = useState(false);
    const [saving, setSaving] = useState(false);
    const [categories, setCategories] = useState([]);

    const [form, setForm] = useState({
        medicine_name: "",
        generic_name: "",
        category: "",
        unit: "",
        qty: "",
        buying_price: "",
        selling_price: "",
        expiry_date: "",
    });

    useEffect(() => {
        loadDropdowns();
        if (isEdit) {
            loadMedicine();
        }
    }, []);

    const loadDropdowns = async () => {
        try {
            const categoryRes = await getCategories();
            setCategories(categoryRes.data.results || categoryRes.data);
        } catch {
            toast.error("Unable to load dropdown data.");
        }
    };

    const loadMedicine = async () => {
        try {
            setLoading(true);
            const response = await getMedicine(id);
            const medicine = response.data;
            setForm({
                medicine_name: medicine.medicine_name || "",
                generic_name: medicine.generic_name || "",
                category: medicine.category || "",
                unit: medicine.unit || "",
                qty: medicine.qty?.toString() || "",
                buying_price: medicine.buying_price?.toString() || "",
                selling_price: medicine.selling_price?.toString() || "",
                expiry_date: medicine.expiry_date || "",
            });
        } catch {
            toast.error("Unable to load medicine.");
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setForm((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSaving(true);

        try {
            if (isEdit) {
                await updateMedicine(id, form);
                toast.success("Medicine updated successfully.");
            } else {
                await createMedicine(form);
                toast.success("Medicine created successfully.");
            }
            navigate("/medicines");
        } catch (error) {
            toast.error(
                error?.response?.data?.detail ||
                error?.response?.data?.message ||
                "Unable to save medicine."
            );
        } finally {
            setSaving(false);
        }
    };

    if (loading) {
        return (
            <div className="flex justify-center items-center h-96">
                Loading...
            </div>
        );
    }

    return (
        <div className="max-w-7xl mx-auto p-6">
            <div className="flex justify-between items-center mb-6">
                <div>
                    <h1 className="text-3xl font-bold">
                        {isEdit ? "Edit Medicine" : "Add Medicine"}
                    </h1>
                    <p className="text-gray-500">
                        Complete the medicine information below.
                    </p>
                </div>
                <button
                    type="button"
                    onClick={() => navigate(-1)}
                    className="flex items-center gap-2 border px-4 py-2 rounded-lg"
                >
                    <ArrowLeft size={18} />
                    Back
                </button>
            </div>

            <form onSubmit={handleSubmit} className="bg-white shadow rounded-xl p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <div>
                        <label className="block mb-2 font-medium">
                            Medicine Name
                        </label>
                        <input
                            type="text"
                            name="medicine_name"
                            value={form.medicine_name}
                            onChange={handleChange}
                            className="w-full border rounded-lg px-3 py-2"
                        />
                    </div>

                    <div>
                        <label className="block mb-2 font-medium">
                            Generic Name
                        </label>
                        <input
                            type="text"
                            name="generic_name"
                            value={form.generic_name}
                            onChange={handleChange}
                            className="w-full border rounded-lg px-3 py-2"
                        />
                    </div>

                    <div>
                        <label className="block mb-2 font-medium">
                            Category
                        </label>
                        <select
                            name="category"
                            value={form.category}
                            onChange={handleChange}
                            className="w-full border rounded-lg px-3 py-2"
                        >
                            <option value="">Select Category</option>
                            {categories.map((category) => (
                                <option key={category.id} value={category.id}>
                                    {category.category_name || category.name}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div>
                        <label className="block mb-2 font-medium">
                            Unit
                        </label>
                        <select
                            name="unit"
                            value={form.unit}
                            onChange={handleChange}
                            className="w-full border rounded-lg px-3 py-2"
                        >
                            <option value="">Select Unit</option>
                            {UNIT_OPTIONS.map((unit) => (
                                <option key={unit} value={unit}>
                                    {unit}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div>
                        <label className="block mb-2 font-medium">
                            Quantity
                        </label>
                        <input
                            type="number"
                            name="qty"
                            value={form.qty}
                            onChange={handleChange}
                            min="0"
                            className="w-full border rounded-lg px-3 py-2"
                        />
                    </div>

                    <div>
                        <label className="block mb-2 font-medium">
                            Buying Price
                        </label>
                        <input
                            type="number"
                            name="buying_price"
                            value={form.buying_price}
                            onChange={handleChange}
                            step="0.01"
                            min="0"
                            className="w-full border rounded-lg px-3 py-2"
                        />
                    </div>

                    <div>
                        <label className="block mb-2 font-medium">
                            Selling Price
                        </label>
                        <input
                            type="number"
                            name="selling_price"
                            value={form.selling_price}
                            onChange={handleChange}
                            step="0.01"
                            min="0"
                            className="w-full border rounded-lg px-3 py-2"
                        />
                    </div>

                    <div className="md:col-span-2 lg:col-span-1">
                        <label className="block mb-2 font-medium">
                            Expiry Date
                        </label>
                        <input
                            type="date"
                            name="expiry_date"
                            value={form.expiry_date}
                            onChange={handleChange}
                            className="w-full border rounded-lg px-3 py-2"
                        />
                    </div>
                </div>

                <div className="mt-8 flex justify-end gap-3">
                    <button
                        type="button"
                        onClick={() => navigate(-1)}
                        className="border px-5 py-2 rounded-lg"
                    >
                        Cancel
                    </button>
                    <button
                        type="submit"
                        disabled={saving}
                        className="flex items-center gap-2 bg-blue-600 text-white px-5 py-2 rounded-lg disabled:opacity-50"
                    >
                        <Save size={18} />
                        {saving ? "Saving..." : "Save Medicine"}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default MedicineForm;

//                         <label className="block mb-2 font-medium">

//                             Barcode

//                         </label>

//                         <input

//                             type="text"

//                             name="barcode"

//                             value={form.barcode}

//                             onChange={handleChange}

//                             className="w-full border rounded-lg px-3 py-2"

//                         />

//                     </div>

//                     <div>

//                         <label className="block mb-2 font-medium">

//                             RFID Tag

//                         </label>

//                         <input

//                             type="text"

//                             name="rfid_tag"

//                             value={form.rfid_tag}

//                             onChange={handleChange}

//                             className="w-full border rounded-lg px-3 py-2"

//                         />

//                     </div>

//                     <div>

//                         <label className="block mb-2 font-medium">

//                             Category

//                         </label>

//                         <select

//                             name="category"

//                             value={form.category}

//                             onChange={handleChange}

//                             className="w-full border rounded-lg px-3 py-2"

//                         >

//                             <option value="">Select Category</option>

//                             {categories.map((category) => (

//                                 <option

//                                     key={category.id}

//                                     value={category.id}

//                                 >

//                                     {category.name}

//                                 </option>

//                             ))}

//                         </select>

//                     </div>

//                     <div>

//                         <label className="block mb-2 font-medium">

//                             Supplier

//                         </label>

//                         <select

//                             name="supplier"

//                             value={form.supplier}

//                             onChange={handleChange}

//                             className="w-full border rounded-lg px-3 py-2"

//                         >

//                             <option value="">Select Supplier</option>

//                             {suppliers.map((supplier) => (

//                                 <option

//                                     key={supplier.id}

//                                     value={supplier.id}

//                                 >

//                                     {supplier.name}

//                                 </option>

//                             ))}

//                         </select>

//                     </div>

//                 </div>

//             </form>

//         </div>

//     );

// };

// export default MedicineForm;
