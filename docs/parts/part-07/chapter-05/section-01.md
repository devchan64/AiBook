# P7-5.1 화풍 참조 셋 생성: 로컬 GPU로 프레임 없는 기준 만들기

> Section ID: `P7-5.1`
> Version: `v2026.08.03`

캐릭터를 만들기 전에 화풍 기준을 먼저 고정해야 할 때가 있습니다. 여기서 화풍 참조 셋은 보기 좋은 배경을 모은 폴더가 아닙니다. 인물과 소품을 넣기 전, 선의 역할, 색의 겹침, 시간대의 광원, 장소의 폭, 카메라 구도를 **같은 기준으로 비교할 수 있게 만든 검수 입력**입니다. 한 장이 마음에 들어도 다른 장소와 카메라에서 계약이 무너지면, 그 한 장은 캐릭터 참조 셋의 화풍 기준이 될 수 없습니다.

이 절의 질문은 **8 GB급 로컬 GPU에서 만든 배경 화풍 표본이 다음 캐릭터 참조 셋의 기준이 되려면 무엇을 검수해야 하는가**입니다. 이 절의 산출물은 승인된 화풍 그 자체가 아니라, 후보 이미지·행별 판정·실패 이유·다음 생성을 막거나 통과시키는 gate입니다.

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

## 후보를 팩으로 오해하지 않는 판정표

현재 로컬 `FLUX.2-klein-base-4B`는 sequential CPU offload에서 `768 x 1152`, 50 step, batch 1의 배경 후보를 만들 수 있었습니다. 이것은 **실행 가능성**일 뿐 **화풍 팩 승인**은 아닙니다. 아래 표는 지금 보존한 후보가 어느 행의 근거인지와, 무엇 때문에 전체 팩을 아직 통과시키지 않는지를 구분합니다.

| 행 | 보존한 근거 | 현재 판정 | 아직 필요한 것 |
| --- | --- | --- | --- |
| 실내·새벽·high angle | 아트리움 하향 시점, 야외 courtyard 재생성 | courtyard 행 승인 | 이 승인은 high-angle 후보에만 적용되며 전체 팩 승인은 별도 |
| 실내·밤·oblique | 광원 보강 여객기 창가 view | 행 승인 | 이 승인은 실내·밤·oblique 원본에만 적용됨 |
| 실외·낮·wide eye-level | 도심 측면 교차로 재생성, 도시 공원 연못 | 행 승인 | 이 승인은 도심 원본의 낮 팔레트·측면 구도에만 적용됨 |
| 실외·해질녘·low angle | curb-height 주택가 | 행 승인 | 이 승인은 해질녘 low-angle 원본에만 적용됨 |
| 실외·우천 야간·overhead high angle | 옥상 광장 하향 시점 | 행 승인 | 이 승인은 우천 야간 overhead 원본에만 적용됨 |

베니스 사선 운하는 outdoor oblique의 보조 근거로 보존했지만, 위 다섯 행 중 하나를 대체하지는 않습니다. 첫 flat-color pack은 장소·시간·카메라 폭이 좁았고, 수채화 후보 일부는 page frame을 crop해야 했으며 여러 표본은 수직 중앙 소실점으로 수렴했습니다. 세탁소 야간 후보는 공간 원근은 맞았지만 해칭이 과도했습니다. 이런 PNG는 화풍 기준 자산으로 보존하지 않고 [검수 ledger](../../../assets/part-07/chapter-05/p7-5-1-local-style-pack-review.json)에 실패 원인만 남깁니다.

우천 야간 열차 승강장은 다섯 행의 overhead 행을 대신하지 않는 보조 장소 검증이다. 레일을 많이 그리거나 빗줄기를 화면 전체에 넣으면 선이 해칭처럼 보이기 쉽다. 따라서 이 후보는 레일을 두 줄로 제한하고, 작은 플랫폼 램프와 먼 역 조명이 젖은 바닥에서 끊긴 반사로 보이는지를 별도로 확인한다.

## 실패 원인을 다음 프롬프트의 구조로 바꾸기

실패한 후보에 `no frame`이나 `no hatching`을 더 쓰는 것만으로는 충분하지 않았습니다. 도심은 넓은 도로를 요청했을 때 중앙 소실점의 거리 복도로 수렴했습니다. 이를 고치기 위해 금지어를 늘리는 대신, 가까운 모퉁이에서 옆으로 건너다보는 **측면 교차로**로 장면 구조를 바꿨습니다. 여객기도 전체 좌석 열을 요청했을 때 패널 프레임과 문자형 표식이 생겼습니다. 창·좌석 등받이·천장만 보이는 **창가 close view**로 바꾸자, 야간과 사선 구도는 유지하면서 그 결함을 제거할 수 있었습니다.

반대로 장가계는 외곽 프레임은 사라졌지만 절벽의 반복 선이 해칭처럼 남았고, 우천 야간 플랫폼은 비·레일·지붕 선이 화면을 지배했습니다. 이 경우에는 crop이나 부분 보정으로 통과시키지 않습니다. `무엇이 틀렸는가`를 다음 생성의 구도·피사체 밀도·광원 조건으로 번역하고, 새 원본을 다시 검수합니다.

