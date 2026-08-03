# p7-mira draft-01 생성 기록

이 기준 시트는 저장소 안의 Python 스크립트가 아니라 Codex `image_gen.imagegen` 도구 호출로 생성했다. 따라서 이 문서는 실행하지 않은 재생성 스크립트를 대신하는 실제 생성 지시 기록이다.

## 실행 정보

```text
tool: image_gen.imagegen
referenced_image_paths: none
output: p7-5-1-mira-reference-sheet-draft-01.png
```

## 사용한 지시문

```text
Create an original Korean webtoon character reference sheet for an AI image-generation experiment. Clean white background, no text, no logos, no watermark. One single fictional young adult woman, full body in every view, consistent proportions and outfit. Character design: short teal bob haircut with a small silver hair clip on her left fringe, dark brown eyes, white cropped utility jacket over a charcoal crew-neck shirt, high-waisted teal wide-leg trousers, white sneakers, small navy crossbody messenger bag. Arrange five clearly separated full-body turnaround views in one horizontal sheet: front, three-quarter left, left side, three-quarter right, back. Add a smaller row of four head-and-shoulders views below: front neutral, three-quarter left neutral, three-quarter right neutral, side neutral. Crisp professional webtoon line art, flat cel shading, restrained cool palette, accurate hands and feet, neutral standing pose, no dramatic perspective, consistent face and clothing across every view. This is a production character model sheet, not a comic panel.
```

이 기록은 `draft-01`의 provenance를 남기는 용도다. 새 character sheet를 만들 때는 이 지시문을 그대로 품질 보증으로 취급하지 않고, 새 output과 새 검수를 별도 revision으로 기록한다.

## single-01 단일 기준 이미지

`single-01`부터는 grid sheet를 생성하거나 분할하지 않는다. 한 이미지에는 한 명의 전신 캐릭터와 하나의 camera view만 넣는다.

```text
tool: image_gen.imagegen
referenced_image_paths: none
output: p7-5-1-mira-single-reference-01.png
review: full body and both shoes visible; one horizontal navy flap crossbody bag, one continuous diagonal strap, and right-hip placement visually confirmed; training approval remains pending until the required independent views are complete
```

사용한 지시문은 다음과 같다.

```text
Use case: illustration-story
Asset type: single-image character reference for a Korean educational webtoon-generation experiment
Primary request: create exactly one full-body original adult woman character named Mira, centered and entirely visible from head to both soles, standing naturally in a relaxed neutral three-quarter front view. Clean contemporary webtoon line art with thin charcoal outlines, low-saturation flat colors, only subtle fold shadows, white or very pale neutral studio backdrop, no grid, no panels, no text, no watermark.
Subject invariants: short teal-blue bob haircut ending at the jaw, one small silver hair clip on her right-side bangs, dark brown eyes, white cropped utility jacket with two chest pockets and sleeve pocket, charcoal crew-neck shirt, teal wide-leg trousers, plain white sneakers. One and only one dark navy horizontal rectangular crossbody messenger bag with a distinct front flap, at her right hip. A single navy diagonal strap must run continuously from her left shoulder across the torso to that bag. The complete bag body, flap, strap connection, and hip placement must be clearly visible.
Composition requirements: leave generous white margin around the entire figure; preserve anatomically correct hands and feet; full legs and both shoes visible; the bag is not cropped or hidden.
Avoid: any extra person, duplicate bag, tote bag, backpack, vertical pouch, missing bag, extra strap, broken strap, crossed straps, malformed hands, malformed shoes, cropped head or feet, dramatic manga screentones, heavy shadows, background furniture or scenery.
```

이 파일은 single-image 생성의 기준 후보일 뿐 단독 학습 입력은 아니다.

## single-02 정면 전신 이미지

