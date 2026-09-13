# 모델 가중치 인벤토리

`model-weights.cdx.json`은 원고 에셋 생성 소스가 참조하는 외부 모델, 체크포인트, 어댑터, LoRA 가중치의 원본을 추적하는 CycloneDX 1.7 AI/ML-BOM이다. CycloneDX는 `machine-learning-model`, 모델 카드, 배포 참조를 지원하므로 모델 ID만 적은 표보다 출처·버전·사용 코드·라이선스 검토 상태를 함께 관리하기에 적합하다.

이 폴더는 가중치를 저장하거나 배포하지 않는다. 공개 원고 자산은 계속 `docs/assets/`에서 관리하고, 이 인벤토리는 그 자산을 만든 Python 소스의 외부 모델 의존성만 기록한다. 이후 내려받는 모델 파일의 로컬 보관 위치는 저장소 루트 기준 `.tmp/download/`로 통일한다. `.tmp/`는 Git ignore 대상이므로 가중치·캐시·압축 해제 파일을 커밋하지 않는다.

## 기록 규칙

- `externalReferences[type=distribution]`은 원본 다운로드를 시작할 저장소 또는 특정 파일 경로다.
- `aibook:download-selector`는 실제로 사용한 모델 저장소 안의 파일 또는 파일군이다.
- `aibook:source-files`는 해당 가중치를 참조하는 저장소 상대 경로다.
- 삭제된 소스 경로는 `aibook:source-files`에서 제거한다. 현재 소스가 하나도 남지 않으면 해당 속성을 `aibook:source-status`로 대체해 소스 부재를 표시하며, 모델 출처·가중치·캐시 검토 이력은 별도 정리 전까지 유지한다.
- `aibook:observed-revision`은 소스 코드의 Hugging Face cache 경로에서 확인한 immutable snapshot이다. 없으면 아직 고정하지 않은 참조다.
- `aibook:license-review=review-required`는 공개 실습 자산으로 승인됐다는 뜻이 아니다. 원문 라이선스와 모델 카드를 확인하기 전까지는 채택을 보류한다.

새 모델을 소스에 추가할 때는 먼저 이 BOM에 모델 저장소 URL, 모델 카드, file selector, source file을 추가한다. 가능한 경우 commit SHA와 실제 파일 SHA-256을 보강한다. 직접 다운로드는 `.tmp/download/artifacts/<bom-ref의 안전한 슬러그>/` 아래에 두고, 절대 cache 경로는 코드나 BOM의 원본 경로로 쓰지 않는다. 코드에는 repository ID + revision + file selector를 사용한다.

모델을 정리할 때는 먼저 `tool/model_weight_manager.py audit-cache`로 인벤토리와 cache의 차이를 확인한다. 인벤토리에서 제거하기 전에는 에셋 소스의 참조가 사라졌는지 확인하고, 바로 삭제하지 말고 `quarantine`으로 격리한 뒤 필요 기간 동안 재현·복구 가능 여부를 확인한다.

`aibook:` 속성은 CycloneDX 확장 property namespace다. 표준 필드를 대체하지 않는다.

## 검증

```bash
.venv/bin/python -m json.tool model-inventory/model-weights.cdx.json > /dev/null
```

스키마 호환성은 CycloneDX 1.7 JSON schema 또는 사용하는 BOM 도구로 별도 확인한다.

## 근거

- [CycloneDX specification overview](https://cyclonedx.org/specification/overview/)
- [CycloneDX AI Models and Model Cards use case](https://cyclonedx.org/use-cases/ai-models-and-model-cards/)
- [`management/guidelines/source-copyright-guidelines.md`](../management/guidelines/source-copyright-guidelines.md)

## 로컬 저장 경로

저장소 루트의 `.tmp/download/`를 사용한다. `tmp/download/`나 최상위 `model-*`, `weight-*` 폴더를 새로 만들지 않는다.

| 종류 | 기준 경로 | 관리 방식 |
| --- | --- | --- |
| 직접 받은 모델·LoRA·GGUF | `.tmp/download/artifacts/<component-slug>/` | BOM의 `bom-ref`에서 `:` 등 특수문자를 `-`로 치환한다. 원본 파일명과 download-record.json을 유지한다. |
| Hugging Face 표준 캐시 | `.tmp/download/huggingface/hub/` | models--조직--저장소/blobs/refs/snapshots 구조와 심볼릭 링크를 유지한다. |
| 별도 출처 자료 | `.tmp/download/sources/<provider>/` | 출처별 묶음이며 신규 모델 가중치는 BOM 등록 후 artifacts로 받는다. |
| 패키지·제공자 캐시 | `.tmp/download/caches/pip/`, `.tmp/download/caches/modelscope/` | 재생성 가능한 다운로드 캐시로 구분한다. |
| 이전·격리 기록 | `.tmp/download/migrations/`, `.tmp/download/huggingface/migrations/`, `.tmp/download/huggingface/quarantine/` | 검증 기록과 격리 자료를 가중치와 구분한다. |

직접 받은 가중치의 버전은 파일명 또는 revision 하위 폴더로 구분하며 기존 파일을 덮어쓰지 않는다. 다운로드 기록에는 저장소 ID·revision·selector·SHA-256을 남긴다. `weight-mira-*` 같은 이름만으로 자체 학습 산출물이라고 판단하지 않고 기록된 원본을 확인한다.

자체 학습 LoRA는 다운로드 자료가 아니다. `.tmp/training/<section-id>/<run-id>/checkpoints/`를 신규 학습의 기준으로 하고, 설정·로그·평가 결과도 같은 run 아래에 구분한다. 진행 중인 학습의 출력 경로는 변경하지 않는다. 원고에는 채택한 결과와 공개용 실행 기록을 두며 가중치는 Git에 넣지 않는다.

경로 변경 전 실행 중인 작업의 입력·출력 사용 여부를 확인한다. 같은 파일시스템의 디렉터리 이동은 파일 내용과 링크 대상을 보존하고, 이동 후 소스·설정·다운로드 기록·BOM의 참조를 검증한다. 기존 생성 결과의 코드·가중치 해시를 현재 파일의 해시로 덮어쓰지 않는다. 중복·미등록 모델은 자동 삭제하지 않고 audit-cache와 quarantine으로 따로 판단한다.
