import React from "react";

const StockStatusCard = ({ total, lowStock, outOfStock }) => {
    return (
        <div className="bg-white rounded-xl shadow p-5">

            <h2 className="text-lg font-semibold mb-5">
                Stock Status
            </h2>

            <div className="space-y-4">

                <div className="flex justify-between items-center">
                    <span>Total Inventory</span>
                    <span className="font-bold text-blue-600">
                        {total}
                    </span>
                </div>

                <div className="flex justify-between items-center">
                    <span>Low Stock</span>
                    <span className="font-bold text-yellow-500">
                        {lowStock}
                    </span>
                </div>

                <div className="flex justify-between items-center">
                    <span>Out of Stock</span>
                    <span className="font-bold text-red-600">
                        {outOfStock}
                    </span>
                </div>

            </div>

        </div>
    );
};

export default StockStatusCard;