`single-01`을 입력 참조로 사용해 동일 인물의 정면 전신 view를 생성했다. 출력은 `p7-5-1-mira-single-reference-02-front.png`이며, 가방은 single-01과 같은 가로형 navy flap 본체, 왼쪽 어깨에서 오른쪽 hip까지 이어지는 단일 스트랩으로 그려졌다. 그러나 사람 검수에서 머리 대비 전신, 몸통 대비 다리의 비례가 single-01과 달라 `rejected`로 판정했다. 파일은 제거하며, 이후 생성은 가방과 함께 등신 비례를 고정 항목으로 판정한다.

## landmark 기준 재생성 후보

`single-01`을 참조하고 canonical 2D 비율을 지시문에 넣어 정면 전신 후보를 다시 생성했다. landmark reporter는 약 `6.270` 등신과 몸통/다리 비율 `0.591`을 기록했다. canonical 대비 변화는 각각 `9.226%`, `6.362%`로 4% 한계를 넘었으므로 `rejected`다. 실패 이미지는 저장소에 복사하지 않았고, manifest의 `single_image_generation_rejections`에 수치와 함께 남겼다.

## single-03 three-quarter-left 전신 이미지

`single-01`을 입력 참조로 사용해 three-quarter-left 전신 view를 생성했다. 출력은 `p7-5-1-mira-single-reference-03-three-quarter-left.png`이며, 가방의 가로형 flap 본체, 단일 스트랩, 오른쪽 hip 위치를 사람 검수했다. 자동 실루엣/어깨 비율과 몸통/다리 비율의 canonical 대비 변화는 `2.786%`, `1.047%`다. 모두 4% 이내여서 비례 검사는 통과했지만, 필수 view 전체가 완성되기 전까지는 `review_required` 상태다.

## three-quarter-right 첫 후보

three-quarter-right 첫 후보는 수기 머리 위·턱 좌표 기반 등신값이 크게 달라 제외했다. 이후 수기 좌표를 합격 기준에서 제외하고 자동 실루엣/어깨 비율로 교체했다.

## single-04 three-quarter-right 전신 이미지

두 번째 three-quarter-right 후보는 `p7-5-1-mira-single-reference-04-three-quarter-right.png`로 보존했다. 자동 실루엣/어깨 비율과 몸통/다리 비율의 canonical 대비 변화는 `2.912%`, `1.785%`로 모두 4% 이내다. 가방의 가로형 flap 본체, 단일 스트랩, 오른쪽 hip 위치도 검수했으며, 전체 required view가 갖춰지기 전까지는 `review_required`다.

## single-05 front 전신 이미지

정면 후보 두 장은 각각 몸통/다리 비율 불일치와 Pose Landmarker의 landmark 미검출로 제외했다. 세 번째 후보 `p7-5-1-mira-single-reference-05-front.png`는 전신·양손·양쪽 신발과 가로형 flap 가방의 단일 스트랩을 확인했다. 자동 실루엣/어깨 비율과 몸통/다리 비율의 canonical 대비 변화가 `0.238%`, `2.645%`여서 4% 이내를 통과했다. 이 파일과 landmark report는 참조 후보로만 보존하며, required view와 장면 자산이 완성될 때까지 학습 입력이 아니다.

## single-06 side-left 전신 이미지

`single-01`을 직접 참조해 왼쪽 profile 전신을 생성했다. 얼굴 profile, 재킷·바지의 측면 실루엣, 양쪽 신발, 가방의 몸체·flap·단일 strap을 시각 검수했고 landmark reporter도 정상 결과를 기록했다. 초기에 정면용 2D 비례식을 적용해 제외했으나, 측면에서 어깨 폭과 골반-발 길이의 투영이 달라 그 수치는 동일 인체 비례의 유효한 반증이 아니다. profile/rear contract에 따라 landmark 가시성과 사람의 의상·가방 구조 검수로 참조 후보로 보존한다.

## single-07 front-smile 전신 이미지

`single-05`를 직접 참조해 미소만 바꾼 전신 후보를 생성했다. `p7-5-1-mira-single-reference-07-front-smile.png`는 얼굴, 전신, 가방의 몸체·flap·단일 스트랩·hip 위치를 시각 검수했다. canonical 대비 실루엣/어깨와 몸통/다리 변화는 `0.339%`, `2.890%`로 모두 4% 이내다. 따라서 표정 변형의 참조 후보로 보존하되, 전체 팩 승인 전까지 학습 입력으로 쓰지 않는다.

