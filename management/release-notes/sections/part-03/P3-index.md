# Section Release Note

- Section ID: `P3-index`
- Source File: `docs/parts/part-03/index.md`

### v2026.07.08

- 변경 이유: Chapter 5와 6이 실제 본문에서는 `원시 로그 재구성`, `특징 설계`로만 읽혀, 기준 계획서가 요구한 `수치형/범주형 탐색`, `변수변환/특징 선택` 관점이 장 단위에서 덜 선명하게 보였다.
- 본문 반영: 전체 흐름 문단에 Chapter 5의 수치형/범주형 탐색과 Chapter 6의 변수변환/특징 선택을 직접 적고, Part 3 요약 표의 해당 행도 같은 관점이 드러나게 다시 정리했다.
- 번역 동기화 메모: preserve that Chapter 5 now explicitly frames raw-log restructuring as numerical and categorical exploration, and Chapter 6 as variable transformation plus feature selection. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.08`

- 변경 이유: Part 시작 페이지가 오버뷰보다 `Part 4·5 인계 설계`를 반복해, 독자용 안내보다 집필 설계 메모처럼 읽히는 문제가 남아 있었다.
- 본문 반영: 뒤 Part 인계 문장을 줄이고, Part 3의 목적, 범위, 9개 Chapter 흐름, 현재 Part에서 닫는 문제 구조를 중심으로 다시 정리했다. 마지막 Chapter와 요약 표의 명칭도 `문제 유형 구분`과 `입력/결과 경계` 중심으로 조정했다.
- 번역 동기화 메모: keep the overview centered on Part 3's scope and flow, with only a brief high-level bridge to later learning sections. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.08`

### v2026.07.07-32

- 변경 이유: Part 3 시작 페이지가 반복 질문 축과 뒤 Part 연결을 지나치게 길게 나열해, 오버뷰보다 설계 메모처럼 읽히는 문제가 남아 있었다.
- 본문 반영: 도입부와 전체 흐름 설명에서 중복되는 설계 문단을 줄이고, 긴 질문 축 나열을 핵심 묶음으로 압축했다. 말미의 `짧은 점검`은 제거하고, Part 4·5 연결 설명도 입력 구조와 문제 경계를 닫는 수준으로 간소화했다.
- 번역 동기화 메모: preserve the shorter overview that groups recurring questions into a few modeling axes and keeps the Part 4/5 handoff at a high-level summary only. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-31

- 변경 이유: Chapter 10을 별도 인계 장으로 유지하지 않고 Chapter 5, 8, 9에 흡수하는 권장안을 실제 Part 3 구조에 반영할 필요가 있었다.
- 본문 반영: Part 3 시작 페이지의 전체 흐름을 `10개 Chapter`에서 `9개 Chapter` 구조로 다시 정리했다. 마지막 흐름도 `Chapter 9 안에서 문제 유형 구분과 뒤 Part 연결을 함께 닫는 구조`로 바꾸고, 관련 요약 표와 짧은 점검 문구도 함께 조정했다.
- 번역 동기화 메모: preserve that the overview now treats later-part handoff as absorbed into Chapter 9 rather than as a standalone Chapter 10. / pending
- 번역 반영 상태: not-started
- 관련 자산: `docs/book/table-of-contents.md`, `mkdocs.yml`
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-30

- 변경 이유: 새 Section `P3-10.28`이 추가되면서, Part 3 시작 페이지에도 상위 N건 선별이나 목록 순서처럼 `순위 자체가 목표인 문제`를 분류/회귀와 구분해 적어야 한다는 판단이 Part 4·5 인계 전제의 일부라는 점을 직접 회수할 필요가 생겼다.
- 본문 반영: 도입부와 전체 흐름 설명에 `ranking 메모` 관점을 추가하고, Chapter 요약 표와 반복 질문 축에 `ranking 목적 메모`, `실제 목표가 상위 몇 건 선별이나 목록 순서 최적화인지`를 반영했다.
- 번역 동기화 메모: preserve that the overview now includes ranking-purpose distinction from classification/regression as part of the Part 3 handoff structure before later model-selection and score-reading work. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-29

