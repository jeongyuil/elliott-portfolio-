/**
 * Skill Deep Report — Wireframe 04: 스킬 심층 리포트
 * 스킬 아이덴티티, 점수 오버뷰, AI 인사이트, 세션 추이 차트,
 * 온톨로지 학습맵, 또래 발달 비교, CAN-DO 체크리스트, 발화 예시, 다음 목표
 */
import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { parentApi } from "@/api/client";
import type { Report } from "@/api/types";
import { ChevronLeft } from "lucide-react";
import { toast } from "sonner";

/* ── Mock/Derived data helpers ── */
// In production these would come from the API. For now we derive/mock from report data.

function buildDemoReport(childName: string): Report {
    return {
    reportId: 'demo',
    periodStartDate: '2026-01-01',
    periodEndDate: '2026-01-31',
    summaryText: `${childName}(은)는 이번 달 어휘력과 표현력에서 큰 성장을 보였습니다.`,
    strengthsSummary: '새로운 어휘를 빠르게 흡수하고, 대화에서 자연스럽게 활용하고 있어요.',
    areasToImprove: '발음 정확도가 아직 발전 중이에요.',
    recommendationsNextMonth: '발음 연습 모험을 2주에 3회 이상 진행해보세요',
    skillSummaries: [
        { skillId: 'daily_vocabulary', skillName: '일상 어휘 이해 및 사용', skillNameEn: 'Daily-life Vocabulary', level: 4, trend: 12, summaryForParent: '새로운 단어 12개를 학습했으며, 문맥에 맞게 사용하는 능력이 뛰어납니다.', canDo: '일상 생활 속 사물(음식, 동물, 색깔)을 영어로 말할 수 있어요.', sparkline: [8,10,9,12,14,13,16,15,18,17,20,20] },
        { skillId: 'likes_dislikes', skillName: '좋아하는 것/싫어하는 것 표현', skillNameEn: 'Likes & Dislikes', level: 3, trend: 8, summaryForParent: '"I like..."와 "I don\'t like..." 표현을 사용하기 시작했습니다.', canDo: '"I like pizza", "I don\'t like spiders" 같은 기본 선호 표현이 가능해요.' },
        { skillId: 'pronunciation_clarity', skillName: '기초 영어 발음 명료도', skillNameEn: 'Pronunciation Clarity', level: 2, trend: 5, summaryForParent: '\'th\', \'r\' 발음에서 개선이 필요하지만, 전반적인 명료도는 좋아지고 있어요.' },
        { skillId: 'basic_svo_sentence', skillName: '기초 SVO 문장 구성', skillNameEn: 'Basic SVO Sentences', level: 3, trend: 10, summaryForParent: '2~3개 단어를 연결해 문장을 만들기 시작했습니다.' },
        { skillId: 'wh_question_answer', skillName: '기초 WH-질문 응답', skillNameEn: 'WH-Question Response', level: 3, trend: 6, summaryForParent: '"What is this?", "Where is the cat?" 같은 간단한 WH-질문에 응답할 수 있어요.' },
        { skillId: 'sustained_attention', skillName: '세션 내 지속 주의 집중', skillNameEn: 'Sustained Attention', level: 5, trend: 0, summaryForParent: '높은 집중력으로 세션에 참여하며, 평균 세션 시간이 지난달보다 20% 증가했습니다.', canDo: '5분 이상의 대화 세션을 주도적으로 이끌어갈 수 있어요.' },
        { skillId: 'two_step_instructions', skillName: '두 단계 지시 따르기', skillNameEn: 'Two-step Instructions', level: 3, trend: 1, summaryForParent: '"Open the book and point to the dog" 같은 두 단계 지시를 이해하고 따를 수 있어요.' },
        { skillId: 'topic_switching', skillName: '주제 전환 유연성', skillNameEn: 'Topic Switching', level: 2, trend: 1, summaryForParent: '주제가 바뀔 때 약간의 혼란을 보이지만, 점차 적응하고 있습니다.' },
        { skillId: 'mood_self_report', skillName: '3단계 기분 자기 보고', skillNameEn: 'Mood Self-Report', level: 4, trend: 1, summaryForParent: '"I feel happy/sad/so-so"를 적절한 상황에서 표현할 수 있어요.', canDo: '자신의 기분을 3단계(좋아요/보통/슬퍼요)로 스스로 보고할 수 있어요.' },
        { skillId: 'response_to_praise', skillName: '칭찬/격려에 대한 정서적 반응', skillNameEn: 'Response to Praise', level: 5, trend: 0, summaryForParent: '칭찬에 긍정적으로 반응하고, "Thank you!" 등의 적절한 응답을 합니다.' },
        { skillId: 'preference_expression', skillName: '선호/비선호 정서 표현', skillNameEn: 'Preference Expression', level: 3, trend: 7, summaryForParent: '좋고 싫은 감정을 표현하며, 이유를 간단히 설명하기 시작했어요.' },
    ],
    };
}

