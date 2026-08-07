import { useEffect, useState } from "react";
import { Printer, X } from "lucide-react";
import PrintLayout from "./PrintLayout";

const SellingForm = ({ items = [], onClose }) => {
    const [form, setForm] = useState({
        customerName: "",
    });
    const [quantities, setQuantities] = useState([]);
    const [showReceipt, setShowReceipt] = useState(false);
    const [receiptSale, setReceiptSale] = useState(null);
    const [isSold, setIsSold] = useState(false);

    useEffect(() => {
        if (items.length) {
            setQuantities(items.map((item) => {
                const availableQty = item.qty ?? 0;
                const quantity = 1;
                return {
                    id: item.id,
                    quantity,
                    availableQty,
                    remainingQty: Math.max(availableQty - quantity, 0),
                };
            }));
            setIsSold(false);
        }
    }, [items]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setForm((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleQuantityChange = (id, value) => {
        setQuantities((prev) => prev.map((item) => {
            if (item.id !== id) return item;
            const qty = Number(value) || 0;
            const quantity = Math.min(Math.max(qty, 0), item.availableQty);
            return {
                ...item,
                quantity,
                remainingQty: Math.max(item.availableQty - quantity, 0),
            };
        }));
    };

    const buildSale = () => {
        const saleItems = items.map((item) => {
            const qty = quantities.find((q) => q.id === item.id)?.quantity || 0;
            const price = Number(item.selling_price || 0);
            return {
                medicine: item.medicine_name || item.name || "",
                batch: item.batch || "-",
                quantity: qty,
                price,
                total: qty * price,
            };
        });

        const subtotal = saleItems.reduce((acc, item) => acc + item.total, 0);
        return {
            pharmacy: "ABC PHARMACY",
            saleNo: `SAL-${new Date().toISOString().slice(0, 10).replace(/-/g, "")}-${Math.floor(Math.random() * 1000).toString().padStart(3, "0")}`,
            cashier: "John",
            warehouse: "Main Store",
            saleType: "Cash",
            customer: form.customerName || "Walk-in",
            paymentMethod: "Cash",
            amountPaid: subtotal,
            change: 0,
            subtotal,
            discount: 0,
            vat: 0,
            grandTotal: subtotal,
            items: saleItems,
        };
    };

    const handleSell = () => {
        const sale = buildSale();
        setReceiptSale(sale);
        setShowReceipt(true);
        setIsSold(true);
    };

    return (
        <div className="max-w-3xl mx-auto p-6">

<div className="bg-white shadow-lg rounded-xl p-8 relative">
                    <button
                        type="button"
                        onClick={onClose}
                        className="absolute right-4 top-4 rounded-full bg-red-500 text-white p-2 shadow hover:bg-red-600"
                        title="Close"
                    >
                        <X size={18} />
                    </button>

                    <div className="text-center border-b pb-4 mb-6">

                        <h1 className="text-3xl font-bold text-blue-700">
                            ABC PHARMACY
                        </h1>

                        <p className="text-gray-500">
                            Medicine Selling Form
                        </p>

                    </div>
                {/* Customer */}

                <div className="mb-5">

                    <label className="block font-semibold mb-2">
                        Customer Name
                    </label>

                    <input
                        type="text"
                        name="customerName"
                        value={form.customerName}
                        onChange={handleChange}
                        placeholder="Enter customer name"
                        className="w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500"
                    />

                </div>

                {/* Selected Medicines */}

                <div className="mb-5">
                    <h2 className="font-semibold mb-3">Selected Medicines</h2>
                    <div className="space-y-4">
                        {items.map((item) => {
                            const qtyObj = quantities.find((q) => q.id === item.id) || { quantity: 1, availableQty: item.qty ?? 0 };
                            return (
                                <div key={item.id} className="grid grid-cols-1 md:grid-cols-3 gap-4 items-end border rounded-lg p-4 bg-gray-50">
                                    <div>
                                        <p className="font-semibold">{item.medicine_name || item.name}</p>
                                        <p className="text-sm text-gray-500">Batch: {item.batch || "-"}</p>
                                        <p className="text-sm text-gray-500">Remaining: {qtyObj.remainingQty}</p>
                                    </div>
                                    <div>
                                        <label className="block font-semibold mb-2">Quantity</label>
                                        <input
                                            type="number"
                                            min="1"
                                            max={qtyObj.availableQty}
                                            value={qtyObj.quantity}
                                            onChange={(e) => handleQuantityChange(item.id, e.target.value)}
                                            className="w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500"
                                        />
                                    </div>
                                    <div>
                                        <label className="block font-semibold mb-2">Price</label>
                                        <p className="text-lg font-semibold">TZS {item.selling_price}</p>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </div>

                {/* Buttons */}

                <div className="flex justify-end mt-8">
                    <button
                        type="button"
                        onClick={handleSell}
                        disabled={isSold}
                        className={`flex items-center gap-2 px-6 py-3 rounded-lg text-white ${isSold ? "bg-gray-400 cursor-not-allowed" : "bg-green-600 hover:bg-green-700"}`}
                    >
                        <Printer size={18} />
                        {isSold ? "Done" : "Sell and Print"}
                    </button>
                </div>

            </div>

            {showReceipt && receiptSale && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
                    <div className="relative w-full max-w-4xl bg-white rounded-xl overflow-hidden shadow-xl">
                        <button
                            type="button"
                            onClick={() => setShowReceipt(false)}
                            className="absolute right-4 top-4 rounded-full bg-red-500 text-white p-2 shadow hover:bg-red-600 z-10"
                        >
                            <X size={18} />
                        </button>
                        <PrintLayout sale={receiptSale} />
                        <div className="border-t p-4 text-right bg-gray-50">
                            <button
                                type="button"
                                onClick={() => setShowReceipt(false)}
                                className="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-5 py-2 text-white hover:bg-blue-700"
                            >
                                Back to Selling Form
                            </button>
                        </div>
                    </div>
                </div>
            )}

        </div>
    );
};

export default SellingForm;