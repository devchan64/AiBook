# P2-14.1 Git은 변경 이력을 관리하는 도구

> Section ID: `P2-14.1`
> Version: `v2026.09.15`

## 파일 저장과 변경 기록

파일을 저장하면 현재 상태가 남습니다. 하지만 이전 상태가 왜 바뀌었는지, 어떤 파일들이 함께 바뀌었는지는 자동으로 설명되지 않습니다.

예를 들어 다음 작업을 했다고 가정합니다.

- 한 절의 원고를 작성했다.
- 그래프 생성 스크립트를 추가했다.
- 출력 이미지 두 개를 만들었다.
- 사이트 목차 설정을 수정했다.

이 네 가지는 따로 떨어진 작업처럼 보이지만, 실제로는 “한 절의 그래프 설명과 연결 자산을 함께 반영한다”는 하나의 의미 있는 변경 묶음입니다.

Git은 이런 묶음을 커밋(commit)으로 기록합니다.

커밋은 그 시점의 추적 대상 파일 상태를 가리키는 스냅샷입니다. 변경하지 않은 파일도 그 상태의 일부이며, 이전 커밋과 비교하면 어떤 줄이 달라졌는지 볼 수 있습니다. 커밋 메시지에는 변경 목적을 쓰지만, Git이 파일의 의미나 수정 이유를 자동으로 판단하지는 않습니다.

## 이전 상태와 변경 이유

버전 관리(version control)는 파일의 이전 상태를 다시 찾고 변경 내용을 비교하게 해 줍니다. 변경 이유는 작성자가 커밋 메시지 등에 남겨야 합니다. 기록을 읽으면 다음을 확인할 수 있습니다.

- 어떤 파일이 바뀌었는가?
- 왜 바뀌었는가?
- 어떤 파일들이 함께 바뀌었는가?
- 특정 설명은 언제 들어왔는가?
- 문제가 생겼다면 어느 변경 이후에 생겼는가?

Git 공식 책은 버전 관리를 시간이 지나며 파일 변화 기록을 남기고, 나중에 특정 버전을 다시 불러올 수 있게 하는 시스템으로 설명합니다. 문서와 예제 코드도 이런 방식으로 이전 상태를 확인할 수 있습니다.

## 작업 트리·스테이징·저장소

작업 트리(working tree)는 편집 중인 파일이 있는 곳이고, 스테이징 영역(staging area)은 다음 커밋에 넣을 파일 내용을 담는 곳입니다. 커밋하면 스테이징된 상태가 저장소(repository)의 이력에 남습니다.

```mermaid
--8<-- "assets/part-02/chapter-14/git-three-areas-flow-ko.mmd"
```

이 흐름에서 중요한 점은 `저장`과 `커밋`이 다르다는 것입니다.

파일 저장은 편집기에서 현재 파일 내용을 디스크에 쓰는 일입니다. 커밋은 그중 의미 있는 변경 묶음을 저장소 이력에 기록하는 일입니다.

이 작업은 인터넷 연결 없이 로컬 컴퓨터에서도 가능합니다. Git은 버전 관리 프로그램이고, GitHub는 Git 저장소를 온라인에서 보관하고 협업하게 하는 서비스입니다. 로컬 커밋만 만들면 GitHub에 자동으로 올라가지는 않습니다.

## 상태 확인: git status

Git 작업을 할 때 가장 먼저 확인하는 명령은 보통 `git status`입니다.

아래 명령의 `docs/...` 경로는 이 책의 저장소 루트에서 실행하는 예입니다. 아직 Git 저장소가 아닌 폴더에서는 상태를 읽을 수 없으며, 새 저장소를 만드는 실습은 뒤의 `75 → 80 → 85 기록 실습`에서 다룹니다.

```bash
git status
```

이 명령은 다음 질문에 답합니다.

- 어떤 파일이 수정되었는가?
- 새로 생긴 파일이 있는가?
- 이번 커밋에 포함하기로 고른 파일이 있는가?
- 현재 브랜치(branch)는 무엇인가?

파일 이름 앞 두 칸을 읽으면 스테이징 여부를 구분할 수 있습니다.

```bash
git status --short
```

충돌이 없는 일반 편집 상태에서는 첫째 칸이 직전 커밋과 스테이징 영역의 차이, 둘째 칸이 스테이징 영역과 작업 트리의 차이를 나타냅니다. 아래 `·`는 빈칸을 눈에 보이게 표시한 기호이며 실제 출력에는 공백이 나옵니다.

