"""Load suffixed locale Markdown during mkdocs-static-i18n build-only runs.

When ``BUILD_ONLY_LOCALE=en`` or ``zh`` is used with ``docs_structure: suffix``,
mkdocs-static-i18n temporarily makes that locale the default language. In that
mode unsuffixed Korean source files can be selected for clean ``*.md`` nav
targets. This hook keeps the clean nav targets but swaps the Markdown source to
the matching suffixed file when it exists.
"""

from __future__ import annotations

import os
from pathlib import Path


_SUPPORTED_BUILD_ONLY_LOCALES = {"en", "zh"}


def on_page_markdown(markdown: str, page, config, files) -> str:
    locale = os.environ.get("BUILD_ONLY_LOCALE")
    if locale not in _SUPPORTED_BUILD_ONLY_LOCALES:
        return markdown

    src_path = Path(page.file.src_path)
    if src_path.suffix != ".md" or src_path.name.endswith(f".{locale}.md"):
        return markdown

    localized_src_path = src_path.with_suffix(f".{locale}.md")
    localized_abs_path = Path(config.docs_dir) / localized_src_path
    if not localized_abs_path.exists():
        return markdown

    return localized_abs_path.read_text(encoding="utf-8")
