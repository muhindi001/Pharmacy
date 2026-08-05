import React from "react";

const LowStockTable = ({ medicines = [] }) => {

    return (

        <div className="bg-white rounded-xl shadow p-5">

            <h2 className="text-lg font-semibold mb-5 text-red-600">
                Low Stock Medicines
            </h2>

            <div className="overflow-x-auto">

                <table className="w-full">

                    <thead className="bg-red-50">

                        <tr>

                            <th className="p-3 text-left">
                                Medicine
                            </th>

                            <th className="p-3 text-left">
                                Batch
                            </th>

                            <th className="p-3 text-right">
                                Available
                            </th>

                            <th className="p-3 text-right">
                                Reorder Level
                            </th>

                        </tr>

                    </thead>

                    <tbody>

                        {medicines.length === 0 ? (

                            <tr>

                                <td
                                    colSpan="4"
                                    className="text-center p-5 text-gray-500"
                                >
                                    No low stock medicines
                                </td>

                            </tr>

                        ) : (

                            medicines.map((item) => (

                                <tr
                                    key={item.id}
                                    className="border-b hover:bg-gray-50"
                                >

                                    <td className="p-3">
                                        {item.medicine_name}
                                    </td>

                                    <td className="p-3">
                                        {item.batch_number}
                                    </td>

                                    <td className="p-3 text-right text-red-600 font-bold">
                                        {item.available_quantity}
                                    </td>

                                    <td className="p-3 text-right">
                                        {item.reorder_level}
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

export default LowStockTable;