# P7-5.9 보충학습: Mira의 표정 바꾸기

> Section ID: `P7-5.9`
> Version: `v2026.09.12`

웃을 때는 입꼬리만 올라가는 것이 아니라 볼과 눈의 모양도 달라진다. 놀랄 때는 눈썹·눈·입이 함께 움직인다. [P7-5.2](section-02.md)에서 만든 Mira 정면 머리를 Qwen-Image-Edit-2511에 넣고, 표정을 바꾸면서 같은 얼굴과 머리 모양이 남는지 비교한다.

## 표정과 강도 나누기

![Mira 정면 머리 입력](../../../assets/part-07/chapter-05/p7-5-2-mira-head-qwen-image-bf16-front-v1-code-63ece7-seed-62294-steps-30-size-1280.png)

여섯 계열의 24개 표정에 삐짐·의심·안도 등 12개와 볼 부푼 삐짐 수정 결과·윙크·하품을 더해 39개 조건을 비교한다. 경멸은 입술의 비대칭을 조정한 결과를, 반감·혐오·극심한 혐오는 코 표현을 수정한 결과를 사용한다. 각 조건은 모두 위 이미지를 입력으로 사용한다. 웃는 결과를 다시 화난 표정으로 바꾸는 식으로 이어 붙이지 않는다. 같은 원본·시드·크기·스텝을 유지하고 표정 지시만 바꿔야, 앞선 편집의 변화가 다음 결과에 누적되는 일을 피할 수 있다.

| 계열 | 1단계 | 2단계 | 3단계 | 4단계 |
| --- | --- | --- | --- | --- |
| 분노 | 엄격함 | 분개 | 분노 | 격노 |
| 혐오 | 경멸 | 반감 | 혐오 | 극심한 혐오 |
| 공포 | 걱정 | 불안 | 두려움 | 극도의 공포 |
| 기쁨 | 만족 | 즐거움 | 기쁨 | 큰 웃음 |
| 슬픔 | 낙담 | 우울한 표정 | 슬픔 | 비통함 |
| 놀람 | 주의 집중 | 경이로움 | 놀람 | 충격 |

이 표는 실험에서 비교할 표정 이름과 순서다. 네 단계는 FACS의 강도 점수가 아니며, 모든 사람이 이 순서대로 감정을 느끼거나 표정을 짓는다는 뜻도 아니다. 특히 경멸과 혐오는 구분되는 표현이므로, 이웃한 칸을 같은 움직임의 단순한 확대라고 가정하지 않는다.

공통 지시는 얼굴 비례·홍채색·머리색·헤어스타일과 정면 방향·구도·어깨·배경·조명·화풍을 유지하도록 한다. 눈썹과 입이 움직이는 것은 표정 변화이고, 가르마나 코의 형태까지 바뀌는 것은 별도로 확인할 외형 변화다.

## AU를 움직임 문장으로 풀기

FACS의 Action Unit(AU)은 눈썹 올리기나 입꼬리 당기기처럼 눈에 보이는 얼굴 움직임을 구분하는 코드다. AU 하나가 감정 하나를 확정하지는 않는다. 이 실험에서는 AU를 표정 지시를 작성하는 참고로 사용하고, Qwen에 전달하는 프롬프트는 영어 움직임 문장으로 작성한다.

| 표정 설계 예 | 참고 AU | 실제로 지시하는 움직임 |
| --- | --- | --- |
| 즐거움 | AU6·AU12 | 볼과 입꼬리를 올려 다문 입으로 웃기 |
| 놀람 | AU1·AU2·AU5·AU26 | 눈썹과 위 눈꺼풀을 올리고 턱을 내려 입 벌리기 |
| 슬픔 | AU1·AU4·AU15·AU17 | 눈썹 안쪽을 올려 모으고 입꼬리를 내리며 턱 피부 올리기 |
| 혐오 | AU9·AU10·AU7 | 코를 찡그리고 윗입술을 올리며 눈꺼풀 조이기 |

위 조합은 이 실험의 표현 설계이며 감정의 표준 정답표가 아니다. 예를 들어 AU6은 볼 올리기 자체를 가리키므로 AU12와 반드시 함께 나타나야 하는 것은 아니다. 생성 JSON의 `au_hints`도 사람이 설정한 의도이며 출력에서 측정한 AU가 아니다. Qwen이 AU 번호를 전용 제어 입력으로 해석한다는 보장도 두지 않는다.

