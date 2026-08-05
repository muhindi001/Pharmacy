import React from "react";

const RecentSalesTable = ({ sales = [] }) => {

    return (

        <div className="bg-white rounded-xl shadow p-5">

            <h2 className="text-lg font-semibold mb-5">
                Recent Sales
            </h2>

            <div className="overflow-x-auto">

                <table className="w-full">

                    <thead className="bg-gray-100">

                        <tr>

                            <th className="p-3 text-left">Invoice</th>

                            <th className="p-3 text-left">Customer</th>

                            <th className="p-3 text-left">Cashier</th>

                            <th className="p-3 text-right">Amount</th>

                            <th className="p-3 text-center">Status</th>

                        </tr>

                    </thead>

                    <tbody>

                        {sales.length === 0 ? (

                            <tr>

                                <td
                                    colSpan="5"
                                    className="text-center p-5 text-gray-500"
                                >
                                    No sales available
                                </td>

                            </tr>

                        ) : (

                            sales.map((sale) => (

                                <tr
                                    key={sale.id}
                                    className="border-b hover:bg-gray-50"
                                >

                                    <td className="p-3">
                                        {sale.invoice_number}
                                    </td>

                                    <td className="p-3">
                                        {sale.customer_name}
                                    </td>

                                    <td className="p-3">
                                        {sale.cashier_name}
                                    </td>

                                    <td className="p-3 text-right">
                                        {sale.total_amount}
                                    </td>

                                    <td className="p-3 text-center">

                                        <span
                                            className={`px-3 py-1 rounded-full text-white text-sm
                                            ${
                                                sale.status === "PAID"
                                                    ? "bg-green-500"
                                                    : "bg-yellow-500"
                                            }`}
                                        >
                                            {sale.status}
                                        </span>

                                    </td>

                                </tr>

                            ))

                        )}

                    </tbody>

                </table>

            </div>

        </div>

    );

};

export default RecentSalesTable;