# Part 4 Python 예제 점검 리포트

- 작성일: 2026-07-19
- 점검 범위: `docs/parts/part-04/` 한국어 본문 Section 59개, `docs/assets/part-04/` Python 자산 1개
- 기준 문서: `management/guidelines/python-example-guidelines.md`, `management/guidelines/manuscript-writing-workflow.md`, `management/guidelines/section-metadata-guidelines.md`

## 점검 목적

Part 4의 Python 예제가 머신러닝 모델과 평가를 실제로 확인하게 하는지, 아니면 이미 정해진 점수표나 후보 목록을 코드가 다시 출력하는 데 그치는지 점검했다. 특히 모델 후보, 검증 점수, 테스트 점수, 일반화 gap, 평가 지표처럼 숫자가 이미 고정된 목록에서 `max`, 단순 출력, 단순 분류만 수행하는 블록은 실험형 예제로 보기 어렵기 때문에 표나 사례로 대체했다.

Part 4는 머신러닝 모델의 학습, 평가, 일반화, 분류기별 행동 차이를 다루므로 Python 예제가 중요한 파트다. 실제 `scikit-learn` 모델 학습, 데이터 분리, threshold 변화, 지표 계산, 트리 깊이·leaf·alpha 조정, KNN 거리 계산, PCA 복원 오차, 강화학습 업데이트처럼 입력이나 조작 변수를 바꾸면 출력이 달라지는 코드는 실험형으로 유지했다.

## 수량 점검

| 항목 | 결과 |
| --- | ---: |
| 한국어 본문 Section 수 | 59 |
| 점검 전 Python 코드 블록 수 | 88 |
| 수정 후 Python 코드 블록 수 | 79 |
| 수정 후 Python 코드 블록이 있는 Section 수 | 37 |
| Part 4 Python 자산 수 | 1 |

## 판정 요약

| 판정 | 범위 | 처리 |
| --- | --- | --- |
| 실험형 유지 | P4-4.1, P4-6.2, P4-8.3, P4-9, P4-10, P4-11, P4-12, P4-13, P4-14, P4-15, P4-16, P4-17, P4-18, P4-19의 실제 계산·모델 학습·임계값 변화 코드 | 입력, 모델 설정, threshold, `k`, tree depth, learning rate, reward sign 등을 바꾸면 출력이 달라지므로 유지 |
| 표 대체 | P4-4.2, P4-5.1, P4-5.2, P4-6.1, P4-19.5의 고정 점수·고정 기준 재출력 블록 | 이미 기록된 점수나 기준을 코드가 다시 출력하던 블록 9개를 표와 해석 문장으로 대체 |
| 자산 보정 | P4-11 로지스틱 회귀 차트 생성 스크립트 | Linux 검증 환경에서 한글/CJK 글리프 경고가 나지 않도록 Noto Sans CJK 폰트 후보 추가 |

## 수정 내역

### P4-4.2 검증과 테스트

검증 점수 후보표와 최종 테스트 점수는 이미 본문에서 해석해야 하는 실험 기록이었다. 기존 코드는 후보별 `validation_score`를 출력하고 가장 높은 후보를 고른 뒤 고정된 `test_score`를 출력했다. 또 조기 테스트 확인 예시는 이미 정해진 테스트 점수를 출력하고 `decision changed`라는 문장을 출력했다.

두 블록 모두 실제 모델 학습이나 점수 생성 없이 고정 기록을 다시 출력하는 형태였으므로 표로 대체했다. 검증은 후보 선택용, 테스트는 마지막 확인용이라는 역할 차이를 표 안에서 바로 읽도록 정리했다.

### P4-5.1 과적합과 과소적합

학습 점수와 검증 점수 조합을 출력하고 `gap`을 계산하던 두 블록을 표로 대체했다. `simple_rule`, `balanced_model`, `very_complex_model`처럼 이미 해석이 정해진 예시는 코드보다 표가 더 적합하다. 대체 표에서는 점수 수준, gap, 과소적합·적절한 상태·과적합 의심 해석을 한 번에 비교하게 했다.

### P4-5.2 일반화

