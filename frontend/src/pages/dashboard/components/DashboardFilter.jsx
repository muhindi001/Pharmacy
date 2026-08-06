import { useState, useEffect } from "react";

const DashboardFilter = ({ onFilter }) => {
    const [fromDate, setFromDate] = useState("");
    const [toDate, setToDate] = useState("");

    const handleFilter = () => {
        onFilter({
            start_date: fromDate,
            end_date: toDate,
        });
    };

    const handleReset = () => {
        setFromDate("");
        setToDate("");

        onFilter({});
    };

    // Auto-fetch when dates change (debounced)
    useEffect(() => {
        const timer = setTimeout(() => {
            // Only trigger if either date is set (or if both cleared)
            if (fromDate || toDate) {
                onFilter({ start_date: fromDate, end_date: toDate });
            } else {
                // if both empty, send empty to reset
                onFilter({});
            }
        }, 600);

        return () => clearTimeout(timer);
    }, [fromDate, toDate, onFilter]);

    return (
        <div className="bg-white rounded-xl shadow p-3">
            <div className="flex items-center gap-3">
                <div className="flex flex-col">
                    <label className="text-sm text-slate-500">From</label>
                    <input
                        type="date"
                        value={fromDate}
                        onChange={(e) => setFromDate(e.target.value)}
                        className="border rounded-lg px-2 py-1"
                    />
                </div>

                <div className="flex flex-col">
                    <label className="text-sm text-slate-500">To</label>
                    <input
                        type="date"
                        value={toDate}
                        onChange={(e) => setToDate(e.target.value)}
                        className="border rounded-lg px-2 py-1"
                    />
                </div>

                <div className="flex items-center gap-2">
                    <button
                        onClick={handleFilter}
                        className="bg-blue-600 text-white px-3 py-1 rounded-lg"
                    >
                        Apply
                    </button>

                    <button
                        onClick={handleReset}
                        className="bg-gray-200 text-slate-700 px-3 py-1 rounded-lg"
                    >
                        Reset
                    </button>
                </div>
            </div>
        </div>
    );
};

export default DashboardFilter;