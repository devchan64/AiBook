# P7-5.1 화풍 참조 셋 생성: 로컬 GPU로 프레임 없는 기준 만들기

> Section ID: `P7-5.1`
> Version: `v2026.08.04`

캐릭터를 만들기 전에 화풍 기준을 먼저 고정해야 할 때가 있습니다. 여기서 화풍 참조 셋은 보기 좋은 배경을 모은 폴더가 아닙니다. 인물과 소품을 넣기 전, 선의 역할, 색의 겹침, 시간대의 광원, 장소의 폭, 카메라 구도를 **같은 기준으로 비교할 수 있게 만든 검수 입력**입니다. 한 장이 마음에 들어도 다른 장소와 카메라에서 계약이 무너지면, 그 한 장은 캐릭터 참조 셋의 화풍 기준이 될 수 없습니다.

이 절의 질문은 **8 GB급 로컬 GPU에서 만든 배경 화풍 표본이 다음 캐릭터 참조 셋의 기준이 되려면 무엇을 검수해야 하는가**입니다. 이 절의 산출물은 승인된 화풍 그 자체가 아니라, 후보 이미지·행별 판정·실패 이유·다음 생성을 막거나 통과시키는 gate입니다.

## 화풍 참조 셋은 생성과 검수가 번갈아 가는 파이프라인이다

화풍 생성은 프롬프트 한 번으로 끝나지 않습니다. 먼저 어떤 선과 색을 유지할지 계약을 고정하고, 그 계약이 장소·시간·카메라가 달라져도 남는지 확인할 장면 행렬을 만듭니다. 각 행의 원본을 생성한 뒤 사람은 프레임, 선, 색, 장소, 시간, 카메라를 함께 검수합니다. 불합격이면 이미지를 crop하거나 상태만 바꾸지 않고, 실패 원인을 다음 프롬프트의 장면 구조로 바꿔 같은 행을 다시 생성합니다.

```mermaid
--8<-- "assets/part-07/chapter-05/p7-5-1-style-reference-pipeline-ko.mmd"
```

이 흐름에서 모델은 후보를 만들고, 사람은 후보가 계약을 지키는지 판단합니다. `행 승인`은 한 조건에서의 통과이고, `전체 팩 승인`은 모든 필수 행과 보조 근거를 함께 비교한 뒤의 결론입니다. 승인된 뒤에도 다음 생성은 타일로 합친 이미지를 쓰지 않고 manifest의 개별 원본 하나만 화풍 입력으로 선택합니다.

| 파이프라인 층 | 고정하거나 바꾸는 것 | 다음 단계로 남기는 것 |
| --- | --- | --- |
| 화풍 계약 | 선·수채화 색층·프레임 금지 조건 | 통과·불합격 기준 |
| 장면 행렬 | 장소·시간·카메라 조합 | 필수 행과 보조 행 목록 |
| 행별 생성 | seed와 장면의 구체 구성 | crop하지 않은 후보 원본 |
| 사람 검수 | 외곽·선·색·장소·시간·카메라 판정 | 승인, 불합격 이유, 재생성 지시 |
| 전체 팩 승인 | 행 사이의 일관성과 입력 범위 | ledger의 최종 결론과 manifest |

## AI 모델은 텍스트 조건과 seed에서 후보 원본을 만든다

앞의 흐름도는 작업과 판단의 순서이고, 아래는 그중 **후보 한 장을 만드는 모델 내부 경계**를 단순화한 그림입니다. 이 실습의 `Flux2KleinPipeline`은 사전 학습된 FLUX.2 Klein 4B 가중치를 읽고, 장면 prompt와 공통 화풍 계약을 text condition으로 받아 seed에서 시작한 이미지 표현을 정해진 횟수만큼 갱신합니다. 코드의 `num_inference_steps=50`은 이 배치에서 반복 갱신한 횟수이고, `guidance_scale=4.0`은 텍스트 조건을 따르는 정도에 관여하는 실행 설정입니다. 이 숫자 자체가 화풍의 승인 기준은 아닙니다.

```mermaid
--8<-- "assets/part-07/chapter-05/p7-5-1-ai-model-inference-pipeline-ko.mmd"
```

