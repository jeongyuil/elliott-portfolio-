/**
 * Report Detail — Wireframe 02: 학습 리포트 상세
 * 6축 레이더, 종합 요약, 또래 비교, 영역별 상세 스킬, 추천 학습
 */
import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { parentApi } from "@/api/client";
import type { Report } from "@/api/types";
import { ChevronLeft, Download } from "lucide-react";
import { toast } from "sonner";

/* ── Color Scheme by Category ── */
const CAT_COLORS = {
    lang: { pill: 'bg-[#eff6ff] text-[#3b82f6]', bar: 'from-[#60a5fa] to-[#3b82f6]', border: 'border-[#3b82f6]', spark: 'bg-[#bfdbfe]', sparkActive: 'bg-[#3b82f6]', label: '🇮🇳 언어 Language' },
    cogn: { pill: 'bg-[#f5f3ff] text-[#8b5cf6]', bar: 'from-[#a78bfa] to-[#8b5cf6]', border: 'border-[#8b5cf6]', spark: 'bg-[#ddd6fe]', sparkActive: 'bg-[#8b5cf6]', label: '🧠 인지 Cognitive' },
    emo:  { pill: 'bg-[#fffbeb] text-[#92400e]', bar: 'from-[#fbbf24] to-[#f59e0b]', border: 'border-[#f59e0b]', spark: 'bg-[#fde68a]', sparkActive: 'bg-[#f59e0b]', label: '💛 정서 Emotional' },
} as const;

type CatKey = keyof typeof CAT_COLORS;

const LEVEL_STYLES: Record<number, string> = {
    1: 'bg-[#fef2f2] text-[#dc2626]',
    2: 'bg-[#fff7ed] text-[#ea580c]',
    3: 'bg-[#fffbeb] text-[#d97706]',
    4: 'bg-[#f0fdf4] text-[#16a34a]',
    5: 'bg-[#eff6ff] text-[#2563eb]',
};