- 변경 이유: 새 Section `P3-10.27`이 추가되면서, Part 3 시작 페이지에도 숫자 target이 보이는 문제에서 `연속값 자체를 맞히는 구조`와 `숫자를 잘라 만든 분류 구조`를 함께 적어야 한다는 판단이 Part 4·5 인계 전제의 일부라는 점을 직접 회수할 필요가 생겼다.
- 본문 반영: 도입부와 전체 흐름 설명에 `문제 유형 메모` 관점을 추가하고, Chapter 요약 표와 반복 질문 축에 `regression 가능성 메모`, `숫자 target이 보일 때 원래는 연속값을 맞히는 문제인지 숫자를 잘라 만든 class인지`를 반영했다.
- 번역 동기화 메모: preserve that the overview now includes the distinction between regression targets and discretized classification targets as part of the Part 3 handoff structure before later output/metric reading. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-28

- 변경 이유: 새 Section `P3-10.26`이 추가되면서, Part 3 시작 페이지에도 범주가 여러 개 보이는 문제에서 `정확히 하나를 고르는 구조`와 `여러 라벨이 동시에 가능한 구조`를 함께 적어야 한다는 판단이 Part 4·5 인계 전제의 일부라는 점을 직접 회수할 필요가 생겼다.
- 본문 반영: 도입부와 전체 흐름 설명에 `target 구조` 관점을 추가하고, Chapter 요약 표와 반복 질문 축에 `target 구조 메모`, `범주가 여러 개 보일 때 정답이 정확히 하나인지 여러 라벨이 동시에 가능한가`를 반영했다.
- 번역 동기화 메모: preserve that the overview now includes target-structure distinction between single-label and multilabel cases as part of the Part 3 handoff structure before later output/loss reading. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-27

- 변경 이유: 새 Section `P3-10.25`가 추가되면서, Part 3 시작 페이지에도 binary target과 실제 행동 갈래 수의 차이를 함께 적어야 한다는 판단이 Part 4·5 인계 전제의 일부라는 점을 직접 회수할 필요가 생겼다.
- 본문 반영: 도입부와 전체 흐름 설명에 `행동 흐름 구조` 관점을 추가하고, Chapter 요약 표와 반복 질문 축에 `실제 행동 갈래 메모`, `binary target이 실제로는 몇 갈래 행동으로 연결되는가`를 반영했다.
- 번역 동기화 메모: preserve that the overview now includes the gap between a binary target and a multi-branch operational flow as part of the Part 3 handoff structure before later threshold reading. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-26

- 변경 이유: 새 Section `P3-10.24`가 추가되면서, Part 3 시작 페이지에도 점수를 순위용으로 쓰는지 확률처럼 읽는지를 함께 적어야 한다는 판단이 Part 4·5 인계 전제의 일부라는 점을 직접 회수할 필요가 생겼다.
- 본문 반영: 도입부와 전체 흐름 설명에 `점수 해석 구조` 관점을 추가하고, Chapter 요약 표와 반복 질문 축에 `점수 해석 메모`, `모델 점수를 순위용으로 쓰는가 확률처럼 읽는가`를 반영했다.
- 번역 동기화 메모: preserve that the overview now includes score-meaning interpretation as part of the Part 3 handoff structure before later threshold and calibration reading. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-25

- 변경 이유: 새 Section `P3-10.23`이 추가되면서, Part 3 시작 페이지에도 같은 target 아래에서 어떤 오류가 더 아픈지를 함께 적어야 한다는 판단이 Part 4·5 인계 전제의 일부라는 점을 직접 회수할 필요가 생겼다.
- 본문 반영: 도입부와 전체 흐름 설명에 `오류 비용 구조` 관점을 추가하고, Chapter 요약 표와 반복 질문 축에 `오류 비용 메모`, `같은 target 아래에서 어떤 오류가 더 아픈가`를 반영했다.
- 번역 동기화 메모: preserve that the overview now includes asymmetric error costs under the same target as part of the Part 3 handoff structure before later metric and threshold interpretation. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-24

