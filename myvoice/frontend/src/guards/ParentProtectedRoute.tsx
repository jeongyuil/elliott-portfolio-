import { useAuth } from '../contexts/AuthContext';
import { Navigate, Outlet } from 'react-router-dom';

export default function ParentProtectedRoute() {
    const { isParentAuthenticated, isCheckingAuth } = useAuth();

    if (isCheckingAuth) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="w-8 h-8 border-4 border-[var(--bt-primary)] border-t-transparent rounded-full animate-spin" />
            </div>
        );
    }

    if (!isParentAuthenticated) {
        return <Navigate to="/login" replace />;
    }

    return <Outlet />;
}
