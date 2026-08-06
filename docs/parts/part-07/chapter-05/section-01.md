# P7-5.1 화풍 참조 셋 생성: 로컬 GPU로 프레임 없는 기준 만들기

> Section ID: `P7-5.1`
> Version: `v2026.08.06`

이 프로젝트는 다음 단계에서 FLUX.2 Klein 4B로 캐릭터 기준이 될 참조 패키지를 만듭니다. 그래서 캐릭터를 만들기 전에, 같은 모델에서 사용할 화풍 기준을 먼저 고정해야 합니다. 여기서 화풍 참조 셋은 보기 좋은 배경을 모은 폴더가 아닙니다. 인물과 소품을 넣기 전, 선의 역할, 색의 겹침, 시간대의 광원, 장소의 폭, 카메라 구도를 **같은 기준으로 비교할 수 있게 만든 검수 입력**입니다. 한 장이 마음에 들어도 다른 장소와 카메라에서 계약이 무너지면, 그 한 장은 FLUX.2 Klein 4B로 만들 캐릭터 참조 패키지의 화풍 기준이 될 수 없습니다.

이 절의 질문은 **8 GB급 로컬 GPU에서 FLUX.2 Klein 4B로 만든 배경 화풍 표본이 다음 캐릭터 참조 패키지의 기준이 되려면 무엇을 검수해야 하는가**입니다. 이 절의 산출물은 승인된 화풍 그 자체가 아니라, 후보 이미지·행별 판정·실패 이유·다음 캐릭터 참조 생성을 막거나 통과시키는 gate입니다.

웹툰 컷 생성 전체를 한 번에 해결하려고 하지 않습니다. 이 실험은 8 GB VRAM 환경에서 `화풍 참조 셋 -> 캐릭터 참조 셋 -> 컷씬 -> 화풍 보정`을 네 단계로 나누어 구성합니다. 한 단계의 출력이 다음 단계의 입력이 되려면, 생성된 이미지가 마음에 드는지를 넘어서 어떤 조건을 통과했는지 기록되어야 합니다.

| 단계 | 만드는 것 | 다음 단계로 넘기는 조건 |
| --- | --- | --- |
| P7-5.1 화풍 참조 셋 | 프레임 없는 배경 화풍 원본과 ledger | FLUX.2 Klein 4B가 따라야 할 선·수채화·광원·카메라 기준 |
| P7-5.2 캐릭터 참조 셋 | 같은 화풍 위의 인물 기준 패키지 | 얼굴·전신·의상·소품·view가 분리 검수된 캐릭터 입력 |
| P7-5.3 컷씬 생성 | 캐릭터와 장면 조건을 결합한 컷 | 구조·인물·소품이 함께 보존되는지 판단할 후보 |
| P7-5.4 화풍 보정 | 통과 컷의 색·선·일관성 보정 | 컷 사이 화풍 drift와 국소 실패를 따로 기록한 결과 |

## 화풍 참조 셋은 생성과 검수가 번갈아 가는 파이프라인이다

