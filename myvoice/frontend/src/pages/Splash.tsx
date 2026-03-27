import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Splash() {
    const navigate = useNavigate();

    useEffect(() => {
        const timer = setTimeout(() => navigate('/', { replace: true }), 2000);
        return () => clearTimeout(timer);
    }, [navigate]);

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bt-gradient-night text-white">
            <div className="animate-bounce-in flex flex-col items-center">
                <div className="w-24 h-24 mb-6">
                    <img src="/assets/characters/luna.png" alt="루나" className="w-full h-full object-contain" />
                </div>
                <h1 className="text-3xl font-extrabold tracking-tight">밤토리</h1>
                <p className="text-sm text-white/60 mt-2">밤하늘의 친구들과 함께하는</p>
            </div>
            <div className="absolute bottom-12">
                <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            </div>
        </div>
    );
}
