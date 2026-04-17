import { Home, ClipboardList, Gift, BookOpen, ArrowRightLeft } from "lucide-react";
import { useLocation, Link } from "react-router-dom";

export default function BottomNav() {
    const location = useLocation();

    const navItems = [
        { path: "/kid/home", icon: Home, label: "홈" },
        { path: "/kid/adventures", icon: ClipboardList, label: "모험" },
        { path: "/kid/shop", icon: Gift, label: "상점" },
        { path: "/kid/vocabulary", icon: BookOpen, label: "어휘" },
        { path: "/mode-select", icon: ArrowRightLeft, label: "전환" },
    ];

    return (
        <nav className="bt-bottom-nav">
            {navItems.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.path || location.pathname.startsWith(item.path + "/");

                return (
                    <Link key={item.path} to={item.path} className="flex-1">
                        <div className={`bt-nav-item ${isActive ? "active" : ""}`}>
                            <Icon size={24} strokeWidth={2.5} />
                            <span>{item.label}</span>
                        </div>
                    </Link>
                );
            })}
        </nav>
    );
}