## 사람 판정과 Python gate의 역할

아래 Python 예제는 이미 사람이 쓴 ledger를 읽어 다음 단계 진입을 차단하거나 허용합니다. 이미지의 미적 품질을 자동 채점하는 모델이 아닙니다. 독자가 바꿀 값은 ledger의 `status`와 `next_run_matrix`이며, 이를 바꿨을 때 gate의 `BLOCKED` 또는 `PASS` 출력이 달라집니다. `status`만 바꾸어 통과시키는 것은 금지합니다. 먼저 행별 원본과 검수 이유가 갖춰져야 합니다.

```python
python docs/assets/part-07/chapter-05/p7_5_1_local_style_pack_gate.py
```

현재 출력은 다음과 같습니다.

```text
BLOCKED style pack
- review status: no approved frame-free style pack
```

이 결과는 실패가 아니라 현재 근거에 맞는 보호 장치입니다. 다섯 행의 조건부 통과 이미지가 있어도, 전체 화풍의 일관성을 확인하는 사람 승인이 끝나지 않았으므로 `P7-5.2`로 넘어가지 않습니다.

## 샘플 그리드와 실행 기록

아래 그리드는 전체 화풍 팩이 아니라 행별 검수 근거입니다. `행 승인`은 그 이미지가 해당 장소·시간·카메라 조건을 만족한다는 사람 판정이며, `조건부`는 같은 조건을 더 확인해야 하는 후보입니다. 어느 표시도 전체 팩 승인을 뜻하지 않습니다. 이미지마다 원본·seed·실행 조건·사람 판정은 링크한 JSON에 남기고, 전체 승인 여부는 ledger와 gate가 담당합니다. 색은 화면 CSS가 아니라 생성 원본에서 검수합니다.

<div class="aibook-style-reference-grid">
  <figure class="aibook-style-reference-grid__item is-approved">
    <img src="../../../../assets/part-07/chapter-05/p7-5-1-style-high-angle-courtyard-candidate.png" alt="이른 아침의 하향 courtyard 고각도 화풍 후보">
    <figcaption><strong>행 승인</strong><span>courtyard · 이른 아침 · high angle</span></figcaption>
  </figure>
  <figure class="aibook-style-reference-grid__item is-partial">
    <img src="../../../../assets/part-07/chapter-05/p7-5-1-style-low-angle-medium-chroma-candidate.png" alt="해질녘 주택가를 아래에서 올려다본 저각도 화풍 후보">
    <figcaption><strong>조건부</strong><span>주택가 · 해질녘 · low angle</span></figcaption>
  </figure>
  <figure class="aibook-style-reference-grid__item is-approved">
    <img src="../../../../assets/part-07/chapter-05/p7-5-1-style-venice-medium-chroma-candidate.png" alt="베니스 운하 사선 구도의 해질녘 화풍 후보">
    <figcaption><strong>보조 승인</strong><span>베니스 운하 · 해질녘 · oblique</span></figcaption>
  </figure>
  <figure class="aibook-style-reference-grid__item is-approved">
    <img src="../../../../assets/part-07/chapter-05/p7-5-1-style-gangnam-day-chroma-regenerated-candidate.png" alt="도심 유리 빌딩과 가로수가 있는 낮 화풍 후보">
    <figcaption><strong>행 승인</strong><span>도심 · 낮 · wide eye-level</span></figcaption>
  </figure>
  <figure class="aibook-style-reference-grid__item is-approved">
    <img src="../../../../assets/part-07/chapter-05/p7-5-1-style-daylight-park-medium-chroma-candidate.png" alt="맑은 낮의 공원 연못 화풍 후보">
    <figcaption><strong>보조 승인</strong><span>공원 · 낮 · eye-level</span></figcaption>
  </figure>
  <figure class="aibook-style-reference-grid__item is-approved">
    <img src="../../../../assets/part-07/chapter-05/p7-5-1-style-aircraft-night-lit-candidate.png" alt="야간 창밖과 객실 조명이 보이는 비행기 실내 화풍 후보">
    <figcaption><strong>행 승인</strong><span>여객기 실내 · 밤 · oblique</span></figcaption>
  </figure>
  <figure class="aibook-style-reference-grid__item is-approved">
    <img src="../../../../assets/part-07/chapter-05/p7-5-1-style-rainy-night-medium-chroma-candidate.png" alt="비가 그친 뒤 옥상 광장을 위에서 내려다본 야간 화풍 후보">
    <figcaption><strong>행 승인</strong><span>옥상 광장 · 우천 야간 · overhead</span></figcaption>
  </figure>
  <figure class="aibook-style-reference-grid__item is-approved">
    <img src="../../../../assets/part-07/chapter-05/p7-5-1-style-train-platform-bright-candidate.png" alt="밝은 캐노피 조명과 철로가 보이는 우천 야간 승강장 화풍 후보">
    <figcaption><strong>보조 승인</strong><span>열차 승강장 · 우천 야간 · oblique</span></figcaption>
  </figure>
