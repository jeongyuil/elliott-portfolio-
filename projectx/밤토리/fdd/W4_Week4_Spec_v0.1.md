# Week 4: Going Outside in Disguise (W4_S1 ~ W4_S4)

대상: 7세, 내성적인 여자아이 / 한국어 모국어, 영어는 기초 수준  

캐릭터:

- **Luna**: 우주에서 온 탐사 로봇, 영어만 사용  
- **Popo**: 지구 정부에서 파견된 조사관 & 코치 로봇, 한국어 + 영어 모두 사용  
  - 역할: 아이와 루나 사이 “통역 / 코치 / 안전장치” + 루나 지구 탐사 공식 조사관

---

## 0. 공통 Relationship Blocks (W4_R0 ~ R4)

W1에서 정의한 **R0 ~ R4(Relationship Blocks)**를 그대로 사용하되, W4의 맥락에 맞게 약간의 멘트만 조정한다.

- **R0. Mission Call: Operation 'Disguise'**  
  - 미션: 루나가 지구 밖으로 나가기 위해 "완벽한 지구인 변장"이 필요함.  
  - 캡틴의 역할: 루나의 스타일리스트 및 행동 코치.  
  - 안전 장치: "도우미가 필요하면 언제든 포포 호출"  
- **R1. Relationship Reminder & Running Gag**  
  - "들키면 안 돼!" (Secret Agent 상황극)  
- **R2. Shared Secret / Club Ritual**  
  - "Earth crew, silent mode!" 🤫 (검지 입에 대기)  
- **R3. Emotion Check-in**  
  - "오늘 변장 미션 할 에너지가 얼마나 있어?" (1, 2, 3)  
- **R4. Closing Ritual & Preview**  
  - "Disguise check complete!" 👌  

> 구현 상에서는 W1에서 만든 `relationship_layer()` 공통 모듈을 재사용하고, W4 미션 설명만 세션별 프롬프트로 전달.

---

## 1. W4_S1: Clothes & Colors for Luna (루나에게 옷 입혀주기 1)

### 1.1 세션 메타

- **세션 코드:** `W4_S1_luna_clothes_colors`  
- **시간:** 15~20분  
- **스토리 컨텍스트:**  
  - 루나가 드디어 **밖으로 나갈 준비**를 한다.  
  - 지구인처럼 보이기 위해 옷과 색을 골라야 한다.  
- **언어 목표**
  - 어휘: `shirt, dress, pants, skirt, shoes, hat, coat`, 색깔 `red, blue, yellow, green, pink, black, white`  
  - 패턴:
    - `I like [red shirt].`
    - `I don’t like [black hat].` (선택)
    - `This is [a red shirt].`
- **정서 목표**
  - 아이가 “스타일 디자이너” 역할을 맡아 **주도권**을 느끼도록 설계  
  - 선택지가 많아도, 언제든 “모르겠음/패스” 허용  

### 1.2 세션 플로우

#### T0. Relationship Layer (R0~R3)

- W1과 동일한 공통 블록 실행.  
- 미션 설명만 추가:

Popo (KR, 첩보원 톤)  
> "대원, 드디어 때가 왔어.  
> 루나가 캡틴의 방을 나서서 **바깥세상**으로 나가고 싶어 해.  
> 하지만 그냥 나가면 우주 로봇인 게 들통나겠지?  
> 캡틴이 루나를 **완벽한 지구 아이**처럼 꾸며줘!"

Luna (EN)  
> "I want to go outside!  
> I need a disguise. Help me, Captain."

---

#### T1. 옷 어휘 카드 소개 (Clothes Vocabulary)

- 화면/카드에 4~6개 기본 아이템 노출:
  - shirt, dress, pants, skirt, shoes, hat  

Popo (KR)  
> “여기 옷들이 있어. 셔츠, 원피스, 바지, 치마, 신발, 모자야.  
> 루나는 영어로만 말할 수 있어서, 영어 이름도 같이 알려줄게.”

Luna (EN, 천천히)  
> “shirt… dress… pants… skirt… shoes… hat…”

- 아이가 따라 말하면 `TaskAttempt: T_W4_S1_repeat_clothes` (optional, receptive/발음 점검용).

