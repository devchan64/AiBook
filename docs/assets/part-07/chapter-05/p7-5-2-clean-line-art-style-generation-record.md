# P7-5.1 clean line-art style examples: generation record

- Purpose: train a style-only adapter independently of `p7-mira` character identity.
- Tool: Codex `image_gen` (2026-08-02).
- Visual reference: the project-generated `p7-5-2-mira-reference-sheet-draft-01.png`; it was used only to request its clean line-art properties.
- Output: `p7-5-2-clean-line-art-style-sheet-01.png` through `-05.png`, each a 2x2 sheet of generic adult people and environments.
- Exclusions: every prompt prohibits Mira's teal bob, silver clip, white utility jacket, teal trousers, and navy crossbody bag. No external artist, comic, or copyrighted character style was requested.
- Panel handling: the splitter separates the 2x2 panel boundaries only. It does not crop a person within a panel. Training later uses aspect-ratio-preserving resize and white padding.

## Shared rendering contract

`clean thin dark line art, flat subdued or muted colors, minimal cel shading, sparse white or pale backgrounds, no screentone, no crosshatching, no glossy lighting, no photorealism, no 3D rendering, no text or signage`

## Sheet scene sets

1. Generic people in a bookstore, subway, cafe, and rooftop setting.
2. Rainy bus stop, university corridor, kitchen desk, convenience-store aisle.
3. Park bench, small office presentation, apartment entrance, low-view city crossing.
4. Library table, train interior, cafe counter, rooftop wide perspective.
5. Apartment balcony, subway platform, bookstore conversation, high-view riverside path.

The first candidate without the reference-driven rendering constraint was rejected and is not copied into the repository or used for training.

## Pack 02: controlled character-sheet revision

- Output: `p7-5-2-clean-line-art-style-pack-02-sheet-01.png` through `-04.png`, 16 generic full-body figures.
- Changed condition: remove all scenery and enforce white background, thin uniform charcoal contours, muted palette, and only pale fold shadows. Generic people have varied walking, sitting, reaching, half-turn, crouching, and side/back poses.
- Fixed exclusions: Mira's teal bob, silver clip, white utility jacket, teal wide-leg trousers, and navy crossbody bag remain prohibited.
- Reason: the first style dataset mixed detailed interiors, glossy light, dark shadows, and varied rendering strength. Its shared caption therefore did not identify the approved reference style.

## Mira clean-line scene pack 01

- Output: `p7-5-2-mira-clean-line-scene-pack-01-sheet-01.png`.
- Purpose: first approved-candidate source for a single character-and-scene adapter, not a style-only adapter.
- Four panels: Mira at a studio desk, university corridor, rear rainy-sidewalk walk, and park-bench reading.
- Contract: retain Mira's reference identity while using fine even charcoal outlines, muted colors, pale shadows, and simplified light backgrounds.
- Status: `candidate_approved_for_scene_style_direction`; it is four of the required 16 train scene panels and is not a held-out or quality-pass result.
