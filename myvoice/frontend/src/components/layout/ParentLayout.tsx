/**
 * Parent Layout - Bottom 4-tab navigation (홈/진행도/인사이트/설정)
 */
import { Outlet, useLocation, useNavigate } from 'react-router-dom';
import { Home, TrendingUp, MessageCircle, Settings } from 'lucide-react';

const TABS = [
    { path: '/parent/home', label: '홈', icon: Home },
    { path: '/parent/progress', label: '진행도', icon: TrendingUp },
    { path: '/parent/insights', label: '인사이트', icon: MessageCircle },
    { path: '/parent/settings', label: '설정', icon: Settings },
] as const;

export default function ParentLayout() {
    const location = useLocation();
    const navigate = useNavigate();

    return (
        <div className="min-h-screen bg-gray-50 text-gray-900 pb-[80px]">
            <Outlet />

            {/* Bottom Tab Bar */}
            <nav className="fixed bottom-0 left-0 right-0 z-40 bg-white border-t border-gray-200 px-2 py-2 flex justify-around items-center safe-area-bottom">
                {TABS.map((tab) => {
                    const isActive = location.pathname.startsWith(tab.path);
                    const Icon = tab.icon;
                    return (
                        <button
                            key={tab.path}
                            onClick={() => navigate(tab.path)}
                            className={`flex flex-col items-center gap-0.5 px-3 py-1 rounded-lg transition-colors min-w-[60px] ${
                                isActive
                                    ? 'text-[var(--bt-primary)]'
                                    : 'text-gray-400 hover:text-gray-600'
                            }`}
                        >
                            <Icon size={22} strokeWidth={isActive ? 2.5 : 1.8} />
                            <span className={`text-[10px] ${isActive ? 'font-bold' : 'font-medium'}`}>
                                {tab.label}
                            </span>
                        </button>
                    );
                })}
            </nav>
        </div>
    );
}
