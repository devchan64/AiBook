(function () {
  const names = {
    py: "Python", python: "Python", json: "JSON", js: "JavaScript",
    javascript: "JavaScript", ts: "TypeScript", typescript: "TypeScript",
    sh: "Shell", shell: "Shell", bash: "Bash", console: "Console",
    html: "HTML", css: "CSS", sql: "SQL", yaml: "YAML", yml: "YAML",
    xml: "XML", csv: "CSV", text: "Text", txt: "Text", markdown: "Markdown",
  };

  function initCodeTags() {
    document.querySelectorAll(".md-content div.highlight, .md-content pre").forEach((block) => {
      // Line-number gutters and diagram source are not separate code blocks.
      if (block.dataset.codeTagReady === "true" ||
          block.closest(".mermaid, .aibook-view-contents__source-block") ||
          (block.tagName === "PRE" && block.closest(".highlight"))) return;
      const code = block.querySelector("code");
      if (!code) return;
      const classes = `${block.className} ${code.className}`;
      const language = (classes.match(/\blanguage-([\w+-]+)/) || [])[1] || "text";
      const tag = document.createElement("span");
      tag.className = "aibook-code-language";
      tag.textContent = names[language.toLowerCase()] || language;
      // Keep the label outside pre/code so copying code never includes the tag.
      if (block.tagName === "PRE") block.insertAdjacentElement("beforebegin", tag);
      else block.insertBefore(tag, block.firstChild);
      block.dataset.codeTagReady = "true";
    });
  }

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(initCodeTags);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initCodeTags);
  } else {
    initCodeTags();
  }
})();