</div>

`P7-5.2`의 character reference 생성 입력으로 쓰려면 전체 gate가 통과해야 합니다. [고각 실행 기록](../../../assets/part-07/chapter-05/p7-5-1-style-high-angle-courtyard-candidate.json), [저각 실행 기록](../../../assets/part-07/chapter-05/p7-5-1-style-low-angle-medium-chroma-candidate.json), [베니스 실행 기록](../../../assets/part-07/chapter-05/p7-5-1-style-venice-medium-chroma-candidate.json), [도심 실행 기록](../../../assets/part-07/chapter-05/p7-5-1-style-gangnam-day-chroma-regenerated-candidate.json), [낮 공원 실행 기록](../../../assets/part-07/chapter-05/p7-5-1-style-daylight-park-medium-chroma-candidate.json), [여객기 실행 기록](../../../assets/part-07/chapter-05/p7-5-1-style-aircraft-night-lit-candidate.json), [우천 야간 실행 기록](../../../assets/part-07/chapter-05/p7-5-1-style-rainy-night-medium-chroma-candidate.json), [열차 승강장 실행 기록](../../../assets/part-07/chapter-05/p7-5-1-style-train-platform-bright-candidate.json), [bright platform probe](#local-style-train-platform-bright-probe), [targeted regeneration probe](#local-style-targeted-chroma-regeneration-probe), [platform-aircraft-high-angle probe](#local-style-platform-aircraft-high-angle-regeneration-probe)를 함께 확인합니다.

<details id="local-style-pack-gate" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_1_local_style_pack_gate.py" data-language="python">
<summary>local style pack gate 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

<details id="local-style-high-angle-probe" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_1_flux2_style_high_angle_probe.py" data-language="python">
<summary>frame-free high-angle style probe 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

<details id="local-style-low-angle-probe" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_1_flux2_style_low_angle_probe.py" data-language="python">
<summary>frame-free outdoor sunset low-angle style probe 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

<details id="local-style-location-batch-probe" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_1_flux2_style_location_batch_probe.py" data-language="python">
<summary>location-diverse style batch probe 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

<details id="local-style-location-repair-probe" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_1_flux2_style_location_repair_probe.py" data-language="python">
<summary>failed-location first repair probe 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

<details id="local-style-targeted-repair-probe" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_1_flux2_style_targeted_repair_probe.py" data-language="python">
<summary>failed-location targeted repair probe 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

<details id="local-style-composition-repair-probe" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_1_flux2_style_composition_repair_probe.py" data-language="python">
<summary>composition-changing style repair probe 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

<details id="local-style-rainy-overhead-repair-probe" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_1_flux2_style_rainy_overhead_repair_probe.py" data-language="python">
<summary>rainy-night overhead style repair probe 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

<details id="local-style-daylight-medium-chroma-probe" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_1_flux2_style_daylight_medium_chroma_probe.py" data-language="python">
<summary>daylight medium-chroma style probe 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

<details id="local-style-pack-regeneration-probe" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_1_flux2_time_balanced_style_pack_regeneration.py" data-language="python">
<summary>time-balanced style-pack regeneration probe 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

<details id="local-style-dawn-high-angle-retry-probe" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_1_flux2_dawn_high_angle_regeneration_retry.py" data-language="python">
<summary>frame-free dawn high-angle retry probe 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

<details id="local-style-targeted-chroma-regeneration-probe" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_1_flux2_targeted_chroma_regeneration.py" data-language="python">
<summary>downtown, aircraft, high-angle, Venice targeted regeneration probe 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

<details id="local-style-platform-aircraft-high-angle-regeneration-probe" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_1_flux2_platform_aircraft_high_angle_regeneration.py" data-language="python">
<summary>rainy platform, lit aircraft, high-angle regeneration probe 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

<details id="local-style-train-platform-bright-probe" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_1_flux2_train_platform_bright_rail_retry.py" data-language="python">
<summary>bright rainy-night train-platform regeneration probe 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

## 체크리스트

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| 원본 | crop 없이 프레임 없는 생성 원본인가? |
| 선과 색 | 선화가 살아 있고 수채화 색층이 선을 덮지 않는가? |
| 시간 | 새벽·낮·해질녘·밤·우천 야간이 실제 광원 차이로 읽히는가? |
| 카메라 | 같은 중앙 소실점 반복이 아니라 camera family가 다른가? |
| 실패 해석 | 실패 원인을 crop이나 `status` 변경으로 덮지 않고 다음 구도·피사체 밀도·광원 조건으로 바꿨는가? |
| 다음 입력 | 모든 행의 원본과 사람 판정이 갖춰진 뒤에만 style pack을 승인했는가? |

## 출처와 참고 자료

- Black Forest Labs, [FLUX.2 Klein 4B model card](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-03.
- Hugging Face, [Diffusers FLUX.2 Klein pipeline](https://huggingface.co/docs/diffusers/main/en/api/pipelines/flux2_klein){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-03.
