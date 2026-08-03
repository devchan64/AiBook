(function () {
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
  }

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(initLazySources);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initLazySources);
  } else {
    initLazySources();
  }
})();
