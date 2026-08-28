# 저장소 루트 보조 도구

이 디렉터리는 원고 에셋 제작 과정에서 쓰는 독립 보조 도구를 둔다. 관리 문서 전용 도구는 `management/tools/`에, 모델 파일처럼 원고 자산 소스의 외부 실행 의존성을 다루는 도구는 이 디렉터리에 둔다.

## 모델 가중치 다운로드·검증

`model_weight_manager.py`는 [`model-inventory/model-weights.cdx.json`](../model-inventory/model-weights.cdx.json)의 CycloneDX AI/ML-BOM을 읽어 등록 모델을 조회하고, 가중치를 `.tmp/download/`에 내려받은 뒤 SHA-256 기록을 남긴다. 모델 파일은 Git에 추가하지 않는다.

```bash
./.venv/bin/python tool/model_weight_manager.py list
./.venv/bin/python tool/model_weight_manager.py fetch \
  --ref weight:dx8152-qwen-edit-2509-multiple-angles \
  --dry-run
./.venv/bin/python tool/model_weight_manager.py verify
```

`fetch`는 BOM의 Hugging Face 저장소 URL과 단일 `aibook:download-selector`가 있을 때 revision 기반 `resolve` URL을 만든다. 파일 selector가 여러 개이거나 BOM에 원본 URL이 아직 없으면, 먼저 BOM을 보완한 뒤 `--selector` 또는 직접 artifact URL인 `--url`을 명시한다. 실제 다운로드 기록은 각 component 폴더의 `download-record.json`에 URL, revision, 크기, SHA-256으로 남는다.
