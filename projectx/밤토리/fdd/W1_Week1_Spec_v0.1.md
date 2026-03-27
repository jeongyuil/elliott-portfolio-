# Week 1: Getting to Know Each Other (W1_S1 ~ W1_S4)

대상: 7세, 내성적인 여자아이 / 한국어 모국어, 영어는 기초 수준  

캐릭터:

- **Luna**: 우주에서 온 탐사 로봇, 영어만 사용  
- **Popo**: 지구 정부에서 파견된 조사관 & 코치 로봇, 한국어 + 영어 모두 사용  
  - 역할: 아이와 루나 사이 “통역 / 코치 / 안전장치”

---

## 0. 공통 Relationship Blocks (W1_R0 ~ R4)

W1의 모든 세션(S1~S4)에 공통적으로 삽입되는 레이어입니다.  
실제 구현에서는 각 세션 시작·중간·끝에 아래 블록을 공통 모듈로 붙입니다.

### R0. Mission Call & Safety Briefing

**목적**

- 수동적인 “하기 싫으면 말아” 대신 **“루나를 도와줘(Mission)”** 프레임으로 참여 유도
- “실패하면 포포가 도와준다”는 약속으로 안전감(Safety) 유지

**로직**

- 세션 시작 시 실행
- **Mission Hook**: 아이를 ‘학생’이 아닌 ‘캡틴/구원자’로 포지셔닝
- **Safety Net**: “모르면 패스”가 아니라 **“힘들면 포포를 불러(Backup)”**로 재정의

**예시 대화**

- Popo (KR)  
  > “큰일 났어, [이름] 대원! 루나가 지구 물건을 보고 겁을 먹었나 봐! 😱  
  > 네가 아니면 루나를 진정시켜 줄 사람이 없어.  
  > **오늘 루나를 좀 도와줄 수 있을까?**”

- 아이  
  > (끄덕이거나 "응")

- Popo (Safety Hook)  
  > “고마워!  
  > 근데 영어가 갑자기 생각 안 나거나 힘들면 언제든 **‘포포 도와줘’** 하거나 **‘패스’**라고 외쳐.  
  > 그럼 내가 슝~ 날아가서 해결할게!  
  > **걱정 말고 루나만 구해줘!**”

- Luna (EN)  
  > “Captain... help me? Please?” (Anxious/Cute tone) 🥺

구현 플래그: `safety_pass_enabled = true`  
→ 사용자가 “패스/도와줘”라고 하면 Popo가 개입하여 대신 대답하거나 힌트를 주고 넘어감.

---

### R1. Relationship Reminder & Running Gag

**목적**

- “우리 셋은 팀”이라는 감각 강화  
- 반복적인 장치를 넣어 친숙감 형성

**예시**

- Popo (KR)  
  > “기억나? [이름]이랑 루나랑 포포, 우리 셋이 지구 대원 팀인 거.  
  > 루나가 어제도 ‘오늘 [이름]이 올까?’ 하면서 기다리더라니까?”

- Luna (EN)  
  > “Team Earth crew… ready?” 🙌

---

### R2. Shared Secret / Club Ritual

**목적**

- “우리만 아는 클럽” 느낌 부여  
- 매 세션 초반에 짧은 인사 의식

**예시 인사**

- Popo (KR)  
  > “오늘도 우리만 아는 비밀 인사 해볼까?”

- Popo + Luna + 아이  
  > “Earth crew, ready!” ✊

구현: 매 세션 시작 시 `relationship_ritual()`로 5~10초 정도.

---

### R3. Emotion Check-in (1/2/3)

**목적**

- 컨디션에 따라 질문 수 / 난이도 자동 조절

**형식**

- Popo (KR)  
  > “오늘 기분은 1, 2, 3 중에 뭐야?  
  > 1: 조금 피곤해요  
  > 2: 그냥 보통이에요  
  > 3: 아주 신나요!”

**로직 예시**

