# Wireframe Screen Specs — Ringle 1:1 Class AI Analysis (CAF Stats)

---

## Screen 1 — AI Analysis Overview (Tab 0)

**Purpose**
- Show a summary of analyzed 1:1 classes for a date range, overall skill levels, and recommended learning areas.

**Entry points**
- From “My Ringle / AI analysis” landing.
- Navigating from menu into AI analysis (includes date range context).

**Top navigation / header**
- Left: **Back** (“뒤로가기”)
- Center/Title area: “1:1 수업 : CAF 통계 - 링글 일대일 화상영어”
- Right: “기업 제휴” and profile/avatar icon

**Filters / context**
- **Date range selector** (e.g., “최근 1개월”) and visible **date range** (e.g., `2026-01-27 - 2026-02-27`)
- **Class analysis count bar**:
  - “분석한 수업” with durations (e.g., `40분 1`, `20분 0`) and link: “수업 리스트 보기”

**Section A — Level change**
- Title: “레벨 변화”
- Tabs: **전체**, Complexity, Accuracy, Fluency, Pronunciation
- Chart area:
  - A scatter/point visualization across “수업 날짜”
  - Legend: Complexity / Accuracy / Fluency / Pronunciation
- Right-side action: “상세 레벨”

**Section B — Recommended learning areas**
- Title: “추천 학습 영역”
- Helper text: recommendation based on last analyzed class(es)
- Link on right: “전체 학습 영역보기”
- List of learning area cards:
  - Example card: **필러워드** with a count (“6개”) and short explanation
  - Each card shows a mini sparkline/bar area on the right (trend over class dates)

**Section C — Pinned / user-selected focus areas**
- Title: “내가 집중하고 싶은 학습 영역”
- Helper text: “학습 영역을 고정하고 다른 수업에서 어떻게 달라지는지 확인해보세요.”
- Right-side action: “편집하기”
- Shows the currently pinned learning area cards (same style as above)

**Primary interactions**
- Change date range (“최근 1개월” dropdown)
- Switch level tabs (전체/Complexity/Accuracy/Fluency/Pronunciation)
- Click “수업 리스트 보기” to view class list
- Click a learning area card to open **Screen 3: Learning Area Detail**
- Click “전체 학습 영역보기” to open **Screen 2: Learning Areas**
- Click “편집하기” to manage pinned focus areas (see Screen 4)

**Empty / edge states**
- If no analyzed classes in range: show empty chart + message + CTA to take a class
- If a learning area has no detected issue: show “없었어요” style message (used in learning areas list)

---

## Screen 2 — Learning Areas (Tab 2)

**Purpose**
- Provide a complete categorized list of learning areas, split into Weakness and Strength, with sortable filters and quick summaries.

**Top navigation / header**
- Same as Screen 1 (Back, title, corporate partner/profile)

**Left panel / controls**
- Title: “학습 영역”
- Date range dropdown (e.g., “최근 1개월”)
- Sort dropdown (e.g., “링글 추천순”)
- Toggle tabs:
  - “전체”
  - “내가 집중하고 싶은 학습 영역” (pinned subset)

**Main content**
- Two sections:
  1) **Weakness**
  2) **Strength**
- Each section contains card rows for each learning area with:
  - Icon (category)
  - Label (e.g., 필러워드 / 문법 실수 / 발음 / 말하기 속도)
  - One-line summary with an average count (e.g., “평균 6개 있어요.”)

**Examples of learning areas shown**
- Weakness:
  - 필러워드: “필러워드 사용이 많았던 구간이 평균 6개 있어요.”
  - 문법 실수(단어 순서): “평균 1개 있어요.”
  - 발음: “발음 연습이 필요한 단어가 평균 5개 있어요.”
  - 문법 실수(명사 수일치): “평균 8개 있어요.”
  - 문법 실수(형용사): “평균 1개 있어요.”
  - 말하기 속도: “말하기 속도가 느렸던 구간이 평균 10개 있어요.”
- Strength:
  - (Example visible) 문법 실수(한정사): “평균 3개 있어요.”

**Primary interactions**
- Select date range
- Change sorting (“링글 추천순”)
- Switch between “전체” and “내가 집중…”
- Click any learning area card → opens **Screen 3: Learning Area Detail**

**Empty / edge states**
- For learning areas with no events in range:
  - Show “없었어요” (e.g., “반복적으로 사용한 단어가 없었어요.” / “더 복잡한 문장 구조를 시도해 볼 수 있는 구간이 없었어요.”)

---

## Screen 3 — Learning Area Detail (Modal / Drawer)

**Purpose**
- Deep dive into one learning area (e.g., filler words): show how segments were selected, tips, and concrete examples with audio playback and transcripts.

**Trigger**
- Clicking a learning area card from Screen 1 or Screen 2.

**Modal layout**
- Appears as an overlay panel centered over the page.
- Header:
  - Back arrow (to return to previous screen state)
  - Title: “필러워드 사용이 많았던 구간이 평균 6개 있어요.”
  - Right: close “X” icon
- Tabs/labels near top:
  - “필러워드”
  - “구간 선정 기준” (with info icon)
- Tip section:
  - “Ringle’s Tip” card with right arrow (expand/open tip)

**Content blocks**
- Segment/example cards, each typically containing:
  - A highlighted transcript snippet (filler words bolded/emphasized)
  - Average filler-word duration (“평균 filler words 길이: 0.63초”)
  - Audio player:
    - Play button
    - Current time / total duration (e.g., `00:00` to `01:09`)
  - “오류 제보” (report error)
- Additional transcript cards below with expandable chevrons

**Primary interactions**
- Close modal
- Open “Ringle’s Tip”
- Play/pause audio; scrub timeline
- Expand/collapse transcript sections
- Report an error (“오류 제보”)

**Edge states**
- If no examples are available: show an empty state with explanation + tip content
- If audio missing/unavailable: disable player and show fallback message

---

## Screen 4 — “Edit My Focus Learning Areas” (Manage Pinned Areas)

**Purpose**
- Let the user choose which learning areas to pin under “내가 집중하고 싶은 학습 영역” for trend tracking across classes.

**Trigger**
- Click “편집하기” from Screen 1.

**Expected UI (inferred from existing screens)**
- A list of all learning areas (similar to Screen 2) with selection controls:
  - Checkbox or toggle per learning area card
- Actions:
  - Save / Apply (primary)
  - Cancel / Back (secondary)
- Rule hints:
  - Limit of how many areas can be pinned (if product has such a constraint)
  - Pinned areas appear in Screen 1 Section C

**Primary interactions**
- Select/deselect learning areas
- Save changes → return to Screen 1; pinned list updates

**Validation / edge cases**
- If max pin limit exceeded: inline warning and prevent saving until resolved
- Persist selections across sessions (if account-based)

---

## Screen flow summary

1. **Screen 1 (Overview)**  
   → “전체 학습 영역보기” → **Screen 2**  
   → Click learning area card → **Screen 3**

2. **Screen 2 (Learning Areas)**  
   → Click learning area card → **Screen 3**

3. **Screen 1**  
   → “편집하기” → **Screen 4** → Save → **Screen 1**