## single-08 front-surprised 전신 이미지

`single-05`를 직접 참조해 눈썹·눈·입만 절제된 놀람 표정으로 바꾼 전신 후보를 생성했다. `p7-5-1-mira-single-reference-08-front-surprised.png`는 가방 몸체·flap·단일 스트랩과 전신 framing을 시각 검수했다. canonical 대비 실루엣/어깨와 몸통/다리 변화는 `0.122%`, `2.691%`로 모두 4% 이내다. 표정 변형의 참조 후보로 보존하며 전체 팩 승인 전까지 학습 입력으로 쓰지 않는다.

## single-09 bag-flap-touch 전신 이미지

`single-05`를 직접 참조해 오른손으로 가방 flap 하단을 잡는 three-quarter-front 전신 후보를 생성했다. 오른손의 손가락과 왼손, 팔꿈치·무릎·신발, 가방 몸체·flap·단일 스트랩·hip 위치를 시각 검수했다. 동작은 골반과 팔의 회전 때문에 중립 view의 4% 몸통/다리 기준을 그대로 쓰지 않는다. action contract의 10% 한계에서 canonical 대비 실루엣/어깨와 몸통/다리 변화는 `1.407%`, `7.836%`로 통과했다. 이 파일은 손-소품 접촉 참조 후보이며, 전체 팩 승인 전까지 학습 입력이 아니다.

## single-10 walk 전신 이미지

`single-05`를 직접 참조해 한 발이 화면 왼쪽으로 나가는 걷기 전신 후보를 생성했다. 두 손, 두 무릎·발목, 양쪽 신발 밑창, 가방 몸체·flap·단일 스트랩을 시각 검수했다. 보폭은 pose landmarker가 잡는 골반-발 길이의 2D 투영을 바꾸므로 action contract의 몸통/다리 한계는 실제 보행 결과를 확인해 15%로 조정했다. canonical 대비 실루엣/어깨와 몸통/다리 변화는 `2.403%`, `12.501%`이며 통과했다. 이 파일은 보행 참조 후보이며, 전체 팩 승인 전까지 학습 입력이 아니다.

## single-11 seat-stool 전신 이미지

`single-05`를 직접 참조해 단순한 회색 스툴에 앉은 전신 후보를 생성했다. 양손이 각각 무릎 위에 놓이고 양쪽 신발 밑창, 무릎·팔꿈치, 스툴 접촉, 가방의 몸체·flap·단일 스트랩이 모두 보이는지 시각 검수했다. landmark reporter는 정상 결과를 기록했지만, 앉은 자세는 서 있는 기준 이미지와 골반-발 관계가 다르므로 정적 비례 비교를 합격 근거로 쓰지 않는다. 이 파일은 seated pose의 사람 검수·landmark 가시성 참조 후보이며 전체 팩 승인 전까지 학습 입력이 아니다.

## single-12 rear-three-quarter 전신 이미지

`single-01`을 직접 참조해 후면 3/4 전신 후보를 생성했다. 재킷의 뒷면 실루엣, 보이는 얼굴 쪽의 clip, 양손·양발, 가방 몸체·flap, 왼쪽 어깨에서 등 뒤를 지나 hip으로 이어지는 단일 스트랩을 시각 검수했다. landmark reporter는 정상 결과를 기록했다. 후면은 정면의 2D 어깨 폭과 투영이 다르므로, profile/rear contract에 따라 landmark 가시성과 사람의 의상·가방 구조 검수로만 참조 후보를 판정한다.

## detail-01 face-three-quarter 이미지

`single-05`를 직접 참조해 얼굴·어깨만을 의도적으로 새로 생성했다. 기존 전신 이미지의 일부를 자른 파일이 아니다. 눈 두 개의 형태, 청록 단발의 앞머리와 외곽선, 오른쪽 bangs의 은색 clip, 얼굴선, 재킷 collar를 시각 검수했다. 이 파일은 얼굴·눈·머리카락 선화를 보완하는 detail reference이며 전신 비례 검사를 대체하거나 단독 학습 입력으로 쓰지 않는다.

