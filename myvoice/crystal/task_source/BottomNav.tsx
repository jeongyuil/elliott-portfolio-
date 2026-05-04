/**
 * BottomNav Component
 * Design Philosophy: Duolingo-style bottom navigation with semantic colors
 * - 5 main tabs: Home, Missions, Shop, Vocabulary, Profile
 * - Active state uses green (#58CC02)
 * - Clean icons with labels
 */

import { Home, ClipboardList, Gift, BookOpen, User } from "lucide-react";
import { useLocation, Link } from "wouter";

export default function BottomNav() {
  const [location] = useLocation();

  const navItems = [
    { path: "/home", icon: Home, label: "홈" },
    { path: "/missions", icon: ClipboardList, label: "미션" },
    { path: "/shop", icon: Gift, label: "보상" },
    { path: "/vocabulary", icon: BookOpen, label: "어휘" },
    { path: "/profile", icon: User, label: "프로필" },
  ];

  return (
    <nav className="duo-bottom-nav">
      {navItems.map((item) => {
        const Icon = item.icon;
        const isActive = location === item.path || location.startsWith(item.path + "/");
        
        return (
          <Link key={item.path} href={item.path}>
            <div className={`duo-nav-item ${isActive ? "active" : ""}`}>
              <Icon size={24} strokeWidth={2.5} />
              <span>{item.label}</span>
            </div>
          </Link>
        );
      })}
    </nav>
  );
}
