# Part 7 Character Reference Pack 승인 양식

이 양식은 웹툰 컷 생성 전에 고정할 자체 제작 캐릭터 일러스트를 승인하는 기록이다. 한 장의 인물 이미지를 여러 컷의 identity reference로 바로 사용하지 않는다.

## 기본 정보

```text
character_id:
revision:
creator_or_source:
rights_confirmation:
style_anchor:
approval_status: draft | approved | rejected
```

`rights_confirmation`에는 직접 제작, 사용 허락, 라이선스 확인 중 해당 근거를 적는다. 상업 캐릭터나 권리 불명 이미지는 이 팩에 넣지 않는다.

## 전신 Turnaround

| view | image_file | 전신·발 보임 | 헤어 실루엣 | 의상·신발 | 승인 |
| --- | --- | --- | --- | --- | --- |
| front |  |  |  |  |  |
| three_quarter_left |  |  |  |  |  |
| three_quarter_right |  |  |  |  |  |
| side |  |  |  |  |  |
| back |  |  |  |  |  |

## Face Sheet

| view_or_expression | image_file | 눈·눈썹 | 앞머리·hair clip | 얼굴형 | 승인 |
| --- | --- | --- | --- | --- | --- |
| front_neutral |  |  |  |  |  |
| three_quarter_left_neutral |  |  |  |  |  |
| three_quarter_right_neutral |  |  |  |  |  |
| side_neutral |  |  |  |  |  |
| front_smile |  |  |  |  |  |
| front_surprised |  |  |  |  |  |

## 의상·소품·화풍

| 항목 | 고정값 | 금지 변형 |
| --- | --- | --- |
| 헤어 색·길이 |  |  |
| 눈 색·형태 |  |  |
| 상의·하의·신발 |  |  |
| 반복 소품 |  |  |
| 선·채색·명암 |  |  |
| 배경과 인물 경계 |  |  |

## 승인 판정

```text
approved_by:
approved_at:
rejected_items:
next_revision_reason:
```

전신 turnaround와 face sheet에서 모든 필수 view가 승인되고, 의상·소품·화풍의 고정값이 기록됐을 때만 `approval_status: approved`로 변경한다.
