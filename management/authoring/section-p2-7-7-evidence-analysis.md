# P2-7.7 근거 검토: Python 설치는 언제 필요한가

확인 날짜: 2026-06-24

## 사용한 주요 자료

| 자료 | 확인 내용 | 반영 위치 |
| --- | --- | --- |
| Python documentation, `Python Setup and Usage` | Python 환경 설정, 플랫폼별 사용, 인터프리터 실행을 다루는 공식 문서 구조 | 이 절의 전체 범위 설정 |
| Python.org, `Download Python` | 현재 다운로드 페이지와 활성 Python 릴리스 정보 | 버전과 설치 정보는 작성 시점 확인이 필요하다는 관점 |
| Python documentation, `Using Python on Windows` | Windows에는 시스템 지원 Python 설치가 기본 포함되지 않을 수 있고, Python Install Manager와 `python`, `py` 명령, 프로젝트별 가상환경 권장 설명 | Windows 설치 판단, `python`/`py` 확인 |
| Python documentation, `Using Python on macOS` | macOS에서 Python을 얻는 여러 방법, python.org 설치 패키지, `python3`로 스크립트 실행 가능성 | macOS 설치 판단, `python3` 확인 |
| Python documentation, `Using Python on Unix platforms` | Python이 대부분의 Linux 배포판에 미리 설치되어 있고, 패키지로도 제공된다는 설명 | Linux 설치 판단 |
| Python documentation, `venv` | 가상환경 활성화는 플랫폼별로 다르고, 가상환경은 재생성 가능한 방식으로 관리해야 한다는 설명 | Python 설치와 가상환경 생성 구분 |

## 작성 판단

- 사용자는 초반 실습은 Colab으로 어느 정도 대체 가능하다고 판단했다. 이에 따라 P2-7.7은 설치 절차 안내서가 아니라 “언제 설치가 필요한가”를 판단하는 보충학습으로 작성했다.
- 운영체제별 설치 화면은 자주 바뀌므로 본문에 장황하게 넣지 않았다. 대신 공식 문서와 현재 다운로드 페이지를 확인하도록 안내했다.
- Windows는 `python`, `py`, Python Install Manager를, macOS/Linux는 `python3` 확인 가능성을 소개했다. 다만 특정 명령 하나를 모든 환경의 정답처럼 단정하지 않았다.
- `venv`는 이미 P2-7.4에서 다뤘으므로, 이 절에서는 Python 설치와 가상환경 생성이 다른 일이라는 경계만 다시 강조했다.
- 로컬 설치가 필요한 시점은 프로젝트 폴더, `.py` 파일, 데이터 파일, 가상환경, 패키지 버전, 재현성을 직접 관리해야 할 때로 정리했다.

## 본문에 반영한 안전한 설명

- 초반 학습은 Colab으로 충분할 수 있다.
- 로컬 설치는 실행 환경을 직접 관리해야 할 때 필요해진다.
- Python 설치는 Python 인터프리터를 준비하는 일이고, 가상환경 생성이나 패키지 설치와는 다르다.
- 설치 뒤에는 `python --version`, `python3 --version`, `py --version`처럼 환경에 맞는 확인 명령을 점검해야 한다.
- 운영체제별 설치 방식과 최신 버전 정보는 작성 시점에 공식 문서를 다시 확인해야 한다.

## 제외한 내용

- 설치 화면을 따라가는 단계별 튜토리얼
- PATH 수동 수정 절차
- Windows Store, python.org, winget, Chocolatey 비교
- Homebrew, pyenv, conda, Anaconda 상세 비교
- WSL 설치
- Docker, Dev Container
- IDE별 Python interpreter 설정

이 내용은 실제 프로젝트 환경을 만들 때 필요한 만큼 좁게 다루는 편이 안전하다.
