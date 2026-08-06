# P7-5.3 콘티 생성: 구조 조건으로 컷 만들기

> Section ID: `P7-5.3`
> Version: `v2026.08.06`

`P7-5.1`의 화풍 기준 이미지와 `P7-5.2`의 캐릭터 기준이 준비된 뒤, 이 절에서는 컷의 공간 구조를 먼저 고정하는 **콘티**를 만듭니다. 산출물은 최종 작화가 아니라, 인물·소품·배경이 화면 어디에 놓이고 무엇이 앞뒤에 오는지를 검수할 컷 후보입니다.

ControlNet은 depth, edge, pose 같은 추가 이미지를 생성 조건으로 넣어 공간 구조를 제어한다. 그러나 8 GB VRAM에서는 복수 ControlNet을 기본값으로 두지 않는다. 이 저장소의 SDXL 다중 조건 사전 실험도 OOM과 device mismatch로 중단됐다. 따라서 P7-5.3의 기본 실험은 **SD 1.5, 512 계열, batch 1, 구조 조건 하나**다. CPU offload는 메모리를 낮출 수 있지만 느려질 수 있으므로, 실행 성공과 제작 경로 채택을 분리해 기록한다.

## 컷마다 하나의 구조 조건을 고른다

| 고정 | 값 | 이유 |
| --- | --- | --- |
| base | SD 1.5 계열 + ControlNet 하나 | 8 GB에서 원인 분리가 가능한 최소 경로 |
| 이미지 조건 | 512 x 768 이하, batch 1 | 해상도·batch 때문에 구조 조건 효과를 오해하지 않기 위해 |
| lineart | 인물·소품·문·창의 위치와 윤곽 | 사람의 러프 스케치 또는 단순 blockout에서 만든다 |
| depth | 전경·중경·후경, 가림, 큰 공간 면 | 넓은 실내·거리·옥상 컷에 쓴다 |
| canny | 난간·계단·창문처럼 직선적인 배치 | 깨끗한 기하 blockout에만 쓴다 |
| 관찰 | peak VRAM, 시간, 구조 조건 on/off, PNG | 실행 성공과 구조 통과를 분리하기 위해 |

수채화 배경 원본에서 Canny를 바로 뽑으면 안료 얼룩까지 고정될 수 있다. 따라서 Canny와 lineart의 입력은 최종 그림이 아니라, 사람이 읽고 고친 단순한 콘티·3D blockout·벡터 윤곽으로 만든다. depth도 완성 컷에서 추정하지 말고 같은 blockout에서 만든 깊이 지도를 우선한다.

## 최소 비교 실험을 설계한다

같은 prompt·seed에서 ControlNet만 끈 결과와 하나의 구조 조건을 켠 결과를 비교한다. 처음부터 `depth + lineart + canny`를 함께 넣으면 무엇이 구조를 바꿨는지 알 수 없다.

```python
experiments = [
    ("lineart", "인물과 티켓이 보이는 실내 카페"),
    ("depth", "난간 앞 인물과 먼 건물이 있는 옥상"),
    ("canny", "창문·계단·난간이 있는 아트리움"),
]

for control, intent in experiments:
    print(f"{control}: {intent}; same prompt and seed, ControlNet off/on")
```

각 행은 `guide 파일`, 조건 종류와 scale, seed, 모델 revision, 해상도, peak VRAM, 시간, off/on PNG를 남긴다. 사람은 인물의 표정·나이·동일성보다 먼저 **콘티가 요구한 위치·가림·윤곽을 지켰는지** 판정한다. StoryDiffusion은 이 기본 비교가 통과한 뒤, 인물 반복성을 별도로 살피는 보조 후보로만 둔다.

## 중단 기준

8 GB에서 OOM이 나면 해상도·batch·조건 수를 동시에 낮추지 않는다. 먼저 batch 1과 구조 조건 하나를 유지하고, 해상도만 낮춘 별도 행으로 기록한다. 단일 조건에서도 구조가 지켜지지 않으면 복수 조건·IP-Adapter·inpaint로 덮지 않고 해당 컷의 guide를 다시 만든다.

## 체크리스트

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| guide | 사람 수정이 가능한 lineart·depth·canny blockout인가? |
| 분리 | 한 행에서 구조 조건 하나만 켰는가? |
| 기록 | off/on의 seed, guide, 시간, VRAM peak, PNG를 모두 남겼는가? |
| 판정 | 컷의 위치·가림·윤곽이 의도대로 유지됐는가? |

## 출처와 참고 자료

- Zhou et al., [StoryDiffusion official implementation](https://github.com/HVision-NKU/StoryDiffusion){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-02.
- Zhang, Rao, Agrawala, [Adding Conditional Control to Text-to-Image Diffusion Models](https://openaccess.thecvf.com/content/ICCV2023/papers/Zhang_Adding_Conditional_Control_to_Text-to-Image_Diffusion_Models_ICCV_2023_paper){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-06.
- Hugging Face, [Diffusers ControlNet](https://huggingface.co/docs/diffusers/api/pipelines/controlnet){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-06.
- Hugging Face, [Reduce memory usage](https://huggingface.co/docs/diffusers/optimization/memory){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-06.