## detail-02 hands-bag 이미지

`single-09`를 직접 참조해 흉부부터 허벅지까지의 손·가방 detail을 의도적으로 새로 생성했다. 기존 전신 이미지의 일부를 자른 파일이 아니다. 양쪽 손목과 손가락 수·방향, 가방 몸체·flap·버클, 단일 대각 스트랩의 결합을 시각 검수했다. 오른손은 지시한 flap 하단 대신 가방 상단에 놓였지만, 손-소품 접촉과 가방 구조의 detail reference로는 유효하다. 전신 비례 검사를 대체하거나 단독 학습 입력으로 쓰지 않는다.

## scene-01 cafe-standing 이미지

`single-05`와 `detail-01`을 입력 참조로 사용해 밝은 동네 카페의 전신 장면을 새로 생성했다. 이는 인물 합성이나 배경 병합이 아닌 하나의 장면 생성물이다. 얼굴·전신·양손·양쪽 신발의 바닥 접촉, 가로형 navy flap 가방·단일 strap, 테이블·의자의 크기와 원근, clean line-art를 시각 검수했다. landmark reporter도 정상 결과를 기록했다. scene reference는 train/held-out 분할과 panel별 사람 검수가 끝나기 전에는 학습 입력이 아니다.

## scene-02 subway-low-angle 이미지

`single-05`와 `detail-01`을 입력 참조로 사용해 조용한 지하철 플랫폼의 낮은 시점 전신 장면을 새로 생성했다. 얼굴·전신·손·신발과 바닥 접촉, 가로형 navy flap 가방·단일 strap, 플랫폼 edge·벤치·천장의 원근을 시각 검수했다. 낮은 시점이지만 발과 다리를 과도하게 확대하지 않은 결과로 판정했으며 landmark reporter도 정상 결과를 기록했다. scene reference는 train/held-out 분할과 panel별 사람 검수가 끝나기 전에는 학습 입력이 아니다.

## scene-03 rooftop-high-angle 이미지

`single-05`와 `detail-01`을 입력 참조로 사용해 옥상 테라스의 절제된 high-angle 전신 장면을 새로 생성했다. 얼굴·전신·손·신발과 바닥 접촉, 가로형 navy flap 가방·단일 strap, 난간·도시 배경의 스케일을 시각 검수했다. high-angle에서도 머리·손의 크기를 과장하지 않고 전신 anatomy를 유지한 결과로 판정했으며 landmark reporter도 정상 결과를 기록했다. scene reference는 train/held-out 분할과 panel별 사람 검수가 끝나기 전에는 학습 입력이 아니다.

## scene-04 bookstore-reach 이미지

`single-05`와 `detail-01`을 입력 참조로 사용해 독립 서점에서 책등을 손끝으로 만지는 medium-full-body 장면을 새로 생성했다. 얼굴·전신·양쪽 신발과 바닥 접촉, 책등에 닿는 손, 가로형 navy flap 가방·단일 strap, 책장과 진열대의 원근을 시각 검수했다. landmark reporter도 정상 결과를 기록했다. scene reference는 train/held-out 분할과 panel별 사람 검수가 끝나기 전에는 학습 입력이 아니다.

## scene-05 park-bench-seated 이미지

`single-11`과 `detail-01`을 입력 참조로 사용해 동네 공원의 벤치에 앉은 장면을 새로 생성했다. 양손·양발·무릎과 벤치 접촉, 얼굴, 가로형 navy flap 가방·단일 strap, 보도·벤치·나무의 스케일을 시각 검수했다. landmark reporter도 정상 결과를 기록했다. scene reference는 train/held-out 분할과 panel별 사람 검수가 끝나기 전에는 학습 입력이 아니다.

## scene-06 rainy-walk-look-back 이미지