- 변경 이유: 새 Section `P3-10.22`가 추가되면서, Part 3 시작 페이지에도 현재 개입이 이후 데이터와 라벨을 바꾸는 범위를 함께 적어야 한다는 판단이 Part 4·5 인계 전제의 일부라는 점을 직접 회수할 필요가 생겼다.
- 본문 반영: 도입부와 전체 흐름 설명에 `현재 개입이 이후 데이터를 바꾸는 범위` 관점을 추가하고, Chapter 요약 표와 반복 질문 축에 `현재 개입이 바꾼 후속 데이터 메모`, `현재의 규칙과 조치가 이후 데이터 자체를 바꿨는가`를 반영했다.
- 번역 동기화 메모: preserve that the overview now includes intervention-altered follow-up data as part of the Part 3 handoff structure before later evaluation and sequence-model interpretation. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-23

- 변경 이유: 새 Section `P3-10.21`이 추가되면서, Part 3 시작 페이지에도 확정 라벨이 어떤 사례 집합에만 붙었는지와 그 관측 범위를 함께 적어야 한다는 판단이 Part 4·5 인계 전제의 일부라는 점을 직접 회수할 필요가 생겼다.
- 본문 반영: 도입부와 전체 흐름 설명에 `라벨이 붙은 사례 집합의 범위` 관점을 추가하고, Chapter 요약 표와 반복 질문 축에 `선택적으로 붙은 라벨 메모`, `확정 라벨이 어떤 사례에만 붙었는가`를 반영했다.
- 번역 동기화 메모: preserve that the overview now includes selectively observed confirmed labels as part of the Part 3 handoff structure before later evaluation and sequence-model interpretation. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-22

- 변경 이유: 새 Section `P3-10.20`이 추가되면서, Part 3 시작 페이지에도 실제 목표와 대리 target(proxy target)의 차이를 함께 적어야 한다는 판단이 Part 4·5 인계 전제의 일부라는 점을 직접 회수할 필요가 생겼다.
- 본문 반영: 도입부와 전체 흐름 설명에 `실제 목표와 대리 target의 관계` 관점을 추가하고, Chapter 요약 표와 반복 질문 축에 `실제 목표와 대리 target 메모`, `지금 쓰는 target이 실제 목표 자체인가 아니면 대신 쓰는 대리 target인가`를 반영했다.
- 번역 동기화 메모: preserve that the overview now includes the true-goal versus proxy-target distinction as part of the Part 3 handoff structure before later evaluation and sequence-model interpretation. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-21

- 변경 이유: 새 Section `P3-10.19`가 추가되면서, Part 3 시작 페이지에도 같은 target 이름이라도 판정 기준과 상태 체계가 바뀌면 정의 버전을 함께 남겨야 한다는 판단이 Part 4·5 인계 전제의 일부라는 점을 직접 회수할 필요가 생겼다.
- 본문 반영: 도입부와 전체 흐름 설명에 `target 정의 버전` 관점을 추가하고, Chapter 요약 표와 반복 질문 축에 `target 정의 버전 메모`, `같은 target 이름을 계속 써도 판정 기준과 상태 체계가 정말 같은가`를 반영했다.
- 번역 동기화 메모: preserve that the overview now includes target-definition versioning as part of the Part 3 handoff structure before later evaluation and sequence-model interpretation. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-20

- 변경 이유: 새 Section `P3-10.18`이 추가되면서, Part 3 시작 페이지에도 겹치는 입력 창이 많을 때 창 수와 실제 정보 다양성을 같은 뜻으로 읽지 않는 판단이 Part 4·5 인계 전제의 일부라는 점을 직접 회수할 필요가 생겼다.
- 본문 반영: Chapter 요약 표의 `Part 4·5 인계` 결과 구조와 반복 질문 축에 `창 겹침 메모`, `겹치는 입력 창이 많을 때 창 수가 실제 사건 수보다 얼마나 부풀어 보이는가`를 반영했다.
- 번역 동기화 메모: preserve that the overview now includes overlapping-window caution as part of the Part 3 handoff structure before later sequence-model details. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-19

