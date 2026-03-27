# 나의 스킬 페이지 분석

## 발견된 문제

### 1. 또래 평균 비교 차트가 보이지 않음
- 스크린샷에서 "또래 평균 비교" 제목은 있지만 차트가 표시되지 않음
- 빈 공간이 있는 것으로 보임
- Y축 레이블만 보이고 실제 바 차트가 렌더링되지 않음

### 2. 가능한 원인
- peerComparisonData의 데이터 구조 문제
- BarChart의 dataKey 매핑 문제
- ResponsiveContainer의 높이 설정 문제

## 해결 방법
1. peerComparisonData 확인 및 수정
2. BarChart의 XAxis/YAxis 설정 확인
3. 데이터 값이 제대로 표시되도록 수정