---

#### T2. 색깔 + 옷 조합 선택 (Color + Clothes)

- 옷 한 종류씩 보여주며 색깔 선택 UI:
  - 예: “어떤 셔츠가 좋아? 빨강/파랑/노랑 중 하나!”  

Popo (KR)  
> “먼저 셔츠 색을 골라보자.  
> 빨간 셔츠, 파란 셔츠, 노란 셔츠 중에 뭐가 제일 예뻐 보여?”

- 아이 선택 → `chosen_color_shirt` 저장.  
- Popo가 영어로 매핑:

  - 빨강 → red  
  - 파랑 → blue  
  - 노랑 → yellow  

Popo (KR+EN)  
> “좋아, [색] 셔츠구나.  
> 영어로는 ‘red shirt’, ‘blue shirt’ 이런 식이야.  
> 루나에게 이렇게 말해볼까?  
> **‘I like the red shirt.’**”

Luna (EN)  
> “I like the red shirt.”  

- 아이 발화:

  - 완전 문장: `I like the red shirt.` → `evaluated_correctness = correct`  
  - “red shirt”만 말하면 → `partial` 처리, Popo가 풀 문장으로 리폼.

`TaskAttempt: T_W4_S1_clothes_like_color`  
- `expected_response_pattern: description`  
- `skills: Vocabulary_clothes, Vocabulary_colors, Expressive_basic_sentence`

---

#### T3. 싫어하는 스타일도 하나 선택 (선택적)

- 아이 컨디션이 여유 있을 때만 사용.

Popo (KR)  
> “그럼 루나랑 안 어울릴 것 같은 옷도 하나 골라볼래?  
> ‘이건 별로야~’ 하는 옷.”

아이가 그림 선택 → Popo가 영어 예시:

> “I don’t like the black hat.”

아이가 “don’t like” 패턴이 어렵다면 단어만 말해도 인정.

`TaskAttempt: T_W4_S1_clothes_dislike_optional`

---

#### T4. 최종 코디 요약

- 시스템이 아이가 고른 2~3개 아이템을 요약:

Popo (KR)  
> “정리해보면,  
> [이름]이는 루나에게  
> **[red shirt], [blue pants], [white shoes]**를 입히고 싶어 했어.”

Luna (EN)  
> “[Name] likes the red shirt, blue pants, and white shoes for me.  
> Thank you, stylist!”

- Popo가 아이에게 한 문장만 다시 말해보도록 유도:

Popo (KR)  
> “영어로 하나만 골라서 다시 말해볼까?  
> 예를 들면 ‘I like the red shirt.’”

성공/실패 상관 없이 칭찬 위주로 마무리.

---

#### T5. 마무리 (R4)

- 오늘 미션: “Luna Clothes Plan v1” 저장 언급.
- Closing Ritual 실행.

---

## 2. W4_S2: Put on & Take off (입기 / 벗기기)

### 2.1 세션 메타

- **세션 코드:** `W4_S2_put_on_take_off`  
- **목표**
  - 동사 표현 도입:
    - `put on [coat/hat/shoes]`
    - `take off [coat/hat/shoes]`
  - 간단한 **날씨/상황**과 연결 (“추우면 코트 입기”)  
- **언어 목표**
  - 동사: put on, take off  
  - 명사: coat, hat, shoes  
  - 패턴:
    - `Put on your coat.`
    - `Take off your shoes.`
- **정서 목표**
  - “루나를 챙겨주는 보호자/코치 역할” 경험  
  - 명령문이지만, 게임처럼 가볍게 진행  

### 2.2 세션 플로우

#### T0. Relationship Layer (R0~R3)

- 오늘 미션 소개:

Popo (KR)  
> “오늘은 루나가 밖에 나가기 전에  
> **언제 옷을 입고, 언제 벗어야 하는지** 알려주는 연습을 해볼 거야.”

---

#### T1. 동사 소개: put on / take off

- 간단 애니메이션/이미지:  
  - 룬나 몸에 코트가 “슝” 입혀지는 그림, 다시 사라지는 그림.