머리 방향은 정면으로 요청하고 시선이 옆으로 흐르는지도 검수한다. 씹기·깜박임 같은 시간에 따른 동작은 이번 정지 이미지 비교에 넣지 않는다. AU를 자동 검출하려면 도구가 지원하는 범위를 별도로 확인해야 한다. OpenFace도 일부 AU만 지원하며, 이번 실험에는 AU 검출기를 적용하지 않는다.

[통합 표정 설계·AU 참고 JSON](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-spec.json){ .lazy-source }

## 표정 생성 명령

엄격함·혐오·두려움·기쁨·슬픔·놀람 여섯 조건으로 눈썹·눈·입의 변화와 외형 보존을 검수한 뒤, 같은 설정으로 나머지 18개를 생성했다. 여섯 표본은 같은 강도로 맞춘 비교가 아니라 각 계열의 표현을 살피기 위한 선택이었다.

생성기는 `QwenImageEditPlusPipeline`으로 공식 BF16 모델을 한 번 읽고 선택한 표정을 순서대로 생성한다. 추가 LoRA는 적용하지 않는다. 기본값은 1024×1024, 20스텝, seed `62294`, true CFG `4.0`이며, 원본 1280×1280 이미지를 정사각형 비율 그대로 줄여 입력한다. 모델은 저장소의 `.tmp/download/huggingface/hub` 캐시에서 읽는다.

[Mira 표정 생성 Python](../../../assets/part-07/chapter-05/p7_5_9_qwen_edit_2511_mira_expressions.py){ .lazy-source }

[공통 경로·해시·환경 기록 Python](../../../assets/part-07/chapter-05/p7_5_2_qwen_edit_2511_generate_mira_torso.py){ .lazy-source }

저장소 루트에서 입력·프롬프트·출력 경로를 확인한다.

```bash
.venv/bin/python docs/assets/part-07/chapter-05/p7_5_9_qwen_edit_2511_mira_expressions.py \
  --dry-run
```

대표 여섯 표정을 생성할 때는 다음과 같이 실행한다. 기존 파일을 덮어쓰지 않으므로 재실행에는 새로운 실행 이름을 사용한다. `--expressions`를 생략하면 통합 JSON의 현재 39개 표정을 모두 생성한다.

```bash
.venv/bin/python docs/assets/part-07/chapter-05/p7_5_9_qwen_edit_2511_mira_expressions.py \
  --expressions sternness disgust fear joy sadness surprise \
  --run-label front-repeat-v1
```

즐거움과 큰 웃음만 비교하려면 표정 이름을 선택한다. 두 조건은 입을 다무는지, 치아를 드러내는지와 함께 눈·볼이 어떻게 달라지는지 비교하기 좋다.

```bash
.venv/bin/python docs/assets/part-07/chapter-05/p7_5_9_qwen_edit_2511_mira_expressions.py \
  --expressions amusement laughter --run-label smile-laugh-v1
```

`--input`은 기준 이미지, `--expressions`는 표정, `--seed`는 초기 잡음, `--steps`와 `--cfg`는 생성 조건을 바꾼다. 먼저 같은 입력과 설정으로 표정을 비교하고, 특정 표정이 충분히 나타나지 않을 때 그 조건만 다시 생성한다. 각 PNG와 짝을 이루는 JSON에는 입력·출력 해시, 실제 프롬프트, 설정, 실행 시간과 GPU 메모리 기록을 남긴다.

통합 JSON에는 표정마다 기준 프롬프트 하나만 둔다. 프롬프트를 수정할 때는 해당 항목을 교체하며 폐기한 문구나 버전별 설계를 쌓지 않는다. `--run-label`은 출력 파일을 구분하는 실행 이름이다.

```bash
.venv/bin/python docs/assets/part-07/chapter-05/p7_5_9_qwen_edit_2511_mira_expressions.py \
  --expressions pouting sulking \
  --run-label pouting-repeat
```

현재 경멸·하품·윙크는 제공된 표정 샘플을 참고한 기준 문구를 사용한다. 기존 결과 JSON에는 당시 사용한 프롬프트가 기록돼 있으므로, 현재 기준으로 재실행한 결과와 구분한다.

