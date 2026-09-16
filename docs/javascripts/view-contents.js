(function () {
  const PREVIEW_ROWS = 12;
  let contentsId = 0;
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

  function appendToken(parent, text, tokenType) {
    if (!text) {
      return;
    }
    if (!tokenType) {
      parent.appendChild(document.createTextNode(text));
      return;
    }

    const span = document.createElement("span");
    span.className = `aibook-view-contents__token aibook-view-contents__token--${tokenType}`;
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

  function highlightJson(code, source) {
    const pattern = /"(?:\\.|[^"\\])*"|-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?|\b(?:true|false|null)\b/g;
    let cursor = 0;
    for (const match of source.matchAll(pattern)) {
      appendToken(code, source.slice(cursor, match.index));
      const value = match[0];
      const end = match.index + value.length;
      const type = value.startsWith('"')
        ? (/^\s*:/.test(source.slice(end)) ? "key" : "string")
        : (/^-?\d/.test(value) ? "number" : "keyword");
      appendToken(code, value, type);
      cursor = end;
    }
    appendToken(code, source.slice(cursor));
  }

  function highlightSource(code, source, language) {
    if (language === "python") {
      highlightPython(code, source);
      return;
    }
    if (language === "json") {
      highlightJson(code, source);
      return;
    }
    code.textContent = source;
  }

  function renderSource(source, language) {
    const code = document.createElement("code");
    code.className = `language-${language || "text"}`;
    highlightSource(code, source, language || "text");

    const pre = document.createElement("pre");
    pre.className = "aibook-view-contents__code";
    pre.appendChild(code);
    const wrapper = document.createElement("div");
    wrapper.className = "aibook-view-contents__source-block";
    const tag = document.createElement("span");
    tag.className = "aibook-code-language";
    const names = { python: "Python", json: "JSON", javascript: "JavaScript", typescript: "TypeScript" };
    tag.textContent = names[language] || language || "Text";
    wrapper.appendChild(tag);
    wrapper.appendChild(pre);
    return wrapper;
  }



  function parseCsv(text) {
    text = text.replace(/^\uFEFF/, "");
    const rows = [];
    let row = [];
    let cell = "";
    let inQuotes = false;

    for (let index = 0; index < text.length; index += 1) {
      const char = text[index];
      const next = text[index + 1];

      if (inQuotes) {
        if (char === '"' && next === '"') {
          cell += '"';
          index += 1;
        } else if (char === '"') {
          inQuotes = false;
        } else {
          cell += char;
        }
        continue;
      }

      if (char === '"') {
        inQuotes = true;
      } else if (char === ",") {
        row.push(cell);
        cell = "";
      } else if (char === "\n") {
        row.push(cell);
        rows.push(row);
        row = [];
        cell = "";
      } else if (char !== "\r") {
        cell += char;
      }
    }

    if (cell.length > 0 || row.length > 0) {
      row.push(cell);
      rows.push(row);
    }

    return rows.filter((cells) => cells.some((value) => value.trim() !== ""));
  }

  function createCell(tagName, value) {
    const cell = document.createElement(tagName);
    cell.textContent = value;
    return cell;
  }

  function renderTable(rows, sourceUrl) {
    const wrapper = document.createElement("div");
    wrapper.className = "aibook-view-contents__body";

    if (rows.length === 0) {
      wrapper.textContent = "표시할 CSV 행이 없습니다.";
      return wrapper;
    }

    const header = rows[0];
    const bodyRows = rows.slice(1, PREVIEW_ROWS + 1);
    const columnCount = rows.reduce((count, row) => Math.max(count, row.length), 0);

    const meta = document.createElement("span");
    meta.className = "aibook-view-contents__meta";
    meta.textContent = `앞 ${bodyRows.length}개 데이터 행을 표시합니다. 다운로드와 복사는 전체 CSV 원본을 사용합니다.`;
    wrapper.appendChild(meta);

    const scroll = document.createElement("div");
    scroll.className = "aibook-view-contents__table-wrap";
    scroll.tabIndex = 0;
    scroll.setAttribute("role", "region");
    scroll.setAttribute("aria-label", "CSV 표 — 가로로 스크롤하여 나머지 열 보기");

    const table = document.createElement("table");
    table.className = "aibook-view-contents__table";

    const thead = document.createElement("thead");
    const headRow = document.createElement("tr");
    for (let index = 0; index < columnCount; index += 1) {
      headRow.appendChild(createCell("th", header[index] || ""));
    }
    thead.appendChild(headRow);
    table.appendChild(thead);

    const tbody = document.createElement("tbody");
    for (const row of bodyRows) {
      const tr = document.createElement("tr");
      for (let index = 0; index < columnCount; index += 1) {
        tr.appendChild(createCell("td", row[index] || ""));
      }
      tbody.appendChild(tr);
    }
    table.appendChild(tbody);

    scroll.appendChild(table);
    wrapper.appendChild(scroll);

    const source = document.createElement("p");
    source.className = "aibook-view-contents__source";
    source.textContent = `미리보기 기준 파일: ${sourceUrl}`;
    wrapper.appendChild(source);

    return wrapper;
  }

  function fileTypeTag(language) {
    const tag = document.createElement("span");
    tag.className = "aibook-view-contents__file-type";
    const names = { python: "Python", json: "JSON", csv: "CSV", markdown: "Markdown" };
    tag.textContent = names[language] || language;
    return tag;
  }

  function attachViewContents(link, language) {
    if (link.dataset.viewContentsReady === "true") {
      return;
    }
    link.dataset.viewContentsReady = "true";
    const sourceUrl = link.href;
    const container = link.closest("p, li, td, th, blockquote");

    const button = document.createElement("button");
    button.className = "aibook-view-contents__toggle";
    button.type = "button";
    button.append(fileTypeTag(language), document.createTextNode(" "));
    while (link.firstChild) button.appendChild(link.firstChild);
    const label = document.createElement("span");
    label.className = "aibook-view-contents__action-tag";
    label.textContent = "내용보기";
    button.appendChild(label);
    button.setAttribute("aria-expanded", "false");

    const panel = document.createElement("div");
    panel.className = "aibook-view-contents__panel";
    panel.hidden = true;
    panel.id = `aibook-view-contents-${++contentsId}`;
    button.setAttribute("aria-controls", panel.id);
    let loading = false;

    const status = document.createElement("div");
    status.className = "aibook-view-contents__status";
    status.textContent = "파일 내용을 불러오지 않았습니다.";
    panel.appendChild(status);
    const actions = document.createElement("span");
    actions.className = "aibook-view-contents__actions";
    const download = document.createElement("button");
    download.type = "button";
    download.className = "aibook-view-contents__download";
    download.setAttribute("aria-label", "다운로드");
    download.setAttribute("title", "다운로드");
    download.disabled = true;
    const copy = document.createElement("button");
    copy.type = "button";
    copy.className = "aibook-view-contents__copy";
    copy.setAttribute("aria-label", "클립보드 복사");
    copy.setAttribute("title", "클립보드 복사");
    copy.disabled = true;
    const feedback = document.createElement("span");
    feedback.setAttribute("role", "status");
    actions.appendChild(download);
    actions.appendChild(copy);
    panel.appendChild(feedback);
    panel.appendChild(actions);
    let sourceText = "";
    download.addEventListener("click", () => {
      const url = URL.createObjectURL(new Blob([sourceText], { type: language === "csv" ? "text/csv;charset=utf-8" : "text/plain;charset=utf-8" }));
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = new URL(sourceUrl).pathname.split("/").pop();
      document.body.appendChild(anchor);
      anchor.click();
      anchor.remove();
      setTimeout(() => URL.revokeObjectURL(url), 60000);
    });
    copy.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(sourceText);
        feedback.textContent = "전체 파일 내용을 복사했습니다.";
      } catch (_) {
        feedback.textContent = "클립보드에 복사하지 못했습니다. 브라우저 권한을 확인하거나 다운로드를 이용하세요.";
      }
    });

    button.addEventListener("click", async () => {
      const willOpen = panel.hidden;
      panel.hidden = !willOpen;
      label.textContent = willOpen ? "내용닫기" : "내용보기";
      button.setAttribute("aria-expanded", String(willOpen));

      if (!willOpen || button.dataset.loaded === "true" || loading) {
        return;
      }

      loading = true;
      panel.setAttribute("aria-busy", "true");
      status.textContent = "파일 내용을 불러오는 중입니다.";

      try {
        const response = await fetch(sourceUrl);
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const text = await response.text();
        sourceText = text;
        const content = language === "csv"
          ? renderTable(parseCsv(text), sourceUrl)
          : renderSource(text, language);
        panel.replaceChild(content, status);
        panel.removeChild(actions);
        let header = content.firstChild;
        if (language === "csv") {
          header = document.createElement("span");
          header.className = "aibook-code-language";
          header.textContent = "CSV";
          const meta = content.querySelector(".aibook-view-contents__meta");
          if (meta) {
            content.removeChild(meta);
            header.appendChild(meta);
          }
          content.insertBefore(header, content.firstChild);
        }
        header.appendChild(actions);
        button.dataset.loaded = "true";
        download.disabled = false;
        copy.disabled = false;
      } catch (error) {
        status.textContent = `파일 내용을 불러오지 못했습니다: ${error.message}. 닫았다 다시 열면 재시도합니다.`;
      } finally {
        loading = false;
        panel.setAttribute("aria-busy", "false");
      }
    });

    link.replaceWith(button);
    // Keep the entire surrounding paragraph/list sentence ahead of the preview.
    if (container && container.tagName === "P") {
      container.insertAdjacentElement("afterend", panel);
    } else if (container) {
      container.appendChild(panel);
    } else {
      button.insertAdjacentElement("afterend", panel);
    }
  }

  function attachMarkdownContents(link) {
    if (link.dataset.viewContentsReady === "true") return;
    link.dataset.viewContentsReady = "true";
    const sourceUrl = link.href;
    const container = link.closest("p, li, td, th, blockquote");
    const button = document.createElement("button");
    button.type = "button";
    button.className = "aibook-view-contents__toggle";
    const title = link.textContent;
    const label = document.createElement("span");
    label.className = "aibook-view-contents__action-tag";
    label.textContent = "내용보기";
    button.append(fileTypeTag("markdown"), document.createTextNode(` ${title} `), label);
    button.setAttribute("aria-expanded", "false");
    const panel = document.createElement("div");
    panel.className = "aibook-view-contents__panel";
    panel.id = `aibook-view-contents-${++contentsId}`;
    panel.hidden = true;
    button.setAttribute("aria-controls", panel.id);
    const toolbar = document.createElement("div");
    toolbar.className = "aibook-view-contents__markdown-tools";
    const original = document.createElement("a");
    original.href = sourceUrl;
    original.textContent = "문서 열기";
    const refresh = document.createElement("button");
    refresh.type = "button";
    refresh.textContent = "새로고침";
    toolbar.append(original, refresh);
    const body = document.createElement("div");
    body.className = "aibook-view-contents__markdown";
    body.setAttribute("role", "region");
    body.setAttribute("aria-label", title);
    body.tabIndex = 0;
    panel.append(toolbar, body);
    let loaded = false;
    let loading = false;

    async function load() {
      if (loading) return;
      loading = true;
      refresh.disabled = true;
      panel.setAttribute("aria-busy", "true");
      body.textContent = "문서 내용을 불러오는 중입니다.";
      try {
        const response = await fetch(sourceUrl, { cache: "no-cache" });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        if (new URL(response.url).origin !== location.origin) throw new Error("외부 문서는 미리볼 수 없습니다");
        const parsed = new DOMParser().parseFromString(await response.text(), "text/html");
        const article = parsed.querySelector(".md-content__inner");
        if (!article) throw new Error("문서 본문을 찾지 못했습니다");
        article.querySelectorAll("script, style, link, iframe, object, embed, form, .md-content__button, .headerlink").forEach((node) => node.remove());
        article.querySelectorAll("*").forEach((node) => {
          for (const attr of [...node.attributes]) {
            if (/^on/i.test(attr.name) || ["srcdoc", "srcset", "style"].includes(attr.name)) node.removeAttribute(attr.name);
          }
          if (node.id) node.id = `${panel.id}-${node.id}`;
          for (const attr of ["href", "src"]) {
            if (!node.hasAttribute(attr)) continue;
            const value = node.getAttribute(attr);
            if (attr === "href" && value.startsWith("#")) {
              node.setAttribute(attr, `#${panel.id}-${value.slice(1)}`);
              continue;
            }
            const url = new URL(value, response.url);
            if (!["http:", "https:"].includes(url.protocol)) node.removeAttribute(attr);
            else node.setAttribute(attr, url.href);
          }
        });
        body.replaceChildren(...article.childNodes);
        loaded = true;
        document.dispatchEvent(new Event("aibook:content-loaded"));
      } catch (error) {
        loaded = false;
        body.textContent = `문서를 불러오지 못했습니다: ${error.message}. 새로고침으로 재시도할 수 있습니다.`;
      } finally {
        loading = false;
        refresh.disabled = false;
        panel.setAttribute("aria-busy", "false");
      }
    }
    refresh.addEventListener("click", load);
    button.addEventListener("click", () => {
      panel.hidden = !panel.hidden;
      label.textContent = panel.hidden ? "내용보기" : "내용닫기";
      button.setAttribute("aria-expanded", String(!panel.hidden));
      if (!panel.hidden && !loaded) load();
    });
    link.replaceWith(button);
    if (container?.tagName === "P") container.insertAdjacentElement("afterend", panel);
    else if (container) container.appendChild(panel);
    else button.insertAdjacentElement("afterend", panel);
  }

  function initViewContents() {
    document.querySelectorAll(".md-content a[href]").forEach((link) => {
      let url;
      try { url = new URL(link.href, document.baseURI); } catch (_) { return; }
      if (!/^https?:$/.test(url.protocol)) return;
      if (link.classList.contains("aibook-markdown-preview") && url.origin === location.origin) {
        attachMarkdownContents(link);
        return;
      }
      const extension = url.pathname.split(".").pop().toLowerCase();
      if (["csv", "py", "json"].includes(extension)) {
        attachViewContents(link, extension === "csv" ? "csv" : link.dataset.language || LANGUAGE_BY_EXTENSION[extension] || "text");
      }
    });
  }

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(initViewContents);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initViewContents);
  } else {
    initViewContents();
  }
})();
