# Part 5 Python 예제 점검 리포트

- 작성일: 2026-07-19
- 점검 범위: `docs/parts/part-05/` 한국어 본문 Section 53개, `docs/assets/part-05/` Python 자산 31개
- 기준 문서: `management/guidelines/python-example-guidelines.md`, `management/guidelines/manuscript-writing-workflow.md`, `management/guidelines/section-metadata-guidelines.md`

## 점검 목적

Part 5의 Python 예제가 딥러닝 개념을 실제 입력 변화, 가중치 변화, 임계값 변화, attention weight 변화, sampling weight 변화로 확인하게 하는지 점검했다. 특히 고정 답안 출력, 검색 결과나 후보 목록이 이미 라벨로 들어 있고 코드는 집계만 하는 경우, 표나 사례가 더 적합한데 코드가 다시 출력만 하는 경우를 집중적으로 확인했다.

Part 5는 신경망, 활성화 함수, 손실, 역전파, 학습 루프, CNN, RNN, attention, Transformer, 생성과 sampling의 감각을 다루므로 작은 수치 실험이 많다. 이 파트의 예제는 대부분 실제 프레임워크 학습 코드보다 입문용 축약 계산이지만, `bias`, `threshold`, `learning_rate`, `dropout mask`, `decay`, `attention score`, `head weight`, `sampling weight` 등을 바꾸면 출력이 달라지는 구조를 갖고 있어 실험형으로 유지할 수 있다고 판단했다.

## 수량 점검

| 항목 | 결과 |
| --- | ---: |
| 한국어 본문 Section 수 | 53 |
| Python 코드 블록 수 | 38 |
| Python 코드 블록이 있는 Section 수 | 36 |
| Part 5 Python 자산 수 | 31 |
| 표·사례로 대체한 본문 코드 블록 수 | 0 |

## 판정 요약

| 판정 | 범위 | 처리 |
| --- | --- | --- |
| 실험형 유지 | P5-1.2, P5-2.1, P5-2.2, P5-3.5, P5-4, P5-5, P5-6, P5-7, P5-8, P5-9, P5-10, P5-11, P5-12, P5-13, P5-14, P5-15 | 입력, 가중치, 편향, 임계값, 손실, gradient, learning rate, attention/sampling weight를 바꾸면 출력이 달라져 유지 |
| 본문 대체 없음 | 검색 후보·고정 라벨 재출력 패턴 | Part 5 본문에서는 표로 대체해야 할 고정 후보 목록 재출력 코드를 발견하지 못함 |
| 자산 보정 | P5-2.1, P5-2.2 Chapter 2 차트 스크립트 | 한글 폰트 후보와 Matplotlib 캐시 경로를 보강 |

## 유지한 대표 실험형 예제

| 범위 | 유지 이유 |
| --- | --- |
| P5-1.2 | `alarm_risk`, `bias`, `threshold` 조합을 바꾸면 선형 점수와 출력이 뒤집힘 |
| P5-2.1, P5-2.2 | 은닉층 조합, 출력층 편향, 내부 축 값이 달라지며 중간 표현과 최종 판단이 바뀜 |
| P5-4.1, P5-4.2 | 예측값이나 정답 확률을 바꾸면 평균 손실, worst case, 회귀/분류/생성 손실이 달라짐 |
| P5-5.1, P5-5.2 | `risk_weight`, ReLU gate 상태에 따라 gradient 방향과 전달 여부가 달라짐 |
| P5-6.1~P5-6.4 | batch, epoch, learning/inference mode, dropout, running mean 차이를 실행 결과로 확인함 |
| P5-7.1~P5-7.3 | learning rate와 update step이 손실 감소와 overshoot를 바꿈 |
| P5-11 | convolution, pooling, CNN/ViT 비교가 입력 행렬에서 지역 반응과 patch 요약을 계산함 |
| P5-12 | 순차 상태, decay, 직접 참조 방식이 긴 의존성 판단을 다르게 만듦 |
| P5-13, P5-14 | attention score, head weight, residual, FFN, layer norm이 context와 다음 계산 점수를 바꿈 |
| P5-15.2 | sampling weight가 후보 문장 분포, 선택 다양성, 평균 길이를 바꿈 |

## 자산 스크립트 점검

Part 5 Python 자산 31개를 실행했다. 전체 실행은 종료 코드 0으로 끝났지만, 두 가지 실행 품질 문제가 발견되어 보정했다.

| 파일 | 발견 사항 | 처리 |
| --- | --- | --- |
| `docs/assets/part-05/chapter-02/p5_2_1_hidden_pattern_regions.py` | 한국어 PNG 생성 시 DejaVu Sans 한글 글리프 누락 경고 발생 | 한국어 폰트 후보에 `Noto Sans CJK KR` 추가, 한국어 PNG 재생성 |
| `docs/assets/part-05/chapter-02/p5_2_2_hidden_axis_chart.py` | 사용자 홈의 Matplotlib 캐시 디렉터리에 쓸 수 없다는 경고 발생 | 저장소 내부 `.tmp/matplotlib-cache`를 `MPLCONFIGDIR`, `XDG_CACHE_HOME`으로 쓰도록 설정 |

두 스크립트는 보정 뒤 개별 재실행에서 경고 없이 종료됐다.

## 릴리즈노트 반영

| Section ID | 릴리즈노트 |
| --- | --- |
| `P5-2.1` | 은닉 패턴 영역 차트 스크립트의 한국어 폰트 후보 보강 |
| `P5-2.2` | 은닉축 차트 스크립트의 Matplotlib 캐시 경로 설정 보강 |

본문 Section은 수정하지 않았으므로 본문 Version 변경은 없었다. P5-2.1과 P5-2.2는 이미 `v2026.07.19` 상태였다.

## 검증 명령

```bash
find docs/parts/part-05 -name 'section-[0-9][0-9].md' | sort | wc -l
rg -n '^```python' docs/parts/part-05 -g 'section-[0-9][0-9].md' | wc -l
rg -n '^```python' docs/parts/part-05 -g 'section-[0-9][0-9].md' | cut -d: -f1 | sort -u | wc -l
find docs/assets/part-05 -name '*.py' | sort
for f in $(find docs/assets/part-05 -name '*.py' | sort); do .venv/bin/python "$f"; done
.venv/bin/python docs/assets/part-05/chapter-02/p5_2_1_hidden_pattern_regions.py
.venv/bin/python docs/assets/part-05/chapter-02/p5_2_2_hidden_axis_chart.py
```

## 남은 위험

Part 5는 딥러닝 내부 계산을 초심자용으로 압축해 보여 주기 때문에, 실제 학습 프레임워크 대신 작은 리스트, 배열, 수식 계산을 쓰는 예제가 많다. 이번 기준에서는 조작 변수와 관찰 출력이 분명해 유지했지만, 향후 목표가 `실제 프레임워크 기반 실습 확대`라면 P5-6 이후 일부 예제를 PyTorch 또는 NumPy 자산 파일 중심의 더 큰 실습으로 확장할 수 있다.

이번 점검 기준에서 즉시 표나 사례로 대체해야 할 본문 코드 블록은 없었다. 실행 검증 중 발견된 자산 스크립트 품질 문제 2건만 보정했다.
