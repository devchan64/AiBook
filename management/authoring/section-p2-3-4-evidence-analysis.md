# Section P2-3.4 근거 검토: Google Colab으로 파이썬 코드 실행하기

## 검토 목적

- P2-3.4의 중심 질문은 “파이썬을 설치하지 않은 독자가 다음 Python/NumPy 실습을 어떻게 먼저 실행해 볼 수 있는가?”입니다.
- 이 절은 Colab 자체를 깊게 배우는 절이 아니라, Python/NumPy 실습을 위한 사전 안내입니다.
- Google Colab 사용 안내를 NumPy 실습 본문과 분리해, 실행 환경과 실습 내용을 섞지 않도록 합니다.

## 확인한 자료

Google Colab 공식 안내 문서를 확인하고 `.tmp/section-p2-3-4-evidence/` 아래에 HTML로 저장했습니다.

| 자료 | 저장 위치 | 반영 판단 |
| --- | --- | --- |
| Google, *Welcome to Colab* | `.tmp/section-p2-3-4-evidence/google-colab-intro.html` | Colab 사용 안내서 링크로 사용했습니다. |
| Google, *Google Colab FAQ* | `.tmp/section-p2-3-4-evidence/google-colab-faq.html` | Colab이 설치 없이 사용할 수 있는 hosted Jupyter Notebook 서비스이며 자원 제한이 있을 수 있다는 근거로 사용했습니다. |

## 본문 반영 기준

- Google Colab을 브라우저에서 Jupyter Notebook 형태로 파이썬 코드를 실행할 수 있는 hosted 서비스로 설명했습니다.
- `Welcome to Colab` 안내서 링크를 중심으로 안내했습니다.
- 2026년 6월 24일 확인한 공식 안내와 FAQ 기준으로 작성했으며, Colab의 UI, 사용 조건, 무료 제공 범위, 런타임 정책, 서비스 지속 여부가 바뀔 수 있음을 명시했습니다.
- `%pip install numpy`가 Colab/Jupyter 코드 셀에서 쓰는 매직 명령(magic command)임을 설명했습니다.
- `!pip install numpy`도 문서에서 볼 수 있으나, 이 책에서는 `%pip install numpy`를 우선 사용한다고 정리했습니다.
- Colab 코드 셀 명령, 개인 PC 터미널 명령, 파이썬 코드 안의 `import`를 구분했습니다.

## Section 경계 검토

- P2-3.4는 Colab 사용 준비 절입니다.
- 이 절의 목적은 이후 Python/NumPy 실습을 따라가기 위한 사전 안내임을 본문 도입부와 범위에 명시했습니다.
- NumPy 배열, shape, 행렬 곱 실습은 P2-3.5로 넘겼습니다.
- 개인 PC의 파이썬 설치법, 가상환경, 패키지 관리 세부 절차는 후속 실습 환경 절로 넘겼습니다.
- Colab의 파일 관리, Google Drive 연동, GPU/TPU 런타임, 노트북 공유 권한은 다루지 않았습니다.

## 용어 검토

- `Google Colab`, `파이썬(Python)`, `Jupyter Notebook`, `코드 셀(code cell)`, `매직 명령(magic command)`, `커널(kernel)`, `NumPy`, `터미널(terminal)`을 한영 병기했습니다.

## 주의한 오해

- `%pip`를 일반 파이썬 문법으로 설명하지 않았습니다.
- Colab에서 쓰는 명령과 개인 PC 터미널에서 쓰는 명령을 섞지 않았습니다.
- Colab이 항상 같은 패키지 버전과 자원을 제공한다고 단정하지 않았습니다.
- Colab이 계속 같은 형태로 서비스된다고 단정하지 않았고, 읽는 시점에 공식 문서를 별도 확인해야 함을 안내했습니다.

## 참고 자료

- Google, [Welcome to Colab](https://colab.research.google.com/notebooks/intro.ipynb), 확인 날짜: 2026-06-24.
- Google, [Google Colab FAQ](https://research.google.com/colaboratory/faq.html), 확인 날짜: 2026-06-24.