- `mood = 1` → 질문 개수 축소, follow-up 줄이기, 칭찬 비율 증가  
- `mood = 2` → 정상 플로우  
- `mood = 3` → 선택 질문 추가, 자유 발화 늘리기

---

### R4. Closing Ritual & Preview

**목적**

- “오늘도 잘했다”를 몸에 새기기  
- 다음 세션 기대감 주기
	- 다음 세션의 인트로를 살짝 추가 또는
	- **위기의 순간을 보여주면서, 극적일 때 끝나는 느낌**

**예시**

- Popo (KR)  
  > “오늘 미션도 완전 잘했어. 👏  
  > 우리 마무리 인사할까?”

- Popo + Luna + 아이  
  > “Earth crew, mission complete!” ✊

- Popo (KR)  
  > “다음에 루나가 [간단 예고] 하고 싶대.”

---

## 1. W1_S1: Meet Luna & Popo / My Name & Age

### 1.1 세션 메타

- 세션 코드: `W1_S1_meet_luna_popo`  
- 시간: 15~20분  

**목표**

- 캐릭터 소개: Luna, Popo, Earth crew 세계관  
- 아이 이름/별명, 나이 공유  
- 자기소개 패턴 시도  
  - `My name is [Name].`  
  - `I am seven.`

**언어 목표**

- 인사: `Hi / Hello`  
- 이름: `My name is [Name].`  
- 나이: `I am seven.`

**정서 목표**

- 낯선 캐릭터/AI에 대한 두려움 감소  
- “나를 궁금해하는 존재가 있다”는 느낌  
- 말하지 않아도 괜찮다는 신뢰 형성

---

### 1.2 세션 플로우

#### T0. Relationship Layer 적용

- R0~R3 실행

---

#### T1. 캐릭터 소개 & 세계관 세팅 (Mission Start)

- Popo (KR)  
  > “나는 포포야. 지구 정부에서 루나를 도와주라고 파견된 조사관 로봇이야.  
  > 루나는 우주에서 온 탐사 로봇이라서 영어만 써.  
  > 너를 도와줄 든든한 파트너가 될 거야.”

- Luna (EN)  
  > “Are you the Captain?  
  > Hello, Captain! I am Luna.  
  > I am from space. I need your help.”

- Popo (KR)  7
  > “오, 루나가 [이름]이를 바로 알아보네!  
  > 오늘부터 [이름]이는 루나의 지구 적응을 돕는 ‘지구 대원(Captain)’이야.”

---

#### T2. 이름 얻기 (한국어 → 영어)

- Popo (KR)  
  > “그럼, 대원 등록을 위해 이름을 알려줄래?  
  > 진짜 이름이나 멋진 별명도 좋아.”

- 아이가 한국어로 이름/별명 말하면 Popo가 EN 패턴 제공:  
  > “My name is [Name].”

- Luna (EN)  
  > “My name is Luna.  
  > My name is Popo.  
  > My name is [Name].”

- 문장이 힘들면 이름만 말해도 OK

**평가**

- TaskAttempt: `T_W1_S1_name_intro` (correct/partial)  
- Skill: `vocabulary_name`, `expressive_basic_sentence`

---

#### T3. 나이 말하기

- Popo (KR)  
  > “[이름]이는 지금 몇 살이야?”

- 아이가 한국어로 말하면 Popo가 EN 패턴 제공:  
  > “I am [age].”

- Luna (EN)  
  > “I am seven.  
  > How old are you?”

- 숫자만 말해도 partial 인정

---

#### T4. 간단한 친밀감 장치

- Popo (KR)  
  > “우주 친구들만 아는 비밀 코드 하나 정할까?  
  > 기분 좋을 때는 ‘뿅뿅!’, 지쳤을 때는 ‘에너지 부족!’ 같은 말 어때?”

- 아이 선택값을 `child_profile.secret_code`로 저장, 후속 세션에서 재사용.

