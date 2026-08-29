# 저장소 루트 보조 도구

이 디렉터리는 원고 집필·검수와 에셋 제작 과정에서 쓰는 독립 보조 도구를 둔다. 실행 소스는 모두 저장소 루트의 `tool/`에서 관리하며, 실행 산출물은 원칙적으로 `.tmp/`에 둔다.

## 근거 수집·번역 검수

다음 두 도구의 전체 사용법은 [evidence-and-translation-tools.md](evidence-and-translation-tools.md)에 정리한다.

- `evidence_collector.py`: 원고 Markdown의 외부 URL을 `.tmp/evidence/`에 수집한다. 실제 다운로드 전에 `--dry-run`으로 대상만 확인할 수 있다.
- `translation_quality_report.py`: 한국어 원문과 영어·중국어 번역본을 대조해 추가 번역 또는 집중 검수 대상을 초기 단계에서 찾는다. Ollama 검수 모델이 없으면 `--pull-model`로 내려받을 수 있다.

## 모델 가중치 다운로드·검증

`model_weight_manager.py`는 [`model-inventory/model-weights.cdx.json`](../model-inventory/model-weights.cdx.json)의 CycloneDX AI/ML-BOM을 읽어 등록 모델을 조회하고, 가중치를 `.tmp/download/`에 내려받은 뒤 SHA-256 기록을 남긴다. 모델 파일은 Git에 추가하지 않는다.

```bash
./.venv/bin/python tool/model_weight_manager.py list
./.venv/bin/python tool/model_weight_manager.py fetch \
  --ref weight:dx8152-qwen-edit-2509-multiple-angles \
  --dry-run
./.venv/bin/python tool/model_weight_manager.py relocate \
  --ref weight:dx8152-qwen-edit-2509-multiple-angles \
  --dry-run
./.venv/bin/python tool/model_weight_manager.py relocate-directory \
  --ref model:depth-anything-v2-small-hf \
  --source .tmp/p7-5-3-depth-anything-v2-small \
  --dry-run
./.venv/bin/python tool/model_weight_manager.py audit-cache \
  --hub-root /home/cbsim/.cache/huggingface/hub \
  --unregistered-only
./.venv/bin/python tool/model_weight_manager.py verify
./.venv/bin/python tool/model_weight_manager.py verify-migrations
```

`fetch`는 BOM의 Hugging Face 저장소 URL과 단일 `aibook:download-selector`가 있을 때 revision 기반 `resolve` URL을 만든다. 파일 selector가 여러 개이거나 BOM에 원본 URL이 아직 없으면, 먼저 BOM을 보완한 뒤 `--selector` 또는 직접 artifact URL인 `--url`을 명시한다. 실제 다운로드 기록은 각 component 폴더의 `download-record.json`에 URL, revision, 크기, SHA-256으로 남는다.

기존 Hugging Face cache를 옮길 때는 `relocate`를 사용한다. 이 명령은 구성요소의 원본 저장소에서 Hugging Face cache 디렉터리를 찾고, 이동 전후의 일반 파일마다 SHA-256·크기를 비교한 뒤 `.tmp/download/huggingface/hub/`에 이전 기록을 남긴다. 한 모델만 처리하며, 대상 디렉터리가 이미 있으면 덮어쓰지 않는다.

Hugging Face hub 형식이 아닌 직접 내려받은 모델 폴더는 `relocate-directory`를 사용한다. 이 명령도 이동 전후의 일반 파일 SHA-256·크기를 비교하지만, 대상은 구성요소 `bom-ref`에서 만든 `.tmp/download/<component>/` 경로다. 기존 모델 폴더를 삭제하지 않고 검증된 이동으로만 정리한다.

`verify-migrations`는 과거 `relocate`·`relocate-directory`가 남긴 파일별 매니페스트를 다시 계산해 현재 이동 모델의 SHA-256·크기를 검증한다. 직접 다운로드 파일은 기존 `verify`를 사용한다.

`audit-cache`는 실제 Hugging Face cache와 BOM 등록 항목을 비교한다. `unregistered-candidate`는 단지 인벤토리에 없는 후보일 뿐, 자동 삭제 대상이 아니다. 인벤토리와 에셋 소스 참조를 확인한 뒤에만 `quarantine`으로 `.tmp/download/huggingface/quarantine/`에 격리 이동할 수 있다. `quarantine`도 이동 전후 SHA-256을 비교하며, 삭제 기능은 제공하지 않는다.
