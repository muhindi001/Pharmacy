import React, { useEffect, useState } from "react";

import {
    DollarSign,
    ShoppingCart,
    Package,
    Bell,
    Warehouse,
    Users,
    CreditCard,
    Activity,
} from "lucide-react";

import { getDashboard } from "../../api/dashboardApi";
import DashboardFilter from "./components/DashboardFilter";

import StatCard from "./features/StatCard";
import SalesChart from "./features/SalesChart";
import InventoryChart from "./features/InventoryChart";
import StockStatusCard from "./features/StockStatusCard";
import RecentSalesTable from "./features/RecentSalesTable";
import LowStockTable from "./features/LowStockTable";
import ExpiryTable from "./features/ExpiryTable";
import AlertsCard from "./features/AlertsCard";
import WarehouseCard from "./features/WarehouseCard";
import RFIDStatusCard from "./features/RFIDStatusCard";
import TopMedicines from "./features/TopMedicines";
import RecentActivities from "./features/RecentActivities";

const Dashboard = () => {

    const [loading, setLoading] = useState(true);

    const [dashboard, setDashboard] = useState({
        sales_today: 0,
        revenue_today: 0,
        inventory_items: 0,
        customers: 0,
        alerts: 0,
        warehouses: 0,
        transactions: 0,
        goods_received_today: 0,
        sales_chart: [],
        inventory_chart: [],
    });

    useEffect(() => {
        loadDashboard();
    }, []);

    const loadDashboard = async (filters = {}) => {
        try {
            const response = await getDashboard(filters);
            setDashboard(response.data);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {

        return (

            <div className="flex justify-center items-center h-screen">

                <div className="text-xl font-semibold">

                    Loading Dashboard...

                </div>

            </div>

        );

    }

    return (
        <div className="p-6">
            <div className="sticky top-0 bg-slate-200 z-10 mb-6 py-4">
                <div className="flex items-center justify-between gap-4">
                    <div>
                        <h1 className="text-3xl font-bold">Pharmacy Dashboard</h1>
                        <p className="text-gray-500">Welcome to Pharmacy system</p>
                    </div>

                    <div className="min-w-[320px]">
                        <DashboardFilter onFilter={loadDashboard} />
                    </div>
                </div>
            </div>

            {/* Statistics */}
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
                <StatCard
                    title="Today's Sales"
                    value={dashboard.sales_today}
                    color="bg-blue-500"
                    icon={<ShoppingCart size={20} />}
                />
                <StatCard
                    title="Revenue"
                    value={`TZS ${dashboard.revenue_today}`}
                    color="bg-green-500"
                    icon={<DollarSign size={20} />}
                />
                <StatCard
                    title="Inventory"
                    value={dashboard.inventory_items}
                    color="bg-purple-500"
                    icon={<Package size={20} />}
                />
                <StatCard
                    title="Customers"
                    value={dashboard.customers}
                    color="bg-cyan-500"
                    icon={<Users size={20} />}
                />
                <StatCard
                    title="Alerts"
                    value={dashboard.alerts}
                    color="bg-red-500"
                    icon={<Bell size={20} />}
                />
                <StatCard
                    title="Warehouses"
                    value={dashboard.warehouses}
                    color="bg-orange-500"
                    icon={<Warehouse size={20} />}
                />
                <StatCard
                    title="Transactions"
                    value={dashboard.transactions}
                    color="bg-indigo-500"
                    icon={<CreditCard size={20} />}
                />
                <StatCard
                    title="Goods Received"
                    value={dashboard.goods_received_today}
                    color="bg-emerald-500"
                    icon={<Activity size={20} />}
                />
            </div>

            {/* Charts */}
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 mt-8">
                <SalesChart data={dashboard.sales_chart} />
                <InventoryChart data={dashboard.inventory_chart} />
            </div>

            {/* Recent Activities */}
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 mt-8">
                <div className="bg-white rounded-xl shadow p-5">
                    <h2 className="font-semibold text-lg mb-4">Recent Sales</h2>
                    <table className="w-full">
                        <thead>
                            <tr className="border-b">
                                <th className="text-left py-2">Invoice</th>
                                <th className="text-left">Customer</th>
                                <th className="text-right">Amount</th>
                            </tr>
                        </thead>
                        <tbody>
                            {dashboard.recent_sales?.map((sale) => (
                                <tr key={sale.id} className="border-b">
                                    <td className="py-2">{sale.invoice_number}</td>
                                    <td>{sale.customer_name}</td>
                                    <td className="text-right">{sale.total_amount}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
                <div>
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                        <StockStatusCard
                            total={dashboard.inventory_items}
                            lowStock={dashboard.low_stock}
                            outOfStock={dashboard.out_of_stock}
                        />
                        <div className="lg:col-span-2">
                            <RecentSalesTable sales={dashboard.recent_sales} />
                        </div>
                    </div>
                </div>
            </div>

            <div className="mt-8">
                <LowStockTable medicines={dashboard.low_stock_list} />
            </div>

            {/* expire-alert-warehouse */}
            <div className="grid grid-cols-1 xl:grid-cols-3 gap-6 mt-8">
                <ExpiryTable medicines={dashboard.expiring_medicines} />
                <AlertsCard alerts={dashboard.alert_list} />
                <WarehouseCard warehouses={dashboard.warehouse_summary} />
            </div>

            {/* rfid-status-top-medicines */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-8">
                <RFIDStatusCard rfid={dashboard.rfid} />
                <TopMedicines medicines={dashboard.top_medicines} />
                <RecentActivities activities={dashboard.recent_activities} />
            </div>

            {/* Alerts */}
            <div className="bg-white rounded-xl shadow p-5 mt-8">
                <h2 className="font-semibold text-lg mb-4">Active Alerts</h2>
                <table className="w-full">
                    <thead>
                        <tr className="border-b">
                            <th className="text-left py-2">Medicine</th>
                            <th className="text-left">Alert</th>
                        </tr>
                    </thead>
                    <tbody>
                        {dashboard.alert_list?.map((alert) => (
                            <tr key={alert.id} className="border-b">
                                <td className="py-2">{alert.medicine_name}</td>
                                <td>{alert.alert_type}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default Dashboard;