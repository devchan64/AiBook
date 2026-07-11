# Shared Asset Root

- `docs/assets/` is the single source-of-truth asset root for public manuscript pages.
- Store shared Mermaid sources, SVG files, PNG files, and related asset README files only under `docs/assets/`.
- Do not create separate real asset trees under `docs/en/assets/` or `docs/zh/assets/`.

## Path Rules

- Snippet includes use the MkDocs `pymdownx.snippets` base path `docs`, so manuscript files should keep using `--8<-- "assets/..."` for Mermaid source inclusion.
- Ordinary Markdown image links, file links, and local asset references should use normal relative paths such as `../../../assets/...` from each manuscript page.
- Command examples that point to repository files should refer to real paths under `docs/assets/...`.

## Locale Directory Policy

- Do not recreate `docs/en/assets` or `docs/zh/assets` as symlinks or duplicate directories.
- Keep translated manuscripts beside the Korean source as `section-01.en.md` and `section-01.zh.md`.
- Regardless of manuscript layout, asset storage remains centralized under `docs/assets/`.
- All asset additions and edits must still target the real files under `docs/assets/`.
