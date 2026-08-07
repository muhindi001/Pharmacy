import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
    Search,
    Plus,
    Upload,
    Download,
    ShoppingCart,
    Pencil,
    Trash2,
    RefreshCw,
} from "lucide-react";

import { toast } from "react-toastify";

import {
    getMedicines,
    deleteMedicine,
} from "../../../api/medicineApi";

import { getCategories } from "../../../api/categoryApi";
import SellingForm from "./SellingForm";

const MedicineList = () => {

    const [medicines, setMedicines] = useState([]);
    const [categories, setCategories] = useState([]);
    const [selectedMedicines, setSelectedMedicines] = useState([]);
    const [sellingItems, setSellingItems] = useState([]);

    const [loading, setLoading] = useState(false);

    const [search, setSearch] = useState("");

    const [category, setCategory] = useState("");

    const [page, setPage] = useState(1);

    const [totalPages, setTotalPages] = useState(1);

    const handleSearchChange = (e) => {
        setSearch(e.target.value);
        setPage(1);
    };

    const handleSearchKeyDown = (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            loadMedicines();
        }
    };

    useEffect(() => {

        loadMedicines();

        loadCategories();

    }, [page, search, category]);

    const loadMedicines = async () => {

        try {

            setLoading(true);

            const params = { page };

            if (search.trim()) {
                params.search = search.trim();
            }

            if (category) {
                params.category = category;
            }

            const response = await getMedicines(params);

            setMedicines(response.data.results || []);

            setTotalPages(response.data.total_pages || 1);

        } catch (error) {

            toast.error("Unable to load medicines.");

        } finally {

            setLoading(false);

        }

    };

    const loadCategories = async () => {

        try {

            const response = await getCategories();

            setCategories(response.data.results || response.data);

        } catch {

            toast.error("Unable to load categories.");

        }

    };

    const handleDelete = async (id) => {

        const confirmed = window.confirm(
            "Delete this medicine?"
        );

        if (!confirmed) return;

        try {

            await deleteMedicine(id);

            toast.success("Medicine deleted successfully.");

            loadMedicines();

        } catch {

            toast.error("Unable to delete medicine.");

        }

    };

    const openSellingForm = (items) => {
        setSellingItems(items);
    };

    const closeSellingForm = () => {
        setSellingItems([]);
    };

    const handleToggleSelect = (medicine) => {
        setSelectedMedicines((prev) => {
            const exists = prev.some((item) => item.id === medicine.id);
            if (exists) {
                return prev.filter((item) => item.id !== medicine.id);
            }
            return [...prev, medicine];
        });
    };

    const handleToggleSelectAll = () => {
        if (selectedMedicines.length === medicines.length) {
            setSelectedMedicines([]);
        } else {
            setSelectedMedicines([...medicines]);
        }
    };

    return (

        <div className="p-6">

            <div className="flex justify-between items-center mb-6">

                <div>

                    <h1 className="text-3xl font-bold">
                        Medicines
                    </h1>

                    <p className="text-gray-500">
                        Manage pharmacy medicines.
                    </p>

                </div>

                <Link
                    to="/medicines/create"
                    className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg"
                >

                    <Plus size={18} />

                    Add Medicine

                </Link>

            </div>

            <div className="bg-white rounded-xl shadow p-5">

                <div className="flex flex-wrap gap-4 mb-5">

                    <div className="relative flex-1">

                        <Search
                            className="absolute left-3 top-3 text-gray-400"
                            size={18}
                        />

                        <input
                            type="text"
                            placeholder="Search by medicine name..."
                            value={search}
                            onChange={handleSearchChange}
                            onKeyDown={handleSearchKeyDown}
                            className="w-full border rounded-lg pl-10 pr-3 py-2"
                        />

                    </div>

                    <select
                        value={category}
                        onChange={(e) => setCategory(e.target.value)}
                        className="border rounded-lg px-3 py-2"
                    >

                        <option value="">
                            All Categories
                        </option>

                        {categories.map((item) => (

                            <option
                                key={item.id}
                                value={item.id}
                            >

                                {item.name}

                            </option>

                        ))}

                    </select>


                    <button
                        onClick={loadMedicines}
                        className="bg-gray-600 text-white px-4 rounded-lg"
                    >

                        <RefreshCw size={18} />

                    </button>

                </div>

                <div className="flex flex-wrap gap-3 mb-5">

                    <Link
                        to="/medicines/import"
                        className="flex items-center gap-2 bg-green-600 text-white px-4 py-2 rounded-lg"
                    >

                        <Upload size={18} />

                        Import

                    </Link>

                    <button
                        className="flex items-center gap-2 bg-yellow-500 text-white px-4 py-2 rounded-lg"
                    >

                        <Download size={18} />

                        Export

                    </button>

                    <button
                        type="button"
                        disabled={selectedMedicines.length === 0}
                        onClick={() => openSellingForm(selectedMedicines)}
                        className={`flex items-center gap-2 px-4 py-2 rounded-lg text-white ${selectedMedicines.length === 0 ? "bg-gray-400 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"}`}
                    >
                        <ShoppingCart size={18} />
                        Sell and Print Selected ({selectedMedicines.length})
                    </button>

                </div>
                <div className="overflow-x-auto">

                    <table className="w-full">

                        <thead className="bg-gray-100">

                            <tr>

                                <th className="p-3 text-center">
                                    <input
                                        type="checkbox"
                                        checked={medicines.length > 0 && selectedMedicines.length === medicines.length}
                                        onChange={handleToggleSelectAll}
                                    />
                                </th>

                                <th className="p-3 text-left">Medicine</th>

                                <th className="p-3">Generic Name</th>

                                <th className="p-3">Category</th>

                                <th className="p-3">Unit</th>

                                <th className="p-3">Quantity</th>

                                <th className="p-3">Buying Price</th>

                                <th className="p-3">Selling Price</th>

                                <th className="p-3">Expiry Date</th>

                                <th className="p-3">Actions</th>

                            </tr>

                        </thead>

                        <tbody>

                            {loading ? (

                                <tr>

                                    <td
                                        colSpan="9"
                                        className="text-center p-10"
                                    >

                                        Loading...

                                    </td>

                                </tr>

                            ) : medicines.length === 0 ? (

                                <tr>

                                    <td
                                        colSpan="9"
                                        className="text-center p-10"
                                    >

                                        No medicines found.

                                    </td>

                                </tr>

                            ) : (

                                medicines.map((medicine) => (

                                    <tr
                                        key={medicine.id}
                                        className="border-b hover:bg-gray-50"
                                    >

                                        <td className="p-3 text-center">
                                            <input
                                                type="checkbox"
                                                checked={selectedMedicines.some((item) => item.id === medicine.id)}
                                                onChange={() => handleToggleSelect(medicine)}
                                            />
                                        </td>

                                        <td className="p-3 font-semibold">

                                            {medicine.medicine_name || medicine.name}

                                        </td>

                                        <td className="text-center">

                                            {medicine.generic_name}

                                        </td>

                                        <td className="text-center">

                                            {medicine.category_name}

                                        </td>

                                        <td className="text-center">

                                            {medicine.unit}

                                        </td>

                                        <td className="text-center">

                                            {medicine.qty}

                                        </td>

                                        <td className="text-center">

                                            {medicine.buying_price}

                                        </td>

                                        <td className="text-center">

                                            {medicine.selling_price}

                                        </td>

                                        <td className="text-center">

                                            {medicine.expiry_date}

                                        </td>

                                        <td className="p-3">

                                            <div className="flex justify-center gap-2">

                                                <button
                                                    type="button"
                                                    onClick={() => openSellingForm([medicine])}
                                                    className="text-blue-600 hover:text-blue-800"
                                                    title="Sell"
                                                >
                                                    <ShoppingCart size={18} />
                                                </button>

                                                <Link
                                                    to={`/medicines/edit/${medicine.id}`}
                                                    className="text-green-600 hover:text-green-800"
                                                    title="Edit"
                                                >
                                                    <Pencil size={18} />
                                                </Link>

                                                <button
                                                    onClick={() => handleDelete(medicine.id)}
                                                    className="text-red-600 hover:text-red-800"
                                                    title="Delete"
                                                >
                                                    <Trash2 size={18} />
                                                </button>

                                            </div>

                                        </td>

                                    </tr>

                                ))

                            )}

                        </tbody>

                    </table>

                </div>

            </div>

            <div className="flex justify-between items-center mt-6">

                <button
                    disabled={page === 1}
                    onClick={() => setPage(page - 1)}
                    className="px-4 py-2 border rounded-lg disabled:opacity-40"
                >
                    Previous
                </button>

                <span>

                    Page {page} of {totalPages}

                </span>

                <button
                    disabled={page === totalPages}
                    onClick={() => setPage(page + 1)}
                    className="px-4 py-2 border rounded-lg disabled:opacity-40"
                >
                    Next
                </button>

            </div>

            {sellingItems.length > 0 && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
                    <div className="relative w-full max-w-4xl">
                        <SellingForm
                            items={sellingItems}
                            onClose={closeSellingForm}
                        />
                    </div>
                </div>
            )}

        </div>
    );
};

export default MedicineList;