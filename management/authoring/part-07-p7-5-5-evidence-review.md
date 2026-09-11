# P7-5.5 근거자료 검수

- 확인일: 2026-09-11
- 대상: `docs/parts/part-07/chapter-05/section-05.md`, Version `v2026.09.11`
- 범위: 외부 모델 카드, 현행 원고의 실행 기록과 파일 연결, 통합 관리노트의 현행 경로. 이번 작업에서는 GPU 재생성이나 새 이미지 육안 검수를 수행하지 않았다.

## 근거의 역할

- 모델 카드: 입력 형식·버전·트리거·제작자 사용 안내의 근거다. 실제 장면의 품질을 입증하지 않는다.
- 실행 JSON: 실제 입력·출력과 생성 조건의 근거다. 코드가 이후 수정됐다면 기록 당시 해시를 보존하며 현재 코드로 덮어쓰지 않는다.
- 원고의 이미지 비교 판단: B 얼굴 불일치, 소품 유지, 색조 변화 등 해당 실행에 한정한 관찰이다. LoRA 단독 효과나 일반적인 성공률로 확대하지 않는다.

## 확인 결과와 정리

- BFS Head V5 original은 2511용이며 인물 이미지 → 얼굴 참조 순서다. 원고의 입력 순서와 일치한다. 다른 버전의 반대 순서 예제를 섞지 않는다.
- DeLight 카드의 중립 조명 트리거가 원고와 일치한다. 야외 배경이 희거나 비워질 수 있다는 안내를 원고 관찰과 연결했다.
- Relight 카드의 2509 기반과 조명 트리거를 확인했다. Lightning 병용 안내와 실제 원고의 미사용 조건을 구분하는 설명을 유지했다.
- Grounding DINO의 대상 검출과 SAM 2.1의 점·상자 기반 분리 역할을 구분했다. 사용자 선택 좌표와 경계 후처리는 로컬 설정·코드의 근거다.
- 통합 관리노트에서 현행으로 기술하던 그림자 포함 컷아웃·2단계 착장 경로를 현재 분리 → 아이덴티티 → BFS → DeLight → 합성 → 텍스트 Relight 흐름으로 갱신했다.
- 원고의 로컬 링크와 JSON 구문은 정상이다. JSON 42개를 순회해 동일 객체의 `path`/`sha256` 또는 파일 필드/`*_sha256`으로 식별되고 파일이 존재하는 118쌍을 대조했으며 불일치는 없었다. 이 수치는 중복 파일을 포함하며, 모든 중첩 스키마·모델 가중치·코드 이력을 완전 검증했다는 뜻은 아니다.
- 삭제한 결과를 언급하는 비교 문장은 과거 관찰로 유지한다. 해당 이미지를 이번에 다시 확인한 것으로 표현하지 않는다. 현행 원고에서 빠진 것만으로 실험 코드나 이력 자료를 삭제하지 않았다.

## 누락 검수 후 보강

- 직접 아이덴티티 적용 A·B·C Mira와 C 조연의 실행 JSON 네 개를 결과 표 밖의 개별 링크로 추가했다. 파일 존재와 JSON 구문을 확인했다.
- C 엘리베이티드 BFS, B 30스텝 BFS, 두 이미지 Relight의 미보존 비교 자료는 당시 관찰임을 원고에 명시했다. 위 42개 JSON·118쌍 해시 검사는 보강 전 범위이며 새 네 링크까지 검사한 수치로 확대하지 않는다.

## 원문 확인 기록

Hugging Face의 각 저장소 `raw/main/README.md`를 내려받아 확인했다. BFS 웹 페이지 열기는 실패했으나 raw 원문은 정상적으로 확인했다. 원문은 `.tmp/p7-5-5-evidence-20260911/`에 보관하고 커밋하지 않는다. 아래 해시는 확인한 문서의 해시이며 모델 가중치 해시가 아니다. 라이선스는 카드 메타데이터 표기를 기록한 것으로, 모든 파생 산출물의 권리를 보장한다는 의미는 아니다.

| 제작자 / 모델 카드 | 표시 라이선스 | 원문 SHA-256 |
| --- | --- | --- |
| [IDEA-Research/grounding-dino-tiny](https://huggingface.co/IDEA-Research/grounding-dino-tiny) | apache-2.0 | `cf46f74c7b6850f1d5cbe406028324d8798148726016d46a69a365b4a2d3e89f` |
| [Qwen/Qwen-Image-Edit-2509](https://huggingface.co/Qwen/Qwen-Image-Edit-2509) | apache-2.0 | `43794458d2fafed26f7910459eb716589b4ae2020bf1ac37c7f37510d2ca8c0e` |
| [Qwen/Qwen-Image-Edit-2511](https://huggingface.co/Qwen/Qwen-Image-Edit-2511) | apache-2.0 | `9724c194bef2a6d821090f0cd65774962e8f77e3acbfb2a7cbbdd58c92049902` |
| [dx8152/Qwen-Image-Edit-2509-Relight](https://huggingface.co/dx8152/Qwen-Image-Edit-2509-Relight) | apache-2.0 | `36e287867a5ef04e8ee0fac5a778a89a41b46b56845d4642154af3c26d7e5d4e` |
| [facebook/sam2.1-hiera-small](https://huggingface.co/facebook/sam2.1-hiera-small) | apache-2.0 | `6ec2d54879e41ad876d8cded0d641e8bc6ab74d5e095a73afc3f8406372ee6e9` |
| [mr2along/BFS](https://huggingface.co/mr2along/BFS) | mit | `cfa9d5771edec2e1bc5cdac683bbe36d491d75fc67a43b6fa3f47664053d7afe` |
| [prithivMLmods/QIE-2511-Studio-DeLight](https://huggingface.co/prithivMLmods/QIE-2511-Studio-DeLight) | apache-2.0 | `15d1fd6826d98c9b9b34926b18271316a2ae47a4fc77d8e7f5d5cabcb20a59e5` |

## 누락 근거 재생성 — 2026-09-11

앞선 미보존 표기는 재생성 전 검수 이력이다. 다음 세 조건을 로컬 RTX 5070 Laptop GPU에서 순차 실행하고 결과를 원고에 연결했다. 과거 삭제 파일과의 픽셀 동일성은 확인할 수 없으며, 새 실행 근거로 보존한다.

| 비교 | 새 실행 조건 | 관찰 |
| --- | --- | --- |
| C 엘리베이티드 BFS | 기존 토르소의 `(260, 40, 900, 680)` 크롭, 2511 BFS V5, 10스텝, seed 62294 | 아이레벨 결과와 책·착장·자세는 비슷하지만 눈과 헤어 형태가 다름 |
| B 로우뷰 +45° BFS | 기존 low45-v4 입력·참조·프롬프트, 30스텝, seed 62294 | 기존 10스텝에 비해 얼굴 일치도의 뚜렷한 개선은 보이지 않음 |
| B 두 이미지 Relight | B 합성 + 최초 B 씬, 2509 Relight 강도 1.0, 10스텝, seed 62294 | 노을 반영과 함께 긴 머리 및 왼쪽 아래 추가 신발 유사 형태 발생 |

세 결과는 `evidence-repeat-v1` 이름과 개별 JSON으로 보존한다. C 크롭과 좌표 JSON도 복원했다. Relight의 `--lighting-image-reference`는 비교용이며 기존 text-v2 기본 조건은 유지한다. 현재 채택한 BFS·DeLight·합성·text-v2 결과는 교체하지 않았다.
