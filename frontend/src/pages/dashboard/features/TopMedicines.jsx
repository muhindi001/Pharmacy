import React from "react";

const TopMedicines = ({ medicines = [] }) => {

    return (

        <div className="bg-white rounded-xl shadow p-5">

            <h2 className="text-lg font-semibold mb-5">

                Top Selling Medicines

            </h2>

            <table className="w-full">

                <thead className="bg-gray-100">

                    <tr>

                        <th className="text-left p-3">
                            Medicine
                        </th>

                        <th className="text-right p-3">
                            Sold
                        </th>

                        <th className="text-right p-3">
                            Revenue
                        </th>

                    </tr>

                </thead>

                <tbody>

                    {medicines.length === 0 ? (

                        <tr>

                            <td
                                colSpan="3"
                                className="text-center p-5 text-gray-500"
                            >
                                No sales available.
                            </td>

                        </tr>

                    ) : (

                        medicines.map((medicine) => (

                            <tr
                                key={medicine.id}
                                className="border-b hover:bg-gray-50"
                            >

                                <td className="p-3">

                                    {medicine.name}

                                </td>

                                <td className="p-3 text-right">

                                    {medicine.quantity}

                                </td>

                                <td className="p-3 text-right font-semibold">

                                    TZS {medicine.revenue}

                                </td>

                            </tr>

                        ))

                    )}

                </tbody>

            </table>

        </div>

    );

};

export default TopMedicines;