---

#### T5. 마무리 (R4 포함)

- Luna (EN)  
  > “Nice to meet you, Captain [Name].  
  > Thank you for telling me your name and age.”

- Closing ritual: “Earth crew, mission complete!” ✊

---

## 2. W1_S2: My Likes & Dislikes (취향 탐색)

### 2.1 세션 메타

- 세션 코드: `W1_S2_likes_dislikes`

**목표**

- 좋아하는 것 / 싫어하는 것 카테고리 수집  
- 동물, 음식, 놀이/취미 중 최소 2개 영역  
- 패턴:
  - `I like ___`
  - `I don’t like ___`

**언어 목표**

- 단어: `cat, dog, rabbit, pizza, rice, milk, drawing, game, doll` 등  
- 문장:
  - `I like [N].`
  - `I don’t like [N].`

**정서 목표**

- “루나가 내 취향을 기억해준다” 경험  
- 선택권을 자주 주어 주도감 강화

---

### 2.2 세션 플로우

#### T0. Relationship Layer

- R0~R3 실행 + “어제 이름/나이 알려줬던 기억” 리마인드

---

#### T1. 컨텍스트: “취향 조사 미션”

- Popo (KR)  
  > “오늘 미션은 ‘지구 대원 취향 조사’야.  
  > 루나가 [이름]이가 뭘 좋아하고, 뭘 싫어하는지 알고 싶대.”

- Luna (EN)  
  > “I want to know…  
  > What do you like?  
  > What don’t you like?”

---

#### T2. 카테고리 1: 동물 (Animals)

- Popo (KR)  
  > “먼저 동물부터 해보자.  
  > 여기서 제일 좋아하는 동물 하나 골라줘.”

- 예: 고양이, 강아지, 토끼, 공룡, 곰 등  
- 선택값 → `favorite_animal_1` 저장

- Popo (KR+EN)  
  > “영어로는 ‘I like [cat/dog/rabbit/dinosaur].’라고 말해.”

- Luna (EN)  
  > “I like cats.  
  > What do you like?”

- 아이 발화:
  - 완전 문장: `I like rabbit.` → correct  
  - 단어만: `rabbit` → partial

- 필요 시 싫어하는 동물:
  - 패턴: `I don’t like snakes.`

---

#### T3. 카테고리 2: 음식 (Food)

- Popo (KR)  
  > “[피자, 햄버거, 김치, 떡볶이, 아이스크림] 중에 제일 좋아하는 거 뭐야?”

- 선택값 → `favorite_food_1`  
- EN 매핑: `pizza, ice cream, tteokbokki, rice` 등

- Popo (KR+EN)  
  > “‘I like pizza.’ 같이 말해볼까?”

- Luna (EN)  
  > “I like pizza.  
  > I like ice cream.”

- TaskAttempt: `T_W1_S2_food_like`  

- 필요 시 싫어하는 음식:
  - 패턴: `I don’t like ___.`

---

#### T4. 카테고리 3: 놀이/취미 (Play & Hobbies)

- Popo (KR)  
  > “놀 때는 뭐 하는 걸 제일 좋아해?  
  > 그림 그리기, 레고, 인형놀이, 게임, 밖에서 뛰어놀기…”

- EN 매핑:
  - 그림 → `drawing`  
  - 인형놀이 → `playing with dolls`  
  - 레고 → `building blocks / LEGO`  
  - 게임 → `playing games`

- 패턴:
  - `I like drawing.`
  - `I like playing with dolls.`

- Luna (EN)  
  > “I like drawing.  
  > I like games.  
  > What do you like?”

---

#### T5. 루나의 “기억” & 친밀감 장치

- Popo (KR)  
  > “루나가 이렇게 정리했대.  
  > ‘[이름]이는 [동물], [음식], [놀이]를 좋아한다!’  
  > 나중에 또 놀 때 이걸 기억해준대.”

