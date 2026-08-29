import { Skill, calculateSkillLevel, getSkillLevelDescription, getCategoryColor } from "@/lib/skillsData";

interface SkillProgressProps {
  skill: Skill;
  currentValue: number; // 0-100 for score, 1-5 for level
  showDetails?: boolean;
}

export default function SkillProgress({ skill, currentValue, showDetails = false }: SkillProgressProps) {
  const level = skill.unit === "score_0_100" ? calculateSkillLevel(currentValue) : currentValue;
  const levelDescription = getSkillLevelDescription(level);
  const categoryColorClass = getCategoryColor(skill.category);

  // Calculate progress percentage
  const progressPercentage = skill.unit === "score_0_100" ? currentValue : (currentValue / 5) * 100;

  return (
    <div className="duo-card p-4">
      {/* Skill Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className="text-3xl">{skill.emoji}</span>
          <div>
            <h3 className="font-bold text-gray-800">{skill.name_kr}</h3>
            <p className="text-xs text-gray-500">{skill.name_en}</p>
          </div>
        </div>
        <span className={`px-2 py-1 rounded-full text-xs font-semibold ${categoryColorClass}`}>
          {skill.category === "language" && "언어"}
          {skill.category === "cognitive" && "인지"}
          {skill.category === "emotional" && "정서"}
        </span>
      </div>

      {/* Progress Bar */}
      <div className="mb-2">
        <div className="flex justify-between items-center mb-1">
          <span className="text-sm font-semibold text-gray-700">{levelDescription}</span>
          <span className="text-sm font-bold text-duo-green">
            {skill.unit === "score_0_100" ? `${currentValue}점` : `레벨 ${currentValue}`}
          </span>
        </div>
        <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-duo-green to-green-400 transition-all duration-500"
            style={{ width: `${progressPercentage}%` }}
          />
        </div>
      </div>

      {/* Level Stars */}
      <div className="flex gap-1 mb-3">
        {[1, 2, 3, 4, 5].map((star) => (
          <span
            key={star}
            className={`text-lg ${star <= level ? "text-yellow-400" : "text-gray-300"}`}
          >
            ⭐
          </span>
        ))}
      </div>

      {/* Description */}
      {showDetails && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <p className="text-sm text-gray-600 mb-3">{skill.description}</p>
          <div className="bg-blue-50 p-3 rounded-lg">
            <h4 className="text-sm font-bold text-blue-800 mb-2">💡 이 스킬로 할 수 있는 것:</h4>
            <ul className="space-y-1">
              {skill.can_do_examples.map((example, index) => (
                <li key={index} className="text-xs text-blue-700 flex items-start gap-2">
                  <span className="text-blue-500 mt-0.5">•</span>
                  <span>{example}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
