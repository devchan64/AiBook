# P2-7.3 근거 검토: Python 인터프리터와 스크립트

확인 날짜: 2026-06-24

## 사용한 주요 자료

| 자료 | 확인 내용 | 반영 위치 |
| --- | --- | --- |
| Python Software Foundation, `General Python FAQ` | Python이 interpreted, interactive 언어로 설명된다는 점, Guido van Rossum의 ABC 경험, Amoeba 작업, C 프로그램과 Bourne shell script만으로 부족했던 시스템 관리 맥락, 1991년 공개 | 인터프리터와 스크립트가 함께 등장하는 역사적 배경 |
| Python Software Foundation, `Using the Python Interpreter` | Python 인터프리터를 명령줄에서 호출할 수 있음, 대화형 모드에서 `>>>` 프롬프트가 표시됨, 스크립트 파일 실행 방식 | Python 인터프리터, 대화형 실행, 스크립트 실행 설명 |
| Python Software Foundation, `Command line and environment` | `python -m module` 형식이 모듈을 스크립트처럼 실행한다는 설명, 명령줄 옵션 | `python -m pip ...` 설명 |

## 작성 판단

- 이 절은 Python 문법 학습이 아니라 Python 코드가 실행되는 방식의 구분을 목표로 작성했다.
- 사용자의 피드백에 따라 역사 소개를 추가했다. 다만 Python 언어사 전체가 아니라, Python이 해석형·대화형 언어로 소개되고 스크립팅 필요에서 출발했다는 점만 실행 방식 설명과 연결했다.
- P2-7.1에서 Python 인터프리터를 이미 큰 그림으로 설명했으므로, P2-7.3에서는 대화형 모드, 스크립트 실행, 노트북 코드 셀의 차이를 중심으로 정리했다.
- 터미널과 작업 폴더의 기본 개념은 P2-7.2에서 다루었으므로, 여기서는 스크립트 실행 실패의 원인으로 현재 작업 폴더를 짧게만 연결했다.
- 가상환경과 패키지 설치는 P2-7.4의 도메인으로 남겼다. `python -m pip ...`는 자주 보게 되는 명령이므로 `-m`의 의미만 최소 설명했다.
- Colab/Jupyter는 학습 환경에서 자주 사용되므로 코드 셀의 장점과 주의점을 넣었다. 다만 노트북 구조와 실행 모델의 상세 설명은 P2-10장으로 넘기는 편이 안전하다.

## 본문에 반영한 안전한 설명

- Python 인터프리터는 Python 코드를 읽고 실행하는 프로그램이다.
- Python은 해석형(interpreted), 대화형(interactive) 언어로 소개되며, 스크립팅 필요와 연결된 역사적 배경을 가진다.
- 대화형 모드는 `>>>` 프롬프트에서 한 줄씩 실행해 확인하는 방식이다.
- 스크립트는 `.py` 파일에 저장한 Python 실행 단위로 설명할 수 있다.
- 터미널 명령과 Python 코드는 입력 위치가 다르다.
- Colab/Jupyter 코드 셀은 셀 단위로 Python 코드를 실행하며, 셀 실행 순서에 따라 결과가 달라질 수 있다.
- `python -m`은 모듈을 스크립트처럼 실행하는 명령줄 실행 방식으로 설명할 수 있다.

## 제외한 내용

- Python 문법 상세
- `__name__ == "__main__"` 관용구
- 모듈 검색 경로와 `PYTHONPATH`
- 패키지 설치와 가상환경 활성화 절차
- Jupyter 커널과 노트북 실행 모델 상세

이 내용은 P2-7.4, P2-8장, P2-10장에서 필요한 범위로 다시 다루는 편이 안전하다.