`COMMON_CONTRACT`와 장면별 `prompt`는 별도의 negative prompt 입력이 아니라 하나의 텍스트 조건으로 이어 붙여 전달됩니다. 따라서 `no panel` 같은 금지 문구는 모델에게 원하는 결과를 보장하는 규칙이 아니라, 다른 장면 설명과 함께 해석되는 조건입니다. 프레임이 생기면 모델이 그 조건을 완전히 따르지 못한 것이므로, crop으로 고치지 않고 새 장면 구조와 prompt로 다시 생성합니다.

`torch.Generator(device="cpu").manual_seed(...)`의 seed는 같은 실행 조건에서 시작점을 다시 잡게 하는 값입니다. seed를 고정하면 비교의 출발점을 기록할 수 있지만, 다른 GPU·라이브러리·모델 버전에서도 픽셀까지 같은 결과를 보장하지는 않습니다. `enable_sequential_cpu_offload()`는 필요한 모델 모듈을 CPU와 GPU 사이에서 순차적으로 옮겨 GPU 상주 메모리를 줄이는 방법입니다. 모델의 화풍 판단 능력을 높이는 설정은 아닙니다.

모델 단계의 출력은 `images[0]`의 PNG와 터미널에 출력되는 실행 요약까지입니다. `approved`라는 결론, 필수 행 충족, 다음 단계 입력 가능 여부는 모델이 계산하지 않습니다. 그 판단은 생성 뒤 사람 검수와 ledger가 맡습니다. FLUX.2 Klein 4B는 텍스트 기반 이미지 생성과 참조 편집을 지원하는 rectified-flow transformer이며, prompt를 완전히 따르지 못하거나 텍스트를 왜곡할 수 있다는 한계도 모델 카드에 명시되어 있습니다.

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

## 배경 화풍과 인물 색 계약은 다르다

이 절의 원본은 배경에서 선과 수채 색면이 어떻게 겹치고, 시간대별 광원이 공간의 명도와 반사에 어떻게 나타나는지를 정합니다. 따라서 아트리움의 차가운 새벽빛이나 우천 야간 승강장의 남색 그림자를 그대로 인물의 피부나 머리카락 기본색으로 옮기지 않습니다. 그렇게 하면 같은 캐릭터가 장소마다 다른 피부색과 머리색으로 보일 수 있습니다.

P7-5.1이 다음 단계에 넘기는 것은 얇은 charcoal 선, 반투명 색층, 프레임 없는 캔버스, 시간대별 배경 광원이라는 **배경 화풍 계약**입니다. P7-5.2는 중립 조명에서 머리카락·피부·눈·의상 색을 별도 character contract로 정하고, full body와 얼굴의 일관성을 검수합니다. 배경의 밤·노을·비는 컷신에서 인물에 약한 반사광을 더할 수는 있어도, 승인된 기본색을 새로 정의하는 근거가 될 수 없습니다.

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

## 하나의 생성 스크립트에서 공통 계약과 장면 변수를 분리한다

실제 후보 생성에는 Diffusers의 `Flux2KleinPipeline`을 사용합니다. 현재 아홉 행을 만드는 `p7_5_1_regenerate_local_gpu_style_references.py`만 이 절의 실행 코드입니다. `COMMON_CONTRACT`에는 모든 장면에 공통인 full-bleed, 선, 수채화, 금지 조건을 두고, `SCENES`에는 장면마다 달라져야 하는 장소·시간·카메라·seed를 둡니다. 이 분리가 없으면 장면의 차이 때문에 화풍이 달라졌는지, 화풍 계약 자체가 무너졌는지 구별하기 어렵습니다.

| 코드 위치 | 파이프라인에서 하는 일 | 읽을 때 볼 지점 |
| --- | --- | --- |
| `COMMON_CONTRACT` | 모든 행에 적용하는 화풍·프레임 금지 계약 | `fills all four canvas edges`, charcoal line, transparent watercolor, 금지 질감 |
| `SCENES` | 행마다 바꾸는 장소·시간·카메라와 seed | 같은 계약 아래 어떤 조건을 비교하는지 |
| `enable_sequential_cpu_offload()` | 8 GB급 GPU에서 모델을 순차적으로 옮겨 실행 | 품질 설정이 아니라 메모리 운용 방식 |
| `pipe(...)` | 한 장면 원본을 생성 | 해상도, step, guidance, seed가 재현 조건임 |
| `P7_STYLE_SCENE` | 한 행만 선택하거나 아홉 행 전체를 선택 | 실행 시간을 줄여도 전체 팩 승인은 별도라는 경계 |
| `record`와 `print(...)` | 시간·GPU 메모리·출력 파일을 터미널에 요약 | 생성 성공과 사람 승인을 구분하는 운영 확인 |