| 표시 | 파일 상태 | 일반 커밋에 들어가는 내용 |
| --- | --- | --- |
| `??` | 아직 추적하지 않는 새 파일 | 없음 |
| `·M` | 추적 중인 파일을 수정했지만 미스테이징 | 새 수정은 제외 |
| `M·` | 수정 내용을 스테이징 | 스테이징한 수정 |
| `MM` | 스테이징한 뒤 같은 파일을 다시 수정 | 먼저 스테이징한 수정만 |
| `A·` | 새 파일을 스테이징 | 스테이징한 새 파일 내용 |

`git diff` 출력이 비어 있어도 `??` 파일이 있을 수 있습니다. 일반적인 `git diff`는 아직 추적하지 않는 파일의 내용을 보여 주지 않으므로 `status`도 함께 확인합니다.

## 변경 선택: git add

`git add`는 파일을 즉시 영구 저장한다는 뜻이 아닙니다. 이번 커밋에 포함할 변경을 스테이징 영역(staging area)에 올리는 일입니다.

```bash
git add docs/parts/part-02/chapter-14/section-01.md
```

`git add`는 실행한 시점의 파일 내용을 스테이징합니다. 이후 같은 파일을 더 수정하면 새 수정은 자동으로 스테이징되지 않습니다. 파일이 여러 개 바뀌었더라도 한 커밋에 모두 넣을 필요는 없습니다. 서로 다른 목적의 변경이면 나누어 커밋하는 편이 나중에 읽기 쉽습니다.

예를 들어 다음 두 작업은 가능한 한 나누어 기록합니다.

| 변경 | 커밋을 나누는 이유 |
| --- | --- |
| Chapter 14 원고 작성 | 책 본문 추가라는 목적 |
| CSS 레이아웃 수정 | 화면 표시 개선이라는 목적 |

두 변경을 한 커밋에 넣으면 나중에 “왜 이 CSS가 바뀌었는가?”를 추적하기 어려워집니다.

실수로 고른 파일을 이번 커밋에서 빼려면, 기존 커밋이 있는 저장소에서 다음처럼 스테이징만 해제할 수 있습니다.

```bash
git restore --staged -- docs/parts/part-02/chapter-14/section-01.md
```

`--staged`는 작업 트리의 수정 내용을 그대로 두고 다음 커밋에 넣을 선택만 되돌립니다. 이 옵션 없이 실행하는 `git restore`는 파일 내용 자체를 되돌릴 수 있으므로 같은 명령으로 취급하면 안 됩니다.

## 이력 기록: git commit

`git commit`은 스테이징한 변경을 저장소 이력에 남깁니다.

```bash
git commit -m "docs(part2): add git version control introduction"
```

커밋 메시지는 단순 메모가 아닙니다. 나중에 변경 이력을 읽는 사람에게 “이 변경이 무엇인지” 알려 주는 제목입니다.

좋은 커밋 메시지는 보통 다음 조건을 만족합니다.

- 무엇을 바꿨는지 알 수 있다.
- 너무 넓은 표현을 피한다.
- 파일명보다 변경 목적을 드러낸다.
- 나중에 `git log`에서 읽어도 의미가 통한다.

나쁜 예시는 다음과 같습니다.

```bash
git commit -m "update"
```

이 메시지는 무엇을 업데이트했는지 알려 주지 않습니다.

## 이력 확인: git log

커밋이 쌓이면 `git log`로 이력을 확인할 수 있습니다.

```bash
git log --oneline
```

이 명령은 커밋 목록을 짧게 보여 줍니다. 각 줄에는 커밋을 식별하는 짧은 해시와 메시지 제목이 나옵니다.

`HEAD`는 현재 체크아웃한 커밋을 가리키며, 보통 현재 브랜치를 통해 그 커밋을 참조합니다. 가장 최근 커밋에서 바뀐 파일과 실제 문장을 확인하려면 다음 두 명령을 사용할 수 있습니다.

```bash
git show --stat HEAD
git show HEAD -- docs/parts/part-02/chapter-14/section-01.md
```

첫 명령은 파일별 변경 요약을, 둘째 명령은 해당 파일의 변경 내용을 보여 줍니다. 해시는 변경량이나 품질 점수가 아니라 특정 기록을 찾는 식별자입니다.

학습 문서 프로젝트에서는 `git log`가 다음 질문에 도움을 줍니다.