- 변경 이유: 새 Section `P3-10.17`이 추가되면서, Part 3 시작 페이지에도 여러 목표 라벨 후보 중 무엇을 먼저 대표 target으로 세우는지가 Part 4·5 인계 전제의 일부라는 점을 직접 회수할 필요가 생겼다.
- 본문 반영: Chapter 요약 표의 `Part 4·5 인계` 결과 구조와 반복 질문 축에 `대표 target 선택 메모`, `여러 target 후보가 있으면 무엇을 먼저 대표 목표로 세우는가`를 반영했다.
- 번역 동기화 메모: preserve that the overview now includes representative-target selection as part of the Part 3 handoff structure before later training/evaluation details. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-18

- 변경 이유: 새 Section `P3-10.16`이 추가되면서, Part 3 시작 페이지에도 후속 사건이 여러 개인 문제에서 정답 1건을 어떤 규칙으로 접었는지가 Part 4·5 인계 전제의 일부라는 점을 직접 회수할 필요가 생겼다.
- 본문 반영: Chapter 요약 표의 `Part 4·5 인계` 결과 구조와 반복 질문 축에 `후속 사건 집계 규칙 메모`, `여러 후속 사건이 있을 때 어떤 하나를 target으로 접는가`를 반영했다.
- 번역 동기화 메모: preserve that the overview now includes follow-up event aggregation rules as part of the Part 3 handoff structure before later training/evaluation details. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-17

- 변경 이유: 새 Section `P3-10.15`가 추가되면서, Part 3 시작 페이지에도 목표 라벨의 확정 시점뿐 아니라 음성 0 라벨을 붙일 만큼 충분히 관측했는지까지 Part 4·5 인계 전제의 일부라는 점을 직접 회수할 필요가 생겼다.
- 본문 반영: Chapter 요약 표의 `Part 4·5 인계` 결과 구조와 반복 질문 축에 `음성 라벨 닫힘 조건 메모`, `0 라벨을 붙일 만큼 충분히 끝까지 관측했는가`를 반영했다.
- 번역 동기화 메모: preserve that the overview now includes closed-negative conditions as part of the Part 3 handoff structure before later evaluation details. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-16

- 변경 이유: 새 Section `P3-10.14`가 추가되면서, Part 3 시작 페이지에도 목표 라벨 후보의 존재와 의미 안정성뿐 아니라 라벨이 언제 정답으로 확정되는지까지 Part 4·5 인계 전제의 일부라는 점을 직접 회수할 필요가 생겼다.
- 본문 반영: Chapter 요약 표의 `Part 4·5 인계` 결과 구조와 반복 질문 축에 `라벨 확정 시점 메모`, `목표 라벨은 보통 언제 정답으로 확정되는가`를 반영했다.
- 번역 동기화 메모: preserve that the overview now includes label-confirmation timing as part of the Part 3 handoff structure before later training/evaluation details. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-15

- 변경 이유: 새 Section `P3-9.6`이 추가되면서, Part 3 시작 페이지에도 목표 라벨 후보의 존재뿐 아니라 라벨 의미의 일관성 점검이 문제 유형 구분과 Part 4·5 인계 사이의 흐름이라는 점을 직접 회수할 필요가 생겼다.
- 본문 반영: Part 3 전체 흐름 설명, Chapter 요약 표, 반복 질문 축에 `라벨 후보 일관성 메모`, `라벨 의미 안정성 메모`, `같은 사건과 비슷한 조건에서 비슷한 라벨이 붙는가`를 반영했다.
- 번역 동기화 메모: preserve that the overview now includes target-label consistency and meaning stability as part of the Part 3 handoff preparation before later training/evaluation details. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-14