바꿔 볼 값은 한 `SCENES` 행의 `prompt` 또는 `seed`입니다. `P7_STYLE_SCENE`에 행 ID를 넣으면 한 장면만, 값을 비우면 아홉 행을 생성합니다. 이 차이는 실행 시간을 줄이기 위한 것이며, 한 행을 생성했다고 전체 팩이 승인되는 것은 아닙니다. 새 PNG가 예뻐 보이는지만 보지 말고, 같은 행의 프레임·선·색·시점 조건이 달라지는지를 ledger에서 다시 판정합니다. `guidance_scale`이나 step을 바꾸는 것은 별도의 비교 실험으로 기록해야 합니다.

이전의 시간대 균형 배치와 표적 재생성 파일은 같은 실행 골격에 당시의 `SCENES`만 기록한 이력입니다. 따라서 별도의 생성 방법이나 두 번째 실행 경로로 설명하지 않습니다. P7-5.1의 참조 원본은 로컬 GPU로 생성한 것만 사용할 수 있으며, 내장 이미지 생성으로 만든 자산은 입력·승인·manifest에서 제외했습니다.

<details id="local-gpu-style-reference-regeneration" class="aibook-lazy-source" data-source="/AiBook/assets/part-07/chapter-05/p7_5_1_regenerate_local_gpu_style_references.py" data-language="python">
<summary>아홉 로컬 GPU 화풍 후보 생성 코드 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

### 코드 흐름과 바꿀 값

`main()`은 먼저 `P7_STYLE_SCENE`, `P7_STYLE_EXCLUDE`, `P7_STYLE_RUN_LABEL`을 읽습니다. 예를 들어 `P7_STYLE_SCENE=atrium-dawn-high-angle`는 한 행만 생성하고, `P7_STYLE_EXCLUDE=atrium-dawn-high-angle`은 전체 실행에서 해당 행을 뺍니다. `P7_STYLE_RUN_LABEL=v2`처럼 label을 바꾸면 PNG 파일명이 달라져 이전 run을 덮어쓰지 않습니다.

| 순서 | 코드가 하는 일 | 사람이 확인할 것 |
| --- | --- | --- |
| 1. 행 선택 | `SCENES`에서 요청·제외 조건에 맞는 행을 만든다 | 선택한 행이 필수 행인지 보조 행인지 ledger에서 구분 |
| 2. 메모리 관측 | `gpu_memory_mib()`와 daemon thread가 실행 중 peak VRAM을 약 0.2초 간격으로 기록한다 | peak 값은 실행 가능성 근거이지 이미지 품질 점수가 아님 |
| 3. pipeline 준비 | BF16 가중치를 읽고 `enable_sequential_cpu_offload()`를 켠다 | 8 GB 운용 설정이며 화풍을 고정하는 기능은 아님 |
| 4. 행별 생성 | `scene["prompt"] + COMMON_CONTRACT`와 CPU seed를 `pipe(...)`에 넣고 PNG를 저장한다 | prompt는 장소·시간·camera, contract는 공통 화풍 조건을 맡음 |
| 5. 실행 요약과 사람 판정 | 각 PNG의 seed·시간·파일명과 peak VRAM을 터미널에 출력하고, 사람 판정은 ledger에 쓴다 | 출력 요약은 후보 생성 확인이고, ledger의 상태만 승인 근거 |

행마다 `torch.cuda.empty_cache()`를 호출하는 것은 다음 행을 위한 캐시 반환 요청입니다. GPU 메모리 사용량을 0으로 만들거나 결과 품질을 높이지는 않습니다. pipeline 초기화나 한 행 생성에서 예외가 나면 `finally`가 메모리 관측 thread만 멈춘 뒤 예외를 다시 올리므로, 성공한 것처럼 실행 요약을 출력하지 않습니다. 실행이 끝난 뒤 사람은 PNG를 보고 ledger에 행 승인·불합격 이유를 남깁니다.

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

