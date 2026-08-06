import {
    Database,
    Tags,
    Truck,
    Factory,
    Pill,
    LayoutDashboard,
    Boxes,
    Package,
    PackageCheck,
    ClipboardCheck,
    MonitorSmartphone,
    Receipt,
    CreditCard,
    ArrowLeftRight,
    ScanLine,
    FileText,
    Warehouse,
    ShoppingCart,
    Users,
    User,
} from "lucide-react";

export const menuItems = [
    {
        name: "Dashboard",
        path: "/dashboard",
        icon: LayoutDashboard,
    },

    {
        name: "Master Data",
        path: "/master-data",
        icon: Database,
        children: [
            { name: "Categories", path: "/categories", icon: Tags },
            { name: "Suppliers", path: "/suppliers", icon: Truck },
            { name: "Manufacturers", path: "/manufacturers", icon: Factory },
            { name: "Medicines", path: "/medicines", icon: Pill },
            { name: "Customers", path: "/customers", icon: Users },
        ],
    },

    {
        name: "Inventory",
        icon: Boxes,
        children: [
            { name: "Inventory", path: "/inventory", icon: Package },
            { name: "Batches", path: "/inventory/batches", icon: PackageCheck },
            { name: "Goods Receiving", path: "/inventory/goods-receiving", icon: ClipboardCheck },
            { name: "Stock Adjustment", path: "/inventory/stock-adjustment", icon: ArrowLeftRight },
            { name: "RFID", path: "/inventory/rfid", icon: ScanLine },
        ],
    },

    // { name: "Warehouses", path: "/warehouses", icon: Warehouse },

    {
        name: "Sales",
        icon: ShoppingCart,
        children: [
            { name: "POS", path: "/sales/pos", icon: MonitorSmartphone },
            { name: "Sales", path: "/sales", icon: Receipt },
            { name: "Payments", path: "/sales/payments", icon: CreditCard },
            { name: "Transactions", path: "/sales/transactions", icon: ArrowLeftRight },
            { name: "Invoices", path: "/sales/invoices", icon: FileText },
        ],
    },

    { name: "Profile", path: "/profile", icon: User },
];