interface OntologyNode {
    title: string;
    sub: string;
    progress: number;
    total: number;
    status: 'mastered' | 'in-progress' | 'locked';
}

interface CanDoItem {
    text: string;
    status: 'done' | 'partial' | 'pending';
}

interface UtteranceExample {
    date: string;
    session: string;
    text: string;
    highlights: string[];
    feedback: string;
    scores: string[];
}

interface SessionRecord {
    day: number;
    month: string;
    score: number;
    change: number;
    detail: string;
}

interface NextGoal {
    emoji: string;
    title: string;
    desc: string;
    activity: string;
    locked?: boolean;
}

export default function SkillDeepReport() {
    const { reportId, skillId } = useParams<{ reportId: string; skillId: string }>();
    const navigate = useNavigate();
    const [report, setReport] = useState<Report | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        if (!reportId) return;
        if (reportId === 'demo') {
            (async () => {
                try {
                    const children = await parentApi.listChildren();
                    const name = children.length > 0 ? children[0].name : '우리 아이';
                    setReport(buildDemoReport(name));
                } catch {
                    setReport(buildDemoReport('우리 아이'));
                } finally {
                    setIsLoading(false);
                }
            })();
            return;
        }
        (async () => {
            try {
                const data = await parentApi.getReport(reportId);
                setReport(data);
            } catch {
                toast.error("리포트를 불러오지 못했습니다.");
            } finally {
                setIsLoading(false);
            }
        })();
    }, [reportId]);

    if (isLoading) {
        return (
            <div className="h-screen flex items-center justify-center bg-[#f8f9fa]">
                <div className="w-8 h-8 border-4 border-[#3b82f6] border-t-transparent rounded-full animate-spin" />
            </div>
        );
    }

    if (!report) {
        return <div className="p-8 text-center text-[#6b7280]">리포트를 찾을 수 없습니다.</div>;
    }

    const skill = report.skillSummaries.find(s => s.skillId === skillId) || report.skillSummaries[0];
    if (!skill) {
        return <div className="p-8 text-center text-[#6b7280]">스킬 정보를 찾을 수 없습니다.</div>;
    }

    const level = skill.level || 0;
    const score = level * 20;
    const skillName = skill.skillName || skill.skillId;
    const period = `${new Date(report.periodStartDate).getFullYear()}년 ${new Date(report.periodStartDate).getMonth() + 1}월 리포트`;

    // Derived data
    const ontologyNodes = getOntologyNodes();
    const canDoItems = getCanDoItems();
    const utterances = getUtteranceExamples();
    const sessions = getSessionRecords(score);
    const nextGoals = getNextGoals();

    return (
        <div className="min-h-screen bg-[#f8f9fa]">
            <div className="max-w-[640px] mx-auto px-6 py-8 pb-16">

                {/* Header */}
                <div className="flex items-center gap-3.5 mb-7">
                    <button
                        onClick={() => navigate(`/parent/reports/${reportId}`)}
                        className="w-10 h-10 rounded-lg border border-[#e5e7eb] bg-white flex items-center justify-center text-[#6b7280] hover:bg-gray-50 transition-colors"
                    >
                        <ChevronLeft size={18} />
                    </button>
                    <div>
                        <h1 className="text-[22px] font-extrabold text-[#1a1a2e]">스킬 심층 리포트</h1>
                        <p className="text-[13px] text-[#6b7280] mt-0.5">{period}</p>
                    </div>
                </div>

                {/* Skill Identity Card */}
                <div className="relative overflow-hidden rounded-2xl p-7 mb-6" style={{ background: 'linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%)' }}>
                    <div className="absolute -top-[30px] -right-[30px] w-[120px] h-[120px] rounded-full bg-[rgba(59,130,246,0.08)]" />
                    <div className="text-5xl mb-3">{getSkillEmoji(skill.skillId)}</div>
                    <div className="text-[22px] font-extrabold text-[#1e40af]">{skillName}</div>
                    <div className="text-[13px] text-[#3b82f6] font-medium mt-0.5">{skill.skillId}</div>
                    <div className="flex gap-2 mt-3.5 flex-wrap">
                        <MetaTag className="bg-[#dbeafe] text-[#1d4ed8]">언어 Language</MetaTag>
                        <MetaTag className="bg-[#e0e7ff] text-[#4338ca]">수용+표현 Both</MetaTag>
                        <MetaTag className="bg-[#fef3c7] text-[#92400e]">4~6세</MetaTag>
                        <MetaTag className="bg-[#d1fae5] text-[#065f46]">Score 0-100</MetaTag>
                    </div>
                </div>

                {/* Score Overview */}
                <div className="bg-white rounded-[14px] border border-[#e5e7eb] p-6 mb-5">
                    <div className="grid grid-cols-3 gap-4 text-center">
                        <div>
                            <div className="text-xs text-[#6b7280] font-medium mb-1.5">현재 점수</div>
                            <div className="text-4xl font-extrabold text-[#1e40af]">{score}</div>
                            <div className="text-[13px] text-[#6b7280]">/ 100</div>
                            <div className="flex items-center justify-center gap-1 mt-1">
                                <span className="text-[#16a34a] text-base font-bold">▲ +{Math.max(level * 3, 1)}</span>
                                <span className="text-[11px] text-[#6b7280]">지난달 대비</span>
                            </div>
                        </div>
                        <div>
                            <div className="text-xs text-[#6b7280] font-medium mb-1.5">현재 레벨</div>
                            <div className="mt-1">
                                <span className="inline-flex items-center gap-1 px-4 py-2 rounded-full bg-[#3b82f6] text-white text-base font-bold">
                                    Lv. {level}
                                </span>
                            </div>
                            <div className="text-sm text-[#fbbf24] mt-2 tracking-widest">
                                {'★'.repeat(level)}{'☆'.repeat(Math.max(5 - level, 0))}
                            </div>
                        </div>
                        <div>
                            <div className="text-xs text-[#6b7280] font-medium mb-1.5">또래 백분위</div>
                            <div className="text-[28px] font-extrabold text-[#059669]">상위 {Math.max(100 - score, 5)}%</div>
                            <div className="text-xs text-[#6b7280] mt-1">같은 나이 대비</div>
                        </div>
                    </div>
                </div>

                {/* AI Insight */}
                <div className="rounded-[14px] p-5 mb-5 border border-[#c4b5fd]" style={{ background: 'linear-gradient(135deg, #faf5ff, #ede9fe)' }}>
                    <div className="flex items-center gap-2 mb-3">
                        <span className="bg-[#7c3aed] text-white text-[10px] px-2 py-0.5 rounded-lg font-bold">AI 분석</span>
                        <span className="text-sm font-bold text-[#5b21b6]">밤토리 교육 전문가 분석</span>
                    </div>
                    <p className="text-[13px] text-[#4c1d95] leading-[1.7]">
                        {skill.summaryForParent || '이 스킬에 대한 AI 분석이 아직 생성되지 않았습니다. 학습 데이터가 쌓이면 맞춤형 분석을 제공해드릴게요.'}
                    </p>
                </div>

                {/* Session Trend Chart */}
                <div className="bg-white rounded-[14px] border border-[#e5e7eb] p-6 mb-5">
                    <h3 className="text-base font-bold flex items-center gap-2 mb-4">
                        <span>📈</span> 세션별 점수 추이
                    </h3>
                    <div className="flex gap-1.5 mb-4">
                        {['1주', '1개월', '3개월', '전체'].map((tab, i) => (
                            <button
                                key={tab}
                                className={`px-3.5 py-1.5 rounded-2xl border text-xs transition-colors ${
                                    i === 1
                                        ? 'bg-[#1e40af] text-white border-[#1e40af]'
                                        : 'bg-white text-[#6b7280] border-[#e5e7eb] hover:bg-gray-50'
                                }`}
                            >
                                {tab}
                            </button>
                        ))}
                    </div>
                    <TrendChart score={score} />
                </div>

                {/* Ontology Learning Map */}
                <div className="bg-white rounded-[14px] border border-[#e5e7eb] p-6 mb-5">
                    <h3 className="text-base font-bold flex items-center gap-2 mb-2">
                        <span>🗺️</span> 온톨로지 학습 맵
                    </h3>
                    <p className="text-[13px] text-[#6b7280] mb-4 leading-relaxed">
                        밤토리 교육 온톨로지에 기반한 하위 역량별 학습 현황입니다.
                    </p>
                    <div className="space-y-0">
                        {ontologyNodes.map((node, i) => (
                            <OntologyNodeCard key={i} node={node} isLast={i === ontologyNodes.length - 1} />
                        ))}
                    </div>
                </div>

                {/* Peer Developmental Milestone */}
                <div className="bg-white rounded-[14px] border border-[#e5e7eb] p-6 mb-5">
                    <h3 className="text-base font-bold flex items-center gap-2 mb-2">
                        <span>👫</span> 또래 발달 기준 비교
                    </h3>
                    <p className="text-[13px] text-[#6b7280] mb-5 leading-relaxed">
                        같은 연령대 아동의 평균 발달 이정표 대비 현재 위치입니다.
                    </p>
                    <MilestoneTrack progress={score} />
                    <div className="mt-6 space-y-3.5">
                        <PeerBarRow label="우리 아이" value={score} barClass="bg-[#3b82f6]" />
                        <PeerBarRow label="또래 평균" value={Math.round(score * 0.7)} barClass="bg-[#cbd5e1]" />
                        <PeerBarRow label="상위 10%" value={Math.min(score + 20, 100)} barClass="bg-[#fbbf24]" />
                    </div>
                    <div className="flex gap-4 mt-3 text-[11px] text-[#6b7280]">
                        <span><span className="inline-block w-2 h-2 rounded-sm bg-[#3b82f6] mr-1" />우리 아이</span>
                        <span><span className="inline-block w-2 h-2 rounded-sm bg-[#cbd5e1] mr-1" />또래 평균</span>
                        <span><span className="inline-block w-2 h-2 rounded-sm bg-[#fbbf24] mr-1" />상위 10%</span>
                    </div>
                </div>

                {/* CAN-DO Checklist */}
                <div className="bg-white rounded-[14px] border border-[#e5e7eb] p-6 mb-5">
                    <h3 className="text-base font-bold flex items-center gap-2 mb-2">
                        <span>✅</span> CAN-DO 체크리스트
                    </h3>
                    <p className="text-[13px] text-[#6b7280] mb-4">밤토리 교육 온톨로지 기준 달성 항목입니다.</p>
                    <div className="divide-y divide-[#f3f4f6]">
                        {canDoItems.map((item, i) => (
                            <div key={i} className="flex items-start gap-2.5 py-2.5">
                                <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center text-[11px] flex-shrink-0 mt-0.5 ${
                                    item.status === 'done' ? 'bg-[#3b82f6] border-[#3b82f6] text-white' :
                                    item.status === 'partial' ? 'bg-[#fbbf24] border-[#fbbf24] text-white' :
                                    'border-[#d1d5db] text-transparent'
                                }`}>
                                    {item.status === 'done' ? '✓' : item.status === 'partial' ? '~' : ''}
                                </div>
                                <span className={`text-[13px] leading-relaxed ${item.status === 'pending' ? 'text-[#9ca3af]' : 'text-[#374151]'}`}>
                                    {item.text}
                                </span>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Utterance Examples */}
                <div className="bg-white rounded-[14px] border border-[#e5e7eb] p-6 mb-5">
                    <h3 className="text-base font-bold flex items-center gap-2 mb-2">
                        <span>🎙️</span> 실제 발화 예시
                    </h3>
                    <p className="text-[13px] text-[#6b7280] mb-4">최근 세션에서 이 스킬과 관련하여 말한 문장들입니다.</p>
                    <div className="space-y-2.5">
                        {utterances.map((u, i) => (
                            <div key={i} className="p-4 border border-[#f3f4f6] rounded-[10px]">
                                <div className="text-[11px] text-[#9ca3af] mb-1.5">{u.date} · {u.session}</div>
                                <div className="text-sm font-semibold text-[#1e40af] mb-1">
                                    {u.text}
                                </div>
                                <div className="text-xs text-[#6b7280] leading-relaxed">{u.feedback}</div>
                                <div className="flex gap-2.5 mt-2">
                                    {u.scores.map((s, j) => (
                                        <span key={j} className="text-[11px] px-2 py-0.5 rounded-lg bg-[#eff6ff] text-[#1d4ed8] font-medium">
                                            {s}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Session-by-Session Timeline */}
                <div className="bg-white rounded-[14px] border border-[#e5e7eb] p-6 mb-5">
                    <h3 className="text-base font-bold flex items-center gap-2 mb-4">
                        <span>📅</span> 세션별 기록
                    </h3>
                    <div className="space-y-4">
                        {sessions.map((s, i) => (
                            <div key={i} className="flex gap-3">
                                <div className="w-12 text-center flex-shrink-0">
                                    <div className="text-xl font-extrabold text-[#1e40af]">{s.day}</div>
                                    <div className="text-[10px] text-[#6b7280]">{s.month}</div>
                                </div>
                                <div className="flex-1 bg-[#f9fafb] border border-[#e5e7eb] rounded-[10px] p-3">
                                    <div className="flex justify-between items-center">
                                        <span className="text-[22px] font-extrabold text-[#3b82f6]">{s.score}</span>
                                        <span className={`text-xs font-semibold ${s.change >= 0 ? 'text-[#16a34a]' : 'text-[#ef4444]'}`}>
                                            {s.change >= 0 ? '▲' : '▼'} {s.change >= 0 ? '+' : ''}{s.change}
                                        </span>
                                    </div>
                                    <div className="text-xs text-[#6b7280] mt-1">{s.detail}</div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Next Learning Goals */}
                <div className="bg-white rounded-[14px] border border-[#e5e7eb] p-6 mb-5">
                    <h3 className="text-base font-bold flex items-center gap-2 mb-2">
                        <span>🎯</span> 다음 학습 목표
                    </h3>
                    <p className="text-[13px] text-[#6b7280] mb-4">온톨로지 기반 다음 단계 스킬과 추천 활동입니다.</p>
                    <div className="space-y-2.5">
                        {nextGoals.map((g, i) => (
                            <div key={i} className="flex gap-3.5 p-4 bg-[#f0fdf4] border border-[#bbf7d0] rounded-xl">
                                <div className="text-[28px] flex-shrink-0">{g.emoji}</div>
                                <div className="flex-1">
                                    <div className="text-sm font-semibold text-[#166534]">{g.title}</div>
                                    <div className="text-xs text-[#6b7280] mt-1 leading-relaxed">{g.desc}</div>
                                    <div className="inline-flex items-center gap-1 mt-2 px-2.5 py-1 bg-[#dcfce7] rounded-lg text-[11px] text-[#166534] font-medium">
                                        {g.locked ? '🔒' : '🎮'} {g.activity}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Footer CTA */}
                <div className="bg-white rounded-[14px] border border-[#e5e7eb] p-6 text-center">
                    <p className="text-sm text-[#6b7280] mb-3.5">학습을 응원해주세요! 💙</p>
                    <div className="flex justify-center gap-2">
                        <button
                            onClick={() => navigate('/kid/adventures')}
                            className="px-7 py-3 rounded-[10px] bg-[#3b82f6] text-white text-sm font-bold hover:bg-[#2563eb] transition-colors"
                        >
                            모험 시작하기
                        </button>
                        <button
                            onClick={() => navigate(`/parent/reports/${reportId}`)}
                            className="px-7 py-3 rounded-[10px] border border-[#d1d5db] bg-white text-sm hover:bg-gray-50 transition-colors"
                        >
                            전체 리포트로 돌아가기
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

/* ============================================================
   Sub-components
   ============================================================ */

function MetaTag({ className, children }: { className: string; children: React.ReactNode }) {
    return (
        <span className={`px-2.5 py-1 rounded-xl text-[11px] font-semibold ${className}`}>
            {children}
        </span>
    );
}

function TrendChart({ score }: { score: number }) {
    // Generate 9 data points trending upward toward score
    const pts = Array.from({ length: 9 }, (_, i) => {
        const base = Math.max(score - 30 + i * 4, 10);
        return Math.min(base + Math.round(Math.random() * 6 - 3), 100);
    });
    pts[pts.length - 1] = score;

    const w = 500, h = 200;
    const peerAvg = Math.round(score * 0.7);

    const xStep = w / (pts.length - 1);
    const yScale = (v: number) => h - (v / 100) * h;

    const linePts = pts.map((v, i) => `${i * xStep},${yScale(v)}`).join(' ');
    const areaPath = `M0,${yScale(pts[0])} ${pts.map((v, i) => `L${i * xStep},${yScale(v)}`).join(' ')} L${w},${h} L0,${h} Z`;

    return (
        <div className="relative">
            <div className="flex justify-between text-[10px] text-[#9ca3af] mb-1 ml-8">
                <span>100</span><span>50</span><span>0</span>
            </div>
            <svg viewBox={`0 0 ${w} ${h}`} className="w-full h-[200px]">
                <defs>
                    <linearGradient id="trendGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor="#3b82f6" stopOpacity="0.3" />
                        <stop offset="100%" stopColor="#3b82f6" stopOpacity="0" />
                    </linearGradient>
                </defs>
                {/* Grid lines */}
                {[40, 80, 120, 160].map(y => (
                    <line key={y} x1="0" y1={y} x2={w} y2={y} stroke="#f3f4f6" strokeWidth="1" />
                ))}
                {/* Area */}
                <path d={areaPath} fill="url(#trendGrad)" />
                {/* Line */}
                <polyline points={linePts} fill="none" stroke="#3b82f6" strokeWidth="2.5" />
                {/* Dots */}
                {pts.map((v, i) => (
                    <circle
                        key={i}
                        cx={i * xStep} cy={yScale(v)} r={i === pts.length - 1 ? 6 : 4}
                        fill={i === pts.length - 1 ? '#1d4ed8' : '#3b82f6'}
                        stroke={i === pts.length - 1 ? '#fff' : 'none'}
                        strokeWidth={i === pts.length - 1 ? 2 : 0}
                    />
                ))}
                {/* Current score label */}
                <text x={w} y={yScale(score) - 12} textAnchor="end" fontSize="11" fontWeight="600" fill="#1d4ed8">
                    {score}점
                </text>
                {/* Peer avg line */}
                <line x1="0" y1={yScale(peerAvg)} x2={w} y2={yScale(peerAvg)} stroke="#ef4444" strokeWidth="1" strokeDasharray="4,4" opacity="0.5" />
                <text x={w} y={yScale(peerAvg) - 5} textAnchor="end" fontSize="10" fill="#ef4444" opacity="0.7">
                    또래 평균 {peerAvg}
                </text>
            </svg>
        </div>
    );
}

function OntologyNodeCard({ node, isLast }: { node: OntologyNode; isLast: boolean }) {
    const dotClass = node.status === 'mastered'
        ? 'bg-[#3b82f6] border-[#3b82f6]'
        : node.status === 'in-progress'
        ? 'bg-[#fbbf24] border-[#fbbf24]'
        : 'bg-[#e5e7eb] border-[#d1d5db]';

    const cardClass = node.status === 'mastered'
        ? 'border-[#93c5fd] bg-[#eff6ff]'
        : node.status === 'in-progress'
        ? 'border-[#fde68a] bg-[#fffbeb]'
        : 'border-[#e5e7eb] bg-[#f9fafb] opacity-60';

    const barClass = node.status === 'in-progress' ? 'bg-[#fbbf24]' : 'bg-[#3b82f6]';

    const badgeClass = node.status === 'mastered'
        ? 'bg-[#dbeafe] text-[#1d4ed8]'
        : node.status === 'in-progress'
        ? 'bg-[#fef3c7] text-[#92400e]'
        : 'bg-[#f3f4f6] text-[#9ca3af]';

    const badgeText = node.status === 'mastered' ? '✓ 완료' : node.status === 'in-progress' ? '▶ 학습 중' : '🔒 다음 단계';

    return (
        <div className="flex items-stretch">
            {/* Connector */}
            <div className="w-6 flex flex-col items-center relative">
                <div className={`w-3 h-3 rounded-full border-2 z-10 mt-3.5 ${dotClass}`} />
                {!isLast && <div className="flex-1 w-0.5 bg-[#e5e7eb] mt-0.5" />}
            </div>
            {/* Card */}
            <div className={`flex-1 border rounded-[10px] p-3.5 ml-2.5 mb-3 ${cardClass}`}>
                <div className="text-sm font-semibold">{node.title}</div>
                <div className="text-xs text-[#6b7280] mt-0.5">{node.sub}</div>
                <div className="h-1.5 bg-[#e5e7eb] rounded-full mt-2 overflow-hidden">
                    <div className={`h-full rounded-full ${barClass}`} style={{ width: `${(node.progress / node.total) * 100}%` }} />
                </div>
                <div className="flex justify-between items-center mt-1.5">
                    <span className={`text-[11px] font-semibold ${node.status === 'in-progress' ? 'text-[#d97706]' : node.status === 'mastered' ? 'text-[#3b82f6]' : 'text-[#9ca3af]'}`}>
                        {node.progress}/{node.total} 단어{node.status === 'mastered' ? ' 습득' : ''}
                    </span>
                    <span className={`text-[10px] px-2 py-0.5 rounded-lg font-semibold ${badgeClass}`}>{badgeText}</span>
                </div>
            </div>
        </div>
    );
}

function MilestoneTrack({ progress }: { progress: number }) {
    const milestones = [
        { age: '4세', desc: '기본 명사 10개' },
        { age: '4.5세', desc: '색깔/숫자 표현' },
        { age: '5세', desc: '감정/관계 어휘' },
        { age: '5.5세', desc: '장소/활동 어휘' },
        { age: '6세', desc: '추상 개념 어휘' },
    ];
    const currentIdx = Math.min(Math.floor(progress / 25), 4);

    return (
        <div className="px-2.5 pt-8 pb-2">
            <div className="relative">
                <div className="h-1 bg-[#e5e7eb] rounded-full">
                    <div className="h-full bg-gradient-to-r from-[#3b82f6] to-[#60a5fa] rounded-full" style={{ width: `${progress}%` }} />
                </div>
                <div className="flex justify-between -mt-2">
                    {milestones.map((m, i) => (
                        <div key={i} className="text-center relative">
                            {i === currentIdx && (
                                <div className="absolute -top-7 left-1/2 -translate-x-1/2 bg-[#1e40af] text-white text-[10px] px-2 py-0.5 rounded-lg font-semibold whitespace-nowrap">
                                    현재 ✦
                                </div>
                            )}
                            <div className={`w-4 h-4 rounded-full border-2 mx-auto ${
                                i < currentIdx ? 'bg-[#3b82f6] border-[#3b82f6]' :
                                i === currentIdx ? 'bg-white border-[#3b82f6] shadow-[0_0_0_3px_rgba(59,130,246,0.2)]' :
                                'bg-white border-[#e5e7eb]'
                            }`} />
                            <div className="text-[10px] text-[#6b7280] mt-1.5">{m.age}</div>
                            <div className="text-[10px] text-[#374151] font-medium mt-0.5 max-w-[70px]">{m.desc}</div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

function PeerBarRow({ label, value, barClass }: { label: string; value: number; barClass: string }) {
    return (
        <div className="flex items-center gap-3">
            <span className="w-[60px] text-xs text-[#6b7280] text-right">{label}</span>
            <div className="flex-1 h-6 bg-[#f3f4f6] rounded-md overflow-hidden relative">
                <div className={`h-full rounded-md flex items-center pl-2 text-[11px] font-semibold text-white ${barClass}`} style={{ width: `${value}%` }}>
                    {value}점
                </div>
            </div>
        </div>
    );
}

/* ── Helpers / Mock Data ── */

function getSkillEmoji(skillId: string): string {
    const id = (skillId || '').toLowerCase();
    if (id.includes('vocab')) return '📖';
    if (id.includes('like')) return '❤️';
    if (id.includes('pronun')) return '🗣️';
    if (id.includes('sentence')) return '✍️';
    if (id.includes('question')) return '❓';
    if (id.includes('attention')) return '🎯';
    if (id.includes('mood')) return '😊';
    return '📖';
}

function getOntologyNodes(): OntologyNode[] {
    return [
        { title: '🐾 동물 어휘 (Animals)', sub: 'dog, cat, bird, fish, rabbit, bear, elephant, tiger', progress: 8, total: 8, status: 'mastered' },
        { title: '🎨 색깔 어휘 (Colors)', sub: 'red, blue, yellow, green, pink, orange, purple, black, white', progress: 9, total: 9, status: 'mastered' },
        { title: '🍎 음식 어휘 (Food)', sub: 'apple, banana, milk, water, bread, rice, pizza, ice cream', progress: 7, total: 8, status: 'mastered' },
        { title: '😊 감정 어휘 (Emotions)', sub: 'happy, sad, angry, scared, tired, excited, surprised', progress: 3, total: 7, status: 'in-progress' },
        { title: '👨‍👩‍👧 가족/사람 어휘 (Family & People)', sub: 'mom, dad, sister, brother, baby, friend, teacher', progress: 4, total: 7, status: 'in-progress' },
        { title: '🏠 장소/집 어휘 (Home & Places)', sub: 'house, room, kitchen, school, park, playground', progress: 0, total: 6, status: 'locked' },
        { title: '⛅ 날씨/자연 어휘 (Weather & Nature)', sub: 'sunny, rainy, cloudy, snow, wind, hot, cold', progress: 0, total: 7, status: 'locked' },
    ];
}

function getCanDoItems(): CanDoItem[] {
    return [
        { text: '10개 이상의 일상 영어 단어를 듣고 의미를 이해할 수 있다.', status: 'done' },
        { text: '그림/사진을 보고 해당 영어 단어를 말할 수 있다.', status: 'done' },
        { text: '좋아하는 동물, 음식, 색깔을 영어로 표현할 수 있다.', status: 'done' },
        { text: '기본적인 감정 상태를 영어 단어로 말할 수 있다. (happy, sad)', status: 'partial' },
        { text: '일상 사물(가구, 의류)을 영어로 이름 지을 수 있다.', status: 'pending' },
        { text: '새로운 단어를 들으면 반복하여 따라 말할 수 있다. (7개 이상)', status: 'pending' },
    ];
}

function getUtteranceExamples(): UtteranceExample[] {
    return [
        {
            date: '2026.01.29', session: '세션 #42',
            text: '"I like dog and cat!"',
            highlights: ['dog', 'cat'],
            feedback: '✅ "dog"와 "cat" 어휘를 자연스럽게 활용. 선호 표현 구조("I like")와 함께 사용하여 복합 능력 발휘.',
            scores: ['어휘 정확도 95%', '발음 87%'],
        },
        {
            date: '2026.01.27', session: '세션 #40',
            text: '"The banana is yellow"',
            highlights: ['banana', 'yellow'],
            feedback: '✅ 음식+색깔 어휘를 조합하여 문장 구성. 두 가지 어휘 범주를 연결하는 능력 확인.',
            scores: ['어휘 정확도 100%', '문장구조 82%'],
        },
        {
            date: '2026.01.25', session: '세션 #38',
            text: '"I am... happy? happy!"',
            highlights: ['happy'],
            feedback: '🌱 감정 어휘 "happy"를 처음 시도. 약간의 망설임이 있었으나 정확하게 사용.',
            scores: ['어휘 정확도 90%', '자신감 65%'],
        },
    ];
}

function getSessionRecords(currentScore: number): SessionRecord[] {
    return [
        { day: 31, month: '1월', score: currentScore, change: 3, detail: '세션 #42 · 8분 · 새 단어: rabbit' },
        { day: 29, month: '1월', score: currentScore - 3, change: 2, detail: '세션 #40 · 11분 · 복습: dog, cat, banana' },
        { day: 27, month: '1월', score: currentScore - 5, change: 5, detail: '세션 #38 · 9분 · 새 단어: happy' },
        { day: 23, month: '1월', score: currentScore - 10, change: -1, detail: '세션 #36 · 5분 · 복습 위주 (짧은 세션)' },
    ];
}

function getNextGoals(): NextGoal[] {
    return [
        {
            emoji: '😊', title: '감정 어휘 확장',
            desc: '현재 happy, sad, angry 3개를 습득했어요. scared, tired, excited, surprised까지 확장하면 감정 어휘 영역을 완료할 수 있어요.',
            activity: '추천 활동: 감정 표현 모험 (루나와 감정 카드 놀이)',
        },
        {
            emoji: '👨‍👩‍👧', title: '가족/사람 어휘 완성',
            desc: 'mom, dad, sister, friend 4개 습득 완료. brother, baby, teacher를 추가로 학습하면 이 영역도 마스터할 수 있어요.',
            activity: '추천 활동: 우리 가족 소개하기 (루나에게 가족 이야기)',
        },
        {
            emoji: '🏠', title: '장소/집 어휘 시작 (다음 단계)',
            desc: '감정+가족 어휘를 마스터하면 자연스럽게 장소/집 관련 어휘로 넘어갈 준비가 됩니다.',
            activity: '감정 어휘 80% 이상 달성 후 잠금 해제', locked: true,
        },
    ];
}
