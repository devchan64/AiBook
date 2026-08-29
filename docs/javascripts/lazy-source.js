(function () {
  const LANGUAGE_BY_EXTENSION = {
    csv: "csv",
    js: "javascript",
    json: "json",
    md: "markdown",
    mjs: "javascript",
    mmd: "mermaid",
    py: "python",
    toml: "toml",
    ts: "typescript",
    txt: "text",
    yaml: "yaml",
    yml: "yaml",
  };
  const AUTO_LAZY_SOURCE_EXTENSIONS = new Set(["json", "py"]);

  function inferLanguageFromUrl(url) {
    const pathname = new URL(url, window.location.href).pathname;
    const extension = pathname.split(".").pop().toLowerCase();
    return LANGUAGE_BY_EXTENSION[extension] || "text";
  }

  function filenameFromUrl(url) {
    const pathname = new URL(url, window.location.href).pathname;
    const filename = pathname.split("/").filter(Boolean).pop();
    return filename || pathname;
  }

  function isAutoLazySourceLink(link) {
    const url = new URL(link.href, window.location.href);
    const extension = url.pathname.split(".").pop().toLowerCase();
    const parent = link.parentElement;

    if (
      !AUTO_LAZY_SOURCE_EXTENSIONS.has(extension) ||
      url.origin !== window.location.origin ||
      !parent ||
      parent.tagName.toLowerCase() !== "p" ||
      parent.children.length !== 1
    ) {
      return false;
    }

    return Array.from(parent.childNodes).every(
      (node) => node === link || (node.nodeType === Node.TEXT_NODE && !node.textContent.trim()),
    );
  }

  function isLazySourceLink(link) {
    return link.classList.contains("aibook-source-link") || isAutoLazySourceLink(link);
  }

  function addSourceSummaryMetadata(details, summary, label) {
    const source = details.dataset.source;
    const language = details.dataset.language || inferLanguageFromUrl(source);
    details.dataset.language = language;
    details.classList.add("aibook-lazy-source--with-meta");

    const title = document.createElement("span");
    title.className = "aibook-lazy-source__title";

    const sourceLabel = document.createElement("span");
    sourceLabel.className = "aibook-lazy-source__label";
    sourceLabel.textContent = label || "원문 보기";

    const filename = document.createElement("span");
    filename.className = "aibook-lazy-source__filename";
    filename.textContent = `파일명: ${filenameFromUrl(source)}`;

    const meta = document.createElement("span");
    meta.className = "aibook-lazy-source__meta";
    meta.textContent = `유형: ${language}`;

    title.append(sourceLabel, filename);
    summary.replaceChildren(title, meta);
  }

  function appendToken(parent, text, tokenType) {
    if (!text) {
      return;
    }
    if (!tokenType) {
      parent.appendChild(document.createTextNode(text));
      return;
    }

    const span = document.createElement("span");
    span.className = `aibook-lazy-source__token aibook-lazy-source__token--${tokenType}`;
    span.textContent = text;
    parent.appendChild(span);
  }

  function tokenTypeForPython(match) {
    if (match.startsWith("#")) {
      return "comment";
    }
    if (match.startsWith("@")) {
      return "decorator";
    }
    if (/^["']/.test(match) || /^[rubfRUBF]{0,2}["']/.test(match)) {
      return "string";
    }
    if (/^\d/.test(match)) {
      return "number";
    }
    if (/^(False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)$/.test(match)) {
      return "keyword";
    }
    return "name";
  }

  function highlightPython(code, source) {
    const tokenPattern =
      /("""[\s\S]*?"""|'''[\s\S]*?'''|[rRuUbBfF]{0,2}"(?:\\.|[^"\\])*"|[rRuUbBfF]{0,2}'(?:\\.|[^'\\])*'|#[^\n]*|@[A-Za-z_][\w.]*|\b(?:False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b|\b(?:abs|bool|dict|enumerate|float|int|len|list|open|print|range|set|str|sum|tuple|zip)\b|\b\d+(?:\.\d+)?\b)/g;
    let cursor = 0;
    let match = tokenPattern.exec(source);
    while (match) {
      appendToken(code, source.slice(cursor, match.index));
      appendToken(code, match[0], tokenTypeForPython(match[0]));
      cursor = match.index + match[0].length;
      match = tokenPattern.exec(source);
    }
    appendToken(code, source.slice(cursor));
  }

  function highlightSource(code, source, language) {
    if (language === "python") {
      highlightPython(code, source);
      return;
    }
    code.textContent = source;
  }

  function renderSource(target, source, language) {
    const code = document.createElement("code");
    code.className = `language-${language || "text"}`;
    highlightSource(code, source, language || "text");

    const pre = document.createElement("pre");
    pre.className = "aibook-lazy-source__code";
    pre.appendChild(code);
    target.replaceChildren(pre);
  }

  async function loadSource(details) {
    const target = details.querySelector(".aibook-lazy-source__body");
    if (!target || details.dataset.loaded === "true" || details.dataset.loading === "true") {
      return;
    }

    details.dataset.loading = "true";
    target.textContent = "원문을 불러오는 중입니다.";
    try {
      const response = await fetch(details.dataset.source);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      renderSource(target, await response.text(), details.dataset.language);
      details.dataset.loaded = "true";
    } catch (error) {
      target.textContent = `원문을 불러오지 못했습니다: ${error.message}`;
    } finally {
      delete details.dataset.loading;
    }
  }

  function createLazySourceDetails(link) {
    const details = document.createElement("details");
    details.className = "aibook-lazy-source aibook-lazy-source--from-link";
    details.dataset.source = link.href;
    details.dataset.language = link.dataset.language || inferLanguageFromUrl(link.href);

    const summary = document.createElement("summary");
    addSourceSummaryMetadata(details, summary, link.textContent.trim());

    const body = document.createElement("div");
    body.className = "aibook-lazy-source__body";
    body.textContent = "펼치면 원문을 불러옵니다.";

    details.append(summary, body);
    details.addEventListener("toggle", () => {
      if (details.open) {
        loadSource(details);
      }
    });
    return details;
  }

  function panelInsertionTarget(link) {
    const parent = link.parentElement;
    if (parent && parent.children.length === 1 && parent.tagName.toLowerCase() === "p") {
      return parent;
    }
    return link;
  }

  function initSourceLinks() {
    document.querySelectorAll("a[href]").forEach((link) => {
      if (!isLazySourceLink(link)) {
        return;
      }
      if (link.dataset.lazySourceReady === "true") {
        return;
      }
      link.dataset.lazySourceReady = "true";
      panelInsertionTarget(link).replaceWith(createLazySourceDetails(link));
    });
  }

  function initLazySources() {
    document.querySelectorAll("details.aibook-lazy-source[data-source]").forEach((details) => {
      if (details.dataset.lazySourceReady === "true") {
        return;
      }
      details.dataset.lazySourceReady = "true";
      const summary = details.querySelector(":scope > summary");
      if (summary) {
        addSourceSummaryMetadata(details, summary, summary.textContent.trim());
      }
      details.addEventListener("toggle", () => {
        if (details.open) {
          loadSource(details);
        }
      });
    });
    initSourceLinks();
  }

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(initLazySources);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initLazySources);
  } else {
    initLazySources();
  }
})();