여기서 `COMMON_CONTRACT`를 바꾸면 아홉 행 전체의 비교 기준이 달라집니다. 반대로 `SCENES`의 한 `prompt`를 바꾸면 그 행의 장소·시간·카메라만 재생성합니다. `seed`를 바꾸면 같은 조건의 다른 출발점을 비교할 수 있지만, 프레임 없음이나 물리적으로 가능한 공간을 보장하지는 않습니다.

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

`enable_sequential_cpu_offload()`는 이 4B 모델을 8 GB급 GPU에서 실행하기 위한 메모리 절약 장치입니다. `width`·`height`·step·guidance·seed는 코드와 터미널 요약으로 확인하는 재현 조건이며, 이 값들을 바꾼 결과는 별도 run으로 비교해야 합니다. 이 블록의 `image.save(...)`가 성공했다는 사실은 후보 PNG가 생겼다는 뜻뿐입니다. 외곽선·수채화 질감·공간의 물리성·필수 행 충족 여부는 다음의 사람 검수에서 판정합니다.

## 다섯 필수 행과 보조 근거를 분리한다

로컬 GPU에서 후보를 만들 수 있다는 사실은 화풍 팩 승인과 다릅니다. 재생성 후보는 다섯 필수 행을 하나씩 채우고, 보조 후보는 다른 장소·시간·시점에서도 계약이 유지되는지를 확인합니다. 현재는 아트리움·도심·주택가·옥상 광장의 네 필수 행과 베니스·공원·열차 승강장 보조 행이 사람 승인을 받았습니다. 폐기한 여객기 행은 창밖이 밤이고 작은 스탠드 조명이 있는 창가 독서실의 사선 구도로 대체합니다. 이른 아침 courtyard도 검수 대기입니다.

| 필수 행 | 로컬 GPU 재생성 후보 | 현재 판정 | 이 행이 확인하는 것 |
| --- | --- | --- | --- |
| 실내·새벽·high angle | 아트리움 local-gpu-v5 | 행 승인 | 새벽 광원과 실내 하향 시점 |
| 실내·밤·oblique | 창가 독서실 local-gpu-v1 | 행 승인 | 창밖의 밤, 작은 스탠드 조명, 사선 시점 |
| 실외·낮·wide eye-level | 도심 낮 local-gpu-v1 | 행 승인 | 낮 팔레트와 측면 교차로 시점 |
| 실외·해질녘·low angle | 주택가 local-gpu-v1 | 행 승인 | 제한된 석양빛과 curb-height 상향 시점 |
| 실외·우천 야간·overhead high angle | 옥상 광장 local-gpu-v1 | 행 승인 | 젖은 바닥 반사와 하향 야간 시점 |

이른 아침 courtyard, 베니스 운하, 공원 연못, 열차 승강장은 보조 후보입니다. 각각 high-angle, oblique, 낮 팔레트, 우천 야간 조명을 넓혀 보지만 다섯 필수 행을 대체하지는 않습니다. 불합격 후보는 crop이나 상태값 변경으로 살리지 않고, 실패 이유만 [검수 ledger](../../../assets/part-07/chapter-05/p7-5-1-local-style-pack-review.json)에 남깁니다.

| 보조 행 | 로컬 GPU 재생성 후보 | 넓혀 보는 화풍 조건 |
| --- | --- | --- |
| 이른 아침 courtyard · high angle | courtyard local GPU 후보 | 실외 자연광에서 하향 시점의 선·색면 |
| 베니스 운하 · 석양 · oblique | 베니스 local-gpu-v1 · 행 승인 | 제한된 apricot 역광과 사선 수면 |
| 공원 연못 · 낮 · eye-level | 공원 local-gpu-v1 · 행 승인 | 자연 공간의 낮 팔레트와 수면 반사 |
| 열차 승강장 · 우천 야간 · oblique | 승강장 local-gpu-v1 · 행 승인 | 인공광, 젖은 바닥, 짧은 대각 철로 |