- 변경 이유: 새 Section `P3-10.13`이 추가되면서, Part 3 시작 페이지에도 개체 분리 분할 필요 여부가 Part 4·5 인계 전제의 일부라는 점을 직접 회수할 필요가 생겼다.
- 본문 반영: Chapter 요약 표의 `Part 4·5 인계` 결과 구조에 `개체 분리 분할 필요 여부`를 추가하고, 반복 질문 축에 `같은 개체를 train/test 양쪽에 두지 말아야 하는가`를 반영했다.
- 번역 동기화 메모: preserve that the overview now includes entity/group split necessity as part of Chapter 10 handoff work before later evaluation details. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-13

- 변경 이유: 새 Section `P3-10.12`가 추가되면서, Part 3 시작 페이지에도 시간 순서 분할 필요 여부가 Part 4·5 인계 전제의 일부라는 점을 직접 회수할 필요가 생겼다.
- 본문 반영: Chapter 요약 표의 `Part 4·5 인계` 결과 구조에 `시간 순서 분할 필요 여부`를 추가하고, 반복 질문 축에 `이 문제가 무작위 분할보다 시간 순서 분할을 먼저 요구하는가`를 반영했다.
- 번역 동기화 메모: preserve that the overview now includes chronological-split necessity as part of the Chapter 10 handoff work before later evaluation details. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-12

- 변경 이유: 새 Section `P3-4.5`가 추가되면서, Part 3 시작 페이지에도 샘플 단위 정의와 별도로 `샘플 묶음의 대표성 범위`를 확인하는 질문이 전체 흐름의 일부라는 점을 직접 회수할 필요가 생겼다.
- 본문 반영: Chapter 요약 표의 `샘플과 표 구조 정하기` 결과 구조에 `대표성 범위 메모`를 추가하고, 반복 질문 축에 `지금 모은 샘플이 전체 운영 범위를 얼마나 대표하는가`를 반영했다.
- 번역 동기화 메모: preserve that the overview now includes sample-set representativeness as part of Chapter 4 modeling work before later evaluation and generalization. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-11

- 변경 이유: 새 Section `P3-6.6`이 추가되면서, Part 3 시작 페이지에도 단위·센서 버전·계산 규칙이 달라진 열을 같은 특징처럼 섞지 않는 판단이 특징 설계 단계의 일부라는 점을 직접 회수할 필요가 생겼다.
- 본문 반영: Chapter 요약 표의 `특징 설계` 결과 구조에 `특징 정의 일치 점검`을 추가하고, 반복 질문 축에 `같은 열 이름이라도 단위·버전·계산 규칙이 같아 정말 같은 특징인가`라는 질문을 반영했다.
- 번역 동기화 메모: preserve that the overview now includes feature-definition consistency checks as part of Chapter 6 modeling work. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-10

- 변경 이유: 새 Section `P3-5.5`가 추가되면서, Part 3 시작 페이지에도 값 누락과 샘플 구조 붕괴를 같은 빈칸으로 읽지 않는 판단이 원시 로그 재구성 단계의 일부라는 점을 직접 회수할 필요가 생겼다.
- 본문 반영: Chapter 요약 표의 `원시 로그 재구성` 결과 구조에 `누락/샘플 붕괴 구분`을 추가하고, 반복 질문 축에 `값이 빠지거나 구간이 비었을 때 이 샘플이 아직 같은 비교 단위인가`라는 질문을 반영했다.
- 번역 동기화 메모: preserve that the overview now includes distinguishing missing values from broken sample structure as part of Chapter 5 modeling work. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-9

- 변경 이유: 새 Section `P3-10.11`이 추가되면서, Part 3 시작 페이지에도 목표 라벨 후보의 희귀성과 시간·조건 편중을 인계 전제의 일부로 직접 회수할 필요가 생겼다.
- 본문 반영: Chapter 요약 표의 마지막 행과 반복 질문 축에 `목표 분포 경고`를 반영했다. 이를 통해 Part 3의 마지막 인계가 feature/target 분리뿐 아니라 target 분포 특성 메모까지 포함한다는 점이 시작 페이지에서도 읽히게 했다.
- 번역 동기화 메모: preserve that the overview now treats target rarity and skew as part of the Part 4/5 handoff, not only as a later metrics detail. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-8

