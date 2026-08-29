/**
 * Parent Home — Wireframe 01: 학부모 대시보드
 * 통계 그리드(4열), 주간 바 차트, 리포트 목록
 */
import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
    Clock, TrendingUp, BookOpen, FileText,
    ChevronRight, Settings,
} from 'lucide-react';
import { parentApi } from '@/api/client';
import type { ChildProfile, DashboardStats, Report } from '@/api/types';
import { toast } from 'sonner';

const DAY_LABELS = ['월', '화', '수', '목', '금', '토', '일'];

export default function ParentHome() {
    const navigate = useNavigate();
    const [children, setChildren] = useState<ChildProfile[]>([]);
    const [selectedChild, setSelectedChild] = useState<ChildProfile | null>(null);
    const [stats, setStats] = useState<DashboardStats | null>(null);
    const [reports, setReports] = useState<Report[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        (async () => {
            try {
                const data = await parentApi.listChildren();
                setChildren(data);
                if (data.length > 0) setSelectedChild(data[0]);
            } catch {
                toast.error('아이 목록을 불러오지 못했습니다.');
            } finally {
                setIsLoading(false);
            }
        })();
    }, []);

    useEffect(() => {
        if (!selectedChild) return;
        (async () => {
            try {
                const [statsData, reportsData] = await Promise.all([
                    parentApi.getDashboardStats(selectedChild.childId),
                    parentApi.listReports(selectedChild.childId),
                ]);
                setStats(statsData);
                setReports(reportsData);
            } catch {
                // Non-critical
            }
        })();
    }, [selectedChild]);

    if (isLoading) {
        return (
            <div className="h-screen flex items-center justify-center bg-[#f8f9fa]">
                <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
            </div>
        );
    }

    const totalMinutes = stats?.totalLearningTimeMinutes || 0;
    const totalSessions = stats?.totalSessions || 0;
    const dailyBreakdown = stats?.dailyBreakdown || [];
    const maxMin = Math.max(...dailyBreakdown.map(d => d.minutes), 1);

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <div className="bg-white px-5 pt-12 pb-4 border-b border-gray-100">
                <div className="flex items-center justify-between">
                    <h1 className="text-lg font-bold text-gray-900">학부모 대시보드</h1>
                    {selectedChild && (
                        <button
                            onClick={() => navigate(`/parent/children/${selectedChild.childId}`)}
                            className="flex items-center gap-1 text-[13px] text-gray-500 hover:text-gray-700 transition-colors"
                        >
                            <Settings size={14} />
                            프로필 수정
                        </button>
                    )}
                </div>
                <p className="text-sm text-gray-500 mt-1">자녀의 학습 현황을 확인하고 성장을 응원해주세요.</p>

                {/* Child Selector */}
                {children.length > 1 && (
                    <div className="flex gap-2 mt-3 overflow-x-auto pb-1">
                        {children.map((child) => (
                            <button
                                key={child.childId}
                                onClick={() => setSelectedChild(child)}
                                className={`flex-shrink-0 px-3 py-1.5 rounded-full text-xs font-medium transition-colors ${
                                    selectedChild?.childId === child.childId
                                        ? 'bg-[var(--bt-primary)] text-white'
                                        : 'bg-gray-100 text-gray-500'
                                }`}
                            >
                                {child.name}
                            </button>
                        ))}
                    </div>
                )}
            </div>

            <div className="px-5 py-5 space-y-5">
                {/* Stats Grid — 2 columns */}
                <div className="grid grid-cols-2 gap-3">
                    <StatCard
                        icon={<Clock size={18} className="text-[#9ca3af]" />}
                        label="총 학습 시간 (주간)"
                        value={`${totalMinutes}분`}
                        sub={totalMinutes > 0 ? '지난주 대비 활동 중' : '아직 학습 데이터 없음'}
                        positive={totalMinutes > 0}
                    />
                    <StatCard
                        icon={<TrendingUp size={18} className="text-[#9ca3af]" />}
                        label="완료한 세션"
                        value={`${totalSessions}회`}
                        sub={totalSessions > 0 ? `목표 달성률 ${Math.min(Math.round((totalSessions / 10) * 100), 100)}%` : '세션을 시작해보세요'}
                    />
                    <StatCard
                        icon={<BookOpen size={18} className="text-[#9ca3af]" />}
                        label="학습한 단어"
                        value={`${selectedChild?.stats?.vocabularyLearned || 0}개`}
                        sub="이번 주 새로운 단어"
                    />
                    <StatCard
                        icon={<FileText size={18} className="text-[#9ca3af]" />}
                        label="최근 리포트"
                        isLink
                    >
                        {reports.length > 0 ? (
                            <Link
                                to={`/parent/reports/${reports[0].reportId}`}
                                className="text-[#3b82f6] text-sm font-semibold hover:underline flex items-center gap-1"
                            >
                                {formatDate(reports[0].periodEndDate)} 리포트
                                <ChevronRight size={14} />
                            </Link>
                        ) : (
                            <span className="text-sm text-[#9ca3af]">없음</span>
                        )}
                    </StatCard>
                </div>

                {/* Weekly Learning Chart */}
                {dailyBreakdown.length > 0 && (
                    <div className="bg-white rounded-xl p-5 border border-gray-100">
                        <h2 className="text-[15px] font-bold text-gray-900 mb-4">주간 학습 현황</h2>
                        <div className="flex items-end gap-3 h-40 px-4">
                            {dailyBreakdown.map((day, i) => {
                                const heightPct = Math.max((day.minutes / maxMin) * 100, 5);
                                const isToday = new Date(day.date).toDateString() === new Date().toDateString();
                                return (
                                    <div key={day.date} className="flex-1 flex flex-col items-center gap-1.5">
                                        <div className="relative w-full flex flex-col items-center" style={{ height: '160px', justifyContent: 'flex-end' }}>
                                            {day.minutes > 0 && (
                                                <span className="text-[10px] text-[#3b82f6] font-semibold mb-1">
                                                    {day.minutes}분
                                                </span>
                                            )}
                                            <div
                                                className={`w-full rounded-t-md transition-all ${isToday ? 'bg-[#3b82f6]' : 'bg-[#dbeafe]'}`}
                                                style={{ height: `${heightPct}%`, minHeight: day.minutes > 0 ? '8px' : '4px' }}
                                            />
                                        </div>
                                        <span className="text-[11px] text-[#6b7280]">
                                            {day.dayName || DAY_LABELS[i] || ''}
                                        </span>
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                )}

                {/* Reports List */}
                <div className="bg-white rounded-xl p-5 border border-gray-100">
                    <h2 className="text-[15px] font-bold text-gray-900 mb-4">학습 리포트 내역</h2>

                    {reports.length === 0 ? (
                        <div className="text-center py-12">
                            <p className="text-[#9ca3af] text-sm mb-4">생성된 리포트가 없습니다.</p>
                            <p className="text-[13px] text-[#6b7280] mb-6">학습이 쌓이면 매월 AI가 자녀의 성장 리포트를 생성해드려요.</p>
                            <Link
                                to="/parent/reports/demo"
                                className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-[#6366f1] to-[#3b82f6] text-white text-sm font-semibold rounded-xl hover:brightness-110 transition-all shadow-md"
                            >
                                <FileText size={16} />
                                샘플 리포트 미리보기
                            </Link>
                        </div>
                    ) : (
                        <div className="space-y-3">
                            {reports.map((report) => (
                                <div
                                    key={report.reportId}
                                    className="flex items-center justify-between p-4 border border-[#f3f4f6] rounded-[10px] hover:bg-[#f9fafb] transition-colors"
                                >
                                    <div className="flex items-center gap-3.5">
                                        <div className="w-11 h-11 rounded-full bg-[#dbeafe] flex items-center justify-center text-[#3b82f6]">
                                            <FileText size={20} />
                                        </div>
                                        <div>
                                            <p className="text-[15px] font-semibold text-[#1a1a2e]">
                                                {formatDate(report.periodStartDate)} ~ {formatDate(report.periodEndDate)} 리포트
                                            </p>
                                            <p className="text-[13px] text-[#6b7280] mt-0.5 max-w-[400px] truncate">
                                                {report.summaryText || '요약 정보 없음'}
                                            </p>
                                        </div>
                                    </div>
                                    <Link
                                        to={`/parent/reports/${report.reportId}`}
                                        className="px-3.5 py-2 text-[#3b82f6] text-[13px] font-semibold rounded-md hover:bg-[#eff6ff] transition-colors flex items-center gap-1"
                                    >
                                        상세보기 <ChevronRight size={14} />
                                    </Link>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

/* ---------- Sub-components ---------- */

function StatCard({
    icon,
    label,
    value,
    sub,
    positive,
    isLink,
    children,
}: {
    icon: React.ReactNode;
    label: string;
    value?: string;
    sub?: string;
    positive?: boolean;
    isLink?: boolean;
    children?: React.ReactNode;
}) {
    return (
        <div className="bg-white rounded-xl p-4 border border-gray-100">
            <div className="flex justify-between items-center mb-2">
                <span className="text-[12px] text-gray-500 font-medium">{label}</span>
                {icon}
            </div>
            {isLink ? (
                <div className="mt-1">{children}</div>
            ) : (
                <>
                    <div className="text-xl font-extrabold text-gray-900">{value}</div>
                    {sub && (
                        <p className={`text-[11px] mt-1 ${positive ? 'text-green-600' : 'text-gray-400'}`}>
                            {positive && '▲ '}{sub}
                        </p>
                    )}
                </>
            )}
        </div>
    );
}

function formatDate(dateStr: string) {
    const d = new Date(dateStr);
    return `${d.getFullYear()}.${String(d.getMonth() + 1).padStart(2, '0')}.${String(d.getDate()).padStart(2, '0')}`;
}