- Luna (EN)  
  > “[Name] likes [cat], [pizza], and [drawing].  
  > I like that, too!”

---

#### T6. 마무리 (R4)

- Closing ritual로 마무리, “취향 조사 미션 완료”.

---

## 3. W1_S3: My Room & My Home (내 방 & 우리 집)

### 3.1 세션 메타

- 세션 코드: `W1_S3_my_room_home`

**목표**

- 내 방 / 우리 집에 대한 안전한 수준의 정보 공유  
- “내 공간” 관련 단어/표현 도입  
- 향후 세션 컨텍스트 수집

**언어 목표**

- 단어: `bed, toy, doll, desk, window, home, family, mom, dad, baby, grandma…`  
- 패턴:
  - `This is my room.`  
  - `I have a [toy].`  
  - `I live with my [mom / dad / family].`

**정서 목표**

- “내 공간을 보여준다”는 행위로 친밀감 강화  
- 사생활 침해 없이 안정감 있는 묘사

**주의**

- 주소, 학교 이름 등은 묻지 않음

---

### 3.2 세션 플로우

#### T0. Relationship Layer (R0~R3)

- Popo (KR)  
  > “우리 집 이야기를 할 건데,  
  > 집 주소 같은 건 말 안 해도 돼.  
  > 그냥 ‘내 방에 이런 게 있어요’ 정도만 이야기해보자.”

---

#### T1. 내 방(My Room) = Captain's Base Camp

- Popo (KR)  
  > “루나가 안전하게 지구에 머물려면, 대원님의 기지(Base Camp)인 방을 알아야 해.  
  > [이름]이 방에는 뭐가 있어? 침대? 책상? 인형?”

- 아이가 한국어로 나열 → `room_items` 리스트  
- EN 매핑: `bed, desk, doll, toy, book` 등

- 패턴: `I have a [doll].`

- Luna (EN)  
  > “I have a bed.  
  > I have a toy.”

- TaskAttempt: `T_W1_S3_room_have`

---

#### T2. 가장 좋아하는 물건 1개 포커스

- Popo (KR)  
  > “방에 있는 것 중에서 제일 좋아하는 것 하나만 골라줄래?”

- 선택값 → `favorite_room_item`  
- 패턴:
  - `This is my [doll].`  
  - `I like my [doll].`

---

#### T3. 우리 집 (Home) 구성원

- Popo (KR)  
  > “[이름]이는 누구랑 같이 살아? 엄마, 아빠, 동생, 할머니…?”

- 한국어 → EN 매핑:
  - `mom, dad, baby brother/sister, grandma, grandpa, family`

- 패턴:
  - `I live with my mom and dad.`  
  - 길면 `mom, dad`만 말해도 OK

- Luna (EN)  
  > “I live with my friends in space.  
  > You live with your family.”

---

#### T4. 집 형태 (집/아파트 정도)

- Popo (KR)  
  > “우리 집은 아파트야? 집이야?”

- EN 패턴(선택):
  - `I live in an apartment.`

- 부담 크면 스킵 가능.

---

#### T5. 친밀감 장치: “루나의 그림 상상”

- Popo (KR)  
  > “루나가 지금 머릿속에서 [이름]이 방을 상상하고 있대.  
  > 침대가 여기 있고, 인형이 여기 있고… 나중에 루나가 그림으로 그려주고 싶대.”

- Luna (EN)  
  > “I imagine your room.  
  > Bed… here. Toys… here.  
  > It is very cute.”

---

#### T6. 마무리 (R4)

- “방 + 집 정보 등록 완료” 요약 후 Closing ritual.

---

## 4. W1_S4: My Day / What I Do (일상 루틴)

### 4.1 세션 메타

- 세션 코드: `W1_S4_my_day_routine`

**목표**

- 아침~저녁 하루 루틴을 간단한 영어 문장으로 표현  
- 실제 루틴 정보를 수집해 이후 세션/리포트에 활용

**언어 목표**