화풍 생성은 [프롬프트](../../../reference/concept-glossary-parts/13-pieup.md#prompt) 한 번으로 끝나지 않습니다. 먼저 어떤 선과 색을 유지할지 계약을 고정하고, 그 계약이 장소·시간·카메라가 달라져도 남는지 확인할 장면 행렬을 만듭니다. 각 행의 원본을 생성한 뒤 사람은 프레임, 선, 색, 장소, 시간, 카메라를 함께 검수합니다. 불합격이면 이미지를 crop하거나 상태만 바꾸지 않고, 실패 원인을 다음 프롬프트의 장면 구조로 바꿔 같은 행을 다시 생성합니다.

```mermaid
--8<-- "assets/part-07/chapter-05/p7-5-1-style-reference-pipeline-ko.mmd"
```

이 흐름에서 모델은 후보를 만들고, 사람은 후보가 계약을 지키는지 판단합니다. `행 승인`은 한 조건에서의 통과이고, `전체 팩 승인`은 모든 필수 행과 보조 근거를 함께 비교한 뒤의 결론입니다. 승인된 뒤에도 타일로 합친 비교 이미지는 다음 단계의 모델 입력으로 쓰지 않습니다. 현재 P7-5.1의 인물 화풍 후보 생성은 승인 배경 원본을 근거로 정리한 텍스트 화풍 계약만 prompt에 넣고, 배경 PNG 자체는 모델 입력에 넣지 않습니다.

| 파이프라인 층 | 고정하거나 바꾸는 것 | 다음 단계로 남기는 것 |
| --- | --- | --- |
| 화풍 계약 | 선·수채화 색층·프레임 금지 조건 | 통과·불합격 기준 |
| 장면 행렬 | 장소·시간·카메라 조합 | 필수 행과 보조 행 목록 |
| 행별 생성 | seed와 장면의 구체 구성 | crop하지 않은 후보 원본 |
| 사람 검수 | 외곽·선·색·장소·시간·카메라 판정 | 승인, 불합격 이유, 재생성 지시 |
| 전체 팩 승인 | 행 사이의 일관성과 입력 범위 | ledger의 최종 결론과 manifest |

## FLUX.2 Klein 4B는 작지만 조건 검수가 필요하다

FLUX.2 Klein 4B를 고른 이유는 다음 단계의 캐릭터 참조 패키지까지 같은 모델 계열로 이어 보기 위해서입니다. 모델 카드는 이 모델을 4B 규모의 rectified-flow transformer로 설명하고, text-to-image와 image editing, multi-reference editing을 지원한다고 밝힙니다. 공개 가중치는 Apache 2.0 라이선스로 제공되며, Diffusers에서는 `Flux2KleinPipeline`으로 실행할 수 있습니다.

이 장점이 곧바로 8 GB VRAM에서 안정적인 웹툰 컷 파이프라인을 뜻하지는 않습니다. 모델 카드의 하드웨어 설명은 약 13 GB VRAM급 소비자 GPU를 기준으로 삼습니다. 이 실험은 그보다 작은 8 GB 환경에서 `enable_sequential_cpu_offload()`를 사용해 한 번에 한 단계를 실행하고, 각 단계의 승인 조건을 분리합니다. 따라서 P7-5.1은 모델이 좋은 배경 이미지를 만들 수 있는지 보는 절이 아니라, **8 GB 제약 안에서 다음 단계 입력으로 넘겨도 되는 조건을 사람이 판정하는 절**입니다.

| 구분 | 이 실험에서 유리한 점 | 조심할 점 |
| --- | --- | --- |
| 모델 크기 | 4B 규모라 로컬 실행 실험 대상으로 다룰 수 있음 | 공식 하드웨어 설명은 약 13 GB VRAM 기준이므로 8 GB에서는 offload와 단계 분리가 필요함 |
| 기능 범위 | text-to-image, image editing, multi-reference 흐름을 같은 계열에서 이어 볼 수 있음 | 기능 지원이 곧 캐릭터·소품·화풍 일관성 통과를 뜻하지 않음 |
| 공개 가중치 | Apache 2.0 공개 가중치라 실험 조건과 산출물을 기록하기 좋음 | 모델 출력은 prompt를 놓치거나 왜곡할 수 있어 사람 검수 ledger가 필요함 |
| 빠른 후보 생성 | 여러 장면 후보를 반복해 만들 수 있음 | 빠른 생성은 승인 기준이 아니며, 실패 원인은 다음 prompt 구조로 바꿔야 함 |

## 화풍은 팔레트 하나로 고정되지 않는다

같은 청록색과 주황빛을 쓴다고 같은 웹툰 화풍이 되지는 않습니다. 선이 명암을 대신하는지, 수채화 색면 아래에 남는지, 실내의 인공광과 실외의 자연광에서 색의 대비가 어떻게 달라지는지, 높은 시점과 낮은 시점에서 원근선이 어떻게 놓이는지가 함께 반복되어야 합니다.

이 실습의 수채화 계약은 얇은 charcoal 윤곽선과 건축 구조선을 남기고, 그 아래에 기존보다 한 단계 높은 안료 농도의 투명 색면을 겹치는 것입니다. 채도는 시간대와 무관하게 같은 warm apricot으로 고정하지 않습니다. 낮에는 clear teal·leaf green·cool off-white가 주가 되고, 석양에서만 apricot 역광을 제한적으로 씁니다. 밤과 우천 야간은 indigo·navy 그림자와 작은 tungsten 반사광으로 읽혀야 하며, 하늘을 붉게 물들여 석양처럼 만들지 않습니다. 형광색·neon·불투명 airbrush로 바꾸지 않습니다. 색은 wet-on-wet 번짐, 불규칙한 안료 고임, 반투명 색층으로 남아야 합니다. 해칭, crosshatching, 점묘, 검은 먹 번짐은 드로잉 라인이 아니라 명암을 채우는 질감으로 판단해 제외합니다. 수채화는 선을 흐리게 만드는 필터가 아니라 선이 구획한 면에 겹쳐지는 색층입니다. 따라서 `수채화처럼 보인다`는 인상만으로는 통과할 수 없습니다. 외곽, 선, 색, 공간, 카메라를 각각 확인해야 합니다.

| 확인 축 | 통과 조건 | 불합격 신호 |
| --- | --- | --- |
| 외곽 | 생성 원본이 프레임 없이 캔버스를 채움 | page border, panel frame, 사후 crop 필요 |
| 선 | 윤곽·구조·원근선이 읽힘 | 선이 색 번짐에 묻힘, 명암 해칭이 화면을 지배함 |
| 색 | 한 단계 높은 자연 채도의 반투명 수채화 색층과 시간대별 광원이 함께 보임 | 모든 시간대를 석양색으로 통일함, 단색 먹 질감, 불투명 airbrush, neon, 번짐 없는 평면 도색 |
| 공간 | 실내와 실외가 모두 있음 | 한 장소 유형의 반복 |
| 카메라 | high angle, low angle, wide eye-level, oblique side, overhead high angle이 실제로 다름 | 세로 중앙 소실점·아이레벨 구도 반복 |

## 배경 화풍과 인물 화풍 계약은 다르다

이 절의 원본은 배경에서 선과 수채 색면이 어떻게 겹치고, 시간대별 광원이 공간의 명도와 반사에 어떻게 나타나는지를 정합니다. 따라서 아트리움의 차가운 새벽빛이나 우천 야간 승강장의 남색 그림자를 그대로 인물의 피부나 머리카락 기본색으로 옮기지 않습니다. 그렇게 하면 같은 캐릭터가 장소마다 다른 피부색과 머리색으로 보일 수 있습니다.

인물 화풍은 특정 작가의 이름을 흉내 내는 지시가 아니라, 캐릭터를 반복해서 그릴 때 지켜야 할 **표현 규칙**입니다. 예를 들어 얼굴에서 눈·코·입을 얼마나 단순하게 표시하는지, 머리카락 외곽선과 옷 주름을 어떤 선 굵기로 구분하는지, 전신에서 머리·몸통·팔다리의 비율을 어느 정도로 유지하는지, 피부·머리카락·의상의 색면을 어디까지 나누는지가 그 규칙에 들어갑니다. 이 규칙은 한 장의 예쁜 얼굴보다 정면·측면·전신과 서로 다른 광원에서도 같은 인물로 읽히는지를 기준으로 검수해야 합니다.

P7-5.1이 다음 단계에 넘기는 것은 FLUX.2 Klein 4B가 따라야 할 얇은 charcoal 선, 반투명 색층, 프레임 없는 캔버스, 시간대별 배경 광원이라는 **배경 화풍 계약**입니다. 이 계약은 인물을 배경과 어울리게 놓기 위한 공통 바탕이지만, 얼굴의 특징·신체 비율·의상 구조까지 승인하지는 않습니다. P7-5.2는 같은 모델을 사용해 이 배경 화풍 계약을 바탕으로 머리카락·피부·눈·의상 색과 인물 표현 규칙을 별도 character contract로 정하고, full body와 얼굴의 일관성을 검수합니다. 배경의 밤·노을·비는 컷신에서 인물에 약한 반사광을 더할 수는 있어도, 승인된 기본색이나 인물의 표현 규칙을 새로 정의하는 근거가 될 수 없습니다.

## 다섯 행이 있어야 한 장의 우연을 구별할 수 있다

한 장면에서 seed만 바꾸면 다른 장소와 카메라를 다뤘다고 볼 수 없습니다. 다음 다섯 행은 같은 장면의 변형이 아니라, 장소·시간·카메라가 모두 다른 최소 검수 집합입니다. 새벽의 실내 고각도와 우천 야간의 overhead high angle은 빛과 원근을 동시에 시험하므로, 낮의 거리 한 장으로 대신할 수 없습니다.

| scene ID | 장소 | 시간 | 카메라 |
| --- | --- | --- | --- |
| `indoor-dawn-high-angle` | 실내 | 새벽 | high angle |
| `indoor-night-oblique` | 실내 | 밤 | oblique side view |
| `outdoor-day-wide` | 실외 | 낮 | wide eye-level |
| `outdoor-sunset-low-angle` | 실외 | 해질녘 | low angle |
| `outdoor-rainy-night-overhead` | 실외 | 우천 야간 | overhead high angle |

각 행에는 사람·동물·차량·읽을 수 있는 표지·글자를 넣지 않습니다. 화풍 팩은 캐릭터 identity나 소품 geometry를 정하는 자산이 아니기 때문입니다. 프롬프트에는 `no border frame`, `no panel`, `fill the canvas edge to edge`를 함께 쓰되, 이 단어가 있다고 통과로 처리하지 않습니다. 출력 원본에서 프레임이 보이면 그 이미지는 crop으로 살리지 않고 불합격입니다.

## 실행 코드는 공통 계약과 장면 변수를 분리한다

배경 원본 생성에는 Diffusers의 `Flux2KleinPipeline`을 사용합니다. 아홉 행을 만드는 기준 실행 코드는 `p7_5_1_regenerate_local_gpu_style_references.py`입니다. 학습 관점에서 이 코드는 세 가지를 구분하게 해 줍니다. 첫째, 모든 행에 같은 화풍 계약을 붙입니다. 둘째, 행마다 장소·시간·카메라·seed만 바꿉니다. 셋째, 생성 성공과 사람 승인을 별도 기록으로 남깁니다.

| 코드 위치 | 바꾸면 달라지는 것 | 학습할 경계 |
| --- | --- | --- |
| `COMMON_CONTRACT` | 아홉 행 전체의 선·수채화·프레임 금지 기준 | 공통 계약을 바꾸면 이전 행과 직접 비교하기 어려움 |
| `SCENES`의 `prompt` | 한 행의 장소·시간·카메라 구조 | 실패 원인은 금지어보다 장면 구조로 고침 |
| `SCENES`의 `seed` | 같은 조건의 다른 출발점 | seed 고정은 비교 기록이지 품질 보장이 아님 |
| `P7_STYLE_SCENE`, `P7_STYLE_EXCLUDE` | 생성할 행의 범위 | 한 행 생성은 전체 팩 승인이 아님 |
| `STEPS`, `GUIDANCE`, 해상도 | 추론 조건 전체 | 값을 바꾸면 별도 비교 실험으로 기록함 |
| 터미널 실행 요약 | 시간·GPU 메모리·출력 파일 | 생성 성공과 사람 승인을 분리함 |

이전의 시간대 균형 배치와 표적 재생성 파일은 같은 실행 골격에 당시의 `SCENES`만 기록한 이력입니다. 따라서 별도의 생성 방법이나 두 번째 실행 경로로 설명하지 않습니다. P7-5.1의 참조 원본은 로컬 GPU로 생성한 것만 사용할 수 있으며, 내장 이미지 생성으로 만든 자산은 입력·승인·manifest에서 제외했습니다.

[아홉 로컬 GPU 화풍 후보 생성 코드 보기](/AiBook/assets/part-07/chapter-05/p7_5_1_regenerate_local_gpu_style_references.py){.aibook-source-link}

### 공통 화풍 계약과 장면 조건이 만나는 코드

아래는 실행 파일에서 가져온 핵심 발췌입니다. 긴 영어 prompt를 그대로 반복하지 않고, 독자가 **모든 행에 유지할 조건**과 **한 행에서만 바꿀 조건**의 경계를 읽도록 축약했습니다. 실제 실행 때는 바로 위의 전체 소스를 기준으로 합니다.

```python
# 모든 장면에 같은 조건을 붙인다.
COMMON_CONTRACT = (
    "Create an edge-to-edge Korean webtoon background. "
    "Do not draw an outer rectangular outline or surround the scene with a dark border. "
    "Use a transparent watercolor-and-ink medium with thin charcoal contour lines. "
    "Exclude readable signs, logos, people, animals, and vehicles."
)

# 장소·시간·카메라·seed만 장면 행마다 달라진다.
SCENES = [
    {
        "id": "downtown-clear-day-wide",
        "seed": 420703,
        "prompt": (
            "Create an empty Seoul business intersection in bright clear midday. "
            "View sideways from a shaded near-left sidewalk corner, never a centered road corridor."
        ),
    },
]
```

여기서 `COMMON_CONTRACT`를 바꾸면 아홉 행 전체의 비교 기준이 달라집니다. 반대로 `SCENES`의 한 `prompt`를 바꾸면 그 행의 장소·시간·카메라만 재생성합니다.

다음 발췌는 한 행을 실제로 만드는 부분입니다. `P7_STYLE_SCENE`을 바꾸면 `scenes`에 남는 행 수가 바뀌고, `run_label`을 `v2`처럼 바꾸면 기존 PNG를 덮어쓰지 않고 새 파일로 남깁니다.

```python
pipe = Flux2KleinPipeline.from_pretrained(
    MODEL_ID, torch_dtype=torch.bfloat16, cache_dir=CACHE_DIR
)
pipe.enable_sequential_cpu_offload()

for scene in scenes:
    image = pipe(
        prompt=scene["prompt"] + COMMON_CONTRACT,
        width=768,
        height=1152,
        num_inference_steps=50,
        guidance_scale=4.0,
        generator=torch.Generator(device="cpu").manual_seed(scene["seed"]),
        max_sequence_length=256,
    ).images[0]
    image.save(ASSET_DIR / f"p7-5-1-style-{scene['id']}-local-gpu-{run_label}.png")
```

이 코드 블록에서 파이프라인 분절은 모델 구조를 새로 나누는 일이 아니라, **8 GB VRAM에서 한 번에 들고 있을 것을 줄이는 실행 분절**입니다. `from_pretrained(...)`는 FLUX.2 Klein 4B 가중치를 준비하고, `enable_sequential_cpu_offload()`는 tokenizer·text encoder·transformer·VAE 같은 구성 요소를 실행 순서에 맞춰 CPU와 GPU 사이에서 옮기게 합니다. 그래서 GPU에는 지금 계산에 필요한 모듈과 tensor만 올라오고, 다음 단계가 필요해지면 이전 단계의 일부가 내려갑니다.

`for scene in scenes:`는 이 절의 두 번째 분절입니다. 아홉 장면을 하나의 큰 batch로 묶지 않고, 한 행의 prompt와 seed로 한 장을 만들고 저장한 뒤 다음 행으로 넘어갑니다. 이렇게 해야 8 GB 환경에서 `화풍 참조 셋`의 장면 행렬을 다룰 수 있고, 실패한 행만 `P7_STYLE_SCENE`으로 다시 생성할 수 있습니다. 코드 원문에서는 행 하나가 끝난 뒤 `torch.cuda.empty_cache()`로 다음 행을 위한 캐시 반환도 요청합니다. 이것은 결과를 좋게 만드는 설정이 아니라, 다음 장면을 같은 GPU에서 이어 실행하기 위한 메모리 운용입니다.

따라서 `pipe(...)` 호출 안의 `width`, `height`, `num_inference_steps`, `guidance_scale`, `seed`는 후보를 만드는 추론 조건이고, `enable_sequential_cpu_offload()`와 행별 반복은 그 추론을 8 GB에서 실행 가능하게 나누는 운영 조건입니다. 이 블록의 `image.save(...)`가 성공했다는 사실은 후보 PNG가 생겼다는 뜻뿐입니다. 외곽선·수채화 질감·공간의 물리성·필수 행 충족 여부는 다음의 사람 검수에서 판정합니다.

## AI 모델은 텍스트 조건과 seed에서 후보 원본을 만든다

앞의 코드 발췌는 실행에서 바꿀 값과 저장 경계를 보여 주고, 아래 도식은 그중 **후보 한 장을 만드는 실행 준비·`Flux2KleinPipeline` 내부 처리·검수 경계**를 나눕니다. 코드에서 FLUX.2 Klein 4B 가중치를 `torch_dtype=torch.bfloat16`으로 읽고 `enable_sequential_cpu_offload()`를 켜는 부분은 모델 내부 추론 단계가 아니라 실행 준비에 가깝습니다. 그 준비가 끝난 뒤 `Flux2KleinPipeline`은 장면 prompt와 공통 화풍 계약을 text condition으로 바꾸고, seed에서 시작한 이미지 표현을 정해진 횟수만큼 갱신합니다. 다음 캐릭터 참조 패키지도 같은 모델 계열에서 만들 것이므로, 이 단계의 목적은 다른 모델에 일반화되는 배경 화풍을 찾는 것이 아니라 **FLUX.2 Klein 4B가 안정적으로 따를 수 있는 화풍 입력 조건**을 먼저 고르는 것입니다. 코드의 `num_inference_steps=50`은 이 배치에서 반복 갱신한 횟수이고, `guidance_scale=4.0`은 텍스트 조건을 따르는 정도에 관여하는 실행 설정입니다. 이 숫자 자체가 화풍의 승인 기준은 아닙니다.

도식의 `입력 조건` 구역은 값을 `텍스트 입력`, `이미지 출발 조건`, `추론 설정` 세 묶음으로 정리합니다. 아래 표는 같은 값을 코드 위치와 검수 의미로 더 풀어 쓴 것입니다. 이렇게 보면 어떤 값이 텍스트 조건을 만들고 어떤 값이 latent 출발점과 반복 갱신 조건을 바꾸는지 구별할 수 있습니다.

| 입력 조건 | 코드에서 오는 곳 | 파이프라인에서 쓰이는 곳 | 검수할 때의 의미 |
| --- | --- | --- | --- |
| scene 행 | `SCENES`의 `prompt`, `seed` | `pipe(...)`에 넘길 prompt와 초기 latent | 장소·시간·카메라와 같은 행별 비교 조건 |
| 공통 화풍 계약 | `COMMON_CONTRACT` | `pipe(...)`에 넘길 prompt | 모든 행에서 유지해야 할 선·수채화·프레임 금지 조건 |
| 해상도 | `width=768`, `height=1152` | latent 크기와 VAE 출력 | 이 실험의 후보 원본 형식 |
| 추론 반복 | `num_inference_steps=50` | scheduler의 timesteps와 transformer 반복 | 생성 조건이지 품질 점수는 아님 |
| 텍스트 유도 | `guidance_scale=4.0` | transformer가 텍스트 조건을 반영하는 정도에 관여 | 값 자체가 승인 기준은 아님 |
| seed 생성기 | `torch.Generator(device="cpu").manual_seed(...)` | 초기 latent 출발점 | 비교 기록이며 픽셀 동일성 보장은 아님 |

```mermaid
--8<-- "assets/part-07/chapter-05/p7-5-1-ai-model-inference-pipeline-ko.mmd"
```

`Flux2KleinPipeline` 안에서는 먼저 입력이 prompt, generator, size, step, guidance로 나뉩니다. Qwen 계열 [tokenizer](../../../reference/concept-glossary-parts/12-tieut.md#tokenization)와 text encoder는 prompt를 token ID와 [text embedding](../../../reference/concept-glossary-parts/08-ieung.md#embedding) 같은 조건 표현으로 만들고, CPU seed에서 출발한 noise는 해상도에 맞는 초기 latent가 됩니다. FlowMatch 계열 scheduler는 반복할 timestep을 준비하고, FLUX [transformer](../../../reference/concept-glossary-parts/12-tieut.md#transformer)는 text embedding, timestep, guidance, latent를 함께 보며 latent를 반복 갱신합니다. 마지막에는 VAE가 latent tensor를 RGB 픽셀 이미지로 되돌리고, Python 코드는 그 결과를 PIL 이미지로 받아 PNG로 저장합니다. `enable_sequential_cpu_offload()`는 이 내부 단계들을 바꾸는 알고리즘이 아니라, 각 단계에서 필요한 모듈만 순서대로 GPU에 올리는 메모리 운용입니다. 이 구분이 필요한 이유는 단순합니다. prompt, seed, step, guidance는 **생성 조건**이고, 프레임 없음·선화 유지·시간대 광원·camera 충족은 **생성 뒤 검수 조건**입니다.

| 모델 파이프라인 단계 | 이 절에서 맡는 역할 | 승인 판단과의 관계 |
| --- | --- | --- |
| prompt와 공통 계약 | 장소·시간·카메라와 금지 조건을 한 텍스트 입력으로 묶음 | 금지 문구가 있어도 결과 보장은 아님 |
| tokenizer와 text encoder | 텍스트를 모델이 쓰는 조건 표현으로 바꿈 | 조건 해석의 시작점이지 사람 판정을 대체하지 않음 |
| seed와 latent | 같은 실행 조건의 출발점을 기록함 | 다른 환경에서 픽셀 동일성을 보장하지 않음 |
| scheduler와 transformer 반복 | timestep과 조건 표현을 보며 이미지 표현을 단계적으로 갱신함 | 반복 수와 guidance는 품질 점수가 아님 |
| VAE decode와 PNG 저장 | latent를 이미지로 바꾸고 원본 파일로 남김 | 파일 생성 성공은 후보 생성 성공일 뿐 승인 아님 |
| 사람 검수와 ledger | 외곽·선·색·장소·시간·카메라를 판정함 | 다음 단계 입력 가능 여부를 결정함 |

`COMMON_CONTRACT`와 장면별 `prompt`는 별도의 negative prompt 입력이 아니라 하나의 텍스트 조건으로 이어 붙여 전달됩니다. 따라서 `no panel` 같은 금지 문구는 모델에게 원하는 결과를 보장하는 규칙이 아니라, 다른 장면 설명과 함께 해석되는 조건입니다. seed는 같은 실행 조건의 출발점을 기록하지만, 다른 GPU·라이브러리·모델 버전에서도 픽셀까지 같은 결과를 보장하지는 않습니다. `enable_sequential_cpu_offload()`는 GPU 상주 메모리를 줄이는 실행 방식이지 화풍 판단 능력을 높이는 설정이 아닙니다. FLUX.2 Klein 4B는 prompt를 완전히 따르지 못하거나 텍스트를 왜곡할 수 있다는 한계도 모델 카드에 명시되어 있습니다.

## 다섯 필수 행과 보조 근거를 분리한다

로컬 GPU에서 후보를 만들 수 있다는 사실은 화풍 팩 승인과 다릅니다. 재생성 후보는 다섯 필수 행을 하나씩 채우고, 보조 행은 다른 장소·시간·시점에서도 계약이 유지되는지를 확인합니다. 현재는 창가 독서실이 폐기한 여객기 행을 대체해 다섯 필수 행을 채웠고, courtyard·베니스·공원·열차 승강장까지 네 보조 행도 사람 승인을 받았습니다. 이 아홉 행이 현재 manifest의 승인 원본입니다.

| 필수 행 | 로컬 GPU 재생성 후보 | 현재 판정 | 이 행이 확인하는 것 |
| --- | --- | --- | --- |
| 실내·새벽·high angle | 아트리움 local-gpu-v5 | 행 승인 | 새벽 광원과 실내 하향 시점 |
| 실내·밤·oblique | 창가 독서실 local-gpu-v1 | 행 승인 | 창밖의 밤, 작은 스탠드 조명, 사선 시점 |
| 실외·낮·wide eye-level | 도심 낮 local-gpu-v1 | 행 승인 | 낮 팔레트와 측면 교차로 시점 |
| 실외·해질녘·low angle | 주택가 local-gpu-v1 | 행 승인 | 제한된 석양빛과 curb-height 상향 시점 |
| 실외·우천 야간·overhead high angle | 옥상 광장 local-gpu-v1 | 행 승인 | 젖은 바닥 반사와 하향 야간 시점 |

이른 아침 courtyard, 베니스 운하, 공원 연못, 열차 승강장은 보조 행입니다. 각각 high-angle, oblique, 낮 팔레트, 우천 야간 조명을 넓혀 보지만 다섯 필수 행을 대체하지는 않습니다. 불합격 후보는 crop이나 상태값 변경으로 살리지 않고, 로컬 검수에서 실패 이유를 확인합니다.

| 보조 행 | 로컬 GPU 재생성 후보 | 넓혀 보는 화풍 조건 |
| --- | --- | --- |
| 이른 아침 courtyard · high angle | courtyard local-gpu-v1 · 행 승인 | 실외 자연광에서 하향 시점의 선·색면 |
| 베니스 운하 · 석양 · oblique | 베니스 local-gpu-v1 · 행 승인 | 제한된 apricot 역광과 사선 수면 |
| 공원 연못 · 낮 · eye-level | 공원 local-gpu-v1 · 행 승인 | 자연 공간의 낮 팔레트와 수면 반사 |
| 열차 승강장 · 우천 야간 · oblique | 승강장 local-gpu-v1 · 행 승인 | 인공광, 젖은 바닥, 짧은 대각 철로 |

## Python 검수 gate는 사람 판정의 누락을 막는다

생성기가 PNG를 만들면, 다음 코드는 로컬 검수 ledger의 다음 실행 행렬과 최종 상태를 읽어 P7-5.2 진입을 막거나 허용합니다. 이미지를 보고 선·색·프레임을 자동 채점하는 모델은 아닙니다. 그 판단은 사람이 ledger에 먼저 기록해야 합니다.

```bash
.venv/bin/python docs/assets/part-07/chapter-05/p7_5_1_local_style_pack_gate.py
```

승인된 ledger로 실행한 출력은 다음과 같습니다.

```text
PASS style pack can be used for character-reference generation
```

| 코드 부분 | 검사하는 것 | 통과를 의미하지 않는 것 |
| --- | --- | --- |
| `REQUIRED_CAMERAS`, `REQUIRED_TIMES` | `next_run_matrix`에 다섯 camera family와 다섯 시간대, 실내·실외가 모두 계획됐는지 | 그 행의 PNG가 실제로 구도·광원 조건을 만족한다는 판정 |
| `ledger["status"]` | 사람이 전체 팩을 `approved_for_character_reference`로 기록했는지 | 한 행의 `approved` 또는 PNG 생성 성공 |
| `missing` | 부족한 camera·시간·장소 또는 최종 승인 상태를 모아 `BLOCKED` 이유로 출력 | 실패 원인을 고치거나 ledger 상태를 자동 변경하는 처리 |

일부 행만 승인됐으면 matrix가 완전하더라도 gate는 `BLOCKED`여야 합니다. 반대로 status만 사람이 바꾸어도 실제 행별 원본·검수 이유가 없다면 통과로 다뤄서는 안 됩니다. 이 코드는 그 근거를 만들어 주지 않고, 사람이 남긴 근거와 다음 단계 상태가 서로 어긋나는지를 확인하는 보호 장치입니다.

[화풍 참조 팩 검수 gate 코드 보기](/AiBook/assets/part-07/chapter-05/p7_5_1_local_style_pack_gate.py){.aibook-source-link}

## 실패 원인을 다음 프롬프트의 구조로 바꾸기

실패한 후보에 `no frame`이나 `no hatching`을 더 쓰는 것만으로는 충분하지 않았습니다. 도심은 넓은 도로를 요청했을 때 중앙 소실점의 거리 복도로 수렴했습니다. 이를 고치기 위해 금지어를 늘리는 대신, 가까운 모퉁이에서 옆으로 건너다보는 **측면 교차로**로 장면 구조를 바꿨습니다. 복잡한 실내 좌석 배치는 요구가 길어질수록 공간 구조를 안정적으로 제어하지 못해 이 참조 팩의 범위에서 폐기했습니다. 대체 장면은 필요한 시간·카메라 조건을 더 단순한 구조로 검증해야 합니다.

반대로 장가계는 외곽 프레임은 사라졌지만 절벽의 반복 선이 해칭처럼 남았고, 우천 야간 플랫폼은 비·레일·지붕 선이 화면을 지배했습니다. 이 경우에는 crop이나 부분 보정으로 통과시키지 않습니다. `무엇이 틀렸는가`를 다음 생성의 구도·피사체 밀도·광원 조건으로 번역하고, 새 원본을 다시 검수합니다.

## 사람 판정은 ledger와 manifest로 분리한다

사람이 판단하는 것은 이미지의 미적 품질 점수 하나가 아닙니다. 각 원본에서 외곽·선·색·장소·시간·카메라와 **로컬 GPU 생성 기록**을 확인하고, 행별 승인·불합격 이유와 최종 결론을 로컬 검수 ledger에 적습니다. 다음 단계가 실제로 읽는 입력 목록은 [manifest](../../../assets/part-07/chapter-05/p7-5-1-approved-style-reference-pack.json)에 따로 둡니다. 이 분리 덕분에 `왜 승인했는가`와 `무엇을 다음 생성에 넣을 수 있는가`가 섞이지 않습니다.

현재 참조 셋은 `approved_for_character_reference`입니다. manifest에는 아홉 개의 사람 승인 로컬 GPU 원본이 있으며, 이 원본들은 배경 화풍 계약의 검수 근거입니다. 내장 이미지 생성 원본은 사람 검수를 통과했더라도 P7-5.1의 입력·승인·manifest에서 제외합니다. 그 뒤의 캐릭터 identity, 시점 묶음, 권리 확인은 P7-5.2의 별도 검수 대상입니다.

## 승인된 화풍 원본을 인물 후보에 적용한다

P7-5.1에서 인물 후보 생성으로 넘기는 것은 배경 PNG가 아니라 **배경과 같은 화풍 텍스트 계약**입니다. 프레임 없는 장면, sparse thin charcoal 선, wet-on-wet 번짐, 불규칙한 안료 고임, 반투명 색층, 작은 반사광, natural medium-chroma 안료 같은 조건을 prompt에 넣습니다. 승인된 배경 원본은 이 계약을 사람 검수로 확인한 근거이며, 모델의 image input으로 쓰지 않습니다.

이 예제에서 확인할 것은 `화풍이 인물 장면에서도 남는가`입니다. 같은 인물의 정면·측면을 묶는 turnaround, 얼굴 일관성, 나이·성별·인원수 판정은 P7-5.2의 캐릭터 참조 셋에서 따로 다룹니다.

| 구분 | 이 예제에서 하는 일 | 이 예제에서 하지 않는 일 |
| --- | --- | --- |
| 모델 입력 | P7-5.1 텍스트 화풍 계약과 하나의 장면 prompt를 넣음 | 승인 배경 PNG를 image input으로 넣지 않음 |
| cast 조건 | 성별·나이 정보가 담긴 짧은 `--cast`를 고름 | 얼굴·머리·의상 세부 묘사를 계약으로 고정하지 않음 |
| 장면 조건 | 거리·카페·옥상·공원·아트리움 중 생성 범위를 고름 | 같은 인물의 view 묶음이나 turnaround를 만들지 않음 |
| 검수 기준 | 프레임 없는 단일 장면, 얇은 선, 수채화 색층과 안료 질감 | identity, 얼굴 일관성, 연령·성별·인원수 승인 |

아래 실행은 22세 여성 1명을 거리 장면에서 생성합니다. 결과 PNG와 JSON은 모두 `review_required`이며, 인물 기준으로 자동 승인되지 않습니다.

```bash
PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
  .venv/bin/python docs/assets/part-07/chapter-05/p7_5_1_generate_style_conditioned_cast_candidates.py \
  --cast young_woman_solo \
  --compositions street
```

`--cast`는 성별·나이 정보만 고정한 짧은 생성 프롬프트를 고릅니다. `--compositions`는 거리·카페·옥상·공원·아트리움 장면을 고르는 생성 범위 목록입니다. 후보 PNG에는 `castID-장면ID-실행시각-seed`가 들어갑니다. JSON에는 선택한 성별·나이와 장면 구성, P7-5.1 텍스트 계약의 선·수채화 색층·안료 질감·프레임 없는 단일 장면이 유지되는지 확인할 검수 항목을 남깁니다.

`--steps`는 후보 하나의 확산 반복 횟수이며 기본값은 P7-5.1 기준과 같은 `50`입니다. 낮은 값은 빠른 후보 확인에는 쓸 수 있지만, 화풍·구도 검수를 통과시키는 근거가 되지는 않습니다.

```bash
PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
  .venv/bin/python docs/assets/part-07/chapter-05/p7_5_1_generate_style_conditioned_cast_candidates.py \
  --cast mixed_age_trio \
  --compositions cafe rooftop atrium
```

여러 장면을 한 번에 만들 때는 범위 목록만 바꿉니다. 성별·나이를 바꾸려면 `--cast`만 바꿉니다. 통과한 출력은 화풍 기준 이미지일 뿐 P7-5.2의 identity 기준이나 시점 묶음 입력은 아닙니다.

거리·옥상·카페·공원·아트리움에서 화풍 계약을 통과한 다섯 장면은 아래와 같습니다. 모두 프레임 없는 단일 장면, 얇은 charcoal 선, 반투명 수채화 색층과 안료 번짐을 기준으로 승인했습니다. 이 표는 인물의 얼굴·나이·성별·동일성을 보증하지 않습니다. 승인 목록과 파일명은 [인물 화풍 기준 manifest](../../../assets/part-07/chapter-05/p7-5-1-approved-cast-style-reference-pack.json)에 남깁니다.

| 거리 | 옥상 | 카페 |
| --- | --- | --- |
| ![승인된 거리 인물 화풍 기준 이미지](/AiBook/assets/part-07/chapter-05/p7-5-1-style-conditioned-cast-young_woman_solo-street-20260806T102546225026+0900-seed-62518-candidate.png) | ![승인된 옥상 인물 화풍 기준 이미지](/AiBook/assets/part-07/chapter-05/p7-5-1-style-conditioned-cast-young_woman_solo-rooftop-20260806T103100676848+0900-seed-62519-candidate.png) | ![승인된 카페 인물 화풍 기준 이미지](/AiBook/assets/part-07/chapter-05/p7-5-1-style-conditioned-cast-young_woman_solo-cafe-20260806T122039667151+0900-seed-62521-candidate.png) |

| 공원 | 아트리움 |
| --- | --- |
| ![승인된 공원 인물 화풍 기준 이미지](/AiBook/assets/part-07/chapter-05/p7-5-1-style-conditioned-cast-young_woman_solo-park-20260806T122039667151+0900-seed-62521-candidate.png) | ![승인된 아트리움 인물 화풍 기준 이미지](/AiBook/assets/part-07/chapter-05/p7-5-1-style-conditioned-cast-young_woman_solo-atrium-20260806T122039667151+0900-seed-62521-candidate.png) |

[화풍 조건 인물 후보 생성 코드 보기](/AiBook/assets/part-07/chapter-05/p7_5_1_generate_style_conditioned_cast_candidates.py){.aibook-source-link}

## 승인된 로컬 GPU 원본을 확인한다

아트리움 local-gpu-v5, 창가 독서실 local-gpu-v1과 도심·주택가·옥상 광장·courtyard·베니스·공원·열차 승강장 local-gpu-v1은 사람 승인 원본입니다. 여객기 실내는 반복 생성에서도 좌석 모듈·천장·사선 구도를 함께 안정적으로 만족시키지 못해 후보군과 생성 자산을 모두 폐기했고, 실내·밤·oblique 필수 행은 창밖의 밤과 작은 스탠드 조명만 사용하는 창가 독서실의 단순한 사선 구도로 대체했습니다. 아래 아홉 원본은 manifest에 기록돼 있습니다.

| 1열 | 2열 | 3열 |
| --- | --- | --- |
| **필수 행 1**<br>![새벽의 실내 아트리움을 위에서 내려다본 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-atrium-dawn-high-angle-local-gpu-v5.png)<br>**행 승인** · 실내 아트리움 · 새벽 · high angle · local GPU v5 | **보조 행 1**<br>![이른 아침 courtyard를 위에서 내려다본 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-courtyard-early-morning-high-angle-local-gpu-v1.png)<br>**보조 행 승인** · courtyard · 이른 아침 · high angle · local GPU v1 | **필수 행 2**<br>![창밖의 밤과 작은 스탠드 조명이 있는 창가 독서실 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-night-lit-reading-room-oblique-local-gpu-v1.png)<br>**행 승인** · 창가 독서실 · 밤 · oblique · local GPU v1 |
| **필수 행 3**<br>![맑은 낮 도심 교차로의 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-downtown-clear-day-wide-local-gpu-v1.png)<br>**행 승인** · 도심 · 낮 · wide eye-level · local GPU v1 | **필수 행 4**<br>![해질녘 주택가를 낮은 시점에서 올려다본 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-residential-sunset-low-angle-local-gpu-v1.png)<br>**행 승인** · 주택가 · 해질녘 · low angle · local GPU v1 | **필수 행 5**<br>![우천 야간의 옥상 광장을 위에서 내려다본 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-rooftop-rainy-night-overhead-local-gpu-v1.png)<br>**행 승인** · 옥상 광장 · 우천 야간 · overhead high angle · local GPU v1 |
| **보조 행 2**<br>![해질녘 베니스 운하를 사선으로 본 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-venice-sunset-oblique-local-gpu-v1.png)<br>**보조 행 승인** · 베니스 운하 · 해질녘 · oblique · local GPU v1 | **보조 행 3**<br>![맑은 낮 공원 연못의 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-park-clear-day-eye-level-local-gpu-v1.png)<br>**보조 행 승인** · 공원 연못 · 낮 · eye-level · local GPU v1 | **보조 행 4**<br>![우천 야간 열차 승강장의 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-train-platform-rainy-night-oblique-local-gpu-v1.png)<br>**보조 행 승인** · 열차 승강장 · 우천 야간 · oblique · local GPU v1 |

아홉 장면은 모두 사람 승인을 받았습니다. 이름과 역할은 [manifest](../../../assets/part-07/chapter-05/p7-5-1-approved-style-reference-pack.json)에 남기고, 실행 이력은 커밋하지 않는 로컬 검수 기록으로 분리합니다. 후속 캐릭터 참조 생성의 실제 입력 계약은 P7-5.2에서 다시 정합니다.

## 체크리스트

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| 원본 | crop 없이 프레임 없는 생성 원본인가? |
| 선과 색 | 선화가 살아 있고 수채화 색층이 선을 덮지 않는가? |
| 시간 | 새벽·낮·해질녘·밤·우천 야간이 실제 광원 차이로 읽히는가? |
| 카메라 | 같은 중앙 소실점 반복이 아니라 camera family가 다른가? |
| 실패 해석 | 실패 원인을 crop이나 `status` 변경으로 덮지 않고 다음 구도·피사체 밀도·광원 조건으로 바꿨는가? |
| 생성 출처 | 참조 원본이 로컬 GPU 생성 스크립트와 사람 검수 ledger에 연결되고, 내장 이미지 생성 자산이 섞이지 않았는가? |
| 최종 승인 기록 | 아홉 원본의 사람 승인을 ledger와 manifest에 남기고, 현재 P7-5.1 cast 후보 생성에는 배경 PNG 대신 텍스트 화풍 계약만 사용했는가? |

## 출처와 참고 자료

- Black Forest Labs, [FLUX.2 Klein 4B model card](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-04.
- Hugging Face, [Diffusers Flux2 pipeline](https://huggingface.co/docs/diffusers/api/pipelines/flux2){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-04.
- Hugging Face, [Diffusers Reduce memory usage](https://huggingface.co/docs/diffusers/optimization/memory){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-04.
