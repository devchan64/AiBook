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
- Language-specific manuscript trees under `docs/en/` and `docs/zh/` own text content, not asset storage.
- All asset additions and edits must still target the real files under `docs/assets/`.