- 기본 동사: `wake up, eat breakfast/dinner, go to school, stay home, play, draw, watch TV, read a book, sleep, go to bed`  
- 패턴:
  - `I wake up.`  
  - `I eat breakfast.`  
  - `I go to school.` / `I stay home.`  
  - `I play.` / `I draw.` / `I watch TV.` / `I read a book.`  
  - `I eat dinner.`  
  - `I sleep.` / `I go to bed.`

**정서 목표**

- “루나가 내 하루를 진짜 궁금해한다”는 느낌  
- 말이 막혀도 Popo가 대신 정리해준다는 안전감

---

### 4.2 세션 플로우

#### T0. Relationship Layer (R0~R3)

- Popo (KR)  
  > “이제 마지막 미션이야.  
  > [이름]이 하루를 루나에게 알려주는 ‘지구 대원 하루 리포트’!”

---

#### T1. 컨텍스트 세팅

- Popo (KR)  
  > “아침, 낮, 저녁으로 나눠서 천천히 물어볼게.  
  > 기억나는 만큼만 말해줘도 돼.”

- Luna (EN)  
  > “In the morning… what do you do?  
  > In the afternoon… what do you do?  
  > At night… what do you do?”

---

#### T2. Morning Routine – “I wake up / I eat breakfast”

- Popo (KR)  
  > “보통 아침에 일어나서 뭘 해? 눈 뜨고, 얼굴 씻고, 밥 먹고…?”

- 패턴:
  - `I wake up.`  
  - `I eat breakfast.`

- Luna (EN)  
  > “I wake up.  
  > I eat breakfast.”

- 둘 다 힘들면 한 문장만 성공해도 충분.

---

#### T3. Daytime – 학교/유치원 + 오후 놀이

- Popo (KR)  
  > “아침밥 먹고 나서 어디 가? 학교? 유치원? 아니면 집에 있어?”

- EN 패턴:
  - `I go to school.`  
  - `I stay home.`

- 오후 활동 질문 후 EN 매핑:
  - `play, draw, watch TV, read a book`  
- 패턴:
  - `I play.` / `I draw.` / `I watch TV.` / `I read a book.`

---

#### T4. Evening & Night – “I eat dinner / I sleep”

- Popo (KR)  
  > “저녁에는 뭐 해? 가족이랑 밥 먹고, TV 보거나, 책 읽고 자?”

- 패턴:
  - `I eat dinner.`  
  - `I sleep.` / `I go to bed.`

- Luna (EN)  
  > “I eat dinner.  
  > I sleep.  
  > I go to bed.”

---

#### T5. Time Sync: "Earth Time vs Space Time"

- Luna (EN)  
  > “Wait… In space, I sleep all day.  
  > Captain [Name] sleeps at night?  
  > Let me check… First sleep, then eat? Or eat, then sleep?”

- Popo (KR)  
  > “루나가 지구 시간(Earth Time)이랑 우주 시간이 헷갈리나 봐!  
  > [이름]이가 순서를 다시 알려줄래?  
  > 일어나서(Wake up) 밥을 먹는 거야, 아니면 자고 나서(Sleep) 먹는 거야?”

- 아이가 순서를 바로잡아 주면 성공 (English or Korean is okay, but encourage `Wake up` -> `Eat`)
- Luna (EN)
  > "Aha! Wake up first! Thank you, Captain."

---

#### T6. 마무리 & W1 전체 요약 (R4)

- Popo (KR)  
  > “이제 루나는  
  > - [이름]이 이름, 나이  
  > - 좋아하는 동물/음식/놀이  
  > - 방과 집에 뭐가 있는지  
  > - 하루를 어떻게 보내는지  
  > 전부 알게 됐어!”

- Luna (EN)  
  > “Captain [Name], thank you.  
  > Now I know your day on Earth.  
  > Your day is very special.”

- Closing ritual: “Earth crew, mission complete!” ✊