## Python 검수 gate는 사람 판정의 누락을 막는다

생성기가 PNG를 만들면, 다음 코드는 [검수 ledger](../../../assets/part-07/chapter-05/p7-5-1-local-style-pack-review.json)의 다음 실행 행렬과 최종 상태를 읽어 P7-5.2 진입을 막거나 허용합니다. 이미지를 보고 선·색·프레임을 자동 채점하는 모델은 아닙니다. 그 판단은 사람이 ledger에 먼저 기록해야 합니다.

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

<details id="local-style-pack-gate" class="aibook-lazy-source" data-source="/AiBook/assets/part-07/chapter-05/p7_5_1_local_style_pack_gate.py" data-language="python">
<summary>화풍 참조 팩 검수 gate 코드 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

## 실패 원인을 다음 프롬프트의 구조로 바꾸기

실패한 후보에 `no frame`이나 `no hatching`을 더 쓰는 것만으로는 충분하지 않았습니다. 도심은 넓은 도로를 요청했을 때 중앙 소실점의 거리 복도로 수렴했습니다. 이를 고치기 위해 금지어를 늘리는 대신, 가까운 모퉁이에서 옆으로 건너다보는 **측면 교차로**로 장면 구조를 바꿨습니다. 복잡한 실내 좌석 배치는 요구가 길어질수록 공간 구조를 안정적으로 제어하지 못해 이 참조 팩의 범위에서 폐기했습니다. 대체 장면은 필요한 시간·카메라 조건을 더 단순한 구조로 검증해야 합니다.

반대로 장가계는 외곽 프레임은 사라졌지만 절벽의 반복 선이 해칭처럼 남았고, 우천 야간 플랫폼은 비·레일·지붕 선이 화면을 지배했습니다. 이 경우에는 crop이나 부분 보정으로 통과시키지 않습니다. `무엇이 틀렸는가`를 다음 생성의 구도·피사체 밀도·광원 조건으로 번역하고, 새 원본을 다시 검수합니다.

## 사람 판정은 로컬 GPU 원본만 승인한다

사람이 판단하는 것은 이미지의 미적 품질 점수 하나가 아닙니다. 각 원본에서 외곽·선·색·장소·시간·카메라와 **로컬 GPU 생성 기록**을 확인하고, 그 이유를 ledger에 적습니다. 내장 이미지 생성 원본은 사람 검수를 통과했더라도 P7-5.1에서 승인할 수 없으므로 입력·승인·manifest에서 제외했습니다. 현재 참조 셋은 `approved_for_character_reference`입니다.

로컬 GPU 후보가 다섯 필수 행과 네 보조 근거를 모두 채우고 사람 승인을 받아야 P7-5.2가 manifest에서 고른 개별 원본 하나를 화풍 입력으로 사용할 수 있습니다. 그 뒤에도 캐릭터 identity, 시점 묶음, 권리 확인은 캐릭터 참조 팩의 별도 검수 대상입니다. 최종 결론은 별도의 sheet가 아니라 ledger의 사람 판단으로 기록합니다.

## 승인 원본 manifest

사람의 판단은 행별 승인·불합격 이유와 최종 결론을 [검수 ledger](../../../assets/part-07/chapter-05/p7-5-1-local-style-pack-review.json)에 기록하는 것으로 충분합니다. 별도의 contact sheet를 만들지 않습니다. 다음 단계는 [manifest](../../../assets/part-07/chapter-05/p7-5-1-approved-style-reference-pack.json)가 가리키는 개별 원본 중 하나만 선택해 사용합니다.

이 참조 셋의 상태는 `approved_for_character_reference`다. manifest에는 아홉 개의 사람 승인 로컬 GPU 원본을 기록했으며, 다음 생성은 이 중 하나의 개별 원본만 화풍 입력으로 선택한다.

## 승인된 로컬 GPU 원본과 검수 대기 후보를 구분한다

아트리움 local-gpu-v5, 창가 독서실 local-gpu-v1과 도심·주택가·옥상 광장·courtyard·베니스·공원·열차 승강장 local-gpu-v1은 사람 승인 원본입니다. 여객기 실내는 반복 생성에서도 좌석 모듈·천장·사선 구도를 함께 안정적으로 만족시키지 못해 후보군과 생성 자산을 모두 폐기했고, 실내·밤·oblique 필수 행은 창밖의 밤과 작은 스탠드 조명만 사용하는 창가 독서실의 단순한 사선 구도로 대체했습니다. 아홉 원본은 manifest에 기록돼 있습니다.

