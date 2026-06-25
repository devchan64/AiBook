"""PyMdown SuperFences formatter for D2 diagrams."""

from __future__ import annotations

import html
import subprocess


def fence_d2_format(source, language, class_name, options, md, **kwargs):
    """Render a D2 code fence to inline SVG during MkDocs build."""

    try:
        result = subprocess.run(
            ["d2", "--pad", "24", "-", "-"],
            input=source,
            text=True,
            capture_output=True,
            check=True,
            timeout=30,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(
            "D2 CLI is required to render ```d2 code blocks. "
            "Install d2 or remove the d2 fence."
        ) from exc
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.strip() or exc.stdout.strip() or "unknown D2 render error"
        raise RuntimeError(f"D2 render failed: {detail}") from exc
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("D2 render timed out after 30 seconds.") from exc

    svg = result.stdout.strip()
    if svg.startswith("<?xml"):
        svg = svg.split("?>", 1)[1].lstrip()
    if "<svg" not in svg[:160]:
        raise RuntimeError("D2 render did not return SVG output.")

    return f'<div class="d2-diagram" role="img">{svg}</div>'


def fence_d2_source_format(source, language, class_name, options, md, **kwargs):
    """Fallback source renderer for diagnostics, kept for local debugging."""

    return (
        f'<pre class="{html.escape(class_name)}">'
        f"<code>{html.escape(source)}</code>"
        "</pre>"
    )
