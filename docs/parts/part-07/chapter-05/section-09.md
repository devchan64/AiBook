# P7-5.9 보충학습: Mira의 표정 바꾸기

> Section ID: `P7-5.9`
> Version: `v2026.09.13`

같은 얼굴에서 눈썹·눈·볼·입을 바꾸면 표정이 달라진다. [P7-5.2](section-02.md)의 Mira 정면 머리를 Qwen-Image-Edit-2511로 편집한 39개 결과를 비교한다. 표정 이름에 맞는 움직임이 나타났는지, 그 과정에서 얼굴과 머리 모양이 유지됐는지가 중심이다.

## 같은 얼굴에서 표정 바꾸기

![Mira 정면 머리 입력](../../../assets/part-07/chapter-05/p7-5-2-mira-head-qwen-image-bf16-front-v1-code-63ece7-seed-62294-steps-30-size-1280.png)

39컷은 모두 이 원본에서 독립적으로 생성했다. 웃는 결과를 다시 화난 표정으로 편집하지 않았으므로 앞선 변형이 다음 컷에 누적되지 않는다. 공통 조건은 1024×1024, 20스텝, seed `62294`, true CFG `4.0`이다. 얼굴 비례·홍채색·헤어스타일·정면 구도·배경·조명·화풍은 유지하도록 요청했다.

표정 이름은 생성할 때 정한 의도다. 아래 묶음은 눈·입의 움직임이나 서로 혼동하기 쉬운 결과를 비교하기 위한 배치이며, 표의 순서가 감정의 강도 점수나 표준 분류를 뜻하지 않는다. 관찰은 시각적 검수이며 AU 검출이나 얼굴 동일성 측정 결과가 아니다.

## 39개 표정 비교

### 미소와 웃음

| 만족 | 즐거움 | 기쁨 | 큰 웃음 |
| --- | --- | --- | --- |
| ![Mira 만족](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-satisfaction-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 즐거움](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-amusement-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 기쁨](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-joy-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 큰 웃음](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-laughter-intensity-v1-size-1024-seed-62294-steps-20.png) |

만족과 즐거움은 입을 다문 미소다. 즐거움에서는 볼의 접힌 선과 눈의 좁아짐이 더 나타난다. 기쁨은 치아가 드러나고 큰 웃음은 입이 더 벌어지며 눈이 거의 감긴다. 입 벌림만 보지 않고 볼과 눈이 함께 달라지는지 비교한다.