Popo (KR)  
> "변장의 핵심은 자연스러움이야!  
> 입을 땐 **put on**, 벗을 땐 **take off**.  
> 루나가 헷갈리지 않게 훈련시켜줘."

Luna (EN)  
> "P.u.t.. o.n.. coat. (Robot voice)  
> Is this right, Captain?"

아이가 따라 말하면 `TaskAttempt: T_W4_S2_repeat_verbs` (optional).

---

#### T2. 날씨 상황 카드: Cold vs Warm

- 두 가지 상황만 사용:

  - 그림 1: 눈 오는 추운 날 (❄️)  
  - 그림 2: 햇볕 나는 따뜻한 날 (☀️)  

Popo (KR)  
> “여기 두 가지 날씨가 있어.  
> 눈 오는 추운 날, 그리고 따뜻한 날.  
> 추운 날에는 루나가 뭘 입어야 할까?”

아이가 “코트” 등 한국어로 말하면 → `coat` 매핑.

Popo (KR+EN)  
> “맞아, 코트!  
> 영어로는 ‘coat’.  
> ‘코트 입어!’는  
> ‘Put on your coat.’라고 말할 수 있어.”

Luna (EN)  
> “Put on your coat.” (천천히 반복)

`TaskAttempt: T_W4_S2_put_on_cold`

---

#### T3. 집 안 / 밖 상황: 신발 벗기 & 모자 벗기

상황 1: 집에 들어왔을 때

Popo (KR)  
> “집에 들어왔을 때는 보통 신발을 어떻게 하지?”

아이가 “벗어”라고 하면:

Popo (KR+EN)  
> “맞아, 신발은 벗어야지.  
> ‘Take off your shoes.’라고 말할 수 있어.”

Luna (EN)  
> “Take off your shoes.”

상황 2: 햇볕이 뜨거운 날 모자 쓰기

Popo (KR)  
> “햇볕이 너무 뜨거울 때는?”

아이가 “모자 써” ⇒ `hat` + `put on your hat`.

`TaskAttempt: T_W4_S2_take_off_put_on_context`

---

#### T4. 미니 게임: Luna가 틀리게 행동하기

- 애니메이션 예:  
  - 눈 오는 날, 루나가 코트를 벗어버림.  
  - 집에 들어왔는데 신발을 신고 침대에 올라감.

Luna (EN, 일부러 틀리게)  
> “It is very cold. I take off my coat!”  

Popo (KR)  
> “어? 이게 맞을까?  
> [이름]이가 루나에게 영어로 알려줄래?”

아이 목표:

- “Put on your coat.” 또는  
- “No, put on your coat.” (부분만 말해도 인정)

`TaskAttempt: T_W4_S2_fix_luna_mistake`

---

#### T5. 마무리 (R4)

- 오늘 배운 표현 요약: `put on`, `take off`.  
- 다음 세션(W4_S3)에서 **아이 본인의 옷과 스타일** 이야기로 연결 예고.

---

## 3. W4_S3: My Clothes & My Style (내 옷 / 내가 좋아하는 옷)

### 3.1 세션 메타

- **세션 코드:** `W4_S3_my_clothes_style`  
- **목표**
  - 아이가 **자기 옷/스타일**을 설명하는 간단 문장 말해보기  
  - W1의 “My likes” + W4_S1, S2의 옷 표현을 통합  
- **언어 목표**
  - 명사: T-shirt, dress, pants, skirt, hoodie, shoes  
  - 패턴:
    - `This is my [dress].`
    - `I like my [blue hoodie].`
    - `I wear [a T-shirt].` (선택)
- **정서 목표**
  - “내 옷을 보여준다”는 행위를 통해 친밀감 강화  
  - 아이가 직접 입고 있는 옷을 소재로 쓸 수도, 평소 좋아하는 옷을 상상할 수도 있음  

### 3.2 세션 플로우

#### T0. Relationship Layer (R0~R3)

- 안전/프라이버시 안내 추가:

Popo (KR)  
> “지금 입고 있는 옷을 말해도 되고,  
> 그냥 ‘내가 좋아하는 옷’을 상상해서 말해도 괜찮아.  
> 사진이나 진짜 모습을 꼭 보여줄 필요는 없어.”

