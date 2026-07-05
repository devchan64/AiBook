# evidence-analysis 폐기 감사 메모

## 목적

- `management/authoring/section*-evidence-analysis.md` 문서를 일괄 폐기하지 않고, 섹션별로 대응 원고 반영 여부를 확인한 뒤에만 선별 삭제하기 위한 감사 메모입니다.
- 이 문서는 현재 워크트리 기준 검토 결과만 적습니다.

## 판정 기준

- `반영 확인`: 대응 원고의 본문 주장과 `## 출처와 참고 자료`에 evidence 문서의 핵심 출처와 핵심 정리가 실제로 보입니다.
- `보류`: 대응 원고 파일은 있으나, 핵심 출처와 본문 반영을 아직 수동으로 대조하지 못했습니다.
- `구조 불일치`: evidence 문서의 대상 섹션이 현재 원고 구조와 맞지 않거나, 대응 원고가 사라졌습니다.
- `삭제 완료`: `반영 확인`을 마친 뒤 워크트리에서 선별 삭제했습니다.

## 매핑 규칙

- `section-01`, `section-02`, `section-03` -> `docs/parts/part-01/chapter-01/section-01~03.md`
- `section-X-Y` -> `docs/parts/part-01/chapter-XX/section-YY.md`
- `section-p2-X-Y` -> `docs/parts/part-02/chapter-XX/section-YY.md`
- `section-p7-X-Y` -> `docs/parts/part-04/chapter-XX/section-YY.md`
- 예외:
  - `section-p7-3-3-evidence-analysis.md`는 현재 대응 원고 `docs/parts/part-04/chapter-03/section-03.md`가 없습니다.
  - `section-p7-19-evidence-analysis.md`는 현재 파일명만으로 대응 원고를 확정할 수 없고, 본문도 `P5-19` 기준 메모라 현 구조와 어긋납니다.
  - `section-p7-9-3-evidence-analysis.md`는 현재 대응 원고가 `P4-9.3` 고급 모델 선택 보충학습인데, evidence 본문은 `P5-9.3` LoRA 메모라 현 구조와 어긋납니다.

## 현재 집계

- 초기 검토 대상: `158`개
- 파일명 규칙으로 현재 원고에 매핑 가능한 문서: `156`개
- 대응 원고에 `## 출처와 참고 자료` 절이 있는 문서: `156`개
- 수동 검증 후 삭제 완료: `155`개
- 구조 불일치로 보류: `3`개
- 추가 수동 검증 필요: `0`개

## 삭제 완료군