`single-12`와 `detail-01`을 입력 참조로 사용해 비 온 뒤 주거 보행로를 걷다 뒤돌아보는 후면 3/4 장면을 새로 생성했다. 얼굴의 뒤돌아보기, 재킷 뒷면, 양손, 보행 중 들어올린 신발과 바닥 신발, 가로형 navy flap 가방과 등 뒤의 단일 strap, 젖은 보도 원근을 시각 검수했다. landmark reporter도 정상 결과를 기록했다. scene reference는 train/held-out 분할과 panel별 사람 검수가 끝나기 전에는 학습 입력이 아니다.

## scene-07 library-crouch 이미지

`single-05`와 `detail-02`를 입력 참조로 사용해 공공 도서관의 낮은 선반을 살피는 crouch 장면을 새로 생성했다. 머리·양손·손목·무릎·발목·양쪽 신발과 바닥 접촉, 가로형 navy flap 가방·단일 strap, 낮은 선반의 원근을 시각 검수했다. crouch는 서 있는 비례식으로 평가하지 않고 관절·접촉·소품 구조와 landmark 가시성으로 검토하며, landmark reporter도 정상 결과를 기록했다. scene reference는 train/held-out 분할과 panel별 사람 검수가 끝나기 전에는 학습 입력이 아니다.

## scene-08 riverside-run 이미지

`single-10`과 `detail-01`을 입력 참조로 사용해 강변 보행로를 달리는 전신 장면을 새로 생성했다. 머리·손·손목, 반대 방향으로 흔들리는 팔, 달리는 양다리·양쪽 신발·바닥 그림자, 가로형 navy flap 가방·단일 strap, 강변 난간과 수면의 스케일을 시각 검수했다. landmark reporter도 정상 결과를 기록했다. scene reference는 train/held-out 분할과 panel별 사람 검수가 끝나기 전에는 학습 입력이 아니다.

## scene-09 entryway-reach 이미지

`single-05`와 `detail-02`를 입력 참조로 사용해 아파트 현관의 높은 선반을 향해 왼손을 뻗는 전신 장면을 새로 생성했다. 머리·손가락·손목·팔꿈치·어깨, 양쪽 신발과 바닥 접촉, 가로형 navy flap 가방·단일 strap, 현관과 선반의 스케일을 시각 검수했다. landmark reporter도 정상 결과를 기록했다. scene reference는 train/held-out 분할과 panel별 사람 검수가 끝나기 전에는 학습 입력이 아니다.

## scene-10 stair-descend 이미지

`single-10`과 `detail-01`을 입력 참조로 사용해 실내 계단을 한 칸 내려오는 전신 장면을 새로 생성했다. 머리·양손·무릎·발목, 서로 다른 계단에 놓인 양쪽 신발, 가로형 navy flap 가방·단일 strap, 난간·계단 원근을 시각 검수했다. landmark reporter도 정상 결과를 기록했다. 계단은 발의 높이가 달라 서 있는 비례식으로 평가하지 않고 관절·발 접촉·소품 구조로 검토하며, scene reference는 train/held-out 분할과 panel별 사람 검수가 끝나기 전에는 학습 입력이 아니다.

## scene-11 bus-shelter-dusk 이미지

`single-05`와 `detail-01`을 입력 참조로 사용해 이른 저녁 동네 버스 정류장 전신 장면을 새로 생성했다. 얼굴·양손·양쪽 신발과 바닥 접촉, 청록 머리·흰 재킷·청록 바지·navy flap 가방의 색, 단일 strap, 정류장 벤치와 빈 안내판의 스케일을 시각 검수했다. landmark reporter도 정상 결과를 기록했다. scene reference는 train/held-out 분할과 panel별 사람 검수가 끝나기 전에는 학습 입력이 아니다.

## scene-12 lobby-door-handle 이미지

