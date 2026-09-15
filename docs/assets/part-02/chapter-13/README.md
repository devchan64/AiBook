# Part 2 Chapter 13 Plot Assets

- The three `p2_13_*.py` scripts reproduce the 12 chart sets from the manuscript data.
- Each chart has `-ko.svg`, `-en.svg`, and `-zh.svg` variants. Language variants share data and plotting code.
- The charts encode numeric coordinates, functions, and distributions, so they use Matplotlib rather than flowchart notation.
- Korean manual SVGs and shared English PNGs have been replaced by generated language-specific SVGs.
- Use `--language en` (or `ko`, `zh`) to render one language; the default renders all three.
- Use `--output-dir /tmp/p2-13-preview` for preview generation without replacing book assets.
- Matplotlib and NumPy are required. Localized output also requires an installed CJK font. The default is `Noto Sans CJK JP`; `--font-family` can select another installed font.
- Code examples in the manuscript use English labels for portability. Published images localize those labels without changing numeric inputs.
- SVG creation omits timestamps and uses a stable hash salt. Exact rendering also depends on Matplotlib and font versions.
- PNG previews and caches belong in temporary directories and are not committed.
- Verified with Matplotlib 3.9.4 and NumPy 2.0.2. All 36 SVG files reproduced byte-for-byte in the same environment.
