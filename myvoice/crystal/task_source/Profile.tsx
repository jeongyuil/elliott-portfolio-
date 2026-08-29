            </div>
            <div className="text-center p-3 bg-yellow-50 rounded-xl">
              <Award size={20} className="text-[var(--duo-yellow)] mx-auto mb-1" />
              <div className="text-xl font-bold text-[var(--duo-text)]">
                {userData.stats.pronunciationAccuracy}%
              </div>
              <div className="text-xs text-[var(--duo-text-secondary)] mt-1">발음 정확도</div>
            </div>
          </div>
        </div>

        {/* Weekly Progress */}
        <div className="duo-card p-4 mb-20">
          <h2 className="text-lg font-bold text-[var(--duo-text)] mb-3 flex items-center gap-2">
            📈 주간 학습량
          </h2>
          <div className="flex items-end justify-between gap-2 h-28">
            {weeklyProgress.map((day, index) => {
              const maxMinutes = Math.max(...weeklyProgress.map(d => d.minutes));
              const height = (day.minutes / maxMinutes) * 100;
              const isToday = index === 6;

              return (
                <div key={day.day} className="flex-1 flex flex-col items-center gap-2">
                  <div className="flex-1 flex items-end w-full">
                    <div
                      className={`w-full rounded-t-lg transition-all ${
                        isToday ? "bg-[var(--duo-green)]" : "bg-blue-200"
                      }`}
                      style={{ height: `${height}%` }}
                    />
                  </div>
                  <span className="text-xs font-semibold text-[var(--duo-text-secondary)]">
                    {day.day}
                  </span>
                </div>
              );
            })}
          </div>
        </div>