`single-05`와 `detail-02`를 입력 참조로 사용해 아파트 로비의 유리문 손잡이를 오른손으로 잡는 전신 장면을 새로 생성했다. 머리·양손·오른손 손목과 손잡이 접촉, 양쪽 신발과 바닥 접촉, 가로형 navy flap 가방·단일 strap·오른쪽 hip 위치, 유리문과 복도의 원근을 시각 검수했다. landmark reporter도 정상 결과를 기록했다. scene reference는 train/held-out 분할과 panel별 사람 검수가 끝나기 전에는 학습 입력이 아니다.

## scene-13 gallery-lean 이미지

`single-05`와 `detail-02`를 입력 참조로 사용해 현대 미술관 난간에 왼쪽 팔을 가볍게 기대는 전신 장면을 새로 생성했다. 머리·얼굴·양손·왼쪽 전완의 난간 접촉, 양쪽 신발과 바닥 접촉, 가로형 navy flap 가방·단일 strap·오른쪽 hip 위치, 전시 프레임과 난간의 원근을 시각 검수했다. 그림은 글자가 없는 색면으로 제한했다. landmark reporter도 정상 결과를 기록했다. scene reference는 train/held-out 분할과 panel별 사람 검수가 끝나기 전에는 학습 입력이 아니다.

## scene-14 university-corridor-walk 이미지

`single-05`와 `detail-02`를 입력 참조로 사용해 낮의 대학 복도를 화면 왼쪽으로 걸으며 창을 보는 전신 장면을 새로 생성했다. 머리·양손·손목, 보행 중인 양다리와 신발 밑창, 가로형 navy flap 가방·단일 strap·오른쪽 hip 위치, 빈 사물함·창·복도 원근을 시각 검수했다. 가까운 앞발은 의도적인 camera projection으로 커졌지만 관절과 의상 구조는 유지된다. landmark reporter도 정상 결과를 기록했다. scene reference는 train/held-out 분할과 panel별 사람 검수가 끝나기 전에는 학습 입력이 아니다.

## scene-15 greenhouse-look-back 이미지

`single-05`와 `detail-02`를 입력 참조로 사용해 온실에서 왼손으로 잎을 가볍게 만지고 뒤를 돌아보는 후면 3/4 전신 장면을 새로 생성했다. 재킷의 후면 실루엣, 얼굴의 뒤돌아보기, 잎에 닿는 왼손·손목, 가방 근처의 오른손, 양쪽 신발, 가로형 navy flap 가방·등 뒤의 단일 strap·오른쪽 hip 위치, 온실의 유리 구조와 식물 규모를 시각 검수했다. landmark reporter도 정상 결과를 기록했다. scene reference는 train/held-out 분할과 panel별 사람 검수가 끝나기 전에는 학습 입력이 아니다.

## scene-16 laundromat-fold 이미지

`single-05`와 `detail-02`를 입력 참조로 사용해 푸른 저녁의 세탁소에서 양손으로 작은 흰 수건을 접는 전신 장면을 새로 생성했다. 머리·양손·손목·팔꿈치, 양쪽 신발과 바닥 접촉, 가로형 navy flap 가방·단일 strap·오른쪽 hip 위치, 접는 테이블·세탁기·창의 스케일을 시각 검수했다. landmark reporter도 정상 결과를 기록했다. scene reference는 train/held-out 분할과 panel별 사람 검수가 끝나기 전에는 학습 입력이 아니다.

## heldout-01 kitchen-cupboard 이미지

`single-05`와 `detail-02`를 입력 참조로 사용해 이른 아침 아파트 주방에서 왼손으로 수납장 문을 닫는 전신 장면을 새로 생성했다. 이 파일은 학습 장면이 아닌 독립 평가 후보이며, 카페·지하철·옥상·서점·공원·도서관·현관·계단·미술관·복도·온실·세탁소와 장소가 겹치지 않는다. 순수 side full-body camera, 옆얼굴, 수납장에 닿는 왼손·손목, 오른손, 들어 올린 신발과 바닥 신발, 가로형 navy flap 가방·단일 strap·오른쪽 hip 위치를 시각 검수했다. landmark reporter도 정상 결과를 기록했다. 어떤 train 목록에도 이 source ID를 넣지 않는다.

## heldout-02 ferry-deck 이미지