---

#### T1. 지금 입고 있거나 좋아하는 옷 묻기

Popo (KR)  
> “[이름]이는 어떤 옷을 제일 좋아해?  
> 예를 들면 티셔츠, 원피스, 후드티, 바지 같은 거!”

아이가 한국어로 말하면:

- 티셔츠 → T-shirt  
- 원피스 → dress  
- 후드티 → hoodie  
- 바지 → pants  
- 치마 → skirt  

---

#### T2. 패턴 1: This is my ~

Popo (KR+EN)  
> “예를 들면, 좋아하는 원피스를 말하고 싶으면  
> ‘This is my dress.’라고 말할 수 있어.”

Luna (EN)  
> “This is my dress.  
> This is my T-shirt.”

아이가 해당 패턴으로 한 번이라도 말하면:

`TaskAttempt: T_W4_S3_this_is_my_clothes`

---

#### T3. 색깔까지 붙여보기 (선택)

Popo (KR)  
> “색도 말해볼까?  
> 파란 후드티라면  
> ‘my blue hoodie’라고 할 수 있어.”

Luna (EN)  
> “I like my blue hoodie.”

아이 발화 목표:

- `I like my [color] [clothes].`  
  - 완전 문장 → `correct`  
  - `[blue hoodie]`만 말해도 `partial`.

`TaskAttempt: T_W4_S3_like_my_color_clothes`

---

#### T4. 언제 입는 옷인지 간단하게 (선택)

- 아이 컨디션 좋을 때만.

Popo (KR)  
> “그 옷은 언제 많이 입어?  
> 학교 갈 때? 놀러 갈 때? 집에서 쉴 때?”

아이 답변 한국어로 → 내부 태깅: `usage_context = school/home/outing`.

Luna (EN, 노출용)  
> “I wear my hoodie at school.”  
> “I wear my dress on Sunday.”

> 굳이 아이가 그대로 따라하지 않아도 되고,  
> 원하면 짧게 “school” 정도만 말해도 인정.

---

#### T5. 마무리 (R4)

- Popo가 정리:

Popo (KR)  
> “이제 루나는  
> [이름]이가 좋아하는 옷과 색깔까지 알게 됐어.  
> 나중에 루나가 [이름]이를 떠올릴 때,  
> ‘아, 파란 후드티를 좋아하는 지구 대원!’이라고 기억할 거야.”

---

## 4. W4_S4: Final Disguise Mission & Badge (최종 변장 미션 & 배지 수여)

### 4.1 세션 메타

- **세션 코드:** `W4_S4_final_disguise_badge`  
- **목표**
  - W1~W4에서 다뤘던 **자기소개 / 취향 / 공간 / 옷 / 감정 / 위치 / put on** 등을 가볍게 통합  
  - 아이가 “지구 대원 1단계 완료” 느낌을 받도록 설계  
- **언어 목표 (리뷰 중심)**
  - `My name is ~ / I am seven.`
  - `I like ~.`
  - `This is my ~.`
  - `Put on your ~.`
- **정서 목표**
  - “끝처럼 보이지만, 다음 단계가 있는” 성장 경험  
  - 평가보다는 **축하 및 강화**에 초점  

### 4.2 세션 플로우

#### T0. Relationship Layer (R0~R3)

- 특별 멘트:

Popo (KR)  
> “오늘은 **1단계 마지막 미션**이야.  
> [이름]이가 없었으면 여기까지 못 왔을 거야.”

---

#### T1. 루나 최종 변장 코디 완성

- 시스템이 앞 세션에서 저장된 선호 정보 활용:  
  - 좋아하는 색, 옷, 스타일, put on 규칙 등.

Popo (KR)  
> “지금까지 [이름]이가 도와줘서  
> 루나의 변장 세트가 거의 완성됐어.  
> 마지막으로 한 번 더 골라볼까?”

- 간단한 요약 화면:  
  - 옷 2~3개, 색, 모자/신발 옵션  
- 아이가 마지막 선택 → `final_disguise_config` 저장.

Luna (EN)  
> “This is my disguise.  
> Do I look like an Earth child?”