- 이 절은 언제 추가되었는가?
- 어떤 커밋에서 목차가 바뀌었는가?
- 특정 그림 파일은 어떤 원고와 함께 추가되었는가?
- 배포 전에 어떤 변경이 들어갔는가?

## 원고·코드·이미지의 연결

문서 프로젝트는 단순한 완성 문서가 아니라 학습 과정의 결과입니다. 원고, 조사 메모, 예제 코드, 이미지, 배포 설정이 함께 바뀝니다. 예를 들어 점수 임계값을 75에서 80으로 바꿨다면 조건을 담은 코드와 변경된 결과 설명을 같은 커밋에 담아 비교할 수 있습니다.

Git을 사용하면 다음 관계를 남길 수 있습니다.

| 산출물 | Git으로 남길 수 있는 질문 |
| --- | --- |
| 원고 Markdown | 어떤 설명이 언제 추가되었는가 |
| 조사 메모 | 어떤 자료를 근거로 삼았는가 |
| 예제 코드 | 어떤 출력 이미지를 만들었는가 |
| 이미지 파일 | 어떤 코드나 절과 연결되는가 |
| 사이트 내비게이션 설정 | 어떤 문서가 배포 목차에 들어갔는가 |

임시 캐시나 가상환경처럼 기록하지 않을 파일은 `.gitignore`에 패턴을 적어 관리할 수 있습니다. 이 책의 `.tmp/`, `.venv/` 같은 폴더가 그 예입니다. 다만 `.gitignore`에 추가해도 이미 추적 중인 파일이 이력에서 사라지지는 않습니다. 또한 코드와 이미지가 같은 커밋에 있다는 사실만으로 그 코드가 이미지를 생성했다는 관계가 검증되는 것은 아닙니다. 실행 명령과 입력 조건도 남겨야 합니다.

## 사례 1. add 이후 원고를 다시 수정했다면

원고의 점수 기준을 75에서 80으로 고친 뒤 `git add`를 실행했다고 합시다. 그 후 기준을 85로 한 번 더 고쳐 파일만 저장하면 작업 트리에는 85, 스테이징 영역에는 80이 있습니다. 이 상태에서 일반적인 `git commit -m ...`을 실행하면 기록되는 내용은 80입니다.

```bash
git diff -- docs/parts/part-02/chapter-14/section-01.md
git diff --cached -- docs/parts/part-02/chapter-14/section-01.md
```

첫 명령은 스테이징한 80과 현재 파일의 85를 비교합니다. 둘째 명령은 직전 커밋의 75와 스테이징한 80을 비교합니다. 현재 파일의 85를 기록하려면 해당 파일에 `git add`를 다시 실행한 뒤 커밋합니다.

원고와 그래프 생성 코드가 같은 기준을 설명한다면 둘을 함께 선택해야 합니다. 원고만 85로 바뀌고 코드는 75를 사용하면 이력은 남더라도 설명과 실행 결과가 맞지 않습니다. 커밋 전에 `git diff --cached`로 이번에 기록할 내용이 같은 변경 목적을 이루는지 확인합니다.

## 75 → 80 → 85 기록 실습

Git이 설치된 환경의 Bash에서 실행합니다. 기존 프로젝트 바깥에 아직 없는 `git-record-practice` 폴더를 만듭니다. 이름과 이메일 설정은 이 연습 저장소에만 적용되는 커밋 작성자 정보이며 온라인 로그인 정보가 아닙니다.

```bash
mkdir git-record-practice
cd git-record-practice
git init -b practice
git config user.name "Book Learner"
git config user.email "learner@example.com"
printf 'threshold=75\n' > lesson.txt
git add -- lesson.txt
git commit -m "Record threshold 75"
printf 'threshold=80\n' > lesson.txt
git add -- lesson.txt
printf 'threshold=85\n' > lesson.txt
git status --short
git diff -- lesson.txt
git diff --cached -- lesson.txt
git commit -m "Raise threshold to 80"
git show HEAD:lesson.txt
cat lesson.txt
```

`printf`는 지정한 내용을 파일에 쓰며 `\n`은 줄바꿈입니다. `>`는 해당 연습 파일 내용을 새 내용으로 교체합니다. 첫 커밋 뒤 80을 스테이징하고 85를 저장했으므로 상태는 `MM lesson.txt`입니다. 두 번째 커밋 뒤 `git show HEAD:lesson.txt`는 기록된 파일 전체에서 `threshold=80`을, `cat lesson.txt`는 작업 파일에서 `threshold=85`를 보여 줍니다.

