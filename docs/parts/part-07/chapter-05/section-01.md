# P7-5.1 화풍 참조 셋 생성: 로컬 GPU로 프레임 없는 기준 만들기

> Section ID: `P7-5.1`
> Version: `v2026.08.18`

이 프로젝트는 Qwen Image로 배경 화풍 후보를 생성하고 사람 검수 뒤 승인 참조 셋에 반영합니다. 화풍 참조 셋은 보기 좋은 배경을 모은 폴더가 아닙니다. 선의 역할, 색의 겹침, 시간대의 광원, 장소의 폭, 카메라 구도를 **같은 기준으로 비교할 수 있게 만든 검수 입력**입니다. 한 장이 마음에 들어도 다른 장소와 카메라에서 계약이 무너지면, 화풍 기준으로 승인하지 않습니다.

이 절의 질문은 **로컬 GPU에서 Qwen Image로 만든 배경 화풍 표본을 승인하려면 무엇을 검수해야 하는가**입니다. 이 절의 산출물은 승인된 화풍 그 자체가 아니라, 후보 이미지·행별 판정·실패 이유·다음 단계 사용 가능 여부를 판정하는 gate입니다.

웹툰 컷 생성 전체를 한 번에 해결하려고 하지 않습니다. 이 절은 8 GB VRAM 환경에서 배경의 선·색·광원·카메라 계약을 먼저 만들고 검수하는 데 한정합니다. 한 단계의 출력이 다음 단계에서 쓰이려면, 생성된 이미지가 마음에 드는지를 넘어서 어떤 조건을 통과했는지 기록되어야 합니다.

## 화풍 참조 셋은 생성과 검수가 번갈아 가는 파이프라인이다