---

#### T2. 미니 Role-play 1: 잘못된 변장 고치기

- 애니메이션:  
  - 루나가 한겨울에 반팔만 입고 있음,  
  - 집 안에서 신발 신고 침대에 올라감 등.

Luna (EN, 일부러 틀리게)  
> “It is very cold.  
> I take off my coat.”

Popo (KR)  
> “어? 이거 이상하지 않아?  
> [이름]이가 루나에게 한마디만 해줄래?  
> ‘Put on your coat.’ 처럼.”

아이가 “Put on your coat.” 또는 “coat”만 말해도 성공으로 처리.

`TaskAttempt: T_W4_S4_fix_disguise_context`

---

#### T3. 미니 Role-play 2: 자기소개 + 옷 한 줄

- Popo가 역할극 상황 제공:

Popo (KR)  
> “이제 루나랑 [이름]이가  
> 지구 학교 앞에 서 있다고 상상해보자.  
> 새 친구에게 간단히 소개할 거야.”

구조:

1. Popo가 한국어로 scaffold:
   - “이름이 뭐예요?” → `My name is ~.`  
   - “몇 살이에요?” → `I am seven.`  
   - “이 옷 마음에 들어?” → `I like my ~.`  

2. 아이가 **가능한 만큼만** 영어로 말하면 됨.

예상 발화 (이상적 타겟):

- `My name is [Name].`  
- `I am seven.`  
- `I like my [blue hoodie].`

실제 구현에서는:

- 단어만 말해도 `partial_correct`  
- 전혀 말하지 못해도 Popo가 대신 말해주고,  
  아이가 “Yes / No / head nod” 정도로만 반응해도 성공으로 간주.

`TaskAttempt: T_W4_S4_mini_self_intro_clothes`

---

#### T4. 지구 대원 1단계 배지 수여

Popo (KR)  
> “루나랑 포포가 회의를 해봤는데…  
> [이름]이는 **지구 대원 1단계 미션을 모두 완료**했어! 🎉  
> 그래서 ‘Earth Crew Level 1’ 배지를 주기로 했어.”

Luna (EN)  
> “[Name], you are Earth Crew Level 1.  
> Thank you for helping me.  
> I feel safe with you.”

- 화면에 배지 애니메이션 + 이름 노출:  
  - `Earth Crew Lv.1 – [Name]`  
- 내부 데이터:
  - `badge_earned = earth_crew_lv1`  
  - `event_type = BadgeEarned` 로 이벤트 로그 기록.

---

#### T5. 다음 단계 티저 & Closing (R4)

Popo (KR)  
> “다음에는 루나가 지구에서  
> **더 많은 장소와 사람들**을 만나는 연습을 할 거야.  
> [이름]이가 계속 도와줄 거지?”

Luna (EN)  
> “Will you stay with me, Captain [Name]?”

- 아이가 “응 / yes”라고만 해도 충분.  
- 마지막으로 Ritual:

> “Earth crew, mission complete!” ✊

---

### 참고: W4 주요 TaskAttempt & Skill 예시 요약

- `T_W4_S1_clothes_like_color`  
  - **expected_response_pattern:** description  
  - **skills:**  
    - Vocabulary_clothes  
    - Vocabulary_colors  
    - Expressive_basic_sentence  

- `T_W4_S2_put_on_cold`, `T_W4_S2_take_off_put_on_context`, `T_W4_S2_fix_luna_mistake`  
  - **skills:**  
    - Vocabulary_clothes  
    - Grammar_basic_verbs (put_on / take_off)  
    - Pragmatics_context_appropriate_behavior  

- `T_W4_S3_this_is_my_clothes`, `T_W4_S3_like_my_color_clothes`  
  - **skills:**  
    - Expressive_simple_description  
    - Vocabulary_clothes_colors  

- `T_W4_S4_mini_self_intro_clothes`, `T_W4_S4_fix_disguise_context`  
  - **skills:**  
    - Expressive_self_intro_basic  
    - Discourse_mini_sequence (짧은 시퀀스 말하기)  
    - Confidence_speaking (정서적 지표로 태깅 가능)