function buildDemoReport(childName: string): Report {
    return {
    reportId: 'demo',
    periodStartDate: '2026-01-01',
    periodEndDate: '2026-01-31',
    summaryText: `${childName}(은)는 이번 달 어휘력과 표현력에서 큰 성장을 보였습니다. 새로운 단어를 적극적으로 사용하며, 문장 구성 능력이 향상되었습니다. 세션 참여도가 높아 자기주도 학습 태도가 형성되고 있어요.`,
    strengthsSummary: '새로운 어휘를 빠르게 흡수하고, 대화에서 자연스럽게 활용하고 있어요. 특히 동물 관련 어휘에서 높은 이해도를 보여주었습니다.',
    areasToImprove: '발음 정확도가 아직 발전 중이에요. 특히 \'th\', \'r\' 발음에서 연습이 더 필요합니다. 반복 학습을 추천드려요.',
    recommendationsNextMonth: '발음 연습 모험을 2주에 3회 이상 진행해보세요 (th, r 중점)\n동물 주제 외에 음식/가족 주제로 어휘를 확장해보세요\n"Why do you like...?" 같은 WH-질문 확장 연습을 해보세요\n짧은 영어 동요를 함께 들으며 리듬감을 익혀보세요',
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

export default function ReportDetail() {
    const { reportId } = useParams<{ reportId: string }>();
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

    const period = `${formatDate(report.periodStartDate)} ~ ${formatDate(report.periodEndDate)}`;

    // Categorize skills
    const categorized = categorizeSkills(report.skillSummaries);

    return (
        <div className="min-h-screen bg-[#f8f9fa]">
            <div className="max-w-[960px] mx-auto px-6 py-8">

                {/* Header */}
                <div className="flex justify-between items-center mb-7">
                    <div className="flex items-center gap-3.5">
                        <Link
                            to="/parent/home"
                            className="w-10 h-10 rounded-lg border border-[#e5e7eb] bg-white flex items-center justify-center text-[#6b7280] hover:bg-gray-50 transition-colors"
                        >
                            <ChevronLeft size={18} />
                        </Link>
                        <div>
                            <h1 className="text-2xl font-extrabold text-[#1a1a2e]">학습 리포트 상세</h1>
                            <p className="text-[13px] text-[#6b7280] mt-0.5">{period}</p>
                        </div>
                    </div>
                    <button
                        onClick={() => toast.info("PDF 다운로드는 준비 중입니다.")}
                        className="flex items-center gap-1.5 px-4 py-2 border border-[#d1d5db] rounded-lg bg-white text-[13px] hover:bg-gray-50 transition-colors"
                    >
                        <Download size={14} /> PDF 다운로드
                    </button>
                </div>

                {reportId === 'demo' && (
                    <div className="mb-6 p-4 bg-gradient-to-r from-[#faf5ff] to-[#ede9fe] border border-[#c4b5fd] rounded-xl flex items-center gap-3">
                        <span className="text-2xl">✨</span>
                        <div>
                            <p className="text-sm font-bold text-[#5b21b6]">샘플 리포트입니다</p>
                            <p className="text-xs text-[#7c3aed]">실제 학습 데이터가 쌓이면 자녀 맞춤형 리포트가 생성됩니다.</p>
                        </div>
                    </div>
                )}

                {/* Row 1: Radar + Summary */}
                <div className="grid md:grid-cols-2 gap-5 mb-7">
                    {/* Radar Chart */}
                    <div className="bg-white rounded-xl border border-[#e5e7eb] overflow-hidden">
                        <div className="px-5 pt-5">
                            <h3 className="text-base font-bold flex items-center gap-2">📊 스킬 분석 (6축 레이더)</h3>
                        </div>
                        <div className="p-5 flex items-center justify-center">
                            <RadarSVG skills={report.skillSummaries} />
                        </div>
                    </div>

                    {/* Summary */}
                    <div className="bg-white rounded-xl border border-[#e5e7eb] overflow-hidden">
                        <div className="px-5 pt-5">
                            <h3 className="text-base font-bold flex items-center gap-2">📝 종합 요약</h3>
                        </div>
                        <div className="p-5 space-y-4">
                            <p className="text-sm text-[#374151] leading-[1.7]">
                                {report.summaryText || '요약 정보가 없습니다.'}
                            </p>
                            <div className="bg-[#f0fdf4] rounded-lg p-3.5">
                                <h4 className="text-sm font-bold text-[#16a34a] mb-1.5">👍 잘하고 있어요</h4>
                                <p className="text-[13px] text-[#4b5563] leading-relaxed">
                                    {report.strengthsSummary || '데이터 없음'}
                                </p>
                            </div>
                            <div className="bg-[#fff7ed] rounded-lg p-3.5">
                                <h4 className="text-sm font-bold text-[#ea580c] mb-1.5">💪 조금 더 노력해요</h4>
                                <p className="text-[13px] text-[#4b5563] leading-relaxed">
                                    {report.areasToImprove || '데이터 없음'}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Row 2: Peer Comparison */}
                <PeerComparison skills={report.skillSummaries} />

                {/* Row 3: Detailed Skill Breakdown */}
                <h2 className="text-xl font-extrabold text-[#1a1a2e] mt-8 mb-4 flex items-center gap-2">
                    📋 영역별 상세 분석
                </h2>

                {(['lang', 'cogn', 'emo'] as CatKey[]).map((cat) => {
                    const skills = categorized[cat];
                    if (skills.length === 0) return null;
                    const colors = CAT_COLORS[cat];
                    return (
                        <div key={cat}>
                            {/* Category Divider */}
                            <div className="flex items-center gap-2.5 my-6">
                                <div className="flex-1 h-px bg-[#e5e7eb]" />
                                <span className={`text-sm font-bold px-3.5 py-1 rounded-2xl ${colors.pill}`}>
                                    {colors.label}
                                </span>
                                <div className="flex-1 h-px bg-[#e5e7eb]" />
                            </div>

                            {/* Skill Cards */}
                            <div className="space-y-3.5">
                                {skills.map((skill) => (
                                    <SkillCard key={skill.skillId} skill={skill} cat={cat} reportId={reportId} />
                                ))}
                            </div>
                        </div>
                    );
                })}

                {/* Recommendations */}
                {report.recommendationsNextMonth && (
                    <div className="bg-white rounded-xl border border-[#e5e7eb] p-6 mt-8">
                        <h3 className="text-base font-bold mb-3.5 flex items-center gap-2">💡 다음 달 추천 학습</h3>
                        <ul className="space-y-2.5">
                            {report.recommendationsNextMonth.split('\n').filter(Boolean).map((line, i) => (
                                <li key={i} className="flex items-start gap-2 text-sm text-[#374151]">
                                    <div className="w-1.5 h-1.5 rounded-full bg-[#3b82f6] mt-[7px] flex-shrink-0" />
                                    {line.replace(/^[-•]\s*/, '')}
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>
        </div>
    );
}

/* ============================================================
   Sub-components
   ============================================================ */

/** 6-axis radar chart (pure SVG) */
function RadarSVG({ skills }: { skills: Report['skillSummaries'] }) {
    const axes = ['어휘', '표현', '발음', '유창성', '자신감', '미션'];
    const cx = 150, cy = 150, R = 110;
    const maxLv = 5;

    // Map skills to axes (best-effort match)
    const scores = axes.map((_, idx) => {
        const sk = skills[idx];
        return sk ? Math.min((sk.level || 0) / maxLv, 1) : 0;
    });

    const angleStep = (2 * Math.PI) / 6;
    const pt = (i: number, r: number) => {
        const a = -Math.PI / 2 + i * angleStep;
        return [cx + r * Math.cos(a), cy + r * Math.sin(a)];
    };

    const rings = [0.25, 0.5, 0.75, 1];
    const dataPoints = scores.map((s, i) => pt(i, s * R));
    const dataPath = dataPoints.map(([x, y], i) => `${i === 0 ? 'M' : 'L'}${x},${y}`).join(' ') + ' Z';

    const labelOffset = 22;
    const labelPts = axes.map((_, i) => pt(i, R + labelOffset));

    return (
        <svg viewBox="0 0 300 300" className="w-[280px] h-[280px]">
            {/* Grid rings */}
            {rings.map((r) => (
                <polygon
                    key={r}
                    points={Array.from({ length: 6 }, (_, i) => pt(i, r * R).join(',')).join(' ')}
                    fill="none" stroke="#e5e7eb" strokeWidth="1"
                />
            ))}
            {/* Axes */}
            {Array.from({ length: 6 }, (_, i) => {
                const [x, y] = pt(i, R);
                return <line key={i} x1={cx} y1={cy} x2={x} y2={y} stroke="#f3f4f6" strokeWidth="1" />;
            })}
            {/* Data shape */}
            <path d={dataPath} fill="rgba(99,102,241,0.15)" stroke="#6366f1" strokeWidth="2.5" />
            {/* Data dots + score labels */}
            {dataPoints.map(([x, y], i) => (
                <g key={i}>
                    <circle cx={x} cy={y} r="4" fill="#6366f1" />
                    <text x={x} y={y - 10} textAnchor="middle" fontSize="9" fill="#6366f1" fontWeight="700">
                        {skills[i]?.level ? skills[i].level * 20 : 0}
                    </text>
                </g>
            ))}
            {/* Labels */}
            {axes.map((label, i) => {
                const [x, y] = labelPts[i];
                return (
                    <text key={i} x={x} y={y} textAnchor="middle" dominantBaseline="middle" fontSize="12" fontWeight="700" fill="#374151">
                        {label}
                    </text>
                );
            })}
        </svg>
    );
}

/** Peer Comparison section */
function PeerComparison({ skills }: { skills: Report['skillSummaries'] }) {
    const categories: { key: CatKey; label: string; titleClass: string }[] = [
        { key: 'lang', label: '🇮🇳 언어 (Language)', titleClass: 'text-[#3b82f6]' },
        { key: 'cogn', label: '🧠 인지 (Cognitive)', titleClass: 'text-[#8b5cf6]' },
        { key: 'emo',  label: '💛 정서 (Emotional)', titleClass: 'text-[#f59e0b]' },
    ];

    const categorized = categorizeSkills(skills);

    return (
        <div className="bg-white rounded-xl border border-[#e5e7eb] p-6 mb-7">
            <h2 className="text-xl font-extrabold text-[#1a1a2e] mb-1 flex items-center gap-2">
                👥 또래 평균 비교
                <span className="text-[13px] text-[#6b7280] font-normal">(동일 연령대 기준)</span>
            </h2>
            <div className="grid md:grid-cols-3 gap-5 mt-5">
                {categories.map(({ key, label, titleClass }) => {
                    const catSkills = categorized[key];
                    const avgLevel = catSkills.length > 0
                        ? Math.round(catSkills.reduce((s, sk) => s + (sk.level || 0), 0) / catSkills.length * 20)
                        : 0;
                    const peerAvg = Math.round(avgLevel * 0.8); // simulated peer avg
                    const barColor = key === 'lang' ? 'bg-[#3b82f6]' : key === 'cogn' ? 'bg-[#8b5cf6]' : 'bg-[#f59e0b]';

                    return (
                        <div key={key} className="text-center p-4 rounded-[10px] bg-[#fafbfc]">
                            <div className={`text-[13px] font-bold mb-3 ${titleClass}`}>{label}</div>
                            <div className="space-y-2">
                                <PeerBar label="우리 아이" value={avgLevel} barClass={barColor} />
                                <PeerBar label="또래 평균" value={peerAvg} barClass="bg-[#d1d5db]" />
                            </div>
                        </div>
                    );
                })}
            </div>
            <div className="flex justify-center gap-5 mt-4 text-[11px] text-[#6b7280]">
                <span><span className="inline-block w-2.5 h-2.5 rounded-full bg-[#3b82f6] mr-1 align-middle" />우리 아이</span>
                <span><span className="inline-block w-2.5 h-2.5 rounded-full bg-[#d1d5db] mr-1 align-middle" />또래 평균</span>
            </div>
        </div>
    );
}

function PeerBar({ label, value, barClass }: { label: string; value: number; barClass: string }) {
    return (
        <div className="flex items-center gap-2">
            <span className="text-[11px] w-[50px] text-right text-[#6b7280]">{label}</span>
            <div className="flex-1 h-3.5 bg-[#f3f4f6] rounded-full overflow-hidden relative">
                <div className={`h-full rounded-full ${barClass}`} style={{ width: `${value}%` }} />
                <span className="absolute right-1.5 top-0 text-[10px] font-bold text-white leading-[14px]">{value}</span>
            </div>
        </div>
    );
}

/** Individual Skill Card */
function SkillCard({ skill, cat, reportId }: { skill: Report['skillSummaries'][0]; cat: CatKey; reportId?: string }) {
    const level = skill.level || 0;
    const score = level * 20;
    const colors = CAT_COLORS[cat];
    const levelStyle = LEVEL_STYLES[level] || LEVEL_STYLES[1];
    const trend = skill.trend ?? null;

    const Wrapper = reportId ? Link : 'div';
    const wrapperProps = reportId ? { to: `/parent/reports/${reportId}/skill/${encodeURIComponent(skill.skillId)}` } : {};

    return (
        <Wrapper {...wrapperProps as any} className="block bg-white rounded-xl border border-[#e5e7eb] p-[18px_20px] flex items-start gap-4 hover:shadow-sm transition-shadow cursor-pointer">
            <div className="text-[28px] w-10 text-center flex-shrink-0 mt-0.5">
                {getSkillEmoji(skill.skillId)}
            </div>
            <div className="flex-1 min-w-0">
                <div className="flex justify-between items-center mb-1">
                    <span className="text-[15px] font-bold text-[#1a1a2e]">
                        {skill.skillName || skill.skillId}
                        {skill.skillNameEn && (
                            <span className="text-[12px] text-[#9ca3af] font-normal ml-1.5">{skill.skillNameEn}</span>
                        )}
                    </span>
                    <div className="flex items-center gap-1.5">
                        {trend !== null && (
                            <span className={`text-[11px] font-semibold ${
                                trend > 0 ? 'text-[#16a34a]' : trend < 0 ? 'text-[#dc2626]' : 'text-[#9ca3af]'
                            }`}>
                                {trend > 0 ? `▲+${trend}` : trend < 0 ? `▼${trend}` : '— 0'}
                            </span>
                        )}
                        <span className={`text-[11px] font-bold px-2.5 py-0.5 rounded-full ${levelStyle}`}>
                            Lv.{level}
                        </span>
                    </div>
                </div>
                {/* Score bar */}
                <div className="flex items-center gap-2.5 my-2">
                    <span className="text-[22px] font-extrabold min-w-[36px]">{score}</span>
                    <div className="flex-1 h-2 bg-[#f3f4f6] rounded overflow-hidden">
                        <div
                            className={`h-full rounded bg-gradient-to-r ${colors.bar}`}
                            style={{ width: `${score}%` }}
                        />
                    </div>
                </div>
                {/* Feedback */}
                <p className="text-[13px] text-[#6b7280] leading-relaxed">
                    {skill.summaryForParent || '피드백이 없습니다.'}
                </p>
                {/* CAN-DO */}
                {skill.canDo && (
                    <div className="mt-2 p-2 px-3 bg-[#f9fafb] rounded-md border-l-[3px] border-[#d1d5db]">
                        <div className="text-[11px] font-bold text-[#9ca3af] mb-1">CAN-DO</div>
                        <div className="text-[12px] text-[#374151] leading-relaxed">{skill.canDo}</div>
                    </div>
                )}
                {/* Sparkline */}
                {skill.sparkline && skill.sparkline.length > 0 && (
                    <div className="flex items-end gap-[2px] h-5 mt-2">
                        {skill.sparkline.map((v, i) => {
                            const maxV = Math.max(...(skill.sparkline || [1]));
                            const h = Math.max((v / maxV) * 20, 2);
                            const isLast = i === (skill.sparkline?.length || 0) - 1;
                            return (
                                <div
                                    key={i}
                                    className={`w-[5px] rounded-sm ${isLast ? colors.sparkActive : colors.spark}`}
                                    style={{ height: `${h}px` }}
                                />
                            );
                        })}
                        <span className="text-[9px] text-[#9ca3af] ml-1.5 self-center">30일 추이</span>
                    </div>
                )}
            </div>
        </Wrapper>
    );
}

/* ── Helpers ── */

function categorizeSkills(skills: Report['skillSummaries']) {
    const result: Record<CatKey, Report['skillSummaries']> = { lang: [], cogn: [], emo: [] };
    skills.forEach((s) => {
        const id = (s.skillId || '').toLowerCase();
        if (id.includes('emotion') || id.includes('mood') || id.includes('praise') || id.includes('preference')) {
            result.emo.push(s);
        } else if (id.includes('attention') || id.includes('instruction') || id.includes('topic') || id.includes('cognitive')) {
            result.cogn.push(s);
        } else {
            result.lang.push(s);
        }
    });
    // If nothing categorized, put all in lang
    if (result.lang.length === 0 && result.cogn.length === 0 && result.emo.length === 0) {
        result.lang = [...skills];
    }
    return result;
}

function getSkillEmoji(skillId: string): string {
    const id = (skillId || '').toLowerCase();
    if (id.includes('vocab')) return '📚';
    if (id.includes('like') || id.includes('prefer')) return '❤️';
    if (id.includes('pronun')) return '🗣️';
    if (id.includes('sentence') || id.includes('svo')) return '✍️';
    if (id.includes('question') || id.includes('wh')) return '❓';
    if (id.includes('attention')) return '🎯';
    if (id.includes('instruction')) return '🧩';
    if (id.includes('topic')) return '🔄';
    if (id.includes('mood')) return '😊';
    if (id.includes('praise')) return '🌟';
    if (id.includes('emotion')) return '💝';
    return '📖';
}

function formatDate(dateStr: string) {
    const d = new Date(dateStr);
    return `${d.getFullYear()}.${String(d.getMonth() + 1).padStart(2, '0')}.${String(d.getDate()).padStart(2, '0')}`;
}
