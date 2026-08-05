import React from "react";

import {
    ResponsiveContainer,
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    CartesianGrid,
} from "recharts";

const SalesChart = ({ data }) => {
    return (
        <div className="bg-white rounded-xl shadow-md p-5">

            <h2 className="text-lg font-semibold mb-5">
                Weekly Sales
            </h2>

            <ResponsiveContainer
                width="100%"
                height={320}
            >
                <LineChart data={data}>

                    <CartesianGrid strokeDasharray="3 3" />

                    <XAxis dataKey="day" />

                    <YAxis />

                    <Tooltip />

                    <Line
                        type="monotone"
                        dataKey="sales"
                        strokeWidth={3}
                    />

                </LineChart>
            </ResponsiveContainer>

        </div>
    );
};

export default SalesChart;