- 변경 이유: Part 3의 실제 Chapter 10 보강 범위는 이미 Part 4와 Part 5 공통 인계 구조까지 넓어졌는데, 시작 페이지 일부 표기와 점검 문장은 아직 `Part 4 인계` 중심으로 남아 있었다.
- 본문 반영: 읽는 순서 10단계, Chapter 요약 표의 마지막 행, 파이프라인 도식의 마지막 노드, 짧은 점검 질문을 `Part 4·5 인계` 기준으로 갱신했다. 이에 따라 Part 3 끝의 인계가 표 데이터 입력과 시계열 입력 갈림길까지 포함한다는 점이 시작 페이지에서도 직접 읽히게 했다.
- 번역 동기화 메모: preserve that the overview now frames Chapter 10 as a shared handoff to both Part 4 and Part 5, including the split between tabular and sequence-shaped inputs. / pending
- 번역 반영 상태: not-started
- 관련 자산: `docs/book/table-of-contents.md`, `mkdocs.yml`
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-7

- 변경 이유: 새 Section `P3-9.5`가 추가되면서, Part 3 시작 페이지에도 비교 리포트, 검토 후보 큐, 목표 라벨 후보 표를 가로질러 같은 사건을 어떻게 추적하는지가 전체 흐름의 일부라는 점을 직접 회수할 필요가 생겼다.
- 본문 반영: Part 3 전체 흐름 설명, Chapter 요약 표, 반복 질문 축에 산출물 간 `같은 사건 추적 기준`과 `근거 추적 가능성`을 반영했다. 이를 통해 문제 유형 구분과 Part 4 인계 사이에 사건 정체성과 근거 연결을 유지하는 단계가 시작 페이지에서도 읽히게 했다.
- 번역 동기화 메모: keep the overview explicit that traceability across the report, review-queue, and target-candidate artifacts is now part of the Part 3 flow before handoff. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-6

- 변경 이유: 새 Section `P3-6.5`와 `P3-8.5`가 추가되면서, Part 3 시작 페이지에도 특징의 단위/역할 구분과 여러 비교 열을 검토 우선순위 후보 축으로 묶는 단계가 현재 전체 흐름의 일부라는 점을 직접 회수할 필요가 생겼다.
- 본문 반영: Part 3 전체 흐름 설명, Chapter 요약 표, 반복 질문 축에 `단위와 구조 역할 구분`과 `변화 크기·반복성·해석 신뢰도·운영 중요도` 기반 우선순위 후보 묶음을 반영했다. 이를 통해 특징 설계 뒤와 구조화된 운영 출력 앞 사이의 중간 판단이 시작 페이지에서도 읽히게 했다.
- 번역 동기화 메모: keep the overview explicit that feature-role/unit reading and grouped review-priority axes are now part of the Part 3 flow, not deferred entirely to later Parts. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-5

- 변경 이유: Part 3 시작 페이지가 최근 추가된 `열 역할 구분`과 `보수적 해석 문장을 구조화된 운영 출력으로 바꾸는 단계`를 아직 충분히 안내하지 못하고 있었다.
- 본문 반영: Part 3 전체 흐름 설명에 식별 열·비교 열·목표 후보 열의 역할 분리와 `warning_level`, `review_needed`, `priority_score` 같은 운영 출력 초안 단계를 추가했다. Chapter 요약 표와 반복 질문 축에도 이 연결을 반영해, Part 4 인계가 단순 feature/label 정리가 아니라 운영 출력과 학습 목표의 경계를 가르는 작업임을 더 분명히 했다.
- 번역 동기화 메모: keep the Part 3 overview explicit about column-role separation and the bridge from conservative prose to structured operational outputs before the Part 4 handoff. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-4

