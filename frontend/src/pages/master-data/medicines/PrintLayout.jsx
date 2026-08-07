import React, { useRef } from "react";
import { Printer } from "lucide-react";
import html2canvas from "html2canvas";
import jsPDF from "jspdf";

const PrintLayout = ({ sale }) => {
    const printRef = useRef(null);
    const receipt = sale || {
        pharmacy: "ABC PHARMACY",
        saleNo: "SAL-20260807-001",
        cashier: "John",
        warehouse: "Main Store",
        saleType: "Cash",
        customer: "Walk-in",
        paymentMethod: "Cash",
        amountPaid: 0,
        change: 0,
        subtotal: 0,
        discount: 0,
        vat: 0,
        grandTotal: 0,
        items: [],
    };

    const formatMoney = (value) =>
        Number(value).toLocaleString();

    const handleDownloadPDF = async () => {
        if (!printRef.current) return;

        const element = printRef.current;
        const canvas = await html2canvas(element, {
            scale: 2,
            useCORS: true,
            backgroundColor: "#ffffff",
        });

        const imgData = canvas.toDataURL("image/png");
        const pdf = new jsPDF({ unit: "pt", format: "a4" });
        const pageWidth = pdf.internal.pageSize.getWidth();
        const pageHeight = pdf.internal.pageSize.getHeight();
        const imgWidth = pageWidth - 40;
        const imgHeight = (canvas.height * imgWidth) / canvas.width;

        pdf.addImage(imgData, "PNG", 20, 20, imgWidth, imgHeight);
        pdf.save(`${receipt.saleNo || "receipt"}.pdf`);
    };

    return (
        <div className="max-w-4xl mx-auto p-6">

            <div className="flex justify-end mb-4 print:hidden">

                <button
                    onClick={handleDownloadPDF}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg flex items-center gap-2"
                >
                    <Printer size={18} />
                    Download PDF
                </button>

            </div>

            <div ref={printRef} className="bg-white border rounded-lg p-8 print:border-0">

                {/* Header */}

                <div className="text-center mb-8">

                    <h1 className="text-3xl font-bold">
                        {receipt.pharmacy}
                    </h1>

                    <p className="text-gray-600">
                        SALES RECEIPT
                    </p>

                </div>

                {/* Sale Information */}

                <div className="mb-6">

                    <h2 className="font-bold border-b pb-2 mb-3">
                        SALE INFORMATION
                    </h2>

                    <div className="grid grid-cols-2 gap-2">

                        <p><strong>Sale No:</strong> {receipt.saleNo}</p>

                        <p><strong>Cashier:</strong> {receipt.cashier}</p>

                        <p><strong>Warehouse:</strong> {receipt.warehouse}</p>

                        <p><strong>Sale Type:</strong> {receipt.saleType}</p>

                    </div>

                </div>

                {/* Customer */}

                <div className="mb-6">

                    <h2 className="font-bold border-b pb-2 mb-3">
                        CUSTOMER
                    </h2>

                    <p>
                        <strong>Customer:</strong> {receipt.customer}
                    </p>

                </div>

                {/* Cart */}

                <div className="mb-6">

                    <h2 className="font-bold border-b pb-2 mb-3">
                        CART
                    </h2>

                    <table className="w-full border-collapse">

                        <thead>

                            <tr className="border-b">

                                <th className="text-left py-2">
                                    Medicine
                                </th>

                                <th className="text-left">
                                    Batch
                                </th>

                                <th className="text-center">
                                    Qty
                                </th>

                                <th className="text-right">
                                    Price
                                </th>

                                <th className="text-right">
                                    Total
                                </th>

                            </tr>

                        </thead>

                        <tbody>

                            {receipt.items.map((item, index) => (

                                <tr
                                    key={index}
                                    className="border-b"
                                >

                                    <td className="py-2">
                                        {item.medicine}
                                    </td>

                                    <td>
                                        {item.batch}
                                    </td>

                                    <td className="text-center">
                                        {item.quantity}
                                    </td>

                                    <td className="text-right">
                                        {formatMoney(item.price)}
                                    </td>

                                    <td className="text-right font-semibold">
                                        {formatMoney(item.total)}
                                    </td>

                                </tr>

                            ))}

                        </tbody>

                    </table>

                </div>

                {/* Payment */}

                <div className="mb-6">

                    <h2 className="font-bold border-b pb-2 mb-3">
                        PAYMENT
                    </h2>

                    <div className="grid grid-cols-2 gap-2">

                        <p>
                            <strong>Method:</strong> {receipt.paymentMethod}
                        </p>

                        <p>
                            <strong>Amount Paid:</strong> TZS {formatMoney(receipt.amountPaid)}
                        </p>

                        <p>
                            <strong>Change:</strong> TZS {formatMoney(receipt.change)}
                        </p>

                    </div>

                </div>

                {/* Summary */}

                <div className="flex justify-end">

                    <div className="w-80">

                        <h2 className="font-bold border-b pb-2 mb-3">
                            SUMMARY
                        </h2>

                        <div className="space-y-2">

                            <div className="flex justify-between">

                                <span>Subtotal</span>

                                <span>
                                    TZS {formatMoney(receipt.subtotal)}
                                </span>

                            </div>

                            <div className="flex justify-between">

                                <span>Discount</span>

                                <span>
                                    TZS {formatMoney(receipt.discount)}
                                </span>

                            </div>

                            <div className="flex justify-between">

                                <span>VAT</span>

                                <span>
                                    TZS {formatMoney(receipt.vat)}
                                </span>

                            </div>

                            <hr />

                            <div className="flex justify-between text-xl font-bold">

                                <span>Grand Total</span>

                                <span>
                                    TZS {formatMoney(receipt.grandTotal)}
                                </span>

                            </div>

                        </div>

                    </div>

                </div>

                {/* Footer */}

                <div className="mt-10 text-center text-sm text-gray-500">

                    Thank you for choosing {receipt.pharmacy}

                </div>

            </div>

        </div>
    );
};

export default PrintLayout;