| evidence 문서 | 대응 원고 | 확인 내용 | 상태 |
| --- | --- | --- | --- |
| `section-01-evidence-analysis.md` | `docs/parts/part-01/chapter-01/section-01.md` | OECD, NIST, Cambridge, Merriam-Webster, SEP, NIST 생성형 AI 프로필, LLM survey, Fayyad, DSS 자료가 본문 전개와 참고문헌에 반영됨 | 삭제 완료 |
| `section-02-evidence-analysis.md` | `docs/parts/part-01/chapter-01/section-02.md` | OECD, Cambridge, SEP, AIMA, Poole & Mackworth, Fayyad 자료가 문제 유형 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-1-1-evidence-analysis.md` | `docs/parts/part-02/chapter-01/section-01.md` | MML, Deep Learning Book, Higham, NumPy 논문이 수학 도입부 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-5-1-evidence-analysis.md` | `docs/parts/part-02/chapter-05/section-01.md` | OpenStax, Deep Learning Book 확률 장의 핵심 정리가 본문과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-2-1-evidence-analysis.md` | `docs/parts/part-02/chapter-02/section-01.md` | MML, Deep Learning Book, NumPy 논문이 변수·함수·식 독해와 코드 shape/type 확인 설명 및 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-2-2-evidence-analysis.md` | `docs/parts/part-02/chapter-02/section-02.md` | MML, Deep Learning Book, NumPy 논문이 시그마, 반복 계산, 평균·손실 집계 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-2-3-evidence-analysis.md` | `docs/parts/part-02/chapter-02/section-03.md` | MML, Deep Learning Book, Higham 논문이 극한, 변화율, 미분·최적화로 이어지는 준비 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-3-1-evidence-analysis.md` | `docs/parts/part-02/chapter-03/section-01.md` | MML, Deep Learning Book, NumPy 논문이 스칼라·벡터·행렬과 shape 설명 및 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-3-2-evidence-analysis.md` | `docs/parts/part-02/chapter-03/section-02.md` | MML, Deep Learning Book, NumPy 논문, Bengio 표현학습 리뷰, Mikolov word2vec 논문이 벡터 공간·위치 직관과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-3-3-evidence-analysis.md` | `docs/parts/part-02/chapter-03/section-03.md` | MML, Deep Learning Book, NumPy 논문이 행렬 곱, 가중합, 선형 변환 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-3-4-evidence-analysis.md` | `docs/parts/part-02/chapter-03/section-04.md` | Google Colab 공식 안내와 FAQ가 Colab·로컬 실행 환경 구분 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-3-5-evidence-analysis.md` | `docs/parts/part-02/chapter-03/section-05.md` | NumPy 공식 문서, quickstart, Harris 논문이 NumPy 선형대수 실습 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-4-1-evidence-analysis.md` | `docs/parts/part-02/chapter-04/section-01.md` | OpenStax Calculus Vol.1의 미분 정의 도입이 미분 기억 복구와 변화율 질문 설명, 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-4-2-evidence-analysis.md` | `docs/parts/part-02/chapter-04/section-02.md` | OpenStax Calculus Vol.1의 변화율·할선·접선 흐름이 평균/순간 변화율 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-4-3-evidence-analysis.md` | `docs/parts/part-02/chapter-04/section-03.md` | OpenStax Calculus Vol.1·Vol.3의 미분, 편미분, 그래디언트 흐름이 본문 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-4-4-evidence-analysis.md` | `docs/parts/part-02/chapter-04/section-04.md` | OpenStax Calculus Vol.1·Vol.3, Deep Learning Book 최적화 장이 학습-손실-그래디언트 연결 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-4-5-evidence-analysis.md` | `docs/parts/part-02/chapter-04/section-05.md` | 교육부 2022 고교 교육과정과 KOCW 방향도함수·그래디언트 자료가 그래디언트 보충학습 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-5-2-evidence-analysis.md` | `docs/parts/part-02/chapter-05/section-02.md` | OpenStax Introductory Statistics의 분포·중심·퍼짐 장이 분포, 평균, 분산 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-5-3-evidence-analysis.md` | `docs/parts/part-02/chapter-05/section-03.md` | OpenStax Introductory Statistics의 표본, 표본분포, 중심극한정리 도입이 표본·추정·오차 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-5-4-evidence-analysis.md` | `docs/parts/part-02/chapter-05/section-04.md` | NumPy mean/median/var 문서와 OpenStax 표본 자료가 작은 데이터 통계 실습 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-6-1-evidence-analysis.md` | `docs/parts/part-02/chapter-06/section-01.md` | Boyd·Vandenberghe, SciPy optimize, Deep Learning 최적화 장, Wired Dantzig 기사 근거가 최적화 도입 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-6-2-evidence-analysis.md` | `docs/parts/part-02/chapter-06/section-02.md` | Deep Learning 기초 장과 scikit-learn metrics 문서가 손실 함수·목적 함수 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-6-3-evidence-analysis.md` | `docs/parts/part-02/chapter-06/section-03.md` | Deep Learning 최적화 장과 Convex Optimization 교재가 경사하강법 직관 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-7-1-evidence-analysis.md` | `docs/parts/part-02/chapter-07/section-01.md` | Python 인터프리터, FAQ, venv, Packaging Guide 근거가 로컬 환경·실행 환경 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-7-2-evidence-analysis.md` | `docs/parts/part-02/chapter-07/section-02.md` | Text-Terminal-HOWTO, Bash 매뉴얼, PowerShell 위치 명령, os.getcwd 근거가 터미널·셸·작업 폴더 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-7-3-evidence-analysis.md` | `docs/parts/part-02/chapter-07/section-03.md` | Python FAQ, 인터프리터 문서, command line 문서가 인터프리터·대화형 실행·스크립트 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-7-4-evidence-analysis.md` | `docs/parts/part-02/chapter-07/section-04.md` | PEP 405, venv, Packaging Guide, Installing Python Modules 근거가 가상환경·패키지 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-7-5-evidence-analysis.md` | `docs/parts/part-02/chapter-07/section-05.md` | pip User Guide, pip freeze, Packaging Guide 근거가 의존성·재현성 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-7-6-evidence-analysis.md` | `docs/parts/part-02/chapter-07/section-06.md` | Windows Terminal, Apple Terminal, Ubuntu terminal, PowerShell 위치 명령 근거가 운영체제별 터미널 보충학습과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-7-7-evidence-analysis.md` | `docs/parts/part-02/chapter-07/section-07.md` | Python setup/use, downloads, Windows/macOS/Unix docs, venv 근거가 Python 설치 판단 보충학습과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-8-1-evidence-analysis.md` | `docs/parts/part-02/chapter-08/section-01.md` | Python Executive Summary, Informal Introduction, Built-in Types, Data model 근거가 Python 언어 감각 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-8-2-evidence-analysis.md` | `docs/parts/part-02/chapter-08/section-02.md` | Python Data Structures, Built-in Types, array, NumPy absolute basics 근거가 리스트·배열·ndarray 구분 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-8-3-evidence-analysis.md` | `docs/parts/part-02/chapter-08/section-03.md` | Data Structures, Mapping Types, Glossary, Data model 근거가 딕셔너리·키·hashable 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-8-4-evidence-analysis.md` | `docs/parts/part-02/chapter-08/section-04.md` | More Control Flow Tools, Data Structures, Glossary, for statement, PEP 234 근거가 iterable·iterator·comprehension 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-8-5-evidence-analysis.md` | `docs/parts/part-02/chapter-08/section-05.md` | Defining Functions, Default Argument Values, Function definitions, Data model, Method Objects 근거가 함수·매개변수·인자·메서드 구분 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-8-6-evidence-analysis.md` | `docs/parts/part-02/chapter-08/section-06.md` | Classes, Data model, Method Objects 근거가 객체·클래스·메서드·model.fit() 읽기 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-8-7-evidence-analysis.md` | `docs/parts/part-02/chapter-08/section-07.md` | Python `copy` 표준 라이브러리 근거가 참조·얕은 복사·깊은 복사 구분 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-9-1-evidence-analysis.md` | `docs/parts/part-02/chapter-09/section-01.md` | NIST data structure, abstract data type, Python Data Structures 근거가 자료구조 정의·ADT·연산 관점 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-9-2-evidence-analysis.md` | `docs/parts/part-02/chapter-09/section-02.md` | NumPy ndarray, pandas.DataFrame, NIST tree, NIST graph 근거가 배열·표·트리·그래프 비교 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-9-3-evidence-analysis.md` | `docs/parts/part-02/chapter-09/section-03.md` | NIST graph, NetworkX Graph 근거가 노드·엣지·인접 리스트·방향·가중치 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-9-4-evidence-analysis.md` | `docs/parts/part-02/chapter-09/section-04.md` | NIST data structure, abstract data type, Python Data Structures 근거가 전통 자료구조 입문 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-10-1-evidence-analysis.md` | `docs/parts/part-02/chapter-10/section-01.md` | Jupyter Documentation, Jupyter Architecture, Colab intro 근거가 노트북 정의·코드/마크다운/출력·학습 기록 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-10-2-evidence-analysis.md` | `docs/parts/part-02/chapter-10/section-02.md` | Google Colab FAQ, Jupyter Architecture 근거가 Jupyter·Colab·로컬 실행, 런타임·파일 구분 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-10-3-evidence-analysis.md` | `docs/parts/part-02/chapter-10/section-03.md` | Jupyter Architecture, Jupyter Notebook Format, Google Colab FAQ 근거가 재실행 가능한 노트북 기록 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-11-1-evidence-analysis.md` | `docs/parts/part-02/chapter-11/section-01.md` | NumPy absolute basics, ndarray, Array creation 근거가 NumPy 배열·shape·벡터·행렬 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-11-2-evidence-analysis.md` | `docs/parts/part-02/chapter-11/section-02.md` | NumPy Indexing on ndarrays, NumPy glossary 근거가 인덱싱·슬라이싱·axis 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-11-3-evidence-analysis.md` | `docs/parts/part-02/chapter-11/section-03.md` | NumPy Broadcasting, quickstart, absolute basics 근거가 브로드캐스팅·벡터화 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-12-1-evidence-analysis.md` | `docs/parts/part-02/chapter-12/section-01.md` | pandas.DataFrame, Package overview 근거가 DataFrame 구조·행/열/인덱스·표 해석 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-12-2-evidence-analysis.md` | `docs/parts/part-02/chapter-12/section-02.md` | pandas Indexing and selecting data, Group by, 10 minutes to pandas 근거가 선택·필터링·집계·groupby 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-12-3-evidence-analysis.md` | `docs/parts/part-02/chapter-12/section-03.md` | pandas.get_dummies, scikit-learn Glossary, train_test_split, Common pitfalls 근거가 X/y 분리·분할·누수 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-13-1-evidence-analysis.md` | `docs/parts/part-02/chapter-13/section-01.md` | Matplotlib Quick start guide, Plot types, matplotlib.pyplot 근거가 그래프 역할·Figure/Axes·질문별 plot 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-13-2-evidence-analysis.md` | `docs/parts/part-02/chapter-13/section-02.md` | Matplotlib Quick start guide, Plot types, matplotlib.pyplot 근거가 기본 차트·수식 모양·손실 곡선 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-13-3-evidence-analysis.md` | `docs/parts/part-02/chapter-13/section-03.md` | Matplotlib Quick start guide, Introduction to Axes, Figure.savefig 근거가 subplot 비교·저장·기록 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-14-1-evidence-analysis.md` | `docs/parts/part-02/chapter-14/section-01.md` | Pro Git About Version Control, git-status, git-commit 근거가 Git 목적·상태 확인·커밋 묶음 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-14-2-evidence-analysis.md` | `docs/parts/part-02/chapter-14/section-02.md` | Pro Git Branches in a Nutshell, git-branch, GitHub Pages 근거가 dev/main 운영·브랜치·배포 재현성 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-15-1-evidence-analysis.md` | `docs/parts/part-02/chapter-15/section-01.md` | Python Informal Introduction, NumPy absolute basics, Matplotlib Quick start 근거가 수식-코드 변환 절차와 확인 흐름 설명에 반영됨 | 삭제 완료 |
| `section-p2-15-2-evidence-analysis.md` | `docs/parts/part-02/chapter-15/section-02.md` | scikit-learn Getting Started, Glossary, NumPy absolute basics 근거가 Part 3 진입 전 X/y·fit/predict·shape 점검 설명에 반영됨 | 삭제 완료 |
| `section-p7-1-1-evidence-analysis.md` | `docs/parts/part-04/chapter-01/section-01.md` | scikit-learn, Deep Learning Book 기반의 AI/ML/DL/생성형 AI/LLM 관계 설명이 본문과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-1-2-evidence-analysis.md` | `docs/parts/part-04/chapter-01/section-02.md` | Tom Mitchell, scikit-learn 자료가 `데이터에서 규칙을 배운다` 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-2-1-evidence-analysis.md` | `docs/parts/part-04/chapter-02/section-01.md` | scikit-learn Supervised Learning, Google Supervised Learning 근거가 지도학습·X/y·분류·회귀 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-2-2-evidence-analysis.md` | `docs/parts/part-04/chapter-02/section-02.md` | scikit-learn Unsupervised learning, Google clustering overview 근거가 비지도학습·군집화·차원 축소·이상치 탐지 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-2-3-evidence-analysis.md` | `docs/parts/part-04/chapter-02/section-03.md` | Sutton and Barto, Buffet/Pietquin/Weng RL 근거가 강화학습·상태·행동·보상·정책 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-3-1-evidence-analysis.md` | `docs/parts/part-04/chapter-03/section-01.md` | SEP bounded rationality, AIMA, Pearl heuristics 근거가 휴리스틱 필요성과 검증 가능한 작업 가설 설명에 반영됨 | 삭제 완료 |
| `section-p7-3-2-evidence-analysis.md` | `docs/parts/part-04/chapter-03/section-02.md` | scikit-learn estimator map, cross-validation, ISLR 근거가 휴리스틱 기반 모델 선택과 기준 모델 설명에 반영됨 | 삭제 완료 |
| `section-p7-4-1-evidence-analysis.md` | `docs/parts/part-04/chapter-04/section-01.md` | scikit-learn cross-validation, train_test_split, ISLR 근거가 학습 데이터와 평가 데이터 분리 이유 설명에 반영됨 | 삭제 완료 |
| `section-p7-4-2-evidence-analysis.md` | `docs/parts/part-04/chapter-04/section-02.md` | scikit-learn cross-validation, train_test_split, ISLR 근거가 검증과 테스트 역할 구분 설명에 반영됨 | 삭제 완료 |
| `section-p7-5-1-evidence-analysis.md` | `docs/parts/part-04/chapter-05/section-01.md` | scikit-learn 과적합/과소적합 예제, Google ML Glossary, ISLR 근거가 본문 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-5-2-evidence-analysis.md` | `docs/parts/part-04/chapter-05/section-02.md` | Google ML Glossary, scikit-learn cross-validation, ISLR, 통계학습이론 근거가 일반화 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-6-1-evidence-analysis.md` | `docs/parts/part-04/chapter-06/section-01.md` | scikit-learn model evaluation, Google ML Glossary, van Rijsbergen 근거가 평가 지표 역할 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-6-2-evidence-analysis.md` | `docs/parts/part-04/chapter-06/section-02.md` | scikit-learn model evaluation, clustering evaluation 근거가 분류·회귀·군집화 평가 구분 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-6-3-evidence-analysis.md` | `docs/parts/part-04/chapter-06/section-03.md` | Google SRE Book의 SLO·모니터링 근거가 운영 metric 보충학습 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-7-1-evidence-analysis.md` | `docs/parts/part-04/chapter-07/section-01.md` | scikit-learn feature selection, data leakage, Guyon-Elisseeff 근거가 특징 선택 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-7-2-evidence-analysis.md` | `docs/parts/part-04/chapter-07/section-02.md` | scikit-learn preprocessing, imputation, pipeline, common pitfalls 근거가 전처리 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-8-1-evidence-analysis.md` | `docs/parts/part-04/chapter-08/section-01.md` | Ding/Tarokh/Yang, Raschka 근거가 모델 선택 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-8-2-evidence-analysis.md` | `docs/parts/part-04/chapter-08/section-02.md` | DummyClassifier, DummyRegressor, Raschka 근거가 baseline 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-9-1-evidence-analysis.md` | `docs/parts/part-04/chapter-09/section-01.md` | scikit-learn 튜닝/용어집/common pitfalls, Claesen, Bergstra 근거가 하이퍼파라미터 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-9-2-evidence-analysis.md` | `docs/parts/part-04/chapter-09/section-02.md` | scikit-learn 튜닝/common pitfalls, Bergstra-Bengio 근거가 튜닝과 검증 비용 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-10-1-evidence-analysis.md` | `docs/parts/part-04/chapter-10/section-01.md` | scikit-learn linear models, LinearRegression 근거가 선형회귀 직관 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-10-2-evidence-analysis.md` | `docs/parts/part-04/chapter-10/section-02.md` | scikit-learn model evaluation, MAE/MSE/R2 근거가 선형회귀 평가와 한계 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-11-1-evidence-analysis.md` | `docs/parts/part-04/chapter-11/section-01.md` | scikit-learn logistic regression, LogisticRegression 근거가 로지스틱 회귀 직관 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-11-2-evidence-analysis.md` | `docs/parts/part-04/chapter-11/section-02.md` | scikit-learn logistic regression, LogisticRegression 근거가 결정 경계 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-12-1-evidence-analysis.md` | `docs/parts/part-04/chapter-12/section-01.md` | scikit-learn nearest neighbors, KNeighborsClassifier 근거가 k-NN 직관 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-12-2-evidence-analysis.md` | `docs/parts/part-04/chapter-12/section-02.md` | scikit-learn nearest neighbors, feature scaling 근거가 거리와 스케일 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-13-1-evidence-analysis.md` | `docs/parts/part-04/chapter-13/section-01.md` | scikit-learn SVM, Cortes-Vapnik 근거가 SVM 직관 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-13-2-evidence-analysis.md` | `docs/parts/part-04/chapter-13/section-02.md` | scikit-learn SVM, Boser-Guyon-Vapnik 근거가 kernel 입문 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-14-1-evidence-analysis.md` | `docs/parts/part-04/chapter-14/section-01.md` | scikit-learn decision trees, DecisionTreeClassifier, CART 근거가 결정트리 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-14-2-evidence-analysis.md` | `docs/parts/part-04/chapter-14/section-02.md` | scikit-learn decision trees, DecisionTreeClassifier 근거가 트리 과적합 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-15-1-evidence-analysis.md` | `docs/parts/part-04/chapter-15/section-01.md` | scikit-learn ensemble, RandomForestClassifier, Breiman 근거가 랜덤포레스트 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-15-2-evidence-analysis.md` | `docs/parts/part-04/chapter-15/section-02.md` | scikit-learn ensemble, RandomForestClassifier, Louppe 근거가 특징 중요도 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-15-3-evidence-analysis.md` | `docs/parts/part-04/chapter-15/section-03.md` | scikit-learn ensemble, RandomForestClassifier 근거가 OOB 점검 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-16-1-evidence-analysis.md` | `docs/parts/part-04/chapter-16/section-01.md` | scikit-learn ensemble, Friedman 2001/2002 근거가 그래디언트 부스팅 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-16-2-evidence-analysis.md` | `docs/parts/part-04/chapter-16/section-02.md` | scikit-learn ensemble, Friedman 2002 근거가 부스팅의 성능과 위험 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-17-1-evidence-analysis.md` | `docs/parts/part-04/chapter-17/section-01.md` | scikit-learn clustering, KMeans, DBSCAN 근거가 클러스터링 직관 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-17-2-evidence-analysis.md` | `docs/parts/part-04/chapter-17/section-02.md` | scikit-learn clustering, common pitfalls 근거가 군집 결과 해석 주의점 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-18-1-evidence-analysis.md` | `docs/parts/part-04/chapter-18/section-01.md` | scikit-learn decomposition, PCA 근거가 차원 축소 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-18-2-evidence-analysis.md` | `docs/parts/part-04/chapter-18/section-02.md` | scikit-learn decomposition, PCA 근거가 시각화와 정보 손실 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-19-1-evidence-analysis.md` | `docs/parts/part-04/chapter-19/section-01.md` | Sutton-Barto, Watkins-Dayan, Singh et al. 근거가 가치 기반 강화학습 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-19-2-evidence-analysis.md` | `docs/parts/part-04/chapter-19/section-02.md` | Sutton-Barto, Williams, Sutton et al., Konda-Tsitsiklis 근거가 정책 기반 강화학습 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p7-19-3-evidence-analysis.md` | `docs/parts/part-04/chapter-19/section-03.md` | Sutton-Barto, Amodei et al., Zhao et al. 근거가 강화학습 적용 주의점 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-03-evidence-analysis.md` | `docs/parts/part-01/chapter-01/section-03.md` | OECD, SEP, AIMA, NIST 생성형 AI 프로필, LLM survey가 용어 층위 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-2-1-evidence-analysis.md` | `docs/parts/part-01/chapter-02/section-01.md` | SEP AI, SEP Logic-Based AI, AIMA, Google ML Glossary, Google Supervised Learning, KCI 검색 근거가 본문과 참고문헌에 반영됨 | 삭제 완료 |
| `section-2-2-evidence-analysis.md` | `docs/parts/part-01/chapter-02/section-02.md` | AIMA 목차, Poole & Mackworth, SEP AI, SEP Logic-Based AI가 탐색·지식 표현·확률 추론 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-2-3-evidence-analysis.md` | `docs/parts/part-01/chapter-02/section-03.md` | SEP AI, AIMA 목차, Poole & Mackworth, Fayyad KDD, NIST 생성형 AI 프로필, LLM survey가 역사 흐름 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-p2-1-2-evidence-analysis.md` | `docs/parts/part-02/chapter-01/section-02.md` | MML, Deep Learning Book, NumPy 논문 근거가 수식-코드-데이터 연결 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-3-1-evidence-analysis.md` | `docs/parts/part-01/chapter-03/section-01.md` | MYCIN, SEP Logic-Based AI, AIMA, 얼굴인식·얼굴검출·차선추적·TTS 사례, AlexNet 보조 근거가 규칙 기반 시스템의 강점과 한계 설명 및 참고문헌에 반영됨 | 삭제 완료 |
| `section-3-2-evidence-analysis.md` | `docs/parts/part-01/chapter-03/section-02.md` | SEP AI, Tom Mitchell, Google Supervised Learning, scikit-learn 과적합/과소적합, Fayyad KDD 근거가 데이터에서 패턴을 배운다는 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-3-3-evidence-analysis.md` | `docs/parts/part-01/chapter-03/section-03.md` | SEP AI, Bengio representation learning review, Miller 논문이 규칙 기반 접근과 표현 학습의 차이 설명 및 참고문헌에 반영됨 | 삭제 완료 |
| `section-4-1-evidence-analysis.md` | `docs/parts/part-01/chapter-04/section-01.md` | SEP Models in Science, Etymonline, Google Supervised Learning, Google ML Glossary가 모델/모형 도입 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-4-2-evidence-analysis.md` | `docs/parts/part-01/chapter-04/section-02.md` | SEP AI, Google Supervised Learning이 입력·출력·데이터 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-4-3-evidence-analysis.md` | `docs/parts/part-01/chapter-04/section-03.md` | Google ML Glossary, Google Supervised Learning, SEP AI, Bengio representation learning review가 특징·표현·파라미터 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-4-4-evidence-analysis.md` | `docs/parts/part-01/chapter-04/section-04.md` | Google ML Glossary, Google Supervised Learning, scikit-learn model evaluation, SEP AI가 문제 정의와 평가 기준 설명 및 참고문헌에 반영됨 | 삭제 완료 |
| `section-5-1-evidence-analysis.md` | `docs/parts/part-01/chapter-05/section-01.md` | Google ML Glossary, Deep Learning Book Chapter 5, scikit-learn glossary가 learning/training 구분과 참고문헌에 반영됨 | 삭제 완료 |
| `section-5-2-evidence-analysis.md` | `docs/parts/part-01/chapter-05/section-02.md` | Google ML Glossary, scikit-learn glossary가 inference 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-5-3-evidence-analysis.md` | `docs/parts/part-01/chapter-05/section-03.md` | Google ML Glossary, scikit-learn glossary가 inference/reasoning/prediction/statistical inference/generation 구분과 참고문헌에 반영됨 | 삭제 완료 |
| `section-6-1-evidence-analysis.md` | `docs/parts/part-01/chapter-06/section-01.md` | AIMA 목차, Poole & Mackworth search/uncertainty, SEP AI가 불완전한 정보와 예외가 많은 문제 설명 및 참고문헌에 반영됨 | 삭제 완료 |
| `section-6-2-evidence-analysis.md` | `docs/parts/part-01/chapter-06/section-02.md` | Poole & Mackworth, SEP AI, Hullermeier & Waegeman, scikit-learn calibration이 uncertainty/probability/stochastic 구분과 참고문헌에 반영됨 | 삭제 완료 |
| `section-6-3-evidence-analysis.md` | `docs/parts/part-01/chapter-06/section-03.md` | Google ML Glossary, scikit-learn calibration, Poole & Mackworth가 AI에서 확률적 판단이 쓰이는 위치 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-7-1-evidence-analysis.md` | `docs/parts/part-01/chapter-07/section-01.md` | Poole & Mackworth, AIMA, DeepMind AlphaDev/FunSearch 근거가 탐색 공간과 조합 폭발 설명, 참고문헌에 반영됨 | 삭제 완료 |
| `section-7-2-evidence-analysis.md` | `docs/parts/part-01/chapter-07/section-02.md` | Etymonline, ACM Newell/Simon, Nobel Simon, Poole & Mackworth, AIMA, Google ML Glossary, DeepMind FunSearch가 휴리스틱의 역할과 한계 설명, 참고문헌에 반영됨 | 삭제 완료 |
| `section-7-3-evidence-analysis.md` | `docs/parts/part-01/chapter-07/section-03.md` | Poole & Mackworth, AIMA, Google ML Glossary, scikit-learn calibration이 휴리스틱과 확률 모델의 차이 설명 및 참고문헌에 반영됨 | 삭제 완료 |
| `section-7-4-evidence-analysis.md` | `docs/parts/part-01/chapter-07/section-04.md` | Poole & Mackworth, DARPA RNDF/MDF, 자율주행 motion planning survey, dynamic motion planning framework가 경로/궤적, 글로벌/로컬 계획 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-8-1-evidence-analysis.md` | `docs/parts/part-01/chapter-08/section-01.md` | Google ML Glossary, scikit-learn supervised learning, AWS/IBM data labeling, Datasheets for Datasets가 라벨과 지도학습 설명, 참고문헌에 반영됨 | 삭제 완료 |
| `section-8-2-evidence-analysis.md` | `docs/parts/part-01/chapter-08/section-02.md` | Google ML Glossary, scikit-learn unsupervised/clustering/decomposition, Stanford CS229가 비지도학습과 군집화, 차원 축소 설명 및 참고문헌에 반영됨 | 삭제 완료 |
| `section-8-3-evidence-analysis.md` | `docs/parts/part-01/chapter-08/section-03.md` | Google ML Glossary, OpenAI Spinning Up, Poole & Mackworth가 강화학습의 상태-행동-보상 구조 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-9-1-evidence-analysis.md` | `docs/parts/part-01/chapter-09/section-01.md` | AlexNet, Nature deep learning review, representation learning review, 얼굴인식 survey가 이미지 인식과 표현 학습 설명, 참고문헌에 반영됨 | 삭제 완료 |
| `section-9-2-evidence-analysis.md` | `docs/parts/part-01/chapter-09/section-02.md` | YOLO, WaveNet, Deep Voice 보조 사례가 객체 검출과 음성 생성 사례 설명, 참고문헌에 반영됨 | 삭제 완료 |
| `section-9-3-evidence-analysis.md` | `docs/parts/part-01/chapter-09/section-03.md` | Bengio 2003, Seq2Seq, Attention, Transformer, word2vec, ELMo, ULMFiT, BERT, GPT 계열이 LLM 직접 계보 구분과 참고문헌에 반영됨 | 삭제 완료 |
| `section-10-1-evidence-analysis.md` | `docs/parts/part-01/chapter-10/section-01.md` | Google classification/linear regression, IBM ML/generative AI, Feuerriegel가 분류·예측·생성 구분과 참고문헌에 반영됨 | 삭제 완료 |
| `section-10-2-evidence-analysis.md` | `docs/parts/part-01/chapter-10/section-02.md` | GPT-3, WaveNet, DDPM, Latent Diffusion이 다음 출력 생성 직관과 참고문헌에 반영됨 | 삭제 완료 |
| `section-10-3-evidence-analysis.md` | `docs/parts/part-01/chapter-10/section-03.md` | NIST AI 600-1, OWASP LLM Top 10, USCO, IBM hallucinations, AP 사례가 생성 결과 품질·위험 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-11-1-evidence-analysis.md` | `docs/parts/part-01/chapter-11/section-01.md` | Jurafsky & Martin, Bengio 2003, Mikolov 2013 계열이 통계적 언어 모델과 임베딩 설명, 참고문헌에 반영됨 | 삭제 완료 |
| `section-11-2-evidence-analysis.md` | `docs/parts/part-01/chapter-11/section-02.md` | Cho 2014, Sutskever 2014, Bahdanau 2014, Neubig 2017이 RNN, Seq2Seq, Attention 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-11-3-evidence-analysis.md` | `docs/parts/part-01/chapter-11/section-03.md` | Transformer, ELMo, ULMFiT, BERT, GPT 계열, GPT-3가 사전학습 LLM 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-12-1-evidence-analysis.md` | `docs/parts/part-01/chapter-12/section-01.md` | GPT-3, InstructGPT, prompt engineering survey, OpenAI prompt guide가 프롬프트의 구성과 참고문헌에 반영됨 | 삭제 완료 |
| `section-12-2-evidence-analysis.md` | `docs/parts/part-01/chapter-12/section-02.md` | GPT-3, InstructGPT, prompt engineering survey, OpenAI prompt guide가 지시·맥락·예시 구분과 참고문헌에 반영됨 | 삭제 완료 |
| `section-12-3-evidence-analysis.md` | `docs/parts/part-01/chapter-12/section-03.md` | InstructGPT, prompt engineering survey, NIST AI 600-1, OpenAI prompt guide가 프롬프트 한계와 평가 설명, 참고문헌에 반영됨 | 삭제 완료 |
| `section-13-1-evidence-analysis.md` | `docs/parts/part-01/chapter-13/section-01.md` | Jurafsky & Martin, Bengio 2003, Mikolov 2013 계열이 텍스트 벡터 표현과 임베딩 설명, 참고문헌에 반영됨 | 삭제 완료 |
| `section-13-2-evidence-analysis.md` | `docs/parts/part-01/chapter-13/section-02.md` | Bengio 2003, Mikolov 2013 계열이 유사도 검색과 nearest neighbor 직관 설명, 참고문헌에 반영됨 | 삭제 완료 |
| `section-13-3-evidence-analysis.md` | `docs/parts/part-01/chapter-13/section-03.md` | RAG, Dense Passage Retrieval, REALM이 검색-보강-생성 흐름 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-13-4-evidence-analysis.md` | `docs/parts/part-01/chapter-13/section-04.md` | HNSW, billion-scale similarity search가 벡터 검색 구현 직관과 참고문헌에 반영됨 | 삭제 완료 |
| `section-14-1-evidence-analysis.md` | `docs/parts/part-01/chapter-14/section-01.md` | OpenAI text generation/function calling, NIST AI RMF가 모델·앱·데이터·도구 구성 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-14-2-evidence-analysis.md` | `docs/parts/part-01/chapter-14/section-02.md` | RAG, OpenAI function calling/text generation이 RAG와 도구 사용의 위치 구분과 참고문헌에 반영됨 | 삭제 완료 |
| `section-14-3-evidence-analysis.md` | `docs/parts/part-01/chapter-14/section-03.md` | ReAct, OpenAI Agents SDK/function calling이 에이전트 구조 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-14-4-evidence-analysis.md` | `docs/parts/part-01/chapter-14/section-04.md` | MCP intro/architecture/security가 MCP 연결 표준화 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-14-5-evidence-analysis.md` | `docs/parts/part-01/chapter-14/section-05.md` | harness 어원 자료, agent harness 프리프린트, LangSmith, SWE-agent, OpenHands, OpenAI observability/evals가 하네스와 평가 실행 환경 설명, 참고문헌에 반영됨 | 삭제 완료 |
| `section-14-6-evidence-analysis.md` | `docs/parts/part-01/chapter-14/section-06.md` | OpenAI latency/cost/prompt caching/batch/rate limits/production docs가 AI 서비스 제약 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-15-1-evidence-analysis.md` | `docs/parts/part-01/chapter-15/section-01.md` | NIST AI RMF, OECD/UNESCO 원칙, ProPublica, AP 사례가 편향·안전성·책임 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-15-2-evidence-analysis.md` | `docs/parts/part-01/chapter-15/section-02.md` | 한국 저작권법, USCO AI 자료, AP NYT 소송 보도, 학술 논문들이 저작권·학습 데이터 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-15-3-evidence-analysis.md` | `docs/parts/part-01/chapter-15/section-03.md` | OWASP LLM Top 10, NIST AI RMF/GAI Profile이 보안·개인정보 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-16-1-evidence-analysis.md` | `docs/parts/part-01/chapter-16/section-01.md` | U.S. Department of Education, UNESCO 자료가 개인 학습과 문서화 설명, 참고문헌에 반영됨 | 삭제 완료 |
| `section-16-2-evidence-analysis.md` | `docs/parts/part-01/chapter-16/section-02.md` | NIST AI RMF, U.S. Department of Education, WEF Future of Jobs가 업무 자동화와 검색 설명, 참고문헌에 반영됨 | 삭제 완료 |
| `section-16-3-evidence-analysis.md` | `docs/parts/part-01/chapter-16/section-03.md` | NIST AI RMF, OWASP LLM Top 10, U.S. Department of Education 자료가 프로젝트 검증 방법 설명, 참고문헌에 반영됨 | 삭제 완료 |
| `section-17-1-evidence-analysis.md` | `docs/parts/part-01/chapter-17/section-01.md` | Stanford HAI AI Index 2026, WEF Future of Jobs 2025, NIST AI RMF가 전망 근거 읽기 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-17-2-evidence-analysis.md` | `docs/parts/part-01/chapter-17/section-02.md` | Stanford HAI AI Index 2026, WEF Future of Jobs 2025, U.S. Department of Education 보고서가 언론·칼럼·보고서 읽기 설명과 참고문헌에 반영됨 | 삭제 완료 |
| `section-17-3-evidence-analysis.md` | `docs/parts/part-01/chapter-17/section-03.md` | Stanford HAI AI Index 2026, WEF Future of Jobs 2025, U.S. Department of Education 보고서가 예측과 작업 가설 구분 설명, 참고문헌에 반영됨 | 삭제 완료 |

## 구조 불일치군

| evidence 문서 | 예상 대응 원고 | 판단 | 상태 |
| --- | --- | --- | --- |
| `section-p7-3-3-evidence-analysis.md` | `docs/parts/part-04/chapter-03/section-03.md` | 현재 원고에 `section-03.md`가 없음 | 보류 |
| `section-p7-9-3-evidence-analysis.md` | `docs/parts/part-04/chapter-09/section-03.md` | 현재 원고는 `P4-9.3` 고급 모델 선택 보충학습인데 evidence 본문은 `P5-9.3` LoRA 메모라 구조가 맞지 않음 | 보류 |
| `section-p7-19-evidence-analysis.md` | 불명 | 본문은 `P5-19` 기준 메모인데 현재 파일명 규칙과 현재 파트 구조가 맞지 않음 | 보류 |

## 다음 상태

- Part 2와 Part 4의 매핑 가능한 evidence 문서는 모두 수동 대조를 마쳤습니다.
- 현재 워크트리에 남아 있는 evidence 문서는 구조 불일치 보류 3건뿐입니다.
- 남은 3건은 현재 원고 구조가 바뀌었거나 evidence 본문이 다른 파트 기준 메모라 자동 삭제하지 않았습니다.