- 변경 이유: Part 3 보강 목적이 Part 4와 Part 5의 데이터 과학 이해 준비라는 점을 시작 페이지에서도 더 직접적으로 읽히게 할 필요가 있었다.
- 본문 반영: 도입부에 Part 3이 뒤 Part의 데이터 과학 전제를 맡는다는 연결 문단을 추가했다. `Part 3의 목적`, `왜 필요한가`, `이후 Part로의 연결`에도 Part 4를 표 데이터 중심 데이터 과학 절차로, Part 5를 시계열·표현 학습으로 확장된 데이터 과학 단계로 읽게 하는 설명을 보강했다.
- 번역 동기화 메모: keep the Part 3 overview explicit that it prepares the data-science understanding needed for both Part 4 and Part 5, not just generic model study. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-2

- 변경 이유: Part 3 시작 페이지에도 `이 Part` 중심 안내 문장이 남아 있어, 오버뷰를 Part 이름 기준의 직접 설명형으로 더 통일할 필요가 있었다.
- 본문 반영: 도입부와 목적·범위·연결 문단의 `이 Part` 표현 다수를 `Part 3`으로 바꾸고, 개요 페이지가 문제 구조 설계 Part라는 점이 바로 읽히도록 문장을 정리했다.
- 번역 동기화 메모: keep the Part 3 overview direct and consistently name the Part rather than relying on meta “this Part” guidance. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-3

- 변경 이유: Part 3 보강 목적이 Part 4뿐 아니라 Part 5 이해 전제까지 세우는 데 있다는 점을 시작 페이지에서도 더 직접적으로 드러낼 필요가 있었다.
- 본문 반영: `Part 3의 목적`과 `왜 필요한가`에 Part 5 시계열 딥러닝 입력 구조 전제를 추가했다. `이후 Part로의 연결`에는 RNN, CNN, Attention, Transformer를 읽기 전에 샘플 구간과 입력 구조를 먼저 정해야 한다는 연결 문단을 보강했다.
- 번역 동기화 메모: keep the Part 3 overview explicit that it prepares both Part 4 machine learning and Part 5 sequence/deep-learning input structure assumptions. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-1

- 변경 이유: Part 3 시작 페이지는 현재 10개 Chapter 구조와 짧은 점검까지 반영된 상태였지만, 표시 `Version`이 이전 날짜에 머물러 있어 메타데이터를 현재 작업 기준과 맞출 필요가 있었다.
- 본문 반영: 시작 페이지의 `Version`을 `v2026.07.07`로 갱신해 현재 Part 3 구조 개정 상태와 릴리즈노트 이력을 일치시켰다.
- 번역 동기화 메모: translation should update the displayed `P3-index` version together with the current ten-chapter overview baseline. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.07`

### v2026.07.06-5

- 변경 이유: Part 3 소개 페이지의 개념사전 연결 문장에 남아 있던 `...확인하면 됩니다` 표현을 직접 설명형으로 정리할 필요가 있었다.
- 본문 반영: 3.1과 3.2를 Part 내 최초 개념 설명 위치로 두고, 이후 용어 혼동 시 개념사전이 기준 참조점이 된다는 설명으로 연결 문장을 다듬었다.
- 번역 동기화 메모: keep the Part 3 overview’s glossary handoff declarative and aligned with the “first detailed explanation in-part” rule. / pending
- 번역 반영 상태: not-started
- 관련 자산: `docs/reference/concept-glossary.md`
- 원문 기준 버전: `v2026.07.06-5`

### v2026.07.06-1

- 변경 이유: Part 3 시작 페이지에 Section 메타데이터가 없었고, 도입부 일부가 `익히게 하려 합니다`, `기억할 필요가 있습니다`, `먼저 잡아 두면` 같은 안내형 표현으로 남아 있어 오버뷰 설명 자체를 더 직접적인 본문형으로 정리할 필요가 있었다.
- 본문 반영: `Section ID`, `Version` 메타데이터를 추가했다. / 데이터 정리, 특징 설계, 샘플링, 추론, 문제 구조화 소개 문장을 `차례로 확인합니다`로 조정했다. / `DSS/BI/DW/OLAP` 배경 축 설명과 반복 질문 축 소개 문장을 직접 진술형으로 다듬어 Part 3 오버뷰가 데이터 모델링 판단 구조를 바로 설명하도록 정리했다.
- 번역 동기화 메모: future translations should include explicit section metadata and keep the Part 3 overview in direct explanatory prose, especially around the DSS/BI/DW/OLAP background axis and the recurring question frame. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.06`

