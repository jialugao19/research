(() => {
  const header = document.querySelector("[data-auto-hide]");
  if (header) {
    let lastY = window.scrollY;
    let ticking = false;
    const updateHeader = () => {
      const currentY = Math.max(window.scrollY, 0);
      const navigationOpen = Boolean(
        document.querySelector(".mobile-navigation[open], .mobile-toc-navigation[open]"),
      );
      if (navigationOpen || currentY < 48 || currentY < lastY - 6) {
        header.classList.remove("is-hidden");
      } else if (currentY > lastY + 4 && currentY > 120) {
        header.classList.add("is-hidden");
      }
      lastY = currentY;
      ticking = false;
    };
    window.addEventListener(
      "scroll",
      () => {
        if (!ticking) {
          window.requestAnimationFrame(updateHeader);
          ticking = true;
        }
      },
      { passive: true },
    );
  }

  const sidebarGroups = [...document.querySelectorAll(".sidebar-group")];
  for (const group of sidebarGroups) {
    group.addEventListener("toggle", () => {
      if (!group.open) return;
      const navigation = group.closest(".sidebar-nav");
      for (const sibling of navigation?.querySelectorAll(".sidebar-group[open]") || []) {
        if (sibling !== group) sibling.open = false;
      }
    });
  }

  const tocLinks = [
    ...document.querySelectorAll(
      '.doc-toc a[href^="#"], .mobile-toc-navigation a[href^="#"]',
    ),
  ];
  const tocTargetIds = [
    ...new Set(
      tocLinks.map((link) => decodeURIComponent((link.getAttribute("href") || "").slice(1))),
    ),
  ];
  const tocTargets = tocTargetIds
    .map((targetId) => document.getElementById(targetId))
    .filter(Boolean);
  if (tocLinks.length && tocTargets.length) {
    let tocTicking = false;
    const updateToc = () => {
      const activationY = window.scrollY + Math.min(window.innerHeight * 0.24, 180);
      let current = tocTargets[0];
      for (const target of tocTargets) {
        if (target.getBoundingClientRect().top + window.scrollY <= activationY) current = target;
      }
      for (const link of tocLinks) {
        const targetId = decodeURIComponent((link.getAttribute("href") || "").slice(1));
        const active = targetId === current.id;
        link.classList.toggle("is-current", active);
        if (active) link.setAttribute("aria-current", "location");
        else link.removeAttribute("aria-current");
      }
      tocTicking = false;
    };
    const requestTocUpdate = () => {
      if (!tocTicking) {
        window.requestAnimationFrame(updateToc);
        tocTicking = true;
      }
    };
    window.addEventListener("scroll", requestTocUpdate, { passive: true });
    window.addEventListener("resize", requestTocUpdate);
    updateToc();
  }

  for (const heading of document.querySelectorAll("main h2, main h3")) {
    if (heading.querySelector(".heading-anchor")) continue;
    const anchorTarget = heading.id ? heading : heading.closest("section[id]");
    if (!anchorTarget?.id) continue;
    const anchor = document.createElement("a");
    anchor.className = "heading-anchor";
    anchor.href = `#${anchorTarget.id}`;
    anchor.textContent = "#";
    anchor.setAttribute("aria-label", `Open section anchor for “${heading.textContent.trim()}”`);
    heading.append(anchor);
  }

  const reportImages = [...document.querySelectorAll(".report-figure img")];
  if (reportImages.length && typeof HTMLDialogElement !== "undefined") {
    const lightbox = document.createElement("dialog");
    lightbox.className = "image-lightbox";
    lightbox.innerHTML =
      '<button type="button" class="lightbox-close" aria-label="Close enlarged image">CLOSE</button>' +
      '<img alt=""><p class="lightbox-caption"></p>';
    document.body.append(lightbox);
    const enlarged = lightbox.querySelector("img");
    const caption = lightbox.querySelector(".lightbox-caption");
    let trigger = null;
    const close = () => lightbox.close();
    const open = (image) => {
      trigger = image;
      enlarged.src = image.currentSrc || image.src;
      enlarged.alt = image.alt;
      caption.textContent = image.closest("figure")?.querySelector("figcaption")?.textContent || image.alt;
      lightbox.showModal();
      document.documentElement.classList.add("lightbox-open");
    };
    lightbox.querySelector(".lightbox-close").addEventListener("click", close);
    lightbox.addEventListener("click", (event) => {
      if (event.target === lightbox) close();
    });
    lightbox.addEventListener("close", () => {
      document.documentElement.classList.remove("lightbox-open");
      enlarged.removeAttribute("src");
      trigger?.focus();
    });
    for (const image of reportImages) {
      image.tabIndex = 0;
      image.setAttribute("role", "button");
      image.setAttribute("aria-label", `${image.alt}; open enlarged image`);
      image.addEventListener("click", () => open(image));
      image.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          open(image);
        }
      });
    }
  }

  const search = document.querySelector("#report-search");
  const project = document.querySelector("#project-filter");
  const cards = [...document.querySelectorAll("#report-catalog .catalog-card")];
  const empty = document.querySelector("#no-results");
  if (search && project && cards.length && empty) {
    const filter = () => {
      const query = search.value.trim().toLowerCase();
      const projectId = project.value;
      let visible = 0;
      for (const card of cards) {
        const matchesText = !query || (card.dataset.search || "").includes(query);
        const matchesProject = !projectId || card.dataset.project === projectId;
        const show = matchesText && matchesProject;
        card.hidden = !show;
        if (show) visible += 1;
      }
      empty.hidden = visible !== 0;
    };
    search.addEventListener("input", filter);
    project.addEventListener("change", filter);
  }

  const knowledgeSearch = document.querySelector("[data-knowledge-search]");
  const knowledgeDomain = document.querySelector("[data-knowledge-domain]");
  const knowledgeItems = [...document.querySelectorAll("[data-knowledge-item]")];
  const knowledgeCount = document.querySelector("[data-knowledge-count]");
  const knowledgeEmpty = document.querySelector("[data-knowledge-empty]");
  if (knowledgeItems.length && (knowledgeSearch || knowledgeDomain)) {
    const requestedDomain = new URLSearchParams(window.location.search).get("domain") || "";
    if (knowledgeDomain && [...knowledgeDomain.options].some((option) => option.value === requestedDomain)) {
      knowledgeDomain.value = requestedDomain;
    }
    const filterKnowledge = () => {
      const query = (knowledgeSearch?.value || "").trim().toLocaleLowerCase();
      const domain = knowledgeDomain?.value || "";
      let visible = 0;
      for (const item of knowledgeItems) {
        const haystack = (item.dataset.search || "").toLocaleLowerCase();
        const show = (!query || haystack.includes(query)) && (!domain || item.dataset.domain === domain);
        item.hidden = !show;
        if (show) visible += 1;
      }
      if (knowledgeCount) knowledgeCount.textContent = String(visible);
      if (knowledgeEmpty) knowledgeEmpty.hidden = visible !== 0;
    };
    knowledgeSearch?.addEventListener("input", filterKnowledge);
    knowledgeDomain?.addEventListener("change", filterKnowledge);
    filterKnowledge();
  }
})();
