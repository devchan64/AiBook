# P2-7.4 근거 검토: 가상환경과 패키지

확인 날짜: 2026-06-24

## 사용한 주요 자료

| 자료 | 확인 내용 | 반영 위치 |
| --- | --- | --- |
| Carl Meyer, `PEP 405 – Python Virtual Environments` | 2011년에 생성된 Python 3.3 대상 제안이며, 기존 `virtualenv` 도구가 의존성 관리, 격리, 관리자 권한 없는 패키지 설치, 여러 Python 버전 테스트 등에 이미 널리 쓰였다는 동기 설명 | 가상환경 필요성이 생긴 역사적 배경 |
| Python Software Foundation, `venv — Creation of virtual environments` | `venv`가 가벼운 가상환경을 만들며, 각 가상환경이 독립된 Python 패키지 집합을 가질 수 있다는 설명, `.venv` 디렉터리 관례, 소스 관리에 넣지 않는다는 설명 | 가상환경의 목적과 저장소 관리 설명 |
| Python Packaging User Guide, `Install packages in a virtual environment using pip and venv` | `venv` 생성, 활성화, `pip`로 패키지를 설치하는 흐름 | 가상환경과 패키지 설치 흐름 |
| Python Software Foundation, `Installing Python Modules` | `pip`를 통해 Python 패키지를 설치하는 일반 안내 | `pip install` 설명 |

## 작성 판단

- 이 절은 가상환경 사용 절차 전체가 아니라, 가상환경과 패키지가 왜 필요한지의 개념 설명을 목표로 작성했다.
- 사용자의 피드백에 따라 가상환경 필요성이 생긴 역사적 배경을 PEP 405에 근거해 추가했다. 단순히 “프로젝트별로 나누면 좋다”가 아니라, 기존 `virtualenv` 사용 경험이 표준 `venv`로 이어졌고 의존성 관리, 격리, 권한 문제, 여러 Python 버전 테스트가 주요 동기였다는 흐름을 반영했다.
- P2-7.1에서 가상환경을 큰 그림으로 이미 소개했으므로, P2-7.4에서는 프로젝트별 실행 공간, 패키지 설치 위치, `pip install`과 `import`의 차이를 중심으로 정리했다.
- 운영체제별 가상환경 활성화 명령은 Windows/macOS/Linux 차이가 크고 초심자에게 혼란을 줄 수 있으므로 P2-7.7 보충수업으로 넘겼다.
- Python 설치 자체는 P2-7.6 보충수업의 도메인으로 남겼다.
- 의존성 목록 저장과 재현성은 P2-7.5의 도메인으로 남겼다.
- Colab은 초반 실습을 대체할 수 있지만, 런타임과 로컬 가상환경이 다른 공간이라는 점을 짧게 연결했다.

## 본문에 반영한 안전한 설명

- 가상환경은 프로젝트별 Python 실행 공간으로 설명할 수 있다.
- 가상환경은 Python 생태계에서 패키지와 프로젝트가 늘어나며 생긴 의존성 충돌, 시스템 환경 보호, 권한 문제, 테스트 요구와 연결된 도구로 설명할 수 있다.
- 패키지는 Python에서 가져다 쓰는 코드 묶음이다.
- `pip`는 패키지를 설치하는 도구로 설명할 수 있다.
- `pip install`은 설치이고 `import`는 현재 Python 코드에서 사용하는 일이다.
- 패키지는 특정 Python 실행 환경에 설치된다.
- 가상환경 폴더는 프로젝트 코드 자체가 아니므로 보통 커밋하지 않는다.

## 제외한 내용

- 운영체제별 가상환경 활성화 명령
- `conda`, `poetry`, `uv` 같은 대체 도구 비교
- `requirements.txt`, lock 파일, dependency resolver
- 패키지 빌드와 배포
- 시스템 Python, pyenv, Homebrew Python 비교
- Colab 런타임의 상세 패키지 관리

이 내용은 P2-7.5, P2-7.6, P2-7.7 또는 후속 실습 절에서 필요한 만큼 좁게 다루는 편이 안전하다.
