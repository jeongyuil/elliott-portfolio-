import { useEffect, useState } from "react";
import { parentApi } from "@/api/client";
import type { ChildProfile, DashboardStats, Report } from "@/api/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { BarChart, Clock, BookOpen, FileText, ChevronRight, Settings } from "lucide-react";
import { Link } from "react-router-dom";
import { toast } from "sonner";

export default function ParentDashboard() {
    const [children, setChildren] = useState<ChildProfile[]>([]);
    const [selectedChildId, setSelectedChildId] = useState<string | null>(null);
    const [stats, setStats] = useState<DashboardStats | null>(null);
    const [reports, setReports] = useState<Report[]>([]);
    // const [isLoading, setIsLoading] = useState(false); // Unused for now

    // Fetch Children
    useEffect(() => {
        const fetchChildren = async () => {
            try {
                const data = await parentApi.listChildren();
                setChildren(data);
                if (data.length > 0) {
                    setSelectedChildId(data[0].childId);
                }
            } catch (error) {
                console.error("Failed to fetch children", error);
                toast.error("아이 목록을 불러오지 못했습니다.");
            }
        };
        fetchChildren();
    }, []);

    // Fetch Stats & Reports
    useEffect(() => {
        if (!selectedChildId) return;

        const fetchData = async () => {
            // setIsLoading(true);
            try {
                const [statsData, reportsData] = await Promise.all([
                    parentApi.getDashboardStats(selectedChildId),
                    parentApi.listReports(selectedChildId)
                ]);
                setStats(statsData);
                setReports(reportsData);
            } catch (error) {
                console.error("Failed to fetch dashboard data", error);
                toast.error("대시보드 데이터를 불러오지 못했습니다.");
            } finally {
                // setIsLoading(false);
            }
        };
        fetchData();
    }, [selectedChildId]);

    if (!selectedChildId) {
        return <div className="p-8">아이 프로필을 불러오는 중...</div>;
    }

    return (
        <div className="p-6 max-w-6xl mx-auto space-y-8">
            {/* Header */}
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">학부모 대시보드</h1>
                    <p className="text-muted-foreground mt-1">자녀의 학습 현황을 확인하고 성장을 응원해주세요.</p>
                </div>
                <div className="flex items-center gap-2">
                    <Link to={`/parent/children/${selectedChildId}`}>
                        <Button variant="outline" size="sm">
                            <Settings className="h-4 w-4 mr-2" />
                            프로필 수정
                        </Button>
                    </Link>
                    <Select value={selectedChildId} onValueChange={setSelectedChildId}>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder="아이 선택" />
                        </SelectTrigger>
                        <SelectContent>
                            {children.map((child) => (
                                <SelectItem key={child.childId} value={child.childId}>
                                    {child.name}
                                </SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                </div>
            </div>

            {/* Stats Grid */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">총 학습 시간 (주간)</CardTitle>
                        <Clock className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{stats?.totalLearningTimeMinutes || 0}분</div>
                        <p className="text-xs text-muted-foreground">지난주 대비 +15%</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">완료한 세션</CardTitle>
                        <BarChart className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{stats?.totalSessions || 0}회</div>
                        <p className="text-xs text-muted-foreground">목표 달성률 80%</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">학습한 단어</CardTitle>
                        <BookOpen className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">12개</div>
                        <p className="text-xs text-muted-foreground">이번 주 새로운 단어</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">최근 리포트</CardTitle>
                        <FileText className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        {reports.length > 0 ? (
                            <Link to={`/parent/reports/${reports[0].reportId}`} className="text-sm text-primary hover:underline flex items-center">
                                {new Date(reports[0].createdAt || reports[0].periodEndDate || new Date()).toLocaleDateString()} 리포트 <ChevronRight className="h-3 w-3 ml-1" />
                            </Link>
                        ) : (
                            <div className="text-sm text-muted-foreground">없음</div>
                        )}
                    </CardContent>
                </Card>
            </div>

            {/* Reports List */}
            <Card className="col-span-4">
                <CardHeader>
                    <CardTitle>학습 리포트 내역</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="space-y-4">
                        {reports.length === 0 ? (
                            <div className="text-center py-8 text-muted-foreground">
                                생성된 리포트가 없습니다. 월말에 AI 리포트가 생성됩니다.
                            </div>
                        ) : (
                            reports.map(report => (
                                <div key={report.reportId} className="flex items-center justify-between p-4 border rounded-lg hover:bg-muted/50 transition-colors">
                                    <div className="flex items-center gap-4">
                                        <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600">
                                            <FileText className="h-5 w-5" />
                                        </div>
                                        <div>
                                            <h4 className="font-semibold">
                                                {new Date(report.periodStartDate).toLocaleDateString()} ~ {new Date(report.periodEndDate).toLocaleDateString()} 리포트
                                            </h4>
                                            <p className="text-sm text-muted-foreground line-clamp-1">{report.summaryText || "요약 정보 없음"}</p>
                                        </div>
                                    </div>
                                    <Button variant="ghost" size="sm" asChild>
                                        <Link to={`/parent/reports/${report.reportId}`}>
                                            상세보기 <ChevronRight className="ml-2 h-4 w-4" />
                                        </Link>
                                    </Button>
                                </div>
                            ))
                        )}
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
