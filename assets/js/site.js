(() => {
  const body = document.body;
  const drawer = document.querySelector("[data-drawer]");
  const openButton = document.querySelector("[data-menu-open]");
  const closeButtons = document.querySelectorAll("[data-menu-close]");
  const drawerPanel = drawer?.querySelector(".drawer-panel");
  let lastFocusedElement = null;

  const getFocusableElements = () =>
    drawerPanel
      ? [
          ...drawerPanel.querySelectorAll(
            'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])',
          ),
        ]
      : [];

  const setDrawer = (open) => {
    if (!drawer || !openButton) return;
    if (open) {
      lastFocusedElement = document.activeElement;
    }
    drawer.classList.toggle("is-open", open);
    drawer.setAttribute("aria-hidden", String(!open));
    openButton.setAttribute("aria-expanded", String(open));
    body.classList.toggle("menu-open", open);
    if (open) {
      getFocusableElements()[0]?.focus();
    } else {
      (lastFocusedElement instanceof HTMLElement
        ? lastFocusedElement
        : openButton
      ).focus();
    }
  };

  openButton?.addEventListener("click", () => setDrawer(true));
  closeButtons.forEach((button) =>
    button.addEventListener("click", () => setDrawer(false)),
  );

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && drawer?.classList.contains("is-open")) {
      setDrawer(false);
    }

    if (
      event.key === "Tab" &&
      drawer?.classList.contains("is-open") &&
      drawerPanel
    ) {
      const focusable = getFocusableElements();
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (!first || !last) return;

      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }
  });

  drawerPanel
    ?.querySelectorAll("a")
    .forEach((link) => link.addEventListener("click", () => setDrawer(false)));

  const directoryInput = document.querySelector("[data-directory-search]");
  const directoryItems = [...document.querySelectorAll("[data-directory-item]")];
  const directoryCount = document.querySelector("[data-directory-count]");
  const directoryFilters = [...document.querySelectorAll("[data-directory-filter]")];
  let activeDirectoryFilter = "all";

  const filterDirectory = () => {
    const query = directoryInput.value.trim().toLocaleLowerCase();
    let visible = 0;
    directoryItems.forEach((item) => {
      const haystack = item.dataset.search.toLocaleLowerCase();
      const categories = (item.dataset.category || "").split(/\s+/);
      const matchesQuery = !query || haystack.includes(query);
      const matchesCategory = activeDirectoryFilter === "all" || categories.includes(activeDirectoryFilter);
      const match = matchesQuery && matchesCategory;
      item.hidden = !match;
      if (match) visible += 1;
    });
    if (directoryCount) {
      directoryCount.textContent = `显示 ${visible} 个入口`;
    }
  };

  directoryInput?.addEventListener("input", filterDirectory);
  directoryFilters.forEach((button) => {
    button.addEventListener("click", () => {
      activeDirectoryFilter = button.dataset.directoryFilter || "all";
      directoryFilters.forEach((item) => item.classList.toggle("is-active", item === button));
      filterDirectory();
    });
  });
  if (directoryInput) filterDirectory();

  if (window.lucide) {
    window.lucide.createIcons({
      attrs: {
        "aria-hidden": "true",
        "stroke-width": 1.8,
      },
    });
  }
})();