### v2026.07.06-2

- 변경 이유: Part 3 앞머리에 데이터 모델링 진입 챕터를 추가하면서, 개요 페이지의 읽는 순서와 단계 표도 새 구조를 먼저 반영해야 했다.
- 본문 반영: Part 3가 먼저 `무엇을 달성하려는가`와 `어떤 순서로 진행되는가`를 잡는다는 설명을 추가했다. 읽는 순서 목록과 단계 표에 개념 진입 단계를 새로 넣어 이후 Chapter 재배치와 맞추었다.
- 번역 동기화 메모: translation should reflect the new introductory chapter and keep the overview sequence aligned with the added concept-entry stage. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.06`

### v2026.07.06-3

- 변경 이유: Part 3 전체를 7개 Chapter 흐름으로 리팩터링하려는 기준이 세워졌으므로, 시작 페이지도 기존의 세부 장면 나열보다 `어떤 구조로 읽을 Part인가`를 먼저 보여 주도록 다시 정리할 필요가 있었다.
- 본문 반영: 주요 질문, 읽는 순서, 단계 표를 `역할과 범위 -> 데이터셋 후보 -> 샘플/표 구조 -> 특징 -> 비교 -> 해석 -> 인계`의 7단계 흐름 기준으로 재작성했다. 도입 문단도 세부 Chapter를 하나씩 나열하기보다 Part 3 전체 절차가 보이도록 정리했다.
- 번역 동기화 메모: translation should preserve the new seven-chapter reading map and the emphasis on Part 3 as a structured pre-learning design flow. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.06`

### v2026.07.06-4

- 변경 이유: Part 3 시작 페이지가 데이터 모델링, 샘플, 특징, 기준선 같은 핵심 용어를 다시 소개하면서도 어디서 큰 정의를 먼저 잡고 어디서 진행 순서를 읽어야 하는지 연결이 약했고, `샘플링` 표현도 Part 3 문맥에서는 `샘플 설계`와 섞여 읽힐 수 있었다.
- 본문 반영: 3.1에서 데이터 모델링의 큰 정의를, 3.2에서 진행 순서를 먼저 고정한 뒤 이후 Section는 최소 연결만 남긴다는 안내 문단을 추가했다. 또한 `샘플링(sampling)`은 `샘플 설계(sample design)`로 조정하고, 핵심 용어가 헷갈릴 때는 개념사전의 `중심 Section`과 `등장 Section`을 함께 보게 하는 링크를 보강했다.
- 번역 동기화 메모: translation should keep the stronger link from the Part 3 overview to sections 3.1 and 3.2, preserve the glossary back-reference, and avoid generic sampling wording where the text means sample design. / pending
- 번역 반영 상태: not-started
- 관련 자산: `docs/reference/concept-glossary.md`
- 원문 기준 버전: `v2026.07.06`

### v2026.07.06-6

- 변경 이유: Part 3 시작 페이지에 이전 7개 Chapter 기준 서술이 남아 있어, 현재 10개 Chapter 재구성 및 실제 본문 흐름과 맞지 않는 상태를 정리할 필요가 있었다.
- 본문 반영: `읽는 순서`와 Chapter 요약 표를 10개 Chapter 구조로 다시 맞추고, `원시 로그 재구성`, `문제 유형 구분`, `Part 4 인계`를 별도 단계로 분리해 현재 Part 구성을 정확히 반영했다. 끝에는 짧은 점검을 추가해 Part 3의 전체 파이프라인을 다시 확인하게 했다.
- 번역 동기화 메모: translation should reflect the updated ten-chapter structure and preserve the added self-check prompts about problem-expression flow and Part 4 handoff. / pending
- 번역 반영 상태: not-started
- 관련 자산: 없음.
- 원문 기준 버전: `v2026.07.06`
