import React from "react";

import {
    ResponsiveContainer,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    CartesianGrid,
} from "recharts";

const InventoryChart = ({ data }) => {

    return (

        <div className="bg-white rounded-xl shadow-md p-5">

            <h2 className="text-lg font-semibold mb-5">
                Inventory by Category
            </h2>

            <ResponsiveContainer
                width="100%"
                height={320}
            >

                <BarChart data={data}>

                    <CartesianGrid strokeDasharray="3 3" />

                    <XAxis dataKey="category" />

                    <YAxis />

                    <Tooltip />

                    <Bar
                        dataKey="stock"
                    />

                </BarChart>

            </ResponsiveContainer>

        </div>

    );

};

export default InventoryChart;