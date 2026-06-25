# P2-10.2 근거 검토: Jupyter, Colab, 로컬 실행의 차이

확인 날짜: 2026-06-25

## 내려받은 원문

- `.tmp/section-p2-10-1-evidence/jupyter-architecture.html`
- `.tmp/section-p2-10-1-evidence/colab-faq.html`

## 사용한 주요 자료

| 자료 | 확인 내용 | 반영 위치 |
| --- | --- | --- |
| Google Colab FAQ | Colab은 별도 설정 없이 사용할 수 있는 hosted Jupyter Notebook 서비스이며, 무료 GPU/TPU 접근을 제공하지만 자원이 보장되거나 무제한은 아니라고 설명한다. Jupyter는 Colab의 기반이 되는 오픈소스 프로젝트이고, Colab은 설치 없이 Jupyter notebooks를 사용·공유하게 해 준다고 설명한다. | Jupyter와 Colab의 관계, Colab의 장점과 제한 |
| Google Colab FAQ | Colab 노트북은 Google Drive에 저장되거나 GitHub에서 불러올 수 있고, 공유 시 텍스트, 코드, 출력, 댓글이 공유되지만 가상 머신과 커스텀 파일·라이브러리는 공유되지 않는다고 설명한다. | 공유 시 주의점, 런타임과 노트북 파일 구분 |
| Google Colab FAQ | 코드는 계정에 할당된 가상 머신에서 실행되며, 가상 머신은 일정 시간 유휴 상태가 되면 삭제되고 최대 수명이 있다고 설명한다. 사용량 제한과 GPU/TPU 종류는 시간에 따라 달라질 수 있다고 설명한다. | Colab 런타임, 자원 제한, 파일 지속성 주의 |
| Project Jupyter Architecture | Jupyter Notebook은 코드, 메타데이터, 내용, 출력을 나타내는 구조화된 데이터이며 `.ipynb` JSON 구조로 저장된다고 설명한다. 커널은 셀의 코드를 실행하고, 서버가 브라우저·파일·커널 사이를 연결한다고 설명한다. | 노트북 파일과 런타임 구분, 로컬 Jupyter 설명 |

## 작성 판단

- P2-10.1이 노트북의 학습상 장점을 설명했으므로, P2-10.2는 실행 환경 선택 기준과 혼동 지점에 집중했다.
- P2-3.4가 Colab과 로컬 PC 실행 명령 구분을 이미 다루므로, 이 절에서는 `%pip`, `python -m pip` 같은 명령 구분을 반복하지 않고 파일, 런타임, 공유, 재현성으로 확장했다.
- Colab은 현재 동향과 정책이 바뀔 수 있으므로 2026-06-25 확인 기준을 명시하고, 무료 자원과 런타임 제한을 단정적으로 고정하지 않았다.
- Jupyter, Colab, 로컬 실행을 “어느 것이 더 좋다”가 아니라 학습 목적, 파일 접근, 반복 실행, 공유, 재현성 기준으로 비교했다.

## 본문에 반영한 안전한 설명

- Jupyter는 오픈소스 노트북 도구와 생태계이고, Colab은 Jupyter 기반 hosted 서비스로 설명할 수 있다.
- 노트북 파일(`.ipynb`)과 실행 중인 런타임은 다르다.
- Colab에서 공유되는 것은 노트북 내용이고, 런타임의 임시 파일·설치 상태·개인 Drive 권한은 그대로 공유되지 않을 수 있다.
- Colab은 시작 장벽을 낮추지만 자원과 런타임이 보장되거나 무제한인 환경은 아니다.
- 로컬 Jupyter는 내 환경을 직접 통제하기 좋고, 로컬 스크립트는 반복 실행과 재사용에 유리하다.

## 제외한 내용

- Colab 세부 메뉴 사용법
- Drive mount 절차
- GPU/TPU 설정 방법
- Jupyter 설치 절차
- Jupyter 커널 메시징 프로토콜 세부
- `.ipynb` JSON 스키마 상세
- nbconvert와 자동 배포

이 내용은 이후 실습 환경, 재현성, 배포 자동화 문맥에서 필요한 범위만 다시 다룬다.
