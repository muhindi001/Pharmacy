import React from "react";

const ExpiryTable = ({ medicines = [] }) => {
    return (
        <div className="bg-white rounded-xl shadow p-5">

            <h2 className="text-lg font-semibold text-orange-600 mb-5">
                Expiring Medicines
            </h2>

            <div className="overflow-x-auto">

                <table className="w-full">

                    <thead className="bg-orange-50">

                        <tr>
                            <th className="p-3 text-left">Medicine</th>
                            <th className="p-3 text-left">Batch</th>
                            <th className="p-3 text-left">Expiry Date</th>
                            <th className="p-3 text-right">Days Left</th>
                        </tr>

                    </thead>

                    <tbody>

                        {medicines.length === 0 ? (

                            <tr>
                                <td
                                    colSpan="4"
                                    className="text-center p-5 text-gray-500"
                                >
                                    No medicines nearing expiry.
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

                                    <td className="p-3">
                                        {item.expiry_date}
                                    </td>

                                    <td className="p-3 text-right font-semibold text-orange-600">
                                        {item.days_left}
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

export default ExpiryTable;