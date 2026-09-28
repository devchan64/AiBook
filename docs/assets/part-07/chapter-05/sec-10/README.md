# P7-5.10 캐릭터 일관성을 위한 LoRA 자산

## 기준 파일 4개

| 역할 | 기준 파일 |
| --- | --- |
| 이미지 생성 코드 | [p7_5_10_generate_supplements.py](p7_5_10_generate_supplements.py) |
| 이미지 생성 조건·관리번호·선택·경로 호환 정보 | [p7-5-10-image-generation.json](p7-5-10-image-generation.json) |
| 후보 선택·데이터셋 준비·LoRA 학습 코드 | [p7_5_10_mira_lora.py](p7_5_10_mira_lora.py) |
| 확정 데이터셋·학습 설정 | [p7-5-10-paired-dataset.json](p7-5-10-paired-dataset.json) |

생성 JSON의 `management_index`는 528개 관리번호를 `rules`의 조건 ID에 연결한다. 실행 범위는 `selection`에서 관리번호로 지정하거나 CLI의 `--rule`·`--ids`로 좁힌다. 기존 이미지와 제외 항목은 재생성하지 않는다. 단순 토르소 목표는 5.2 원본을 재사용한다.

데이터셋 JSON의 `items`는 확정 366쌍(학습 347·검증 19), `training_config`는 학습 설정이다. 입력·목표 결과 ID는 `sha256:<전체 이미지 해시>`로 통일한다. 실제 파일은 `training-images/input-images/` 366개와 `training-images/target-images/` 46개이며 기존 경로는 심볼릭 링크로 연결한다.

```bash
.venv/bin/python docs/assets/part-07/chapter-05/sec-10/p7_5_10_generate_supplements.py --rule P710-RULE-INPUT-002 --dry-run
```

```bash
.venv/bin/python docs/assets/part-07/chapter-05/sec-10/p7_5_10_mira_lora.py prepare \
  --manifest docs/assets/part-07/chapter-05/sec-10/p7-5-10-paired-dataset.json \
  --output .tmp/p7-5-10/bfs-paired-366-v1
```

`review-template`·`export`도 같은 LoRA 코드의 하위 명령이다. 검수 목록을 내보내는 작업은 이미지 생성이나 학습 실행을 하지 않는다. `run`은 기본적으로 실행 계획만 출력하며 `--execute`를 지정해야 학습을 실행한다.

[확정 데이터셋 검수표](bfs-paired-dataset-review.md){ .aibook-markdown-preview }

개별 이미지·생성 기록·후보 카탈로그와 학습 패키지는 산출물이다. 기준 파일 4개와 구분하며 중복 복사하지 않는다. sec-12의 외부 평가 입력과 LoRA 평가 코드는 평가용으로 유지한다.

## 생성 출력 경로

새 입력 이미지는 `training-images/input-images/`, 새 목표 이미지는 `training-images/target-images/`에 저장한다. 결과 JSON·카탈로그·상태·잠금 파일은 `generation-records/<규칙 ID>/`에 저장한다. 출력 위치는 생성 JSON의 `storage`에 한 번만 정의하며 `--output-dir` 덮어쓰기는 지원하지 않는다. 규칙의 `legacy_output_dir`은 과거 카탈로그를 읽어 완료 항목을 재사용하는 용도이고 새 출력에는 사용하지 않는다. 생성된 파일을 이 폴더에 저장하는 것만으로 학습 채택이 되지는 않는다.
