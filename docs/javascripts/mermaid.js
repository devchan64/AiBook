(function () {
  function renderMermaid() {
    if (!window.mermaid) {
      return;
    }

    window.mermaid.run({
      nodes: document.querySelectorAll(".mermaid:not([data-processed])"),
    });
  }

  if (window.mermaid) {
    window.mermaid.initialize({ startOnLoad: false });
  }

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(renderMermaid);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderMermaid);
  } else {
    renderMermaid();
  }
})();