| 시점 | 직전 커밋 | 스테이징 영역 | 작업 트리 |
| --- | --- | --- | --- |
| 첫 커밋 직후 | 75 | 75 | 75 |
| 80을 add한 뒤 85 저장 | 75 | 80 | 85 |
| 두 번째 커밋 직후 | 80 | 80 | 85 |

이어서 85를 스테이징하고 `git diff --cached`에서 `80 → 85`를 확인한 뒤 기록합니다.

```bash
git add -- lesson.txt
git diff --cached -- lesson.txt
git commit -m "Raise threshold to 85"
git status --short
git log --oneline
```

다른 변경이 없다면 마지막 상태 출력은 비어 있고 로그에는 커밋 세 개가 나옵니다. 85를 저장한 후 `git add`를 생략했다면 왜 85가 바로 커밋되지 않는지 각 영역의 값으로 설명해 봅니다.

## 체크리스트

- Git이 파일 상태와 변경 이력을 기록하는 방식을 설명할 수 있는가?
- 파일 저장과 Git 커밋의 차이를 설명할 수 있는가?
- 작업 디렉터리, 스테이징 영역, 저장소를 구분할 수 있는가?
- 커밋(commit)은 의미 있는 변경 묶음이라고 말할 수 있는가?
- `git status`, `git add`, `git commit`, `git log`의 역할을 설명할 수 있는가?
- 한 커밋에 하나의 목적을 담아야 하는 이유를 설명할 수 있는가?
- `git add` 이후 다시 수정한 내용이 자동으로 커밋되지 않는 이유를 설명할 수 있는가?
- `MM`과 `??`를 구분하고, `git diff`와 `git diff --cached`의 비교 대상을 말할 수 있는가?
- 스테이징 해제와 작업 파일 내용 복원의 차이를 설명할 수 있는가?
- 학습 문서 프로젝트에서 Git이 원고, 코드, 이미지, 조사 메모의 연결을 추적하는 기록 도구라는 점을 설명할 수 있는가?

## 출처와 참고 자료

- [Pro Git, About Version Control](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control){: target="_blank" rel="noopener noreferrer" } 확인 날짜: 2026-09-15. 버전 기록과 이전 상태 조회.
- [Pro Git, What is Git?](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F){: target="_blank" rel="noopener noreferrer" } 확인 날짜: 2026-09-15. 스냅샷과 로컬 작업.
- [GitHub Docs, What is GitHub?](https://docs.github.com/en/get-started/start-your-journey/what-is-github){: target="_blank" rel="noopener noreferrer" } 확인 날짜: 2026-09-15. Git과 온라인 호스팅 서비스의 구분.
- [Git project, git-status](https://git-scm.com/docs/git-status){: target="_blank" rel="noopener noreferrer" } 확인 날짜: 2026-09-15. 파일 상태와 두 칸의 짧은 출력 형식.
- [Git project, git-add](https://git-scm.com/docs/git-add){: target="_blank" rel="noopener noreferrer" } 확인 날짜: 2026-09-15. 실행 시점의 파일 내용 스테이징.
- [Git project, git-diff](https://git-scm.com/docs/git-diff){: target="_blank" rel="noopener noreferrer" } 확인 날짜: 2026-09-15. 작업 트리·인덱스·커밋 비교 대상.
- [Git project, git-commit](https://git-scm.com/docs/git-commit){: target="_blank" rel="noopener noreferrer" } 확인 날짜: 2026-09-15. 인덱스의 상태를 새 커밋으로 기록.
- [Git project, git-restore](https://git-scm.com/docs/git-restore){: target="_blank" rel="noopener noreferrer" } 확인 날짜: 2026-09-15. 스테이징 해제와 작업 트리 복원의 구분.
- [Git project, git-show](https://git-scm.com/docs/git-show){: target="_blank" rel="noopener noreferrer" } 확인 날짜: 2026-09-15. 커밋 변경과 특정 시점의 파일 조회.
- [Git project, gitignore](https://git-scm.com/docs/gitignore){: target="_blank" rel="noopener noreferrer" } 확인 날짜: 2026-09-15. 미추적 파일 제외 규칙과 이미 추적한 파일의 경계.
- [Git project, git-init](https://git-scm.com/docs/git-init){: target="_blank" rel="noopener noreferrer" } 확인 날짜: 2026-09-15. 실습 저장소와 초기 브랜치 생성.
