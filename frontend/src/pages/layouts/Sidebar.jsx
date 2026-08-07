import { useEffect, useState } from "react";
import { NavLink, useLocation } from "react-router-dom";
import { menuItems } from "../../data/menuItems";
import { LogOut, ChevronDown, ChevronUp } from "lucide-react";

const Sidebar = () => {
    const location = useLocation();
    const [openMenu, setOpenMenu] = useState(null);

    useEffect(() => {
        const activeMenu = menuItems.find((item) =>
            item.children?.some((child) => location.pathname === child.path)
        );
        setOpenMenu(activeMenu?.name || null);
    }, [location.pathname]);

    const toggleMenu = (name) => {
        setOpenMenu((current) => (current === name ? null : name));
    };

    return (
        <aside className="w-64 sticky top-0 h-screen bg-white border-r border-slate-200 shadow-sm p-4 flex flex-col justify-between">
            <nav className="space-y-2 overflow-y-auto">
                {menuItems.map((item) => {
                    const Icon = item.icon;
                    if (item.children) {
                        return (
                            <div key={item.name} className="space-y-2">
                                <button
                                    type="button"
                                    onClick={() => toggleMenu(item.name)}
                                    className="w-full flex items-center justify-between rounded-lg px-3 py-2 text-slate-700 bg-slate-50 hover:bg-slate-100"
                                >
                                    <span className="flex items-center gap-3">
                                        <Icon size={20} />
                                        <span className="font-semibold">{item.name}</span>
                                    </span>
                                    {openMenu === item.name ? (
                                        <ChevronUp size={18} />
                                    ) : (
                                        <ChevronDown size={18} />
                                    )}
                                </button>
                                {openMenu === item.name && (
                                    <div className="space-y-1 pl-10">
                                        {item.children.map((child) => {
                                            const ChildIcon = child.icon;
                                            return (
                                                <NavLink
                                                    key={child.path}
                                                    to={child.path}
                                                    className={({ isActive }) =>
                                                        `flex items-center gap-3 rounded-lg px-3 py-2 transition-colors ${
                                                            isActive
                                                                ? "bg-blue-100 text-blue-700"
                                                                : "text-slate-700 hover:bg-slate-100"
                                                        }`
                                                    }
                                                >
                                                    <ChildIcon size={18} />
                                                    <span>{child.name}</span>
                                                </NavLink>
                                            );
                                        })}
                                    </div>
                                )}
                            </div>
                        );
                    }
                    return (
                        <NavLink
                            key={item.path}
                            to={item.path}
                            className={({ isActive }) =>
                                `flex items-center gap-3 rounded-lg px-3 py-2 transition-colors ${
                                    isActive
                                        ? "bg-blue-100 text-blue-700"
                                        : "text-slate-700 hover:bg-slate-100"
                                }`
                            }
                        >
                            <Icon size={20} />
                            <span>{item.name}</span>
                        </NavLink>
                    );
                })}
            </nav>

            <div className="pt-4 mt-4 border-t border-slate-400">
                <NavLink
                    to="/logout"
                    className="flex items-center gap-3 rounded-lg px-3 py-2 text-white bg-red-500 hover:bg-red-300"
                >
                    <LogOut size={20} />
                    <span>Logout</span>
                </NavLink>
            </div>
        </aside>
    );
};

export default Sidebar;