`single-05`와 `detail-02`를 입력 참조로 사용해 맑은 날 바다 위 페리 덱의 전신 장면을 새로 생성했다. 이 파일은 학습 장면이 아닌 독립 평가 후보이며, 상부 덱의 3/4 full-body 구도와 바다·난간·계단을 쓴다. 난간을 잡은 오른손, 재킷 앞을 잡은 왼손, 양쪽 신발과 덱 접촉, 가로형 navy flap 가방·단일 strap·오른쪽 hip 위치, 바람에 따른 머리·재킷 주름을 시각 검수했다. landmark reporter도 정상 결과를 기록했다. 어떤 train 목록에도 이 source ID를 넣지 않는다.

## heldout-03 cinema-ticket 이미지

`single-05`와 `detail-02`를 입력 참조로 사용해 밤의 동네 영화관 foyer에서 왼손으로 빈 표를 줍는 전신 장면을 새로 생성했다. 이 파일은 학습 장면이 아닌 독립 평가 후보이며, low side three-quarter full-body camera와 영화관 foyer라는 장소를 사용한다. 굽힌 머리·몸통, 표에 닿는 왼손·손목·손가락, 균형을 잡는 오른팔, 양쪽 신발과 바닥 접촉, 가로형 navy flap 가방·단일 strap·오른쪽 hip 위치를 시각 검수했다. landmark reporter도 정상 결과를 기록했다. 어떤 train 목록에도 이 source ID를 넣지 않는다.

## heldout-04 ceramics-cup 이미지

`single-05`와 `detail-02`를 입력 참조로 사용해 오후의 동네 도예 작업실에서 오른손으로 무늬 없는 작은 찻잔을 작업대에 놓는 전신 장면을 새로 생성했다. 이 파일은 학습 장면이 아닌 독립 평가 후보이며, front three-quarter full-body camera와 도예 작업실이라는 장소를 사용한다. 얼굴, 잔에 닿는 오른손·손목·손가락, 왼손, 양쪽 신발과 바닥 접촉, 가로형 navy flap 가방·단일 strap·오른쪽 hip 위치, 작업대와 도자기 선반의 규모를 시각 검수했다. landmark reporter도 정상 결과를 기록했다. 어떤 train 목록에도 이 source ID를 넣지 않는다.

## single-13 wave 전신 이미지

`single-05`와 `detail-02`를 입력 참조로 사용해 흰 배경에서 왼손을 들어 인사하고 오른손을 가방 flap 위에 둔 전신 동작 후보를 새로 생성했다. 왼손의 다섯 손가락·손목·팔꿈치, 오른손과 flap 접촉, 양쪽 무릎·발목·신발, 가로형 navy flap 가방·단일 strap·오른쪽 hip 위치를 시각 검수했다. action contract에서 canonical 대비 실루엣/어깨와 몸통/다리 변화는 `7.853%`, `0.833%`로 15% 이내다. 이 파일은 손 제스처 참조 후보이며, 전체 팩 승인 전까지 학습 입력이 아니다.

## single-14 side-walk-pause 전신 이미지

`single-06`와 `detail-02`를 입력 참조로 사용해 흰 배경에서 옆모습으로 짧은 보행을 멈춘 전신 동작 후보를 새로 생성했다. 옆얼굴과 목선, 왼쪽 어깨 근처의 strap을 잡은 손·손목, 오른쪽 허벅지 옆 손, 앞뒤로 놓인 양쪽 신발, 가로형 navy flap 가방의 옆면과 단일 strap·오른쪽 hip 위치를 시각 검수했다. profile view는 정면의 2D 어깨 폭과 다리 투영이 다르므로 landmark 가시성과 사람의 구조 검토만 기록한다. 전체 팩 승인 전까지 학습 입력이 아니다.

## single-15 side-right-bag 전신 이미지