화풍 생성은 [프롬프트](../../../reference/concept-glossary-parts/13-pieup.md#prompt) 한 번으로 끝나지 않습니다. 먼저 어떤 선과 색을 유지할지 계약을 고정하고, 그 계약이 장소·시간·카메라가 달라져도 남는지 확인할 장면 행렬을 만듭니다. 각 행의 원본을 생성한 뒤 사람은 프레임, 선, 색, 장소, 시간, 카메라를 함께 검수합니다. 불합격이면 이미지를 crop하거나 상태만 바꾸지 않고, 실패 원인을 다음 프롬프트의 장면 구조로 바꿔 같은 행을 다시 생성합니다.

```mermaid
--8<-- "assets/part-07/chapter-05/p7-5-1-style-reference-pipeline-ko.mmd"
```

이 흐름에서 모델은 배경 후보를 먼저 만들고, 사람은 후보가 계약을 지키는지 판단합니다. `행 승인`은 한 조건에서의 통과이고, `전체 팩 승인`은 모든 필수 행과 보조 근거를 함께 비교한 뒤의 결론입니다. 승인된 뒤에도 타일로 합친 비교 이미지는 모델 입력으로 쓰지 않습니다.

| 파이프라인 층 | 고정하거나 바꾸는 것 | 다음 단계로 남기는 것 |
| --- | --- | --- |
| 화풍 계약 | 선·수채화 색층·프레임 금지 조건 | 통과·불합격 기준 |
| 장면 행렬 | 장소·시간·카메라 조합 | 필수 행과 보조 행 목록 |
| 행별 생성 | seed와 장면의 구체 구성 | crop하지 않은 후보 원본 |
| 사람 검수 | 외곽·선·색·장소·시간·카메라 판정 | 승인, 불합격 이유, 재생성 지시 |
| 전체 팩 승인 | 행 사이의 일관성과 입력 범위 | ledger의 최종 결론과 manifest |

## Qwen Image도 조건 검수가 필요하다

Qwen Image는 text-to-image와 이미지 편집을 지원하는 이미지 생성 모델이며, 공개 모델 카드는 Apache 2.0 라이선스와 `QwenImagePipeline` 사용 예시를 제공합니다. 이 실험은 Diffusers의 `QwenImagePipeline`에 Nunchaku FP4 r128 transformer를 연결해 로컬 GPU에서 후보를 만듭니다.

로컬에서 이미지가 생성된다고 해서 웹툰 컷 파이프라인이 안정적이라는 뜻은 아닙니다. 이 실행은 Nunchaku transformer offload와 `enable_sequential_cpu_offload()`로 GPU 상주량을 줄이고 한 행씩 생성합니다. 따라서 P7-5.1은 모델이 좋은 배경 이미지를 만들 수 있는지 보는 절이 아니라, **다음 단계 입력으로 넘겨도 되는 조건을 사람이 판정하는 절**입니다.

| 구분 | 이 실험에서 유리한 점 | 조심할 점 |
| --- | --- | --- |
| 실행 구성 | Qwen Image와 양자화 transformer로 로컬 후보를 반복 생성할 수 있음 | offload와 양자화가 화풍·구도 계약 통과를 보장하지 않음 |
| 기능 범위 | text-to-image와 이미지 편집 흐름을 시험할 수 있음 | 기능 지원이 곧 화풍 계약 통과를 뜻하지 않음 |
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

## 배경 화풍 계약의 범위

P7-5.1이 고정하는 것은 Qwen Image 참조 원본이 따라야 할 얇은 charcoal 선, 반투명 색층, 프레임 없는 캔버스, 시간대별 배경 광원입니다. 이 절에서는 배경의 선·색·공간·카메라만 검수하고, 다른 생성 단계의 기준은 여기서 승인하지 않습니다.

## 다섯 행이 있어야 한 장의 우연을 구별할 수 있다

한 장면에서 seed만 바꾸면 다른 장소와 카메라를 다뤘다고 볼 수 없습니다. 다음 다섯 행은 같은 장면의 변형이 아니라, 장소·시간·카메라가 모두 다른 최소 검수 집합입니다. 새벽의 실내 고각도와 우천 야간의 overhead high angle은 빛과 원근을 동시에 시험하므로, 낮의 거리 한 장으로 대신할 수 없습니다.

| scene ID | 장소 | 시간 | 카메라 |
| --- | --- | --- | --- |
| `indoor-dawn-high-angle` | 실내 | 새벽 | high angle |
| `indoor-night-oblique` | 실내 | 밤 | oblique side view |
| `outdoor-day-wide` | 실외 | 낮 | wide eye-level |
| `outdoor-sunset-low-angle` | 실외 | 해질녘 | low angle |
| `outdoor-rainy-night-overhead` | 실외 | 우천 야간 | overhead high angle |

각 행에는 사람·동물·차량·읽을 수 있는 표지·글자를 넣지 않습니다. 화풍 팩은 배경의 매체 처리와 공간 조건만 검수하는 자산입니다. 프롬프트에는 `no border frame`, `no panel`, `fill the canvas edge to edge`를 함께 쓰되, 이 단어가 있다고 통과로 처리하지 않습니다. 출력 원본에서 프레임이 보이면 그 이미지는 crop으로 살리지 않고 불합격입니다.

## 실행 코드는 공통 계약과 장면 변수를 분리한다

배경 후보 생성에는 Diffusers의 `QwenImagePipeline`을 사용합니다. 스무 장면 후보를 만드는 기준 실행 코드는 `p7_5_1_regenerate_local_gpu_style_references.py`입니다. 학습 관점에서 이 코드는 세 가지를 구분하게 해 줍니다. 첫째, 모든 행에 같은 화풍 계약을 붙입니다. 둘째, 행마다 장소·시간·카메라·seed만 바꿉니다. 셋째, 생성 성공과 사람 승인을 별도 기록으로 남깁니다.

공통 화풍 계약은 [화풍 프롬프트 JSON](../../../assets/part-07/chapter-05/p7-5-1-style-prompt-contract.json)에 분리한다. 이 자산에는 프레임 없는 캔버스, 얇은 charcoal 선, 반투명 수채화 색층, 안료 질감, 제외 대상만 들어 있다. 장소·시간·카메라는 실행 코드의 장면별 prompt가 맡으므로, 한 행의 공간 문제를 고칠 때 공통 화풍 계약을 함께 바꾸지 않는다.

현재 `background-style-v3` 계약은 같은 핵심 조건을 47단어에서 30단어로 압축했다. 1~3번 승인 원본은 이 v3 계약으로 재생성했다. 초기 v1 실행 JSON은 당시 사용한 전문과 단어 수를 보존하므로, 계약을 바꿔도 과거 재현 기록을 소급해 바꾸지 않는다.

| 코드 위치 | 바꾸면 달라지는 것 | 학습할 경계 |
| --- | --- | --- |
| 화풍 프롬프트 JSON의 `common_contract` | 스무 장면 전체의 선·수채화·프레임 금지 기준 | 공통 계약을 바꾸면 이전 행과 직접 비교하기 어려움 |
| `SCENES`의 `prompt` | 한 행의 장소·시간·카메라 구조 | 실패 원인은 금지어보다 장면 구조로 고침 |
| `SCENES`의 `seed` | 같은 조건의 다른 출발점 | seed 고정은 비교 기록이지 품질 보장이 아님 |
| `P7_STYLE_SCENE`, `P7_STYLE_EXCLUDE` | 생성할 행의 범위 | 한 행 생성은 전체 팩 승인이 아님 |
| `STEPS`, `TRUE_CFG_SCALE`, 해상도 | 추론 조건 전체 | 값을 바꾸면 별도 비교 실험으로 기록함 |
| 터미널 실행 요약 | 시간·GPU 메모리·출력 파일 | 생성 성공과 사람 승인을 분리함 |

이전의 시간대 균형 배치와 표적 재생성 파일은 같은 실행 골격에 당시의 `SCENES`만 기록한 이력입니다. 따라서 별도의 생성 방법이나 두 번째 실행 경로로 설명하지 않습니다. P7-5.1의 참조 원본은 로컬 GPU로 생성한 것만 사용할 수 있으며, 내장 이미지 생성으로 만든 자산은 입력·승인·manifest에서 제외했습니다.

[스무 로컬 GPU 화풍 후보 생성 코드 보기](/AiBook/assets/part-07/chapter-05/p7_5_1_regenerate_local_gpu_style_references.py){.aibook-source-link}

### 공통 화풍 계약과 장면 조건이 만나는 코드

아래는 실행 파일에서 가져온 핵심 발췌입니다. 긴 영어 prompt를 그대로 반복하지 않고, 독자가 **모든 행에 유지할 조건**과 **한 행에서만 바꿀 조건**의 경계를 읽도록 축약했습니다. 실제 실행 때는 바로 위의 전체 소스를 기준으로 합니다.

```python
# 모든 장면에 같은 조건을 붙인다.
STYLE_PROMPT_PATH = ASSET_DIR / "p7-5-1-style-prompt-contract.json"
COMMON_CONTRACT = json.loads(
    STYLE_PROMPT_PATH.read_text(encoding="utf-8")
)["common_contract"]

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

여기서 `COMMON_CONTRACT`를 바꾸면 스무 행 전체의 비교 기준이 달라집니다. 반대로 `SCENES`의 한 `prompt`를 바꾸면 그 행의 장소·시간·카메라만 재생성합니다.

다음 발췌는 한 행을 실제로 만드는 부분입니다. `P7_STYLE_SCENE`을 바꾸면 `scenes`에 남는 행 수가 바뀌고, `run_label`을 `v2`처럼 바꾸면 기존 PNG를 덮어쓰지 않고 새 파일로 남깁니다.

```python
transformer = NunchakuQwenImageTransformer2DModel.from_pretrained(TRANSFORMER_ID)
transformer.set_offload(True, use_pin_memory=False, num_blocks_on_gpu=1)
pipe = QwenImagePipeline.from_pretrained(
    MODEL_ID, transformer=transformer, torch_dtype=torch.bfloat16
)
pipe._exclude_from_cpu_offload.append("transformer")
pipe.enable_sequential_cpu_offload()

for scene in scenes:
    image = pipe(
        prompt=scene["prompt"] + COMMON_CONTRACT,
        width=size[0],
        height=size[1],
        num_inference_steps=steps,  # 기본값 30
        true_cfg_scale=4.0,
        negative_prompt=" ",
        generator=torch.Generator(device="cpu").manual_seed(scene["seed"]),
    ).images[0]
    image.save(ASSET_DIR / f"p7-5-1-style-{scene['id']}-qwen-image-{run_label}.png")
```

이 코드 블록에서 파이프라인 분절은 모델 구조를 새로 나누는 일이 아니라, **한 번에 GPU에 상주하는 것을 줄이는 실행 분절**입니다. `from_pretrained(...)`는 Qwen Image 구성 요소를 준비하고, transformer의 Nunchaku offload와 `enable_sequential_cpu_offload()`는 실행 순서에 맞춰 GPU 상주량을 줄입니다. 이 설정은 메모리 운용일 뿐 화풍 품질을 높이는 설정이 아닙니다.

`for scene in scenes:`는 이 절의 두 번째 분절입니다. 스무 장면을 하나의 큰 batch로 묶지 않고, 한 행의 prompt와 seed로 한 장을 만들고 저장한 뒤 다음 행으로 넘어갑니다. 실패한 행만 `P7_STYLE_SCENE`으로 다시 생성할 수 있으며, 코드 원문은 행이 끝날 때 `torch.cuda.empty_cache()`로 다음 장면을 위한 캐시 반환을 요청합니다.

따라서 `pipe(...)` 호출 안의 `width`, `height`, `num_inference_steps`, `true_cfg_scale`, `seed`는 후보를 만드는 추론 조건이고, offload와 행별 반복은 그 추론을 나누는 운영 조건입니다. 기본값 `STEPS=30`은 이번 후보 생성의 기본 운용점입니다. 이 블록의 `image.save(...)`가 성공했다는 사실은 후보 PNG가 생겼다는 뜻뿐입니다. 외곽선·수채화 질감·공간의 물리성·필수 행 충족 여부는 다음의 사람 검수에서 판정합니다.

## AI 모델은 텍스트 조건과 seed에서 후보 원본을 만든다

앞의 코드 발췌는 실행에서 바꿀 값과 저장 경계를 보여 주고, 아래 도식은 그중 **후보 한 장을 만드는 실행 준비·`QwenImagePipeline` 처리·검수 경계**를 나눕니다. Qwen Image 구성 요소를 `torch_dtype=torch.bfloat16`으로 읽고 Nunchaku transformer offload 및 `enable_sequential_cpu_offload()`를 켜는 부분은 모델 내부 추론 단계가 아니라 실행 준비에 가깝습니다. 그 준비가 끝난 뒤 `QwenImagePipeline`은 장면 prompt와 공통 화풍 계약을 조건으로 바꾸고, seed에서 시작한 이미지 표현을 정해진 횟수만큼 갱신합니다. 이 단계의 목적은 다른 모델에 일반화되는 배경 화풍을 찾는 것이 아니라 **Qwen Image가 이 계약을 어느 정도 따르는지** 확인하는 것입니다. 기본 `STEPS=30`과 `true_cfg_scale=4.0`은 이번 후보 생성의 실행 설정이며, 이 숫자 자체가 화풍의 승인 기준은 아닙니다.

도식의 `입력 조건` 구역은 값을 `텍스트 입력`, `이미지 출발 조건`, `추론 설정` 세 묶음으로 정리합니다. 아래 표는 같은 값을 코드 위치와 검수 의미로 더 풀어 쓴 것입니다. 이렇게 보면 어떤 값이 텍스트 조건을 만들고 어떤 값이 latent 출발점과 반복 갱신 조건을 바꾸는지 구별할 수 있습니다.

| 입력 조건 | 코드에서 오는 곳 | 파이프라인에서 쓰이는 곳 | 검수할 때의 의미 |
| --- | --- | --- | --- |
| scene 행 | `SCENES`의 `prompt`, `seed` | `pipe(...)`에 넘길 prompt와 초기 latent | 장소·시간·카메라와 같은 행별 비교 조건 |
| 공통 화풍 계약 | 화풍 프롬프트 JSON의 `common_contract` | `pipe(...)`에 넘길 prompt | 모든 행에서 유지해야 할 선·수채화·프레임 금지 조건 |
| 해상도 | 기본 `1024×1024`, 또는 `P7_STYLE_WIDTH`, `P7_STYLE_HEIGHT` | latent 크기와 VAE 출력 | 실행별 JSON에 함께 남기는 후보 원본 형식 |
| 추론 반복 | `num_inference_steps=30` 기본값 | scheduler의 timesteps와 transformer 반복 | 생성 조건이지 품질 점수는 아님 |
| 텍스트 유도 | `true_cfg_scale=4.0`, `negative_prompt=" "` | classifier-free guidance 계산에 쓰이는 조건 | 값 자체가 승인 기준은 아님 |
| seed 생성기 | `torch.Generator(device="cpu").manual_seed(...)` | 초기 latent 출발점 | 비교 기록이며 픽셀 동일성 보장은 아님 |

```mermaid
--8<-- "assets/part-07/chapter-05/p7-5-1-ai-model-inference-pipeline-ko.mmd"
```

`QwenImagePipeline` 안에서는 먼저 입력이 prompt, generator, size, step, true CFG로 나뉩니다. tokenizer와 text encoder는 prompt를 token ID와 [text embedding](../../../reference/concept-glossary-parts/08-ieung.md#embedding) 같은 조건 표현으로 만들고, CPU seed에서 출발한 noise는 해상도에 맞는 초기 latent가 됩니다. scheduler와 [transformer](../../../reference/concept-glossary-parts/12-tieut.md#transformer)는 조건 표현과 timestep을 보며 latent를 반복 갱신하고, VAE는 이를 RGB 픽셀 이미지로 되돌립니다. offload는 이 내부 단계를 바꾸는 알고리즘이 아니라 GPU 상주량을 줄이는 메모리 운용입니다. prompt, seed, step, guidance는 **생성 조건**이고, 프레임 없음·선화 유지·시간대 광원·camera 충족은 **생성 뒤 검수 조건**입니다.

| 모델 파이프라인 단계 | 이 절에서 맡는 역할 | 승인 판단과의 관계 |
| --- | --- | --- |
| prompt와 공통 계약 | 장소·시간·카메라와 금지 조건을 한 텍스트 입력으로 묶음 | 금지 문구가 있어도 결과 보장은 아님 |
| tokenizer와 text encoder | 텍스트를 모델이 쓰는 조건 표현으로 바꿈 | 조건 해석의 시작점이지 사람 판정을 대체하지 않음 |
| seed와 latent | 같은 실행 조건의 출발점을 기록함 | 다른 환경에서 픽셀 동일성을 보장하지 않음 |
| scheduler와 transformer 반복 | timestep과 조건 표현을 보며 이미지 표현을 단계적으로 갱신함 | 반복 수와 guidance는 품질 점수가 아님 |
| VAE decode와 PNG 저장 | latent를 이미지로 바꾸고 원본 파일로 남김 | 파일 생성 성공은 후보 생성 성공일 뿐 승인 아님 |
| 사람 검수와 ledger | 외곽·선·색·장소·시간·카메라를 판정함 | 다음 단계 입력 가능 여부를 결정함 |

`COMMON_CONTRACT`와 장면별 `prompt`는 하나의 positive prompt로 이어 붙여 전달되고, 빈 문자열이 아닌 공백인 `negative_prompt=" "`를 함께 넘깁니다. 따라서 `no panel` 같은 금지 문구는 원하는 결과를 보장하는 규칙이 아니라 다른 장면 설명과 함께 해석되는 조건입니다. seed는 같은 실행 조건의 출발점을 기록하지만, 다른 GPU·라이브러리·모델 버전에서도 픽셀까지 같은 결과를 보장하지는 않습니다.

## 30스텝으로 생성한 1~15번 행을 승인한다

아트리움 한 행을 1024×1024, seed `420713`, 102단어 prompt로 비교했을 때 4·10·20·30·40·50스텝 후보를 만들었습니다. 20스텝부터 선과 색층의 기본 형태는 읽을 수 있었지만, 30스텝을 이후 후보 생성의 기본값으로 두었습니다. 30스텝 아트리움 후보의 행 생성 시간은 99.8초였고, 전체 실행의 GPU 메모리 peak은 5,467 MiB였습니다. 이 결과는 한 장면·한 해상도에서의 운용 기록이지 모든 장면의 필요 스텝이나 품질 보장은 아닙니다.

| 1번 · 실내 아트리움 · 새벽 · high angle · 1024×1024 | 2번 · courtyard · 이른 아침 · high angle · 768×1152 | 3번 · 도심 · 낮 · wide eye-level · 768×1152 |
| --- | --- | --- |
| ![30스텝 Qwen Image v3 아트리움 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-atrium-dawn-high-angle-qwen-image-qwen30-v3-scene01-code-7a21c8-seed-420713-steps-30.png) | ![30스텝 Qwen Image v3 courtyard 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-courtyard-early-morning-high-angle-qwen-image-qwen30-v3-scene02-code-6d4e55-seed-420702-steps-30.png) | ![30스텝 Qwen Image v3 도심 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-downtown-clear-day-wide-qwen-image-qwen30-v3-scene03-code-1f7147-seed-420703-steps-30.png) |

| 4번 · 주택가 · 해질녘 · low angle · 1024×1024 | 5번 · 독서실 · 밤 · oblique · 1024×1024 | 6번 · 옥상 광장 · 우천 야간 · overhead high angle · 1024×1024 |
| --- | --- | --- |
| ![30스텝 Qwen Image v3 주택가 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-residential-sunset-low-angle-qwen-image-qwen30-v3-scene04-code-a895b0-seed-420704-steps-30.png) | ![30스텝 Qwen Image v3 야간 독서실 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-night-lit-reading-room-oblique-qwen-image-qwen30-v3-scene05-code-b45954-seed-420705-steps-30.png) | ![30스텝 Qwen Image v3 우천 야간 옥상 광장 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-rooftop-rainy-night-overhead-qwen-image-qwen30-v3-scene06-code-7f2220-seed-420706-steps-30.png) |

| 7번 · 베니스 · 해질녘 · oblique · 1024×1024 | 8번 · 공원 · 낮 · eye-level · 1024×1024 | 9번 · 열차 승강장 · 우천 야간 · oblique · 1024×1024 | 10번 · gallery · 낮 · oblique · 1024×1024 |
| --- | --- | --- | --- |
| ![30스텝 Qwen Image v3 베니스 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-venice-sunset-oblique-qwen-image-qwen30-v3-scene07-code-5ac727-seed-420707-steps-30.png) | ![30스텝 Qwen Image v3 공원 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-park-clear-day-eye-level-qwen-image-qwen30-v3-scene08-code-41a06e-seed-420708-steps-30.png) | ![30스텝 Qwen Image v3 열차 승강장 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-train-platform-rainy-night-oblique-qwen-image-qwen30-v3-scene09-code-8839e3-seed-420709-steps-30.png) | ![30스텝 Qwen Image v3 gallery 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-gallery-midday-oblique-qwen-image-qwen30-v3-scene10-code-cd1676-seed-420810-steps-30.png) |

사람 검수로 1번 아트리움부터 10번 gallery까지 승인했습니다. 1·3·4·5·6번은 필수 행을, 2·7·8·9·10번은 보조 행을 맡으며, 열 원본으로 manifest의 같은 행을 교체합니다. 1번은 v3 계약을 결합한 85단어 prompt로 99.8초에 생성했고 GPU 메모리 peak은 6,000 MiB였습니다. 2·3번은 각각 72단어·70단어 prompt로 99.9초·99.0초에 생성했고, GPU 메모리 peak은 5,802 MiB·5,456 MiB였습니다. 4·5·6번은 각각 71단어·86단어·77단어 prompt로 99.6초·99.8초·100.0초에 생성했고, GPU 메모리 peak은 6,012 MiB·5,453 MiB·5,464 MiB였습니다. 7·8·9·10번은 각각 71단어·66단어·73단어·74단어 prompt로 99.4초·99.2초·100.5초·100.3초에 생성했고, GPU 메모리 peak은 5,492 MiB·5,804 MiB·5,458 MiB·5,444 MiB였습니다. 재현 비용을 늘린 40·50스텝 후보는 보관하지 않습니다.

## 다섯 필수 행과 보조 근거를 분리한다

로컬 GPU에서 후보를 만들 수 있다는 사실은 화풍 팩 승인과 다릅니다. 재생성 후보는 다섯 필수 행을 하나씩 채우고, 보조 행은 다른 장소·시간·시점에서도 계약이 유지되는지를 확인합니다. 현재는 창가 독서실이 폐기한 여객기 행을 대체해 다섯 필수 행을 채웠고, courtyard·베니스·공원·열차 승강장·세라믹 스튜디오와 열 확장 장소까지 열다섯 보조 행도 사람 승인을 받았습니다. 이 스무 행이 현재 manifest의 승인 원본입니다.

| 필수 행 | 로컬 GPU 재생성 후보 | 현재 판정 | 이 행이 확인하는 것 |
| --- | --- | --- | --- |
| 실내·새벽·high angle | Qwen Image 아트리움 30 step | 행 승인 | 새벽 광원과 실내 하향 시점 |
| 실내·밤·oblique | Qwen Image 독서실 30 step | 행 승인 | 창밖의 밤, 작은 스탠드 조명, 사선 시점 |
| 실외·낮·wide eye-level | Qwen Image 도심 30 step | 행 승인 | 낮 팔레트와 측면 교차로 시점 |
| 실외·해질녘·low angle | Qwen Image 주택가 30 step | 행 승인 | 제한된 석양빛과 curb-height 상향 시점 |
| 실외·우천 야간·overhead high angle | Qwen Image 옥상 광장 30 step | 행 승인 | 젖은 바닥 반사와 하향 야간 시점 |

이른 아침 courtyard, 베니스 운하, 공원 연못, 열차 승강장, 세라믹 스튜디오와 gallery·greenhouse·hillside alley·ferry deck·cinema foyer·market arcade·riverside terrace·underpass·harbor terrace·높은 로비 도서관은 보조 행입니다. 각각 high-angle, oblique, 낮 팔레트, 우천 야간 조명, 실내 작업 공간의 오후 광원과 장소 폭을 넓혀 보지만 다섯 필수 행을 대체하지는 않습니다. 불합격 후보는 crop이나 상태값 변경으로 살리지 않고, 로컬 검수에서 실패 이유를 확인합니다.

| 보조 행 | 로컬 GPU 재생성 후보 | 넓혀 보는 화풍 조건 |
| --- | --- | --- |
| 이른 아침 courtyard · high angle | Qwen Image courtyard 30 step · 행 승인 | 실외 자연광에서 하향 시점의 선·색면 |
| 베니스 운하 · 석양 · oblique | Qwen Image 베니스 30 step · 행 승인 | 제한된 apricot 역광과 사선 수면 |
| 공원 연못 · 낮 · eye-level | Qwen Image 공원 30 step · 행 승인 | 자연 공간의 낮 팔레트와 수면 반사 |
| 열차 승강장 · 우천 야간 · oblique | Qwen Image 승강장 30 step · 행 승인 | 인공광, 젖은 바닥, 짧은 대각 철로 |
| 세라믹 스튜디오 · 오후 · oblique | 세라믹 스튜디오 local-gpu-v1 · 행 승인 | 실내 작업 공간의 창빛과 재료 색층 |
| gallery · 낮 · oblique | Qwen Image gallery 30 step · 행 승인 | 밝은 실내 벽·바닥의 사선 평면 |
| greenhouse · blue hour · eye-level | greenhouse local-gpu-v1 · 행 승인 | 유리 구조와 식물의 푸른 시간대 색층 |
| hillside alley · 오후 · eye-level | hillside alley local-gpu-v1 · 행 승인 | 경사 골목의 식생·벽면·오후 그림자 |
| ferry deck · 아침 · oblique | ferry deck local-gpu-v1 · 행 승인 | 개방 수면과 난간의 아침 반사광 |
| cinema foyer · 밤 · oblique | cinema foyer local-gpu-v1 · 행 승인 | 어두운 실내 바닥과 작은 인공광 |
| market arcade · 흐림 · oblique | market arcade local-gpu-v1 · 행 승인 | 반복 지붕과 습한 바닥의 확산광 |
| riverside terrace · 밤 · oblique | riverside terrace local-gpu-v1 · 행 승인 | 물·포장·먼 조명의 야간 반사 |
| underpass · 우천 twilight · oblique | underpass local-gpu-v1 · 행 승인 | 콘크리트·젖은 바닥·안전등의 색층 |
| harbor terrace · 해돋이 · high oblique | harbor terrace local-gpu-v1 · 행 승인 | 수면·낮은 방파제·제한된 새벽 띠 |
| 높은 로비 도서관 · 낮 · high oblique | 높은 로비 도서관 local-gpu-v1 · 행 승인 | 수직 공간·벽면 책장·창 반사광 |

## Python 검수 gate는 사람 판정의 누락을 막는다

생성기가 PNG를 만들면, gate 코드는 로컬 검수 ledger의 다음 실행 행렬과 최종 상태를 읽어 배경 화풍 참조 셋의 사용 가능 여부를 판정합니다. 이미지를 보고 선·색·프레임을 자동 채점하는 모델은 아닙니다. 그 판단은 사람이 ledger에 먼저 기록해야 합니다. ledger는 로컬 실행 기록으로만 보관하므로, 이 공개 원고에서는 실행 명령이나 특정 `PASS` 출력을 실습 결과로 제시하지 않습니다.

| 코드 부분 | 검사하는 것 | 통과를 의미하지 않는 것 |
| --- | --- | --- |
| `REQUIRED_CAMERAS`, `REQUIRED_TIMES` | `next_run_matrix`에 다섯 camera family와 다섯 시간대, 실내·실외가 모두 계획됐는지 | 그 행의 PNG가 실제로 구도·광원 조건을 만족한다는 판정 |
| `ledger["status"]` | 사람이 전체 팩을 `approved_for_downstream_reference`로 기록했는지 | 한 행의 `approved` 또는 PNG 생성 성공 |
| `missing` | 부족한 camera·시간·장소 또는 최종 승인 상태를 모아 `BLOCKED` 이유로 출력 | 실패 원인을 고치거나 ledger 상태를 자동 변경하는 처리 |

일부 행만 승인됐으면 matrix가 완전하더라도 gate는 `BLOCKED`여야 합니다. 반대로 status만 사람이 바꾸어도 실제 행별 원본·검수 이유가 없다면 통과로 다뤄서는 안 됩니다. 이 코드는 그 근거를 만들어 주지 않고, 사람이 남긴 근거와 다음 단계 상태가 서로 어긋나는지를 확인하는 보호 장치입니다.

## 실패 원인을 다음 프롬프트의 구조로 바꾸기

실패한 후보에 `no frame`이나 `no hatching`을 더 쓰는 것만으로는 충분하지 않았습니다. 도심은 넓은 도로를 요청했을 때 중앙 소실점의 거리 복도로 수렴했습니다. 이를 고치기 위해 금지어를 늘리는 대신, 가까운 모퉁이에서 옆으로 건너다보는 **측면 교차로**로 장면 구조를 바꿨습니다. 복잡한 실내 좌석 배치는 요구가 길어질수록 공간 구조를 안정적으로 제어하지 못해 이 참조 팩의 범위에서 폐기했습니다. 대체 장면은 필요한 시간·카메라 조건을 더 단순한 구조로 검증해야 합니다.

반대로 장가계는 외곽 프레임은 사라졌지만 절벽의 반복 선이 해칭처럼 남았고, 우천 야간 플랫폼은 비·레일·지붕 선이 화면을 지배했습니다. 이 경우에는 crop이나 부분 보정으로 통과시키지 않습니다. `무엇이 틀렸는가`를 다음 생성의 구도·피사체 밀도·광원 조건으로 번역하고, 새 원본을 다시 검수합니다.

## 사람 판정은 ledger와 manifest로 분리한다

사람이 판단하는 것은 이미지의 미적 품질 점수 하나가 아닙니다. 각 원본에서 외곽·선·색·장소·시간·카메라와 **로컬 GPU 생성 기록**을 확인하고, 행별 승인·불합격 이유와 최종 결론을 로컬 검수 ledger에 적습니다. 다음 단계가 실제로 읽는 입력 목록은 [manifest](../../../assets/part-07/chapter-05/p7-5-1-approved-style-reference-pack.json)에 따로 둡니다. 이 분리 덕분에 `왜 승인했는가`와 `무엇을 다음 생성에 넣을 수 있는가`가 섞이지 않습니다.

현재 참조 셋은 `approved_for_downstream_reference`입니다. manifest에는 스무 개의 사람 승인 로컬 GPU 원본이 있으며, 이 중 1~15번 행은 Qwen Image 30스텝 원본으로 교체했습니다. 이 원본들은 배경 화풍 계약의 검수 근거입니다. 내장 이미지 생성 원본은 사람 검수를 통과했더라도 P7-5.1의 입력·승인·manifest에서 제외합니다.

## 승인된 로컬 GPU 원본을 확인한다

Qwen Image 아트리움·courtyard·도심·주택가·독서실·옥상 광장·베니스·공원·열차 승강장·gallery 30스텝 원본과 세라믹 스튜디오·greenhouse·hillside alley·ferry deck·cinema foyer·market arcade·riverside terrace·underpass·harbor terrace·높은 로비 도서관 local-gpu-v1은 사람 승인 원본입니다. 아래 스무 원본은 manifest에 기록돼 있습니다.

| 필수 행 1 · 실내 아트리움 · 새벽 · high angle · Qwen Image 30 step | 보조 행 1 · courtyard · 이른 아침 · high angle · Qwen Image 30 step | 필수 행 2 · 창가 독서실 · 밤 · oblique · Qwen Image 30 step | 필수 행 3 · 도심 · 낮 · wide eye-level · Qwen Image 30 step |
| --- | --- | --- | --- |
| ![새벽의 실내 아트리움을 위에서 내려다본 Qwen Image v3 30스텝 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-atrium-dawn-high-angle-qwen-image-qwen30-v3-scene01-code-7a21c8-seed-420713-steps-30.png) | ![이른 아침 courtyard를 위에서 내려다본 Qwen Image v3 30스텝 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-courtyard-early-morning-high-angle-qwen-image-qwen30-v3-scene02-code-6d4e55-seed-420702-steps-30.png) | ![창밖의 밤과 작은 스탠드 조명이 있는 Qwen Image v3 30스텝 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-night-lit-reading-room-oblique-qwen-image-qwen30-v3-scene05-code-b45954-seed-420705-steps-30.png) | ![맑은 낮 도심 교차로의 Qwen Image v3 30스텝 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-downtown-clear-day-wide-qwen-image-qwen30-v3-scene03-code-1f7147-seed-420703-steps-30.png) |

| 필수 행 4 · 주택가 · 해질녘 · low angle · Qwen Image 30 step | 필수 행 5 · 옥상 광장 · 우천 야간 · overhead high angle · Qwen Image 30 step | 보조 행 2 · 베니스 운하 · 해질녘 · oblique · local GPU v1 | 보조 행 3 · 공원 연못 · 낮 · eye-level · local GPU v1 |
| --- | --- | --- | --- |
| ![해질녘 주택가를 낮은 시점에서 올려다본 Qwen Image v3 30스텝 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-residential-sunset-low-angle-qwen-image-qwen30-v3-scene04-code-a895b0-seed-420704-steps-30.png) | ![우천 야간의 옥상 광장을 위에서 내려다본 Qwen Image v3 30스텝 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-rooftop-rainy-night-overhead-qwen-image-qwen30-v3-scene06-code-7f2220-seed-420706-steps-30.png) | ![해질녘 베니스 운하를 사선으로 본 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-venice-sunset-oblique-local-gpu-v1.png) | ![맑은 낮 공원 연못의 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-park-clear-day-eye-level-local-gpu-v1.png) |

| 보조 행 4 · 열차 승강장 · 우천 야간 · oblique · local GPU v1 | 보조 행 5 · 세라믹 스튜디오 · 오후 · oblique · local GPU v1 | 보조 행 6 · gallery · 낮 · oblique · local GPU v1 | 보조 행 7 · greenhouse · blue hour · eye-level · local GPU v1 |
| --- | --- | --- | --- |
| ![우천 야간 열차 승강장의 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-train-platform-rainy-night-oblique-local-gpu-v1.png) | ![오후 창빛이 들어오는 세라믹 스튜디오의 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-ceramics-studio-afternoon-local-gpu-v1.png) | ![맑은 낮 gallery의 사선 실내 평면을 담은 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-gallery-midday-oblique-local-gpu-v1.png) | ![blue hour greenhouse의 유리와 식물 색층을 담은 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-greenhouse-blue-hour-local-gpu-v1.png) |

| 보조 행 8 · hillside alley · 오후 · eye-level · local GPU v1 | 보조 행 9 · ferry deck · 아침 · oblique · local GPU v1 | 보조 행 10 · cinema foyer · 밤 · oblique · local GPU v1 | 보조 행 11 · market arcade · 흐림 · oblique · local GPU v1 |
| --- | --- | --- | --- |
| ![오후 hillside alley의 경사와 식생을 담은 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-hillside-alley-late-afternoon-local-gpu-v1.png) | ![아침 ferry deck의 개방 수면을 담은 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-ferry-deck-morning-local-gpu-v1.png) | ![밤 cinema foyer의 바닥 반사를 담은 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-cinema-foyer-night-local-gpu-v1.png) | ![흐린 market arcade의 반복 지붕을 담은 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-market-arcade-overcast-local-gpu-v1.png) |

| 보조 행 12 · riverside terrace · 밤 · oblique · local GPU v1 | 보조 행 13 · underpass · 우천 twilight · oblique · local GPU v1 | 보조 행 14 · harbor terrace · 해돋이 · high oblique · local GPU v1 | 보조 행 15 · 높은 로비 도서관 · 낮 · high oblique · local GPU v1 |
| --- | --- | --- | --- |
| ![밤 riverside terrace의 물과 조명 반사를 담은 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-riverside-terrace-night-local-gpu-v1.png) | ![우천 twilight underpass의 젖은 바닥을 담은 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-underpass-rainy-twilight-local-gpu-v1.png) | ![해돋이 harbor terrace의 수면과 방파제를 담은 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-harbor-plaza-sunrise-high-local-gpu-v1.png) | ![높은 로비 도서관의 벽면 책장과 창 반사광을 담은 local GPU 화풍 원본](/AiBook/assets/part-07/chapter-05/p7-5-1-style-library-tall-lobby-local-gpu-v1.png) |

스무 장면은 모두 사람 승인을 받았습니다. 이름과 역할은 [manifest](../../../assets/part-07/chapter-05/p7-5-1-approved-style-reference-pack.json)에 남기고, 실행 이력은 커밋하지 않는 로컬 검수 기록으로 분리합니다.

## 실험에서 확인한 기능과 변경 결정

아래 결정은 한 번의 출력이 보기 좋았는지가 아니라, 같은 로컬 GPU 조건에서 다음 단계가 비교 가능한 입력을 받는지를 기준으로 정했습니다. 표의 결과는 이 승인 팩에서 확인한 범위이며, 다른 모델·해상도·prompt에 그대로 일반화하지 않습니다.

| 확인한 기능 또는 변경 | 결정 이유 | 이 실험에서 확인한 결과 | 이 결과가 뜻하지 않는 것 |
| --- | --- | --- | --- |
| Nunchaku·순차 CPU offload와 행별 생성 | GPU 상주량을 줄이고 실패 행만 다시 실행하려고 함 | offload와 행별 저장으로 스무 로컬 GPU 후보 행을 같은 계약으로 실행할 수 있음 | offload가 선화·구도 품질을 높이거나 모든 환경에서 같은 속도를 보장한다는 뜻은 아님 |
| Qwen Image 30스텝 기본값 | 1024×1024 아트리움 비교에서 20스텝부터 기본 형태가 읽혔지만 이후 후보의 일관된 운용점을 남기려고 함 | 1번 아트리움, 2번 courtyard, 3번 도심의 30스텝 원본을 사람 승인하고 prompt 단어 수·시간·메모리 기록을 보관함 | 30스텝이 모든 장면의 필요량을 뜻하는 것은 아님 |
| 공통 화풍 계약과 장면 행의 분리 | 선·수채화·프레임 조건을 바꾸지 않은 채 장소·시간·camera 차이만 비교하려고 함 | 같은 계약 아래 실내·실외, 새벽·낮·석양·밤·우천 야간, 다섯 camera family를 승인 팩에서 대조함 | 공통 prompt 하나가 모든 장면의 공간 구조를 자동으로 고정한다는 뜻은 아님 |
| 중앙 도로 대신 측면 교차로로 도심 조건 변경 | 넓은 도로 요구가 중앙 소실점의 거리 복도로 수렴한 실패를 장면 구조 문제로 판단함 | 측면 모퉁이에서 비스듬히 보는 도심 원본으로 교체해 낮·wide 행을 승인함 | 금지어를 더 많이 쓰면 모든 원근 오류를 고칠 수 있다는 뜻은 아님 |
| 여객기 실내를 창가 독서실로 대체 | 좌석 모듈·천장·사선 구도를 동시에 안정적으로 만족한 원본을 확보하지 못함 | 밤·실내·oblique 조건은 단순한 독서실과 작은 스탠드 조명으로 검수함 | 복잡한 실내 장면이 모델에서 불가능하다는 일반 결론은 아님 |
| ledger와 Python gate의 분리 | 미적 판단을 자동화하지 않으면서 필수 camera·시간·장소·최종 상태의 누락을 막으려 함 | 승인 당시의 로컬 ledger에서 필수 행과 최종 상태를 대조했고, 저장소에는 승인 manifest만 남김 | gate가 이미지의 선·색·공간 품질을 자동 채점하거나 사람 승인을 대신한다는 뜻은 아님 |

## 체크리스트

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| 원본 | crop 없이 프레임 없는 생성 원본인가? |
| 선과 색 | 선화가 살아 있고 수채화 색층이 선을 덮지 않는가? |
| 시간 | 새벽·낮·해질녘·밤·우천 야간이 실제 광원 차이로 읽히는가? |
| 카메라 | 같은 중앙 소실점 반복이 아니라 camera family가 다른가? |
| 실패 해석 | 실패 원인을 crop이나 `status` 변경으로 덮지 않고 다음 구도·피사체 밀도·광원 조건으로 바꿨는가? |
| 생성 출처 | 참조 원본이 로컬 GPU 생성 스크립트와 사람 검수 ledger에 연결되고, 내장 이미지 생성 자산이 섞이지 않았는가? |
| 최종 승인 기록 | 스무 원본의 사람 승인을 ledger와 manifest에 남겼는가? |

## 출처와 참고 자료

- Qwen, [Qwen-Image model card](https://huggingface.co/Qwen/Qwen-Image){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-18.
- Hugging Face, [Diffusers QwenImage pipeline](https://huggingface.co/docs/diffusers/api/pipelines/qwenimage){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-18.
- Hugging Face, [Diffusers Reduce memory usage](https://huggingface.co/docs/diffusers/optimization/memory){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-04.
