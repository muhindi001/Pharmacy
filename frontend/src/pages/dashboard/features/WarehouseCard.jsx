import React from "react";

const WarehouseCard = ({ warehouses = [] }) => {

    return (

        <div className="bg-white rounded-xl shadow p-5">

            <h2 className="text-lg font-semibold mb-5">
                Warehouse Summary
            </h2>

            <div className="overflow-x-auto">

                <table className="w-full">

                    <thead className="bg-gray-100">

                        <tr>

                            <th className="p-3 text-left">
                                Warehouse
                            </th>

                            <th className="p-3 text-right">
                                Medicines
                            </th>

                            <th className="p-3 text-right">
                                Stock
                            </th>

                        </tr>

                    </thead>

                    <tbody>

                        {warehouses.length === 0 ? (

                            <tr>

                                <td
                                    colSpan="3"
                                    className="text-center p-5 text-gray-500"
                                >
                                    No warehouses found.
                                </td>

                            </tr>

                        ) : (

                            warehouses.map((warehouse) => (

                                <tr
                                    key={warehouse.id}
                                    className="border-b hover:bg-gray-50"
                                >

                                    <td className="p-3">

                                        {warehouse.warehouse_name}

                                    </td>

                                    <td className="p-3 text-right">

                                        {warehouse.total_medicines}

                                    </td>

                                    <td className="p-3 text-right font-semibold">

                                        {warehouse.total_stock}

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

export default WarehouseCard;