## 여섯 계열의 24개 표정

분노·공포·기쁨·슬픔·놀람은 첫 생성 결과이며, 경멸은 입 모양을 조정한 결과이고, 반감·혐오·극심한 혐오는 코 붉어짐을 줄이려고 표현을 수정한 결과다. 각 표는 설계한 1~4단계 순서다. 단계 차이는 출력에서 실제로 보이는 움직임으로 비교한다. 아래 관찰은 시각적 검수이며 AU 검출 점수나 얼굴 동일성 측정값이 아니다.

### 분노

| 엄격함 | 분개 | 분노 | 격노 |
| --- | --- | --- | --- |
| ![Mira 엄격함](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-sternness-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 분개](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-indignation-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 분노](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-anger-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 격노](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-rage-intensity-v1-size-1024-seed-62294-steps-20.png) |

엄격함과 분개는 미간 수축의 차이가 작다. 분노에서는 입술이 벌어져 맞물린 치아가 보이고, 격노에서는 입이 크게 열린다. 뒤의 두 조건은 구분되지만 네 칸이 균등한 강도 간격을 이루지는 않는다. 격노에서는 아래턱 윤곽과 목 그림자도 달라졌다.

[엄격함 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-sternness-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[분개 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-indignation-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[분노 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-anger-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[격노 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-rage-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

### 경멸·혐오

| 경멸 | 반감 | 혐오 | 극심한 혐오 |
| --- | --- | --- | --- |
| ![Mira 경멸](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-disdain-lower-lip-relaxed-size-1024-seed-62294-steps-20.png) | ![Mira 반감](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-aversion-expansion-v1-size-1024-seed-62294-steps-20.png) | ![Mira 혐오](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-disgust-nose-wording-v1-size-1024-seed-62294-steps-20.png) | ![Mira 극심한 혐오](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-revulsion-expansion-v1-size-1024-seed-62294-steps-20.png) |

[경멸 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-disdain-lower-lip-relaxed-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

경멸은 눈을 좁히고 미간을 모으며 윗입술 한쪽을 조금 더 들어 치아가 살짝 보이도록 했다. 입 전체를 비튼다는 표현을 빼고 아랫입술을 중앙에 유지하도록 바꾸자, 한쪽으로 쏠리는 움직임은 줄고 윗입술의 비대칭은 남았다. 다만 아랫입술이 두툼하게 돌출된 느낌은 일부 남아 있다.

[반감 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-aversion-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[혐오 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-disgust-nose-wording-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[극심한 혐오 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-revulsion-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

코 찡그림을 콧등 주변 근육의 당김과 주름 위치로 풀어 쓰자 반감·혐오의 코 붉어짐이 줄었다. 극심한 혐오에는 붉은 색조가 일부 남았다. 반감에서는 코끝 수축과 윗입술 올림도 약해져 걱정과 비슷해 보인다. 색 변화가 줄었다는 사실과 원하는 표정이 유지됐다는 판단은 구분해야 한다.

### 공포

| 걱정 | 불안 | 두려움 | 극도의 공포 |
| --- | --- | --- | --- |
| ![Mira 걱정](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-concern-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 불안](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-anxiety-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 두려움](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-fear-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 극도의 공포](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-terror-intensity-v1-size-1024-seed-62294-steps-20.png) |

걱정은 눈썹 안쪽이 조금 올라가고 입이 다물려 있다. 불안에서는 입이 가로로 조금 벌어지고, 두려움에서는 눈과 입이 더 열린다. 극도의 공포는 입 벌림뿐 아니라 눈 주변 선·코 옆 주름·목 힘줄과 그림자까지 강해져 기준 얼굴의 인상이 달라졌다.

[걱정 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-concern-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[불안 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-anxiety-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[두려움 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-fear-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[극도의 공포 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-terror-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

### 기쁨

| 만족 | 즐거움 | 기쁨 | 큰 웃음 |
| --- | --- | --- | --- |
| ![Mira 만족](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-satisfaction-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 즐거움](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-amusement-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 기쁨](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-joy-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 큰 웃음](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-laughter-intensity-v1-size-1024-seed-62294-steps-20.png) |

만족과 즐거움은 입을 다문 미소다. 즐거움에서 볼의 접힌 선과 눈의 좁아짐이 더 나타난다. 기쁨은 치아가 드러나고, 큰 웃음은 입이 더 벌어지며 눈이 거의 감긴다. 네 조건은 입 벌림과 눈·볼의 변화로 구분된다.

[만족 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-satisfaction-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[즐거움 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-amusement-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[기쁨 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-joy-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[큰 웃음 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-laughter-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

### 슬픔

| 낙담 | 우울한 표정 | 슬픔 | 비통함 |
| --- | --- | --- | --- |
| ![Mira 낙담](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-dejection-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 우울한 표정](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-melancholy-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 슬픔](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-sadness-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 비통함](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-grief-intensity-v1-size-1024-seed-62294-steps-20.png) |

낙담과 우울한 표정은 눈썹·입꼬리가 비슷하고, 우울한 표정의 눈꺼풀이 더 내려온다. 슬픔에서는 미간 주름과 눈가 광택이 커진다. 비통함에서는 입이 크게 열리지만 붉은 코와 강한 주름, 눈물처럼 보이는 가는 자국도 추가됐다. 약한 두 조건의 차이와 강한 조건의 외형 변화를 따로 살펴야 한다.

[낙담 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-dejection-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[우울한 표정 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-melancholy-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[슬픔 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-sadness-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[비통함 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-grief-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

### 놀람

| 주의 집중 | 경이로움 | 놀람 | 충격 |
| --- | --- | --- | --- |
| ![Mira 주의 집중](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-alertness-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 경이로움](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-wonder-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 놀람](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-surprise-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 충격](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-shock-intensity-v1-size-1024-seed-62294-steps-20.png) |

주의 집중은 입이 거의 다물려 있고, 경이로움은 입술이 조금 벌어진다. 놀람은 입이 둥글게 열리고, 충격은 입이 더 크게 열린다. 다만 충격에서는 눈썹 안쪽이 모이고 미간 주름이 강해져 공포 계열과 닮은 요소도 나타난다.

[주의 집중 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-alertness-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[경이로움 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-wonder-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[놀람 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-surprise-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[충격 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-shock-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

## 삐짐·의심·안도 등 12개 표정

추가 표정은 강도 순서가 아니라 서로 다른 움직임을 비교하는 조건이다. 삐짐은 아래입술 내밀기, 토라짐은 입술 누르기로 설계했다. 감정 이름은 작업용 라벨로 남기고 모델에는 움직임 문장을 전달했다. 코와 볼의 기존 피부색 유지도 요청했으며, AU 조합은 지정하지 않았다. 얼굴만으로 실제 감정을 판정하는 분류표는 아니다.

### 삐짐·토라짐·서운함·억울함

| 삐짐 | 토라짐 | 서운함 | 억울함 |
| --- | --- | --- | --- |
| ![Mira 삐짐](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-pouting-expansion-v1-size-1024-seed-62294-steps-20.png) | ![Mira 토라짐](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-sulking-expansion-v1-size-1024-seed-62294-steps-20.png) | ![Mira 서운함](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-hurt_feelings-expansion-v1-size-1024-seed-62294-steps-20.png) | ![Mira 억울함](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-aggrieved-expansion-v1-size-1024-seed-62294-steps-20.png) |

[삐짐 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-pouting-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[토라짐 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-sulking-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[서운함 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-hurt_feelings-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[억울함 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-aggrieved-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

삐짐은 아래입술 돌출이 약하고 눈썹 안쪽이 올라가 슬픔에 가까워졌다. 토라짐은 입술 누름이 약해 중립과 비슷하다. 서운함은 입꼬리가 충분히 내려가지 않아 작은 미소처럼 보이고, 억울함은 미간 수축이 강해 분노에 가까워졌다. 네 이름을 그대로 학습 라벨로 채택하기보다 실제 움직임과 맞는지 다시 확인해야 한다.

### 수줍음·머쓱함·민망함·난처함

| 수줍은 미소 | 머쓱한 미소 | 민망함 | 난처함 |
| --- | --- | --- | --- |
| ![Mira 수줍은 미소](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-shy_smile-expansion-v1-size-1024-seed-62294-steps-20.png) | ![Mira 머쓱한 미소](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-sheepish_smile-expansion-v1-size-1024-seed-62294-steps-20.png) | ![Mira 민망함](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-embarrassed-expansion-v1-size-1024-seed-62294-steps-20.png) | ![Mira 난처함](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-perplexed-expansion-v1-size-1024-seed-62294-steps-20.png) |

[수줍은 미소 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-shy_smile-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[머쓱한 미소 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-sheepish_smile-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[민망함 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-embarrassed-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[난처함 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-perplexed-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

수줍은 미소는 다문 입과 내려온 눈꺼풀이 함께 나타나지만 기존 만족·즐거움과 겹칠 수 있다. 머쓱한 미소는 미간의 긴장과 미소가 함께 보여 수줍은 미소와 구분된다. 민망함에서는 입술을 안으로 마는 움직임이 약했고, 난처함에서는 미간과 입 주변 수축이 강해 불만·분노처럼 보였다.

### 의심·못마땅함·장난기·안도

| 의심 | 못마땅함 | 장난기 | 안도 |
| --- | --- | --- | --- |
| ![Mira 의심](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-skeptical-expansion-v1-size-1024-seed-62294-steps-20.png) | ![Mira 못마땅함](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-unimpressed-expansion-v1-size-1024-seed-62294-steps-20.png) | ![Mira 장난기](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-mischievous-expansion-v1-size-1024-seed-62294-steps-20.png) | ![Mira 안도](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-relieved-expansion-v1-size-1024-seed-62294-steps-20.png) |

[의심 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-skeptical-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[못마땅함 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-unimpressed-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[장난기 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-mischievous-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[안도 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-relieved-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

의심은 눈썹 비대칭이 나타나지만 차이가 작다. 못마땅함은 내려온 눈꺼풀과 수평으로 다문 입이 보이나 토라짐과 비슷하다. 장난기는 요청한 한쪽 입꼬리 올림이 약해 일반 미소에 가깝다. 안도는 부드럽게 감긴 눈과 작은 미소가 함께 나타나, 볼을 강하게 올리는 큰 웃음과 구분된다.

## 볼 부푼 삐짐

볼 부푼 삐짐은 입술을 내미는 동작과 볼의 부피 변화를 함께 요청했다. 첫 결과는 양 볼이 과하게 부풀어 얼굴 폭과 턱선이 달라져 폐기했다. 수정 설계에서는 입술을 살짝 앞으로 내밀고, 볼의 변화는 입 바로 옆 아래쪽에만 약하게 나타나도록 했다. 전체 얼굴 폭·턱선·턱끝은 거의 유지하도록 요청했다.

| 볼 부푼 삐짐 · v2 |
| --- |
| ![Mira 볼 부푼 삐짐 수정 결과](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-puffed_pout-puffed-pout-v2-size-1024-seed-62294-steps-20.png) |

[볼 부푼 삐짐 수정 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-puffed_pout-puffed-pout-v2-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

수정 결과에서는 과도한 볼 팽창이 줄고, 다문 입과 내려간 입꼬리가 보인다. 다만 입술의 전방 돌출과 볼 부풀림도 약해 일반적인 삐짐에 가까워졌다. 얼굴 윤곽의 과장을 줄이는 것과 원하는 볼 움직임을 남기는 것은 별도로 확인해야 한다.

같은 설계를 재실행하려면 `--expressions puffed_pout`을 지정한다. 기존 결과를 덮어쓰지 않도록 새 실행 이름을 사용한다.

```bash
.venv/bin/python docs/assets/part-07/chapter-05/p7_5_9_qwen_edit_2511_mira_expressions.py \
  --expressions puffed_pout \
  --run-label puffed-pout-v2-repeat
```

## 윙크

한쪽 눈을 감고 같은 쪽 윗볼을 살짝 올리며 작게 미소 짓도록 지시했다. 결과에서는 화면 왼쪽 눈이 닫히고 오른쪽 눈이 열린 모습이 나타났다. 요청한 화면 오른쪽과 감긴 눈의 방향이 반대이므로, 방향 제어와 윙크 표현은 구분해서 본다.

| 윙크 |
| --- |
| ![Mira 윙크](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-wink-reference-size-1024-seed-62294-steps-20.png) |

[윙크 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-wink-reference-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

다문 입의 미소와 한쪽 눈 감김이 함께 보인다. 볼 올림은 약하고 감긴 눈의 선이 강조돼 있다. 머리색·가르마·정면 구도는 대체로 유지됐다.

```bash
.venv/bin/python docs/assets/part-07/chapter-05/p7_5_9_qwen_edit_2511_mira_expressions.py \
  --expressions wink --run-label wink-repeat
```

## 하품

하품은 강도 단계를 나누지 않고 감긴 눈·살짝 모인 미간·내려간 턱·세로 타원형 입을 함께 지시한 한 컷으로 비교한다. 제공된 샘플은 움직임 문구를 작성할 때 참고했으며, 모델에는 위의 Mira 원본 한 장만 입력했다. 샘플 사진은 원고 자산에 포함하지 않는다.

![Mira 하품 결과](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-yawn-reference-size-1024-seed-62294-steps-20.png)

[하품 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-yawn-reference-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

눈이 감기고 눈썹 안쪽이 모였으며, 입이 세로로 크게 열렸다. 입안에는 혀와 치아가 구분되고, 입꼬리가 옆으로 당겨지는 큰 웃음과 다른 모양이 나타났다. 머리색·가르마·단발과 정면 구도는 대체로 유지됐지만 미간·코 옆 주름과 턱 윤곽도 달라졌다. 원하는 입 벌림과 외형 보존을 따로 확인한다. 이 정지 이미지 한 장으로 하품의 시간에 따른 움직임이나 강도 차이를 검증한 것은 아니다.

같은 기준 문구로 재실행하려면 하품만 선택한다. 출력은 공통 설정인 1024×1024·20스텝·seed `62294`이며 추가 LoRA는 사용하지 않았다.

```bash
.venv/bin/python docs/assets/part-07/chapter-05/p7_5_9_qwen_edit_2511_mira_expressions.py \
  --expressions yawn --run-label yawn-repeat
```

## 실행 시간과 메모리

RTX 5070 Laptop GPU 8GB·시스템 RAM 64GB 환경에서 BF16·순차 CPU 오프로딩으로 생성했다. 완료된 24회 추론 시간은 장당 약 5분 48초~8분 16초, 합계 약 2시간 27분 12초다. 모델 로딩과 중단된 실행 시간은 이 합계에서 제외했다. PyTorch가 기록한 최대 할당 메모리는 약 4.15GiB, 최대 예약 메모리는 실행별 약 4.19~4.68GiB다. 이 값은 다른 프로세스를 포함한 GPU 전체 사용량이 아니다. 수정·추가 15회 추론은 합계 약 88분 48초였고, 별도로 생성한 수정 혐오 한 컷은 약 6분 12초였다. 이 16컷도 원본에서 독립 편집했다. 볼 부푼 삐짐 수정 결과는 같은 설정으로 약 6분 15초, 하품은 약 6분 45초, 윙크는 약 6분 13초가 걸렸다. 경멸의 최신 입 모양 수정 결과는 약 6분 33초가 걸렸다.

## 코 찡그림과 붉어짐

첫 결과에서 경멸은 한쪽 입꼬리를, 반감·혐오·극심한 혐오는 코 찡그림과 윗입술 올림을 요청했다. 뒤의 세 조건에서 코 붉어짐이 뚜렷했다. 프롬프트에는 홍조 요청이 없었고 피부색 유지 지시도 없었다.

혐오의 `a clearly wrinkled nose`를 콧등 옆 근육을 위로 당겨 위쪽 양옆에 짧은 주름을 만든다는 문장으로 바꿨다. 감정 이름·입술·눈꺼풀 지시와 생성 설정을 유지한 비교에서 붉어짐은 줄었지만 코끝 주름도 약해졌다. 반감과 극심한 혐오에도 같은 방식으로 위치와 움직임을 풀어 썼고, 경멸에는 코 주변 근육의 이완을 요청했다.

‘코 찡그림’이 감기나 코 자극을 연상시켰을 가능성은 작업 가설이다. 문구 변경의 출력 영향은 관찰했지만 모델 내부에서 감기와 연결됐다는 증거는 없다. 한 시드에서 확인한 결과이므로 다른 시드에서도 붉어짐과 코 움직임을 함께 비교해야 한다. 추가 12개에는 감정 이름 제거와 피부색 유지 지시를 함께 적용했으므로 이 한 조건 비교와 같은 단일 변수 실험으로 해석하지 않는다.

## 표정과 외형을 따로 비교하기

머리색·가르마·단발 실루엣과 정면 구도는 본문 39개 결과에서 대체로 유지됐다. 표정 변화가 작은 조건은 서로 비슷하게 보이기도 했다. 반대로 격노·극심한 혐오·극도의 공포·비통함처럼 입을 크게 벌린 조건은 턱 윤곽이나 주름·목 그림자가 함께 달라졌다.

| 비교 항목 | 관찰 | 해석 |
| --- | --- | --- |
| 약한 단계 구분 | 엄격함과 분개, 낙담과 우울한 표정의 차이가 작음 | 단계 이름만으로 서로 다른 학습 표본이라고 판단하지 않음 |
| 표정 외의 변화 | 혐오 계열의 코 붉어짐, 비통함의 강한 주름과 눈물 같은 자국 | 요청한 얼굴 움직임과 추가 효과를 구분함 |
| 단계별 움직임 | 기쁨·놀람은 입 벌림 차이가 보이지만 추가 표정의 입술 움직임은 약한 경우가 있음 | 강도 번호가 모든 얼굴 부위의 일관된 증가를 보장하지 않음 |
| 계열 간 구분 | 두려움은 가로로, 놀람은 둥글게 입이 열리지만 충격에는 미간 모임이 추가됨 | 감정 이름 대신 실제 눈썹·눈·입 모양을 함께 확인함 |

표정은 눈썹·눈꺼풀·볼·입이 지시한 방향으로 함께 움직였는지 본다. 외형은 그 변화 속에서도 얼굴 윤곽, 코, 홍채색, 가르마와 단발 실루엣이 이어지는지 본다. 입을 크게 벌렸다는 이유만으로 웃음이 성공한 것은 아니며, 웃음이 분명해도 얼굴이 다른 사람처럼 바뀌었다면 Mira 참조로 바로 채택하기 어렵다.

본문의 39개 조건을 생성했지만 모든 표정이 같은 정도로 구분되거나 외형을 보존한 것은 아니다. 재생성할 때는 혐오의 코 붉어짐과 약한 윗입술 올림, 슬픔의 약한 턱 움직임처럼 관찰한 문제를 골라 지시를 수정하고 같은 조건으로 비교한다.

학습 데이터 후보를 고를 때도 표정 이름만 붙여 모두 넣지 않는다. 얼굴·헤어가 흔들리거나 치아·입술이 어색한 이미지는 재생성 후보로 남긴다. 이 정면 표정 묶음은 표정의 다양성을 보강하지만, 새로운 포즈나 카메라 각도까지 검증한 자료는 아니다.

## 체크리스트

- 미소와 웃음에서 입뿐 아니라 눈과 볼의 차이도 보이는가?
- 놀람·슬픔·화남이 눈썹·눈·입의 조합으로 구분되는가?
- 약한 표정과 강한 표정 중 어느 쪽에서 원본의 얼굴·헤어·배경이 더 달라졌는가?
- 표정이 잘 나타난 결과와 Mira의 외형이 잘 유지된 결과를 따로 골랐는가?

## 출처와 참고 자료

- Paul Ekman Group, [Facial Action Coding System](https://www.paulekman.com/facial-action-coding-system/){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-09-12. 얼굴 움직임의 기술과 감정 해석을 구분하는 기준.
- Tadas Baltrušaitis, [OpenFace Action Units](https://github.com/TadasBaltrusaitis/OpenFace/wiki/Action-Units){: target="_blank" rel="noopener noreferrer" }, GitHub, 확인일: 2026-09-12. 지원 AU와 검출·강도 출력의 구분.

- Qwen, [Qwen-Image-Edit-2511 모델 카드](https://huggingface.co/Qwen/Qwen-Image-Edit-2511){: target="_blank" rel="noopener noreferrer" }, Hugging Face, 확인일: 2026-09-11. 이미지 입력과 편집 지시를 받는 공식 Diffusers 실행 예시를 참고했다.
