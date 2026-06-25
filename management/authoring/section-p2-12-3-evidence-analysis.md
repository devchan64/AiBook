# P2-12.3 근거 검토: 학습용 데이터셋(dataset) 준비의 직관

## 사용한 주요 자료

| 자료 | 확인한 핵심 | 본문 반영 지점 |
| --- | --- | --- |
| pandas Developers, `pandas.get_dummies` | 범주형 변수를 dummy/indicator variables로 변환하는 함수로 설명한다. | 범주형 열은 바로 쓰기보다 표현을 바꿔야 할 수 있다는 설명 |
| scikit-learn Developers, `Glossary` | feature는 데이터 행렬에서 열(columns)로 표현되고, sample은 하나의 feature vector, target은 지도학습의 종속 변수로 설명한다. | `X`, `y`, sample, feature, target의 역할 구분 |
| scikit-learn Developers, `train_test_split` | 배열이나 행렬을 train/test subset으로 분리하는 도구로 설명한다. | 학습용 데이터 분리의 기본 직관 |
| scikit-learn Developers, `Common pitfalls and recommended practices` | inconsistent preprocessing과 data leakage를 경고하고, test data에 `fit`/`fit_transform`을 쓰지 말아야 함을 설명한다. | 분리 순서, 전처리 기준, 데이터 누수 경고 |

## 범위 판단

- P2-12.1은 DataFrame의 구조 이해에 집중했다.
- P2-12.2는 선택, 필터링, 집계, `groupby` 같은 표 조작 흐름에 집중했다.
- 따라서 P2-12.3은 `표를 모델 학습용 데이터셋으로 다시 읽는 기준`에 초점을 맞췄다.
- 결측치 세부 처리, 스케일링, 인코딩 비교, 파이프라인 구현, 교차검증 상세 절차는 이 절에서 깊게 다루지 않았다.

## 일반화 원칙

- `X`, `y` 표기는 scikit-learn 문맥에서 널리 쓰이는 표준 표기로 소개했다.
- sample / feature / target은 영어 병기를 유지해 이후 공식 문서와 연결되도록 했다.
- `get_dummies()`는 하나의 예시로만 언급하고, 인코딩 기법 비교 자체로 확장하지 않았다.
- `train`, `validation`, `test`는 엄밀한 실험 설계 전체가 아니라 초심자가 평가 왜곡을 피하기 위한 최소 구조로 설명했다.

## 조심한 지점

- “모든 문자열 열은 무조건 인코딩해야 한다”처럼 과도하게 단정하지 않았다.
- “식별자는 항상 쓸모없다”처럼 일반화하지 않고, 보통 제외 또는 재검토 대상이라는 수준으로 표현했다.
- data leakage는 구현 버그가 아니라 평가 구조의 문제라는 점을 강조했다.
- 이 절에서 모델 학습 코드, 파이프라인, 스케일링 공식을 길게 전개하지 않았다. 그 내용은 이후 Chapter와 Part의 범위다.

## 이 절의 핵심 정리

- P2-12.3의 중심 질문은 “표를 어떻게 학습용 데이터셋으로 다시 구성하는가?”다.
- 핵심 답은 `문제 정의 -> X/y 분리 -> train/validation/test 분리 -> train 기준으로만 전처리 학습`의 흐름이다.
- Pandas는 표 읽기와 점검, 열 선택, 기초 변환의 도구이고, 평가 구조의 공정성은 분리 순서와 학습 절차가 함께 결정한다.
