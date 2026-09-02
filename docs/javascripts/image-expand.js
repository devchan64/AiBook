(function () {
  const DESKTOP_QUERY = window.matchMedia("(min-width: 45em)");
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
    if (!DESKTOP_QUERY.matches || !image.currentSrc) {
      return;
    }

    const viewer = dialog();
    const expanded = viewer.querySelector(".aibook-image-dialog__image");
    expanded.src = image.currentSrc;
    expanded.alt = image.alt;
    viewer.showModal();
  }

  function isExpandable(image) {
    return image.closest(".md-typeset") && !image.closest("a") && image.currentSrc;
  }

  function markExpandableImages() {
    document.querySelectorAll(".md-typeset img").forEach((image) => {
      if (!isExpandable(image)) {
        return;
      }
      image.dataset.aibookExpandable = "true";
      image.tabIndex = 0;
      image.setAttribute("role", "button");
      image.setAttribute("aria-label", `${image.alt || "이미지"} 확대해서 보기`);
    });
  }

  document.addEventListener("click", (event) => {
    const image = event.target.closest(".md-typeset img[data-aibook-expandable='true']");
    if (image) {
      openImage(image);
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Enter" && event.key !== " ") {
      return;
    }
    const image = event.target.closest(".md-typeset img[data-aibook-expandable='true']");
    if (image) {
      event.preventDefault();
      openImage(image);
    }
  });

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(markExpandableImages);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", markExpandableImages);
  } else {
    markExpandableImages();
  }
})();
