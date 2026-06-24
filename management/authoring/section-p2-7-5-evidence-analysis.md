# P2-7.5 근거 검토: 의존성과 재현성

확인 날짜: 2026-06-24

## 사용한 주요 자료

| 자료 | 확인 내용 | 반영 위치 |
| --- | --- | --- |
| pip documentation, `User Guide` | `python -m pip` 실행 방식, requirements files가 `pip install`에 전달할 설치 항목 목록이라는 설명, `pip freeze > requirements.txt`와 `pip install -r requirements.txt` 흐름, repeatable installs 언급 | requirements 파일, `pip freeze`, 반복 가능한 설치 설명 |
| pip documentation, `pip freeze` | 현재 환경에 설치된 패키지를 requirements 형식으로 출력하는 명령 | `pip freeze` 설명 |
| Python Packaging User Guide, `install_requires vs requirements files` | requirements 파일과 프로젝트 설치 요구사항의 역할 차이 | requirements 파일과 프로젝트 설정 파일 구분 |

## 작성 판단

- 이 절은 의존성 관리 도구 전체가 아니라, 입문자가 “내 컴퓨터에서는 된다” 문제를 이해하기 위한 최소 개념을 목표로 작성했다.
- P2-7.4에서 가상환경과 패키지를 설명했으므로, P2-7.5에서는 패키지 목록을 기록하고 다시 설치할 수 있게 만드는 흐름으로 연결했다.
- `requirements.txt`, `pip freeze`, 버전 고정은 소개하되, lock 파일과 resolver, 컨테이너, CI는 후속 주제로 남겼다.
- Colab은 실행이 쉽지만 런타임 초기화와 기본 패키지 버전 변화가 있을 수 있으므로, 재현성 문제가 사라지는 것은 아니라는 관점만 반영했다.
- P2-7.6과 P2-7.7은 사용자 요청에 따라 순서를 바꾸었다. P2-7.6은 운영체제별 터미널 사용법, P2-7.7은 Python 설치 보충학습으로 분리한다.
- 사용자 요청에 따라 예시를 보강했다. 예시는 `ModuleNotFoundError`, Colab 런타임 초기화, 작은 실습 폴더 전달 상황으로 구성해 의존성 기록의 필요성을 입문자가 체감할 수 있게 했다.

## 본문에 반영한 안전한 설명

- 의존성은 내 코드가 실행되기 위해 필요한 외부 패키지로 설명할 수 있다.
- 재현성은 같은 코드를 나중에 다시 실행할 수 있는 조건으로 설명할 수 있다.
- requirements 파일은 `pip install`에 넘길 설치 항목 목록이다.
- `pip freeze`는 현재 환경의 설치 패키지와 버전을 기록하는 데 쓰일 수 있다.
- 버전 고정은 재현성을 높일 수 있지만 운영체제, Python 버전, 하드웨어, 패키지 배포 상태까지 모두 해결하지는 않는다.

## 제외한 내용

- lock 파일과 dependency resolver 상세
- `pyproject.toml` 기반 dependency groups 상세
- Poetry, uv, conda, pip-tools 비교
- Docker, Dev Container, CI 재현 환경
- 해시 기반 보안 설치
- 플랫폼별 binary wheel 문제

이 내용은 후속 실습이나 프로젝트 파트에서 필요한 만큼 다시 다루는 편이 안전하다.
