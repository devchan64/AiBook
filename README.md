# AiBook

AiBook은 AI를 다시 배우기 위한 정적 웹 책 프로젝트입니다. AI를 처음 공부하는 사람, 예전에 AI 개론을 배웠지만 개념이 흐릿해진 사람, AI 도구는 써 봤지만 내부 원리를 더 알고 싶은 비전공자가 같은 학습 흐름을 따라갈 수 있게 구성합니다.

- 배포 페이지: [https://devchan64.github.io/AiBook/](https://devchan64.github.io/AiBook/)
- 독자용 소개: [`docs/index.md`](docs/index.md)
- 독자용 목차: [`docs/table-of-contents.md`](docs/table-of-contents.md)
- 전역 작업 기준: [`AGENTS.md`](AGENTS.md)
- 관리 문서 인덱스: [`management/README.md`](management/README.md)

이 저장소의 목표는 자료를 많이 모으는 것이 아닙니다. `AI 개론과 지형도 -> 기초 복구 -> 데이터 모델링 -> 머신러닝 -> 딥러닝 -> LLM과 생성형 AI -> 프로젝트`로 이어지는 재학습 경로를 만들고, 독자가 AI 서비스를 볼 때 어떤 개념이 어디에서 쓰이는지 설명할 수 있게 하는 것입니다.

## 책의 구성

- **Part 1. AI 개론과 지형도**: AI의 범위, 역사, 규칙과 학습의 차이, LLM 사용 경험의 기본 요소를 잡습니다.
- **Part 2. 기초 복구**: 수학, Python, 데이터 도구, 실행 환경을 AI 모델 계산을 읽는 데 필요한 만큼 복구합니다.
- **Part 3. 데이터 모델링**: 원천데이터를 학습 가능한 입력과 비교 가능한 결과 구조로 정리합니다.
- **Part 4. 머신러닝**: 문제 설정, 데이터 분리, 학습, 평가, 대표 알고리즘을 하나의 공통 구조로 봅니다.
- **Part 5. 딥러닝**: 신경망 계산, 역전파(backpropagation), CNN, RNN, attention, Transformer로 이어지는 구조를 다룹니다.
- **Part 6. LLM과 생성형 AI**: 토큰, 프롬프트, 생성 설정, 임베딩, 검색, RAG, 에이전트, 평가를 연결합니다.
- **Part 7. 프로젝트**: 앞에서 배운 개념을 작은 산출물로 만들고, 실행 로그와 평가 기준으로 검증합니다.

## 대상 독자

- AI를 처음 공부하지만, 용어와 흐름을 천천히 연결하며 배우고 싶은 독자
- 예전에 AI 개론이나 기초 과목을 배웠지만, 지금은 기억이 많이 흐릿해진 독자
- LLM, 챗봇, 이미지 생성 도구 같은 AI 서비스를 써 봤지만 내부 개념은 정리되지 않은 독자

초심자는 `대학 학사 교육을 받지 않았을 수 있는 독자`를 기준으로 잡습니다. 대학 수준의 수학, 프로그래밍, 시스템 기초를 이미 안다고 가정하지 않되, 쉬운 비유만으로 끝내지 않고 핵심 용어를 표준적인 설명과 연결합니다.

## 작성 관점

이 책은 개인적인 직관을 출발점으로 삼을 수는 있지만, 그 직관을 그대로 정답처럼 두지 않습니다. 설명은 가능한 한 다음 세 층으로 구분합니다.

- `표준적 설명`: 교과서, 논문, 공식 문서, 신뢰 가능한 자료와 연결되는 설명
- `작업 가설`: 이해를 돕는 개인적 비유나 임시 설명
- `검증 필요`: 표준 설명과 충돌하거나 근거가 아직 충분하지 않은 부분

AI 도구는 커리큘럼 구성, 자료 조사, 초안 작성, 비교 정리, 다이어그램 작성, 문서 구조화를 돕습니다. Codex는 이 과정에서 초안 생성과 검토 보조를 수행하는 LLM 에이전트 관점의 도구로 다룹니다. 다만 생성형 AI의 출력은 항상 검토 대상이며, 자연스러운 문장이라는 이유만으로 사실로 받아들이지 않습니다.

## 저장소 구조

- `docs/`: 독자에게 배포할 책 본문과 공개 자산
- `docs/index.md`: 한국어 소개 페이지
- `docs/table-of-contents.md`: 독자용 목차 설명
- `docs/parts/part-XX/`: Part별 본문
- `docs/reference/concept-glossary.md`: 개념사전
- `docs/assets/`: 본문에서 쓰는 이미지, Mermaid, 차트 자산
- `management/`: 집필 기준, 조사 자료, 근거 분석, 릴리즈노트
- `management/guidelines/`: 원고 작성, 메타데이터, 차트, 예제, 번역 가이드
- `management/release-notes/sections/`: Section 단위 개정 이력
- `.tmp/`: 외부 자료 확인용 임시 작업공간. 커밋하지 않습니다.
- `site/`, `site-dev/`: MkDocs 빌드 산출물. 명시적 지시 없이 커밋하지 않습니다.

배포 목차는 `mkdocs.yml`의 `nav`에서 관리합니다. 관리 문서와 조사 메모는 배포 목차에 연결하지 않습니다.

## 작업 기준

작업 전에는 [`AGENTS.md`](AGENTS.md)를 먼저 확인합니다. 작업 유형에 따라 다음 가이드를 함께 봅니다.

- 원고 작성과 큰 구조 수정: [`management/guidelines/manuscript-writing-workflow.md`](management/guidelines/manuscript-writing-workflow.md)
- Section ID, Version, 릴리즈노트 연결: [`management/guidelines/section-metadata-guidelines.md`](management/guidelines/section-metadata-guidelines.md)
- 릴리즈노트 파일 형식: [`management/release-notes/sections/README.md`](management/release-notes/sections/README.md)
- Python 예제: [`management/guidelines/python-example-guidelines.md`](management/guidelines/python-example-guidelines.md)
- 차트와 다이어그램: [`management/guidelines/chart-guidelines.md`](management/guidelines/chart-guidelines.md)
- 영어 번역: [`management/guidelines/english-translation-guidelines.md`](management/guidelines/english-translation-guidelines.md)
- 중국어 간체 번역: [`management/guidelines/chinese-translation-guidelines.md`](management/guidelines/chinese-translation-guidelines.md)

본문 Section을 수정했다면 제목 아래 `Section ID`와 `Version`을 확인하고, 대응 릴리즈노트를 같은 작업 안에서 갱신합니다. `docs/table-of-contents.md`와 `docs/reference/concept-glossary.md`는 전용 규칙에 따라 별도 Section 릴리즈노트를 운영하지 않습니다.

## 브랜치와 배포

- `dev`: 일반 작성과 편집 브랜치
- `main`: 배포 브랜치

일반적인 문서 작성, 초안 추가, 구조 변경, 커밋, 푸시는 `dev`에서 진행합니다. `main`에 push하면 GitHub Actions가 GitHub Pages 배포를 실행하므로, `main` 반영은 배포 작업으로 취급합니다.

## 로컬 실행

처음 환경을 준비할 때는 다음 순서로 실행합니다.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./.venv/bin/python -m mkdocs serve
```

기본 로컬 주소는 `http://127.0.0.1:8000`입니다.

개발 중 반복 확인할 때는 `mkdocs.dev.yml`을 사용하면 출력 디렉터리를 `site-dev/`로 분리하고 일부 플러그인 부담을 줄일 수 있습니다.

```bash
BUILD_ONLY_LOCALE=ko \
MKDOCS_ENABLE_GIT_REVISION=false \
MKDOCS_ENABLE_MINIFY=false \
./.venv/bin/python -m mkdocs serve -f mkdocs.dev.yml
```

이 경우 기본 로컬 주소는 `http://127.0.0.1:9000`입니다.

영어 또는 중국어 간체만 확인할 때도 같은 개발용 설정을 사용합니다.

```bash
BUILD_ONLY_LOCALE=en \
MKDOCS_ENABLE_GIT_REVISION=false \
MKDOCS_ENABLE_MINIFY=false \
./.venv/bin/python -m mkdocs serve -f mkdocs.dev.yml
```

- `BUILD_ONLY_LOCALE=ko`, `en`, `zh`처럼 지정하면 해당 locale만 빌드합니다.
- `BUILD_ONLY_LOCALE`을 지정하지 않으면 `ko`, `en`, `zh` 전체를 빌드합니다.
- `MKDOCS_ENABLE_GIT_REVISION=false`는 수정일 계산 플러그인을 끕니다.
- `MKDOCS_ENABLE_MINIFY=false`는 HTML minify를 끕니다.
- 검색 인덱스까지 끄고 싶다면 `MKDOCS_ENABLE_SEARCH=false`를 추가할 수 있습니다.

## 빌드 검증

기본 빌드 확인 명령은 다음과 같습니다.

```bash
./.venv/bin/python -m mkdocs build
```

가상환경을 활성화했더라도 시스템 `python3`와 `.venv` 패키지 경로가 섞이면 플러그인 import 문제가 날 수 있습니다. MkDocs 관련 명령은 `./.venv/bin/python -m mkdocs ...` 형식을 우선 사용합니다.

`--dirty`는 변경된 파일 중심으로 다시 빌드해 체감 속도를 줄일 수 있지만, 이 저장소는 `i18n` 플러그인, 큰 `nav`, `pymdownx.snippets` 기반 Mermaid include를 함께 사용합니다. Mermaid 원본을 `docs/assets/.../*.mmd`에서 수정할 때는 `--dirty` 없이 일반 `serve`로 확인하는 편이 안전합니다.

## GitHub Pages 배포

배포 페이지는 [https://devchan64.github.io/AiBook/](https://devchan64.github.io/AiBook/)입니다.

1. GitHub 저장소의 `Settings > Pages`에서 `Build and deployment`의 `Source`를 `GitHub Actions`로 설정합니다.
2. `main` 브랜치에 push하면 `.github/workflows/deploy.yml`이 정적 사이트를 빌드하고 GitHub Pages에 배포합니다.
