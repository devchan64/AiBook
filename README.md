# AiBook

AiBook은 AI를 처음 배우는 사람부터, 예전에 배웠지만 개념이 흐릿해진 사람, AI 도구를 써 봤지만 더 깊이 이해하고 싶은 비전공자까지 함께 읽을 수 있게 설계한 재학습용 정적 웹 책 프로젝트입니다.

배포 페이지: [https://devchan64.github.io/AiBook/](https://devchan64.github.io/AiBook/)

이 저장소는 단순한 자료 모음이 아니라, `AI 개론과 지형도 -> 기초 복구 -> 데이터 모델링 -> 머신러닝 -> 딥러닝 -> LLM과 생성형 AI -> 프로젝트`로 이어지는 재학습 경로를 책처럼 읽을 수 있게 만드는 것을 목표로 합니다. 특히 `AI`, `머신러닝(machine learning)`, `딥러닝(deep learning)`, `생성형 AI(generative AI)`, `LLM(large language model)`, `에이전트(agent)`가 서로 어떻게 연결되는지 다시 설명할 수 있는 상태로 돌아가는 것을 목표로 합니다. 또한 개인의 경험적 지식과 직관을 검토 가능한 설명과 근거 위에서 다시 정리해, 더 넓게 재사용할 수 있는 일반화된 지식으로 업데이트하는 것도 이 프로젝트의 중요한 목적입니다.

## 대상 독자

- AI를 처음 공부하지만, 용어와 흐름을 천천히 연결하며 배우고 싶은 독자
- 예전에 AI 개론이나 기초 과목을 배웠지만, 지금은 기억이 많이 흐릿해진 독자
- LLM, 챗봇, 이미지 생성 도구 같은 AI 서비스를 써 봤지만 내부 개념은 정리되지 않은 독자

이 저장소에서 초심자는 `대학 학사 교육을 받지 않았을 수 있는 독자`를 기준으로 잡습니다. 그래서 대학 수준의 수학, 프로그래밍, 시스템 기초를 모른다고 가정해도 따라올 수 있어야 합니다.

## 책의 범위

- Part 1: AI 전체 지형, 핵심 용어, 역사적 흐름, 서비스 구조, 윤리·저작권·보안 같은 기본 지도를 잡습니다.
- Part 2: 수학, Python, 실행 환경, 데이터 도구, 시각화, Git 같은 기초를 복구합니다.
- Part 3: 원천데이터를 샘플, 데이터셋, 특징, 기준선, 해석 가능한 구조로 바꾸는 데이터 모델링을 다룹니다.
- Part 4: 머신러닝의 문제 설정, 학습, 검증, 평가, 대표 알고리즘을 흐름 중심으로 다룹니다.
- Part 5: 신경망, 역전파(backpropagation), CNN, RNN, Attention, Transformer 같은 딥러닝 핵심 구조를 다룹니다.
- Part 6: 토큰, 임베딩, 사전학습, 프롬프트, RAG, 도구 사용, 에이전트, MCP, 평가까지 LLM과 생성형 AI의 본류를 다룹니다.
- Part 7: 작은 프로젝트와 문서화로 앞에서 배운 내용을 검증하고 재사용 가능한 학습 기록으로 정리합니다.

이 저장소는 처음부터 특정 프레임워크의 세부 API, 대규모 운영 최적화, 연구용 수식 전개 전체를 빠르게 밀어 넣는 방향을 목표로 하지 않습니다. 먼저 `왜 필요한가`, `문제와 입력·출력은 무엇인가`, `핵심 원리는 무엇인가`를 설명한 뒤 세부 구현으로 이동합니다.

## AI로 만들어지는 책

이 책은 AI 도구를 사용해 만들어집니다. 사람은 방향과 검토 기준을 세우고, AI는 커리큘럼 구성, 자료 조사, 초안 작성, 다이어그램 작성, 문서 구조화를 돕습니다.

따라서 이 책에는 틀린 내용, 불완전한 설명, 과도하게 단순화된 해석이 포함될 수 있습니다. 생성형 AI가 만든 문장은 자연스러워 보여도 근거가 없을 수 있습니다. 이 저장소에서 중요한 일은 그럴듯한 문장을 늘리는 것이 아니라, 각 문장이 실제 근거를 가지는지 확인하고 잘못된 설명을 고치는 것입니다.

이 과정에서 Codex는 핵심 협업 도구로 사용됩니다. Codex는 초안 생성과 검토 보조를 수행하는 LLM 에이전트 관점의 도구로 다루며, 그 역할과 한계는 `management/` 아래 관리 문서에서 계속 정리합니다.

## 설명 원칙

이 저장소는 개인적인 이해를 출발점으로 삼을 수는 있지만, 그 직관을 그대로 정답처럼 두지 않습니다. 설명은 가능한 한 다음 세 층으로 구분합니다.

- `표준적 설명`: 교과서, 논문, 공식 문서, 신뢰 가능한 자료와 연결되는 설명
- `작업 가설`: 이해를 돕는 개인적 비유나 임시 설명
- `검증 필요`: 표준 설명과 충돌하거나 근거가 아직 충분하지 않은 부분

## 저장소 구조

- 독자에게 배포할 책 본문은 `docs/` 아래 Markdown 파일로 작성합니다.
- Part 본문은 `docs/parts/part-XX/` 아래에 둡니다.
- 집필 기준, 조사 자료, 작성 원칙 같은 관리자료는 `management/` 아래에 둡니다.
- 목차는 `mkdocs.yml`의 `nav`에서 관리합니다.
- `mkdocs.yml`의 `nav`에는 배포할 책 본문만 연결합니다.
- `.tmp/`는 외부 자료 확인용 임시 작업공간이며 커밋하지 않습니다.
- `site/`는 MkDocs 빌드 산출물이며 명시적 지시 없이 커밋하지 않습니다.

## 작성 원칙

- 설명은 가능한 한 `왜 필요한가 -> 핵심 원리는 무엇인가 -> 어떻게 확인할 수 있는가`의 흐름을 따릅니다.
- 처음 등장하는 핵심 용어는 필요한 경우 `한국어(English)`로 병기합니다.
- 초심자를 위해 짧은 직관, 작은 표, 간단한 도식, 실행 결과 예시를 우선 사용합니다.
- 외부 자료를 참고하거나 인용한 경우 문서 하단에 출처를 남깁니다.
- 차트와 다이어그램은 가능한 한 Mermaid, SVG, Python 등 오픈소스 기반 도구로 작성합니다.
- 정적 사이트에서 렌더링 가능한 형태로 관리합니다.

## 브랜치 운영

- `main`: 배포 브랜치입니다. `main`에 push되면 GitHub Actions를 통해 GitHub Pages 배포가 실행됩니다.
- `dev`: 일반 작성과 편집 작업을 진행하는 브랜치입니다.

일반적인 문서 작성, 구조 변경, 초안 추가는 `dev` 브랜치에서 진행합니다. 검토가 끝난 변경만 `main`으로 반영합니다.

## 로컬 실행

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./.venv/bin/python -m mkdocs serve
```

브라우저에서 `http://127.0.0.1:8000`을 열어 확인합니다.

배포 기준 설정은 `mkdocs.yml`, 개발 중 반복 확인용 진입점은 `mkdocs.dev.yml`입니다. 개발용 설정은 배포 설정을 상속하면서 출력 디렉터리를 `site-dev/`로 분리합니다.

수정 중 반복 확인할 때는 다음 명령을 우선 사용합니다.

```bash
BUILD_ONLY_LOCALE=ko \
MKDOCS_ENABLE_GIT_REVISION=false \
MKDOCS_ENABLE_MINIFY=false \
./.venv/bin/python -m mkdocs serve -f mkdocs.dev.yml
```

이 경우 브라우저에서는 `http://127.0.0.1:9000`을 열어 확인합니다.

영문이나 중국어만 확인할 때도 같은 개발용 설정 파일을 사용합니다.

```bash
BUILD_ONLY_LOCALE=en \
MKDOCS_ENABLE_GIT_REVISION=false \
MKDOCS_ENABLE_MINIFY=false \
./.venv/bin/python -m mkdocs serve -f mkdocs.dev.yml
```

- `BUILD_ONLY_LOCALE=ko`처럼 실행하면 개발 중에는 해당 locale만 빌드할 수 있어 다국어 전체 빌드보다 가볍게 확인할 수 있습니다.
- `BUILD_ONLY_LOCALE`를 지정하지 않으면 기존처럼 `ko`, `en`, `zh` 전체를 빌드합니다.
- `MKDOCS_ENABLE_GIT_REVISION=false`는 수정일 계산 플러그인을 끄고, `MKDOCS_ENABLE_MINIFY=false`는 HTML minify를 꺼서 개발 중 재빌드 부담을 줄입니다.
- 검색 인덱스까지 끄고 싶다면 `MKDOCS_ENABLE_SEARCH=false`를 추가할 수 있습니다. 다만 이 경우 로컬 검색 UI 확인은 함께 생략됩니다.
- `-w docs/parts`는 보통 필요 없습니다. `mkdocs serve`는 기본적으로 `docs/` 아래를 감시하고, `-w`는 추가 감시 경로를 더할 때 사용합니다.

### `--dirty` 사용 메모

- `--dirty`는 변경된 파일 중심으로 다시 빌드해 체감 속도를 줄일 수 있습니다.
- 다만 이 저장소는 `i18n` 플러그인, 큰 `nav`, `pymdownx.snippets` 기반 외부 Mermaid `.mmd` include를 함께 사용합니다.
- 그래서 `--dirty`를 써도 완전히 `수정한 파일 하나만` 처리되는 수준은 아니며, 외부 `.mmd` 자산 변경이 포함된 경우에는 감지는 되더라도 해당 본문 페이지가 다시 렌더링되지 않을 수 있습니다.
- 특히 Mermaid 원본을 `docs/assets/.../*.mmd`에서 수정할 때는 `--dirty` 없이 일반 `serve`로 확인하는 편이 안전합니다.

## 빌드 검증

```bash
./.venv/bin/python -m mkdocs build
```

현재 로컬 환경에서는 시스템 `python3`와 `.venv` 패키지 경로가 섞이면 플러그인 import 문제가 날 수 있습니다. 가상환경을 활성화했더라도 위처럼 `./.venv/bin/python -m mkdocs ...` 형식으로 실행하는 편이 안전합니다.

## GitHub Pages 배포

배포 페이지: [https://devchan64.github.io/AiBook/](https://devchan64.github.io/AiBook/)

1. GitHub 저장소의 `Settings > Pages`에서 `Build and deployment`의 `Source`를 `GitHub Actions`로 설정합니다.
2. `main` 브랜치에 push하면 `.github/workflows/deploy.yml`이 정적 사이트를 빌드하고 GitHub Pages에 배포합니다.
