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

  function renderSource(target, source, language) {
    const code = document.createElement("code");
    code.className = `language-${language || "text"}`;
    code.textContent = source;

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
    const title = document.createElement("span");
    title.className = "aibook-lazy-source__title";

    const label = document.createElement("span");
    label.className = "aibook-lazy-source__label";
    label.textContent = link.textContent.trim() || "원문 보기";

    const filename = document.createElement("span");
    filename.className = "aibook-lazy-source__filename";
    filename.textContent = `파일: ${filenameFromUrl(link.href)}`;

    const meta = document.createElement("span");
    meta.className = "aibook-lazy-source__meta";
    meta.textContent = details.dataset.language;

    title.append(label, filename);
    summary.append(title, meta);

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
    document.querySelectorAll("a.aibook-source-link[href]").forEach((link) => {
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
