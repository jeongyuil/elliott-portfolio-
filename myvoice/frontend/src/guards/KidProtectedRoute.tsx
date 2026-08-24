import { useAuth } from '../contexts/AuthContext';
import { Navigate, Outlet } from 'react-router-dom';

export default function KidProtectedRoute() {
    const { isChildAuthenticated } = useAuth();

    if (!isChildAuthenticated) {
        return <Navigate to="/mode-select" replace />;
    }

    return <Outlet />;
}
