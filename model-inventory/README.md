# 모델 가중치 인벤토리

`model-weights.cdx.json`은 원고 에셋 생성 소스가 참조하는 외부 모델, 체크포인트, 어댑터, LoRA 가중치의 원본을 추적하는 CycloneDX 1.7 AI/ML-BOM이다. CycloneDX는 `machine-learning-model`, 모델 카드, 배포 참조를 지원하므로 모델 ID만 적은 표보다 출처·버전·사용 코드·라이선스 검토 상태를 함께 관리하기에 적합하다.

이 폴더는 가중치를 저장하거나 배포하지 않는다. 공개 원고 자산은 계속 `docs/assets/`에서 관리하고, 이 인벤토리는 그 자산을 만든 Python 소스의 외부 모델 의존성만 기록한다. 이후 내려받는 모델 파일의 로컬 보관 위치는 저장소 루트 기준 `.tmp/download/`로 통일한다. `.tmp/`는 Git ignore 대상이므로 가중치·캐시·압축 해제 파일을 커밋하지 않는다.

## 기록 규칙

- `externalReferences[type=distribution]`은 원본 다운로드를 시작할 저장소 또는 특정 파일 경로다.
- `aibook:download-selector`는 실제로 사용한 모델 저장소 안의 파일 또는 파일군이다.
- `aibook:source-files`는 해당 가중치를 참조하는 저장소 상대 경로다.
- `aibook:observed-revision`은 소스 코드의 Hugging Face cache 경로에서 확인한 immutable snapshot이다. 없으면 아직 고정하지 않은 참조다.
- `aibook:license-review=review-required`는 공개 실습 자산으로 승인됐다는 뜻이 아니다. 원문 라이선스와 모델 카드를 확인하기 전까지는 채택을 보류한다.

새 모델을 소스에 추가할 때는 먼저 이 BOM에 모델 저장소 URL, 모델 카드, file selector, source file을 추가한다. 가능한 경우 commit SHA와 실제 파일 SHA-256을 보강한다. 다운로드는 `.tmp/download/<provider>/<repository-or-model>/` 아래에 두고, 절대 cache 경로는 코드나 BOM의 원본 경로로 쓰지 않는다. 코드에는 repository ID + revision + file selector를 사용한다.

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
