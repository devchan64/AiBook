"""Normalize MkDocs i18n source-style links in generated HTML.

Localized pages use suffixed source files such as ``section-02.en.md``.
If an internal generated href still contains one of those source filenames,
rewrite only that href to the clean MkDocs URL.
"""

from __future__ import annotations

import re
from urllib.parse import SplitResult, urlsplit, urlunsplit


_HREF_RE = re.compile(r'(?P<prefix>\bhref=")(?P<href>[^"]+)(?P<suffix>")')
_LOCALIZED_MD_RE = re.compile(r"\.(?:en|zh)\.md$")


def _normalize_href(href: str) -> str:
    parsed = urlsplit(href)

    if parsed.scheme or parsed.netloc:
        return href

    path = parsed.path
    if not _LOCALIZED_MD_RE.search(path):
        return href

    if path.endswith("/index.en.md") or path.endswith("/index.zh.md"):
        path = path.rsplit("/", 1)[0] + "/"
    elif path in {"index.en.md", "index.zh.md"}:
        path = "./"
    else:
        path = _LOCALIZED_MD_RE.sub("/", path)

    return urlunsplit(
        SplitResult(
            scheme=parsed.scheme,
            netloc=parsed.netloc,
            path=path,
            query=parsed.query,
            fragment=parsed.fragment,
        )
    )


def on_post_page(output: str, page, config) -> str:
    def replace(match: re.Match[str]) -> str:
        href = match.group("href")
        return f'{match.group("prefix")}{_normalize_href(href)}{match.group("suffix")}'

    return _HREF_RE.sub(replace, output)