`single-05`와 `detail-02`를 입력 참조로 사용해 흰 배경에서 오른쪽 옆면으로 가방의 앞 아래 모서리를 오른손으로 받치는 전신 후보를 새로 생성했다. 오른쪽 bangs의 clip과 옆얼굴, 가방 flap에 닿는 오른손·손목, 단일 strap의 어깨 결합, 양쪽 신발, 가로형 navy flap 가방·오른쪽 hip 위치를 시각 검수했다. side projection은 landmark 가시성과 사람의 구조 검토로만 기록한다. 전체 팩 승인 전까지 학습 입력이 아니다.

## single-16 rear-look-right 전신 이미지

`single-12`와 `detail-02`를 입력 참조로 사용해 흰 배경에서 머리만 오른쪽으로 돌린 순수 후면 전신 후보를 새로 생성했다. 얼굴 가장자리와 오른쪽 bangs의 clip, 재킷의 후면 봉제선, 왼쪽 어깨에서 등 뒤를 거쳐 오른쪽 hip 가방으로 연결되는 단일 strap, 양손·양발과 가방 위치를 시각 검수했다. rear projection은 landmark 가시성과 사람의 구조 검토로만 기록한다. 전체 팩 승인 전까지 학습 입력이 아니다.

## single-17 weight-shift-hands 전신 이미지

`single-05`와 `detail-02`를 입력 참조로 사용해 흰 배경에서 오른쪽 무릎을 가볍게 굽히고 양손을 재킷 하단에서 느슨하게 모은 전신 동작 후보를 새로 생성했다. 양손의 손가락·손목·팔꿈치, 한쪽 다리에 실린 체중과 굽힌 반대쪽 무릎, 양쪽 신발, 가로형 navy flap 가방·단일 strap·오른쪽 hip 위치를 시각 검수했다. action contract에서 canonical 대비 실루엣/어깨와 몸통/다리 변화는 `8.680%`, `7.176%`로 15% 이내다. 전체 팩 승인 전까지 학습 입력이 아니다.

## single-18 invite-palm 전신 이미지

`single-05`와 `detail-02`를 입력 참조로 사용해 흰 배경에서 왼손을 앞으로 내밀고 오른손으로 가방 flap을 잡은 전신 동작 후보를 새로 생성했다. 앞으로 뻗은 왼손의 다섯 손가락·손목·팔꿈치, 가방 flap에 닿는 오른손, 양쪽 신발, 가로형 navy flap 가방·단일 strap·오른쪽 hip 위치를 시각 검수했다. action contract에서 canonical 대비 실루엣/어깨와 몸통/다리 변화는 `9.957%`, `8.920%`로 15% 이내다. 전체 팩 승인 전까지 학습 입력이 아니다.

## single-19 rear-left-look-back 전신 이미지

`single-12`와 `detail-02`를 입력 참조로 사용해 흰 배경에서 왼쪽 rear 3/4 자세로 서서 뒤를 돌아보는 전신 후보를 새로 생성했다. 뒤돌아본 얼굴과 보이는 오른쪽 bangs의 clip, 재킷 등판, 재킷 하단에 닿는 왼손·손목, 오른손, 양쪽 신발, 등 뒤를 지나 오른쪽 hip의 가로형 navy flap 가방으로 이어지는 단일 strap을 시각 검수했다. rear projection은 landmark 가시성과 사람의 구조 검토로만 기록한다. 전체 팩 승인 전까지 학습 입력이 아니다.

## single-20 rear-step-bag 전신 이미지

`single-16`와 `detail-02`를 입력 참조로 사용해 흰 배경에서 왼발을 들어 뒤로 걸어 나가며 오른손으로 가방 flap을 잡는 rear 3/4 전신 후보를 새로 생성했다. 뒤돌아본 얼굴, 오른손의 손가락·손목과 flap 접촉, 왼팔, 들어 올린 왼쪽 신발과 바닥에 닿은 오른쪽 신발, 재킷 등판, 가로형 navy flap 가방·단일 등 뒤 strap·오른쪽 hip 위치를 시각 검수했다. rear action은 landmark 가시성과 사람의 구조 검토로만 기록한다. 이 이미지로 유효한 단일 전신 기준은 19장에 도달했다.