- ![새벽의 실내 아트리움을 위에서 내려다본 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-atrium-dawn-high-angle-local-gpu-v5.png)

  **행 승인** · 실내 아트리움 · 새벽 · high angle · local GPU

- ![이른 아침 courtyard를 위에서 내려다본 local GPU 화풍 검수 후보](/AiBook/assets/part-07/chapter-05/p7-5-1-style-courtyard-early-morning-high-angle-local-gpu-v1.png)

  **행 승인** · courtyard · 이른 아침 · high angle · local GPU

- ![창밖의 밤과 작은 스탠드 조명이 있는 창가 독서실 local GPU 화풍 검수 후보](/AiBook/assets/part-07/chapter-05/p7-5-1-style-night-lit-reading-room-oblique-local-gpu-v1.png)

  **행 승인** · 창가 독서실 · 밤 · oblique · local GPU v1

- ![맑은 낮 도심 교차로의 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-downtown-clear-day-wide-local-gpu-v1.png)

  **행 승인** · 도심 · 낮 · wide eye-level · local GPU

- ![해질녘 주택가를 낮은 시점에서 올려다본 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-residential-sunset-low-angle-local-gpu-v1.png)

  **행 승인** · 주택가 · 해질녘 · low angle · local GPU

- ![우천 야간의 옥상 광장을 위에서 내려다본 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-rooftop-rainy-night-overhead-local-gpu-v1.png)

  **행 승인** · 옥상 광장 · 우천 야간 · overhead high angle · local GPU

- ![해질녘 베니스 운하를 사선으로 본 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-venice-sunset-oblique-local-gpu-v1.png)

  **보조 행 승인** · 베니스 운하 · 해질녘 · oblique · local GPU

- ![맑은 낮 공원 연못의 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-park-clear-day-eye-level-local-gpu-v1.png)

  **보조 행 승인** · 공원 연못 · 낮 · eye-level · local GPU

- ![우천 야간 열차 승강장의 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-train-platform-rainy-night-oblique-local-gpu-v1.png)

  **보조 행 승인** · 열차 승강장 · 우천 야간 · oblique · local GPU

{: .aibook-style-reference-grid}

아홉 장면은 모두 사람 승인을 받았습니다. 이름과 역할은 [manifest](../../../assets/part-07/chapter-05/p7-5-1-approved-style-reference-pack.json)에, 판정과 실행 이력은 [검수 ledger](../../../assets/part-07/chapter-05/p7-5-1-local-style-pack-review.json)에 남깁니다. P7-5.2는 타일로 합친 비교 이미지를 입력으로 쓰지 않고 이 중 하나의 개별 원본만 선택합니다.

## 체크리스트

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| 원본 | crop 없이 프레임 없는 생성 원본인가? |
| 선과 색 | 선화가 살아 있고 수채화 색층이 선을 덮지 않는가? |
| 시간 | 새벽·낮·해질녘·밤·우천 야간이 실제 광원 차이로 읽히는가? |
| 카메라 | 같은 중앙 소실점 반복이 아니라 camera family가 다른가? |
| 실패 해석 | 실패 원인을 crop이나 `status` 변경으로 덮지 않고 다음 구도·피사체 밀도·광원 조건으로 바꿨는가? |
| 생성 출처 | 참조 원본이 로컬 GPU 생성 스크립트와 사람 검수 ledger에 연결되고, 내장 이미지 생성 자산이 섞이지 않았는가? |
| 최종 승인 기록 | 아홉 원본의 사람 승인을 ledger에 남기고, 다음 생성에는 manifest의 개별 원본 하나만 사용했는가? |

## 출처와 참고 자료

- Black Forest Labs, [FLUX.2 Klein 4B model card](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-03.
- Hugging Face, [Diffusers FLUX.2 Klein pipeline](https://huggingface.co/docs/diffusers/main/en/api/pipelines/flux2_klein){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-03.
