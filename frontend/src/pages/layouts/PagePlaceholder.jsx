import { useLocation } from "react-router-dom";
import { menuItems } from "../../data/menuItems";

const PagePlaceholder = () => {
    const { pathname } = useLocation();

    const exactItem = menuItems.find((item) => item.path === pathname);
    const childItem = menuItems
        .flatMap((item) => item.children || [])
        .find((child) => child.path === pathname);

    const title = exactItem?.name || childItem?.name || pathname.replace(/\//g, " ").trim();

    return (
        <div className="p-6">
            <h1 className="text-3xl font-bold mb-4">{title}</h1>
            <p className="text-slate-600">This is the page content for <span className="font-medium">{pathname}</span>.</p>
        </div>
    );
};

export default PagePlaceholder;
