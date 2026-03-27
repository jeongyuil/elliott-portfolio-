import { Outlet } from 'react-router-dom';
import BottomNav from './BottomNav';

export default function KidLayout() {
    return (
        <div className="min-h-screen bg-[var(--bt-bg)] text-[var(--bt-text)] pb-[80px]">
            <Outlet />
            <BottomNav />
        </div>
    );
}
