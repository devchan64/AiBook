# P2-7.6 근거 검토: 운영체제별 터미널 사용법

확인 날짜: 2026-06-24

## 사용한 주요 자료

| 자료 | 확인 내용 | 반영 위치 |
| --- | --- | --- |
| Microsoft Learn, `What is Windows Terminal?` | Windows Terminal이 Command Prompt, PowerShell, WSL의 bash 같은 명령줄 셸을 실행하는 현대적인 호스트 앱이라는 설명 | Windows에서 터미널 앱과 셸을 구분하는 설명 |
| Microsoft Learn, `What is Windows Terminal?` | Windows Terminal의 기본 단축키 예시로 `Ctrl+Shift+C`, `Ctrl+Shift+T`, `Ctrl+Tab` 언급 | 단축키 Tip에서 Windows Terminal 예시 |
| Apple Support, `Terminal User Guide` | macOS Terminal 사용 안내, 셸 스크립트와 명령 실행 문맥 | macOS Terminal 설명 |
| Apple Support, `Keyboard shortcuts in Terminal on Mac` | macOS Terminal의 새 탭, 복사, 붙여넣기, 명령줄 이동, `Tab` 자동완성, 중단 단축키 설명 | 단축키 Tip에서 macOS 예시 |
| Ubuntu Documentation, `UsingTheTerminal` | Linux/Ubuntu에서 터미널을 여는 방법, `Ctrl + Alt + T`, `pwd`, `ls`, `cd` 설명, 명령 복사 사용에 대한 입문 설명 | Linux 터미널 설명, 공통 명령, 복사 실행 주의 |
| Microsoft Learn, `Get-Location` | PowerShell에서 현재 위치 확인 명령 | Windows 위치 확인 설명 |
| Microsoft Learn, `Set-Location` | PowerShell에서 현재 작업 위치 변경 명령 | Windows 폴더 이동 설명 |
| Microsoft Learn, `Get-ChildItem` | PowerShell에서 파일과 폴더 목록 확인 명령 | Windows 파일 목록 확인 설명 |

## 작성 판단

- P2-7.2가 터미널, 셸, 작업 폴더의 개념을 설명했으므로 P2-7.6은 운영체제별 실제 사용 절차로 제한했다.
- Python 설치는 P2-7.7로 넘기고, 이 절에서는 `python --version`, `python3 --version`, `py --version`처럼 설치 여부를 확인하는 수준만 다뤘다.
- Windows에서는 Command Prompt보다 PowerShell과 Windows Terminal을 우선 설명했다. 다만 Command Prompt와 WSL도 만날 수 있음을 함께 언급했다.
- macOS/Linux는 `pwd`, `ls`, `cd` 중심으로 설명하고, Windows PowerShell은 공식 명령 이름인 `Get-Location`, `Get-ChildItem`, `Set-Location`을 함께 소개했다.
- 터미널 단축키는 운영체제와 터미널 앱에 따라 달라질 수 있으므로, 전체 목록이 아니라 `Tab`, `Ctrl+C`, 복사·붙여넣기, 새 탭 같은 입문용 단축키만 Tip으로 추가했다.
- 사용자의 요청에 따라 `Ctrl+C`, `Ctrl+V`의 혼동을 따로 설명했다. 일반 앱의 복사/붙여넣기와 터미널의 실행 중단 신호가 충돌할 수 있으므로 Windows/Linux의 `Ctrl+Shift+C/V`, macOS의 `Command+C/V`, 실행 중단용 `Ctrl+C`를 구분했다.
- 위험한 명령은 구체적 사용법을 가르치기보다 “의미를 확인하기 전에는 실행하지 않는다”는 안전 기준으로만 언급했다.

## 본문에 반영한 안전한 설명

- Windows Terminal은 여러 명령줄 셸을 실행할 수 있는 호스트 앱으로 설명할 수 있다.
- 터미널 실습 전에는 현재 위치와 파일 목록을 먼저 확인하는 것이 중요하다.
- Windows와 macOS/Linux는 경로 표기와 기본 명령이 다를 수 있다.
- 단축키는 환경마다 다를 수 있으므로 앱 메뉴나 설정에서 확인해야 한다.
- 터미널에서 `Ctrl+C`는 복사가 아니라 실행 중단으로 동작할 수 있다.
- 문서의 프롬프트 기호는 실제 입력할 명령이 아닐 수 있다.
- Colab과 로컬 PC의 실행 환경을 같은 것으로 오해하지 않아야 한다.

## 제외한 내용

- Windows Terminal 설치 절차 상세
- WSL 설치와 Linux 배포판 선택
- 셸 설정 파일과 PATH 설정 상세
- 관리자 권한 명령 사용법
- 파일 삭제, 권한 변경, 리다이렉션, 파이프, 셸 스크립트
- Python 설치 절차 상세

이 절은 터미널 실습의 진입 장벽을 낮추기 위한 보충학습이다. 운영체제별 개발 환경 세팅은 후속 보충학습이나 프로젝트 파트에서 필요한 만큼 다시 다루는 편이 안전하다.
