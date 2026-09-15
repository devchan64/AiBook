(function () {
  const PREVIEW_ROWS = 12;
  let previewId = 0;

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
    wrapper.className = "aibook-csv-preview__body";

    if (rows.length === 0) {
      wrapper.textContent = "표시할 CSV 행이 없습니다.";
      return wrapper;
    }

    const header = rows[0];
    const bodyRows = rows.slice(1, PREVIEW_ROWS + 1);
    const columnCount = rows.reduce((count, row) => Math.max(count, row.length), 0);

    const meta = document.createElement("p");
    meta.className = "aibook-csv-preview__meta";
    meta.textContent = `앞 ${bodyRows.length}개 데이터 행을 표시합니다. 전체 원본은 CSV 링크에서 확인합니다.`;
    wrapper.appendChild(meta);

    const scroll = document.createElement("div");
    scroll.className = "aibook-csv-preview__table-wrap";
    scroll.tabIndex = 0;
    scroll.setAttribute("role", "region");
    scroll.setAttribute("aria-label", "CSV 표 — 가로로 스크롤하여 나머지 열 보기");

    const table = document.createElement("table");
    table.className = "aibook-csv-preview__table";

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
    source.className = "aibook-csv-preview__source";
    source.textContent = `미리보기 기준 파일: ${sourceUrl}`;
    wrapper.appendChild(source);

    return wrapper;
  }

  function attachPreview(link) {
    if (link.dataset.csvPreviewReady === "true") {
      return;
    }
    link.dataset.csvPreviewReady = "true";

    const button = document.createElement("button");
    button.className = "aibook-csv-preview__toggle";
    button.type = "button";
    button.textContent = "내용 보기";
    button.setAttribute("aria-expanded", "false");

    const panel = document.createElement("div");
    panel.className = "aibook-csv-preview__panel";
    panel.hidden = true;
    panel.id = `aibook-csv-preview-${++previewId}`;
    button.setAttribute("aria-controls", panel.id);
    let loading = false;

    const status = document.createElement("div");
    status.className = "aibook-csv-preview__status";
    status.textContent = "CSV 내용을 불러오지 않았습니다.";
    panel.appendChild(status);

    button.addEventListener("click", async () => {
      const willOpen = panel.hidden;
      panel.hidden = !willOpen;
      button.textContent = willOpen ? "내용 닫기" : "내용 보기";
      button.setAttribute("aria-expanded", String(willOpen));

      if (!willOpen || button.dataset.loaded === "true" || loading) {
        return;
      }

      loading = true;
      panel.setAttribute("aria-busy", "true");
      status.textContent = "CSV 내용을 불러오는 중입니다.";

      try {
        const response = await fetch(link.href);
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const text = await response.text();
        const rows = parseCsv(text);
        panel.replaceChild(renderTable(rows, link.getAttribute("href") || link.href), status);
        button.dataset.loaded = "true";
      } catch (error) {
        status.textContent = `CSV 내용을 불러오지 못했습니다: ${error.message}. 닫았다 다시 열면 재시도합니다.`;
      } finally {
        loading = false;
        panel.setAttribute("aria-busy", "false");
      }
    });

    link.insertAdjacentElement("afterend", button);
    button.insertAdjacentElement("afterend", panel);
  }

  function initCsvPreviews() {
    document.querySelectorAll("a.csv-preview[href]").forEach((link) => {
      const url = new URL(link.href, document.baseURI);
      if (/\.csv$/i.test(url.pathname) && /^(https?:)$/.test(url.protocol)) {
        attachPreview(link);
      }
    });
  }

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(initCsvPreviews);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initCsvPreviews);
  } else {
    initCsvPreviews();
  }
})();
