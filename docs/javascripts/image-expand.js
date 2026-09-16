(function () {
  const DIALOG_ID = "aibook-image-dialog";

  function dialog() {
    let element = document.getElementById(DIALOG_ID);
    if (element) {
      return element;
    }

    element = document.createElement("dialog");
    element.className = "aibook-image-dialog";
    element.id = DIALOG_ID;
    element.innerHTML = [
      '<button class="aibook-image-dialog__close" type="button" aria-label="확대 이미지 닫기">×</button>',
      '<figure class="aibook-image-dialog__figure"><img class="aibook-image-dialog__image" alt=""></figure>',
    ].join("");
    element.querySelector(".aibook-image-dialog__close").addEventListener("click", () => element.close());
    element.addEventListener("click", (event) => {
      if (event.target === element) {
        element.close();
      }
    });
    document.body.appendChild(element);
    return element;
  }

  function openImage(image) {
    if (!(image.currentSrc || image.src)) {
      return;
    }

    const viewer = dialog();
    const expanded = viewer.querySelector(".aibook-image-dialog__image");
    expanded.src = image.currentSrc || image.src;
    expanded.alt = image.alt;
    viewer.showModal();
  }

  function isExpandable(image) {
    return image.closest(".md-typeset") && (image.currentSrc || image.src);
  }

  function markExpandableImages() {
    document.querySelectorAll(".md-typeset img").forEach((image) => {
      if (!isExpandable(image)) {
        return;
      }
      image.dataset.aibookExpandable = "true";
      const control = image.closest("a") || image;
      control.tabIndex = 0;
      control.setAttribute("role", "button");
      control.setAttribute("aria-haspopup", "dialog");
      control.setAttribute("aria-label", `${image.alt || "이미지"} 확대해서 보기`);
    });
  }

  function eventImage(target) {
    if (!(target instanceof Element)) {
      return null;
    }
    return target.closest(".md-typeset img[data-aibook-expandable='true']") ||
      target.closest(".md-typeset a")?.querySelector("img[data-aibook-expandable='true']");
  }

  document.addEventListener("click", (event) => {
    const image = eventImage(event.target);
    if (image) {
      event.preventDefault();
      event.stopPropagation();
      openImage(image);
    }
  }, true);

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Enter" && event.key !== " ") {
      return;
    }
    const image = eventImage(event.target);
    if (image) {
      event.preventDefault();
      event.stopPropagation();
      openImage(image);
    }
  }, true);

  document.addEventListener("aibook:content-loaded", markExpandableImages);

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(markExpandableImages);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", markExpandableImages);
  } else {
    markExpandableImages();
  }
})();
