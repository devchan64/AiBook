# Part 1 Chapter 1 Mermaid Assets

- Public manuscript pages can include the language-specific `.mmd` files through `pymdownx.snippets`.
- The `-en.mmd` files are the canonical English originals for future translation work.
- When updating a Mermaid asset set, revise the English structure first, then sync the Korean and Chinese derivatives so all files keep the same conceptual flow.
- If a translated diagram is identical to the English original, do not keep a duplicated language file. Let that language page include the shared `-en.mmd` asset directly.
- Current language sets:
  - `ai-scope-map-en.mmd` / `ai-scope-map-ko.mmd`
    `docs/zh/parts/part-01/chapter-01/section-01.md` currently shares `ai-scope-map-en.mmd`.
  - `problem-definition-flow-en.mmd` / `problem-definition-flow-ko.mmd`
    `docs/zh/parts/part-01/chapter-01/section-02.md` currently shares `problem-definition-flow-en.mmd`.
  - `ai-to-llm-map-en.mmd` / `ai-to-llm-map-ko.mmd`
    `docs/zh/parts/part-01/chapter-01/section-03.md` currently shares `ai-to-llm-map-en.mmd`.