[만족 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-satisfaction-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[즐거움 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-amusement-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[기쁨 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-joy-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[큰 웃음 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-laughter-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

### 수줍음과 장난기

| 수줍은 미소 | 머쓱한 미소 | 민망함 | 장난기 |
| --- | --- | --- | --- |
| ![Mira 수줍은 미소](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-shy_smile-expansion-v1-size-1024-seed-62294-steps-20.png) | ![Mira 머쓱한 미소](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-sheepish_smile-expansion-v1-size-1024-seed-62294-steps-20.png) | ![Mira 민망함](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-embarrassed-expansion-v1-size-1024-seed-62294-steps-20.png) | ![Mira 장난기](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-mischievous-expansion-v1-size-1024-seed-62294-steps-20.png) |

수줍은 미소는 내려온 눈꺼풀과 다문 미소가 함께 보이지만 만족·즐거움과 겹친다. 머쓱한 미소에는 미간의 긴장이 더해진다. 민망함은 의도한 입술 말아 넣기가 약하고, 장난기는 한쪽 입꼬리 올림보다 양쪽 미소에 가까워졌다. 이름이 달라도 결과의 움직임은 비슷할 수 있다.

[수줍은 미소 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-shy_smile-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[머쓱한 미소 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-sheepish_smile-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[민망함 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-embarrassed-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[장난기 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-mischievous-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

### 윙크·안도·하품

| 윙크 | 안도 | 하품 |
| --- | --- | --- |
| ![Mira 윙크](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-wink-reference-size-1024-seed-62294-steps-20.png) | ![Mira 안도](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-relieved-expansion-v1-size-1024-seed-62294-steps-20.png) | ![Mira 하품](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-yawn-reference-size-1024-seed-62294-steps-20.png) |

윙크는 한쪽 눈 감김과 작은 미소가 함께 보인다. 다만 화면 오른쪽 눈을 감으라는 지시와 달리 왼쪽 눈이 닫혔고, 윗볼 상승은 약하다. 안도는 양쪽 눈을 부드럽게 감고 작게 미소 짓는다. 하품은 미간이 모이고 입이 세로로 크게 열리며 혀·치아가 구분된다. 하품에서 강해진 코 옆 주름과 달라진 턱 윤곽은 외형 변화로 따로 확인한다.

[윙크 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-wink-reference-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[안도 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-relieved-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[하품 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-yawn-reference-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

### 삐짐과 못마땅함

| 삐짐 | 볼 부푼 삐짐 | 토라짐 | 못마땅함 |
| --- | --- | --- | --- |
| ![Mira 삐짐](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-pouting-expansion-v1-size-1024-seed-62294-steps-20.png) | ![Mira 볼 부푼 삐짐](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-puffed_pout-puffed-pout-v2-size-1024-seed-62294-steps-20.png) | ![Mira 토라짐](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-sulking-expansion-v1-size-1024-seed-62294-steps-20.png) | ![Mira 못마땅함](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-unimpressed-expansion-v1-size-1024-seed-62294-steps-20.png) |

삐짐은 아래입술 돌출이 약하고 눈썹 안쪽이 올라가 슬픔과 닮았다. 볼 부푼 삐짐은 다문 입과 내려간 입꼬리가 보이지만 입 옆 볼의 부피 변화가 약해 일반 삐짐에 가깝다. 토라짐과 못마땅함은 입술 누름이 약하고 서로 비슷하다. 볼의 부피, 입술 돌출, 입술 압착을 같은 움직임으로 취급하지 않는다. ICT-FaceKit도 입술 오므림(`mouthPucker`)과 볼 부풀림(`cheekPuff_L/R`)을 별도 표정 형태로 구분한다. 이 구분을 설계에 참고했으며, Qwen의 표정 강도를 수치로 제어한 것은 아니다.

[삐짐 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-pouting-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[볼 부푼 삐짐 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-puffed_pout-puffed-pout-v2-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[토라짐 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-sulking-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[못마땅함 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-unimpressed-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

### 서운함·억울함·난처함·의심

| 서운함 | 억울함 | 난처함 | 의심 |
| --- | --- | --- | --- |
| ![Mira 서운함](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-hurt_feelings-expansion-v1-size-1024-seed-62294-steps-20.png) | ![Mira 억울함](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-aggrieved-expansion-v1-size-1024-seed-62294-steps-20.png) | ![Mira 난처함](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-perplexed-expansion-v1-size-1024-seed-62294-steps-20.png) | ![Mira 의심](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-skeptical-expansion-v1-size-1024-seed-62294-steps-20.png) |

서운함은 입꼬리가 충분히 내려가지 않아 작은 미소처럼 보인다. 억울함과 난처함은 미간·입 주변 수축이 강해 분노나 불만에 가깝다. 의심은 눈썹 비대칭이 나타나지만 차이가 작다. 이 네 이름은 설계 의도이며, 출력만으로 실제 감정을 확정할 수는 없다.

[서운함 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-hurt_feelings-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[억울함 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-aggrieved-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[난처함 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-perplexed-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[의심 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-skeptical-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

### 엄격함과 분노

| 엄격함 | 분개 | 분노 | 격노 |
| --- | --- | --- | --- |
| ![Mira 엄격함](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-sternness-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 분개](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-indignation-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 분노](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-anger-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 격노](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-rage-intensity-v1-size-1024-seed-62294-steps-20.png) |

엄격함과 분개는 미간 수축의 차이가 작다. 분노에서는 벌어진 입술 사이로 맞물린 치아가 보이고, 격노에서는 입이 크게 열린다. 격노는 아래턱 윤곽과 목 그림자도 달라졌다. 표정의 차이가 커진 것과 얼굴 형태가 유지된 것은 별개의 결과다.

[엄격함 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-sternness-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[분개 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-indignation-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[분노 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-anger-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[격노 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-rage-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

### 경멸과 혐오

| 경멸 | 반감 | 혐오 | 극심한 혐오 |
| --- | --- | --- | --- |
| ![Mira 경멸](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-disdain-lower-lip-relaxed-size-1024-seed-62294-steps-20.png) | ![Mira 반감](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-aversion-expansion-v1-size-1024-seed-62294-steps-20.png) | ![Mira 혐오](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-disgust-nose-wording-v1-size-1024-seed-62294-steps-20.png) | ![Mira 극심한 혐오](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-revulsion-expansion-v1-size-1024-seed-62294-steps-20.png) |

경멸은 윗입술의 비대칭과 소량의 치아 노출이 남아 있다. 아랫입술의 한쪽 쏠림은 줄었지만 두툼한 돌출은 일부 보인다. 반감은 코끝 수축과 윗입술 올림이 약해 걱정과 비슷하다. 혐오는 콧등 주변의 당김을 볼 수 있고, 극심한 혐오에는 코의 붉은 색조가 일부 남았다. 경멸의 비대칭과 혐오의 코·윗입술 움직임은 같은 동작의 강도 차이가 아니다.

[경멸 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-disdain-lower-lip-relaxed-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[반감 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-aversion-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[혐오 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-disgust-nose-wording-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[극심한 혐오 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-revulsion-expansion-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

### 걱정과 공포

| 걱정 | 불안 | 두려움 | 극도의 공포 |
| --- | --- | --- | --- |
| ![Mira 걱정](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-concern-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 불안](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-anxiety-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 두려움](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-fear-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 극도의 공포](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-terror-intensity-v1-size-1024-seed-62294-steps-20.png) |

걱정은 눈썹 안쪽이 조금 올라가고 입이 다물려 있다. 불안은 입이 가로로 조금 벌어지며, 두려움에서는 눈과 입이 더 열린다. 극도의 공포는 눈 주변 선·코 옆 주름·목 힘줄과 그림자가 강해져 기준 얼굴의 인상도 달라졌다.

[걱정 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-concern-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[불안 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-anxiety-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[두려움 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-fear-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[극도의 공포 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-terror-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

### 주의 집중과 놀람

| 주의 집중 | 경이로움 | 놀람 | 충격 |
| --- | --- | --- | --- |
| ![Mira 주의 집중](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-alertness-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 경이로움](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-wonder-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 놀람](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-surprise-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 충격](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-shock-intensity-v1-size-1024-seed-62294-steps-20.png) |

주의 집중은 입이 거의 다물려 있고 경이로움은 입술이 조금 벌어진다. 놀람은 입이 둥글게 열리고 충격에서는 더 크게 열린다. 충격은 눈썹 안쪽이 모이고 미간 주름도 강해져 공포와 닮은 요소가 나타난다.

[주의 집중 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-alertness-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[경이로움 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-wonder-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[놀람 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-surprise-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[충격 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-shock-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

### 낙담과 슬픔

| 낙담 | 우울한 표정 | 슬픔 | 비통함 |
| --- | --- | --- | --- |
| ![Mira 낙담](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-dejection-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 우울한 표정](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-melancholy-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 슬픔](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-sadness-intensity-v1-size-1024-seed-62294-steps-20.png) | ![Mira 비통함](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-grief-intensity-v1-size-1024-seed-62294-steps-20.png) |

낙담과 우울한 표정은 눈썹·입꼬리가 비슷하며 우울한 표정의 눈꺼풀이 더 내려온다. 슬픔에서는 미간 주름과 눈가 광택이 커진다. 비통함은 입이 크게 열리지만 붉은 코와 강한 주름, 눈물처럼 보이는 가는 자국도 추가됐다. 표정 지시 외에 생긴 색·광택·자국을 구분해서 본다.

[낙담 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-dejection-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[우울한 표정 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-melancholy-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[슬픔 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-sadness-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

[비통함 입력·프롬프트·결과 기록](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-grief-intensity-v1-size-1024-seed-62294-steps-20-result.json){ .lazy-source }

## 움직임을 프롬프트로 쓰기

FACS의 Action Unit(AU)은 눈썹 올리기나 입꼬리 당기기처럼 얼굴 움직임을 구분하는 코드다. 이 실험에서는 AU를 설계 참고로 사용하고 모델에는 영어 움직임 문장을 전달한다.

| 참고 동작 | AU | 문장으로 표현할 내용 |
| --- | --- | --- |
| 볼·입꼬리 올리기 | AU6·AU12 | 볼과 입꼬리를 올려 미소 짓기 |
| 눈썹·눈꺼풀 올리기와 턱 내리기 | AU1·AU2·AU5·AU26 | 눈썹과 눈을 열고 턱을 내려 입 벌리기 |
| 코 주름과 윗입술 올리기 | AU9·AU10 | 코 주변을 당기고 윗입술 올리기 |

이 조합은 감정의 정답표가 아니다. AU6은 볼 올리기 자체를 가리키며 AU12와 반드시 함께 나타나야 하는 것은 아니다. JSON의 `au_hints`는 사람이 정한 의도이고 출력에서 측정한 값이 아니다. Qwen이 AU 번호를 전용 제어 입력으로 해석한다고 가정하지 않는다.

경멸은 입 전체를 비튼다는 지시를 윗입술의 비대칭과 아랫입술 이완으로 교체했다. 볼 부푼 삐짐은 눈에 띄는 공기 팽창을 요청하는 대신 입 옆의 약한 부피 변화로 범위를 좁혔다. 원하는 부위의 움직임을 구체화하되, 실패할 때마다 조건을 덧붙여 프롬프트를 길게 만들지는 않는다.

코 찡그림은 콧등 주변의 당김과 주름 위치로 풀어 쓰자 붉어짐이 줄었지만 코끝 수축도 약해졌다. 감기나 코 자극과의 연관성은 작업 가설이며 모델 내부에서 확인한 원인은 아니다. 한 시드의 결과이므로 색 변화 감소와 표정 유지가 다른 조건에서도 함께 나타나는지는 별도로 확인해야 한다.

## 생성과 실행 기록

통합 JSON에는 표정별 기준 프롬프트 하나씩 39개를 둔다. 수정할 때는 해당 문구를 교체하며 폐기 프롬프트와 버전별 설계는 쌓지 않는다. 각 결과 JSON에는 실행 당시 프롬프트와 입력·출력 해시가 남는다.

[통합 표정 설계 JSON](../../../assets/part-07/chapter-05/p7-5-9-mira-expression-spec.json){ .lazy-source }

[Mira 표정 생성 Python](../../../assets/part-07/chapter-05/p7_5_9_qwen_edit_2511_mira_expressions.py){ .lazy-source }

[공통 경로·해시·환경 기록 Python](../../../assets/part-07/chapter-05/p7_5_2_qwen_edit_2511_generate_mira_torso.py){ .lazy-source }

생성기는 `QwenImageEditPlusPipeline`으로 공식 BF16 모델을 한 번 읽고 선택한 표정을 순차 생성한다. 원본 1280×1280 이미지를 1024×1024로 줄여 입력하고 추가 LoRA는 사용하지 않는다. 모델은 `.tmp/download/huggingface/hub`의 로컬 캐시에서 읽는다.

저장소 루트에서 비교할 표정의 프롬프트와 경로를 확인한 뒤 생성한다.

```bash
.venv/bin/python docs/assets/part-07/chapter-05/p7_5_9_qwen_edit_2511_mira_expressions.py \
  --expressions amusement laughter --run-label smile-comparison --dry-run
```

```bash
.venv/bin/python docs/assets/part-07/chapter-05/p7_5_9_qwen_edit_2511_mira_expressions.py \
  --expressions amusement laughter --run-label smile-comparison
```

`--expressions`를 생략하면 현재 39개 표정을 모두 생성한다. `--run-label`은 출력 파일을 구분하는 이름이며 기존 결과가 있으면 덮어쓰지 않는다. `--input`, `--seed`, `--size`, `--steps`, `--cfg`로 입력과 조건을 바꿀 수 있다. 표현 문구의 영향을 비교할 때는 같은 입력·시드·설정을 유지한다.

RTX 5070 Laptop GPU 8GB·시스템 RAM 64GB 환경에서 순차 CPU 오프로딩으로 실행했다. 본문에 채택한 39컷의 추론 시간은 장당 5.8~8.3분, 합계 약 236.8분이다. 각 실행 JSON의 시간을 합산했으며 모델 로딩과 폐기 결과의 생성 시간은 제외했다. PyTorch 최대 할당 메모리는 약 4.15GiB, 최대 예약 메모리는 4.19~4.68GiB였다. 다른 프로세스를 포함한 GPU 전체 사용량은 아니다.

## 표정과 외형 검수

39개 이름이 곧 서로 구분되는 학습 표본 39개를 뜻하지는 않는다. 수줍은 미소와 즐거움, 토라짐과 못마땅함처럼 결과가 겹칠 수 있다. 반대로 격노·비통함·하품처럼 변화가 큰 결과는 턱 윤곽·주름·목 그림자까지 달라진다.

학습 데이터 후보는 눈썹·눈·입의 실제 움직임을 확인해 고른다. 표정이 분명해도 얼굴·헤어가 흔들리거나 입술·치아가 어색하다면 재검수한다. 이 묶음은 같은 정면 얼굴에서 얻은 결과이므로 새 포즈나 카메라 각도의 보존까지 검증한 자료는 아니다.

## 체크리스트

- 이름이 다른데도 비슷하게 보이는 두 결과는 무엇이며, 어느 부위가 같은가?
- 미소·윙크·하품에서 눈 감김과 입 모양은 어떻게 다른가?
- 경멸의 입술 비대칭과 혐오의 코 움직임을 구분할 수 있는가?
- 표정 변화와 함께 얼굴 윤곽·피부색·주름이 달라진 결과를 골랐는가?

## 출처와 참고 자료

- Paul Ekman Group, [Facial Action Coding System](https://www.paulekman.com/facial-action-coding-system/){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-09-12. 얼굴 움직임의 기술과 감정 해석을 구분하는 기준.
- Tadas Baltrušaitis, [OpenFace Action Units](https://github.com/TadasBaltrusaitis/OpenFace/wiki/Action-Units){: target="_blank" rel="noopener noreferrer" }, GitHub, 확인일: 2026-09-12. 지원 AU와 검출·강도 출력의 구분.

- Qwen, [Qwen-Image-Edit-2511 모델 카드](https://huggingface.co/Qwen/Qwen-Image-Edit-2511){: target="_blank" rel="noopener noreferrer" }, Hugging Face, 확인일: 2026-09-11. 이미지 입력과 편집 지시를 받는 공식 Diffusers 실행 예시를 참고했다.

- USC Institute for Creative Technologies, [ICT-FaceKit: Expression Shapes](https://github.com/USC-ICT/ICT-FaceKit#expression-shapes){: target="_blank" rel="noopener noreferrer" }, GitHub, 확인일: 2026-09-13. 입술 오므림과 볼 부풀림을 별도로 기술하는 설계 참고.