일반화 gap과 표현 변화 점수 예시는 이미 고정된 점수 조합을 코드가 출력하던 형태였다. 두 블록을 표로 대체해, `차이가 작아도 둘 다 낮을 수 있음`, `새 표현에서 점수가 급락할 수 있음` 같은 해석을 직접 읽게 했다.

### P4-6.1 평가 지표

`model_A`, `model_B`의 accuracy, precision, recall이 이미 고정되어 있고 코드는 그대로 출력만 했다. 이 블록을 표로 바꾸어 같은 accuracy라도 놓침과 괜한 경보의 의미가 달라진다는 해석을 바로 보이게 했다.

### P4-19.5 벨만 방정식, 수렴, 함수 근사

상태 수가 작으면 Q-table, 크면 함수 근사라는 판단은 이미 기준이 정해진 설명형 분기였다. 코드가 기준을 재출력하는 대신, 벨만식 값은 같지만 상태 수가 커질수록 표현 방식이 달라진다는 점을 비교표로 정리했다.

### P4-11 차트 자산

`docs/assets/part-04/chapter-11/p4_11_logistic_charts.py`는 한국어·중국어 PNG를 생성하지만 폰트 후보에 Noto CJK가 없어 검증 환경에서 DejaVu Sans로 떨어지고 글리프 누락 경고가 발생했다. 한국어 후보에 `Noto Sans CJK KR`, 중국어 후보에 `Noto Sans CJK SC`를 추가하고 PNG를 재생성했다. 재실행 결과 경고 없이 종료됐다.

## 유지한 대표 실험형 예제

| 범위 | 유지 이유 |
| --- | --- |
| P4-4.1 데이터 분리 | `test_size`, `random_state`, 라벨 분포가 실제 출력에 영향을 줌 |
| P4-6.2 threshold 평가 | threshold를 바꾸면 TP/TN/FP/FN, precision, recall이 바뀜 |
| P4-9, P4-14, P4-15 | 실제 `scikit-learn` 모델을 학습하고 depth, leaf, alpha, tree 수 같은 조작 변수를 비교함 |
| P4-11.1, P4-11.2 | sigmoid 출력과 threshold 변화가 예측 경계를 바꿈 |
| P4-12 | 거리 계산, scale 적용, `k` 변화가 이웃 순서와 예측을 바꿈 |
| P4-16 | learning rate와 보정 단계 변화가 residual을 바꿈 |
| P4-17, P4-18 | 군집 알고리즘과 PCA가 실제 입력 배열에서 결과를 생성함 |
| P4-19.1, P4-19.2, P4-19.3 | 보상, 다음 행동, 할인율, 실패 비용이 업데이트나 정책 확률을 바꿈 |

## 검증 명령

```bash
find docs/parts/part-04 -name 'section-[0-9][0-9].md' | sort | wc -l
rg -n '^```python' docs/parts/part-04 -g 'section-[0-9][0-9].md' | wc -l
rg -n '^```python' docs/parts/part-04 -g 'section-[0-9][0-9].md' | cut -d: -f1 | sort -u | wc -l
find docs/assets/part-04 -name '*.py' | sort
.venv/bin/python docs/assets/part-04/chapter-11/p4_11_logistic_charts.py
```

## 남은 위험

Part 4에는 입문 독자를 위해 작은 리스트나 배열을 직접 넣은 코드가 많다. 이 중 일부는 실제 데이터셋 전체를 쓰는 실험은 아니지만, 지표 계산, threshold 변화, 거리 계산, 모델 설정 변화처럼 조작 변수와 관찰 출력이 분명하므로 현재 기준에서는 유지하는 것이 맞다.

다만 향후 목표가 `본문 안 장난감 데이터 최소화`로 바뀐다면, P4-6.3의 운영 지표 사례, P4-19.3의 보상 설계 사례처럼 작은 고정 데이터로 비용 함수를 계산하는 블록은 CSV 자산 또는 더 큰 실습으로 확장할 수 있다. 이번 점검 기준에서 즉시 수정이 필요했던 항목은 고정 점수·고정 기준 재출력 코드 9개였다.
