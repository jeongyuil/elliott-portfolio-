/**
 * Learning Dashboard - Wireframe #10
 * 바 차트, 세션 요약, 스테이지 현황
 */
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
    Clock, TrendingUp, BookOpen, ChevronRight,
    BarChart3, Target, Award,
} from 'lucide-react';
import { parentApi } from '@/api/client';
import type { ChildProfile, DashboardStats, Report } from '@/api/types';
import { toast } from 'sonner';

export default function LearningDashboard() {
    const [children, setChildren] = useState<ChildProfile[]>([]);
    const [selectedChild, setSelectedChild] = useState<ChildProfile | null>(null);
    const [stats, setStats] = useState<DashboardStats | null>(null);
    const [reports, setReports] = useState<Report[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    // Fetch children
    useEffect(() => {
        (async () => {
            try {
                const data = await parentApi.listChildren();
                setChildren(data);
                if (data.length > 0) setSelectedChild(data[0]);
            } catch {
                toast.error('데이터를 불러오지 못했습니다.');
            } finally {
                setIsLoading(false);
            }
        })();
    }, []);

    // Fetch stats when child changes
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
            <div className="h-screen flex items-center justify-center">
                <div className="w-8 h-8 border-4 border-[var(--bt-primary)] border-t-transparent rounded-full animate-spin" />
            </div>
        );
    }

    const totalMinutes = stats?.totalLearningTimeMinutes || 0;
    const totalSessions = stats?.totalSessions || 0;
    const childStats = selectedChild?.stats;
    const dailyBreakdown = stats?.dailyBreakdown || [];

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <div className="bg-white px-5 pt-12 pb-4 border-b border-gray-100">
                <h1 className="text-lg font-bold text-gray-900">학습 진행도</h1>

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
                {/* Overview Stats */}
                <div className="grid grid-cols-3 gap-3">
                    <MiniStat icon={<Clock size={16} />} value={`${totalMinutes}분`} label="학습 시간" color="blue" />
                    <MiniStat icon={<TrendingUp size={16} />} value={`${totalSessions}회`} label="세션" color="green" />
                    <MiniStat icon={<BookOpen size={16} />} value={`${childStats?.vocabularyLearned || 0}개`} label="단어" color="purple" />
                </div>

                {/* Weekly Bar Chart */}
                <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-sm font-bold text-gray-800 flex items-center gap-2">
                            <BarChart3 size={16} className="text-[var(--bt-primary)]" />
                            주간 학습 시간
                        </h3>
                        <span className="text-xs text-gray-400">최근 7일</span>
                    </div>

                    {dailyBreakdown.length > 0 ? (
                        <div className="flex items-end justify-between gap-2 h-32">
                            {dailyBreakdown.map((day) => {
                                const maxMin = Math.max(...dailyBreakdown.map(d => d.minutes), 1);
                                const heightPct = Math.max((day.minutes / maxMin) * 100, 4);
                                const isToday = new Date(day.date).toDateString() === new Date().toDateString();
                                return (
                                    <div key={day.date} className="flex-1 flex flex-col items-center gap-1">
                                        <span className="text-[9px] text-gray-400 mb-1">
                                            {day.minutes > 0 ? `${day.minutes}분` : ''}
                                        </span>
                                        <div
                                            className={`w-full rounded-t-lg transition-all ${
                                                isToday ? 'bg-[var(--bt-primary)]' : 'bg-[var(--bt-primary)] opacity-50'
                                            }`}
                                            style={{ height: `${heightPct}%` }}
                                        />
                                        <span className={`text-[10px] ${isToday ? 'font-bold text-[var(--bt-primary)]' : 'text-gray-400'}`}>
                                            {day.dayName}
                                        </span>
                                    </div>
                                );
                            })}
                        </div>
                    ) : (
                        <p className="text-sm text-gray-400 text-center py-8">
                            이번 주 학습 데이터가 아직 없어요.
                        </p>
                    )}
                </div>

                {/* Session Summary */}
                <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
                    <div className="flex items-center justify-between mb-3">
                        <h3 className="text-sm font-bold text-gray-800 flex items-center gap-2">
                            <Target size={16} className="text-green-500" />
                            세션 요약
                        </h3>
                    </div>
                    <div className="space-y-3">
                        <SessionSummaryRow label="총 세션 수" value={`${totalSessions}회`} />
                        <SessionSummaryRow label="평균 세션 길이" value={totalSessions > 0 ? `${Math.round(totalMinutes / totalSessions)}분` : '—'} />
                        <SessionSummaryRow label="발음 정확도" value={childStats?.pronunciationAccuracy ? `${childStats.pronunciationAccuracy}%` : '측정 중'} />
                        <SessionSummaryRow label="미션 완료" value={`${childStats?.missionsCompleted || 0}개`} />
                    </div>
                </div>

                {/* Stage Progress */}
                <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
                    <div className="flex items-center justify-between mb-3">
                        <h3 className="text-sm font-bold text-gray-800 flex items-center gap-2">
                            <Award size={16} className="text-amber-500" />
                            레벨 현황
                        </h3>
                    </div>
                    <div className="flex items-center gap-4">
                        <div className="w-16 h-16 rounded-full bg-gradient-to-br from-[var(--bt-primary)] to-indigo-600 flex items-center justify-center text-white">
                            <span className="text-lg font-bold">Lv.{selectedChild?.level || 1}</span>
                        </div>
                        <div className="flex-1">
                            <p className="text-sm font-medium text-gray-700">
                                경험치 {selectedChild?.xp || 0} XP
                            </p>
                            <div className="mt-1.5 bg-gray-200 h-2 rounded-full overflow-hidden">
                                <div
                                    className="bg-[var(--bt-primary)] h-full rounded-full transition-all"
                                    style={{ width: `${Math.min(((selectedChild?.xp || 0) % 100), 100)}%` }}
                                />
                            </div>
                            <p className="text-[10px] text-gray-400 mt-1">
                                다음 레벨까지 {100 - ((selectedChild?.xp || 0) % 100)} XP
                            </p>
                        </div>
                    </div>
                </div>

                {/* Reports List */}
                <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
                    <h3 className="text-sm font-bold text-gray-800 mb-3">학습 리포트</h3>
                    {reports.length === 0 ? (
                        <p className="text-sm text-gray-400 text-center py-6">
                            생성된 리포트가 없습니다.
                        </p>
                    ) : (
                        <div className="space-y-2">
                            {reports.slice(0, 3).map((report) => (
                                <Link
                                    key={report.reportId}
                                    to={`/parent/reports/${report.reportId}`}
                                    className="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 transition-colors"
                                >
                                    <div>
                                        <p className="text-sm font-medium text-gray-700">
                                            {new Date(report.periodStartDate).toLocaleDateString('ko-KR')} ~ {new Date(report.periodEndDate).toLocaleDateString('ko-KR')}
                                        </p>
                                        <p className="text-xs text-gray-400 line-clamp-1 mt-0.5">
                                            {report.summaryText || '요약 정보 없음'}
                                        </p>
                                    </div>
                                    <ChevronRight size={16} className="text-gray-300 flex-shrink-0" />
                                </Link>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

function MiniStat({ icon, value, label, color }: { icon: React.ReactNode; value: string; label: string; color: string }) {
    const bgMap: Record<string, string> = { blue: 'bg-blue-50', green: 'bg-green-50', purple: 'bg-purple-50' };
    const textMap: Record<string, string> = { blue: 'text-blue-500', green: 'text-green-500', purple: 'text-purple-500' };
    return (
        <div className={`${bgMap[color] || 'bg-gray-50'} rounded-xl p-3 text-center`}>
            <div className={`${textMap[color] || 'text-gray-500'} flex justify-center mb-1`}>{icon}</div>
            <p className="text-lg font-bold text-gray-900">{value}</p>
            <p className="text-[10px] text-gray-500">{label}</p>
        </div>
    );
}

function SessionSummaryRow({ label, value }: { label: string; value: string }) {
    return (
        <div className="flex items-center justify-between">
            <span className="text-sm text-gray-500">{label}</span>
            <span className="text-sm font-semibold text-gray-800">{value}</span>
        </div>
    );
}
