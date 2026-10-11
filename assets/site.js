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

  const taxonomyToggles = [...document.querySelectorAll("[data-taxonomy-toggle]")];
  const taxonomyLinks = [...document.querySelectorAll("[data-taxonomy-link]")];
  const normalizedPath = (path) => path.replace(/\/index\.html$/, "/");
  const currentPath = normalizedPath(window.location.pathname);
  const taxonomyTarget = (link) => {
    const url = new URL(link.href, window.location.href);
    return normalizedPath(url.pathname) === currentPath ? decodeURIComponent(url.hash.slice(1)) : "";
  };
  const setTaxonomyBranch = (button, expanded) => {
    const branch = document.getElementById(button.getAttribute("aria-controls") || "");
    if (!branch) return;
    button.setAttribute("aria-expanded", String(expanded));
    branch.hidden = !expanded;
  };
  for (const button of taxonomyToggles) {
    button.addEventListener("click", () => {
      setTaxonomyBranch(button, button.getAttribute("aria-expanded") !== "true");
    });
  }
  const openTaxonomyAncestors = (hash) => {
    if (!hash.startsWith("#topic-")) return false;
    const targetId = decodeURIComponent(hash.slice(1));
    const matchingLinks = taxonomyLinks.filter((link) => taxonomyTarget(link) === targetId);
    for (const link of matchingLinks) {
      let branch = link.closest(".sidebar-taxonomy-branch");
      while (branch) {
        const button = branch.previousElementSibling?.querySelector("[data-taxonomy-toggle]");
        if (button) setTaxonomyBranch(button, true);
        branch = branch.parentElement?.closest(".sidebar-taxonomy-branch") || null;
      }
    }
    return matchingLinks.length > 0;
  };
  if (window.location.hash) openTaxonomyAncestors(window.location.hash);
  window.addEventListener("hashchange", () => openTaxonomyAncestors(window.location.hash));
  for (const link of taxonomyLinks) {
    link.addEventListener("click", () => {
      const url = new URL(link.href, window.location.href);
      if (normalizedPath(url.pathname) === currentPath) openTaxonomyAncestors(url.hash);
    });
  }

  const taxonomyTargets = [...document.querySelectorAll(".research-taxonomy-node[id]")];
  if (taxonomyLinks.length && taxonomyTargets.length) {
    let taxonomyTicking = false;
    const updateTaxonomyCurrent = () => {
      const activationY = window.scrollY + Math.min(window.innerHeight * 0.24, 180);
      let current = taxonomyTargets[0];
      for (const target of taxonomyTargets) {
        if (target.getBoundingClientRect().top + window.scrollY <= activationY) current = target;
      }
      for (const link of taxonomyLinks) {
        const active = taxonomyTarget(link) === current.id;
        link.classList.toggle("is-current", active);
        if (active) link.setAttribute("aria-current", "location");
        else link.removeAttribute("aria-current");
      }
      taxonomyTicking = false;
    };
    const requestTaxonomyUpdate = () => {
      if (!taxonomyTicking) {
        window.requestAnimationFrame(updateTaxonomyCurrent);
        taxonomyTicking = true;
      }
    };
    window.addEventListener("scroll", requestTaxonomyUpdate, { passive: true });
    window.addEventListener("resize", requestTaxonomyUpdate);
    updateTaxonomyCurrent();
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
  const stage = document.querySelector("#stage-filter");
  const cards = [...document.querySelectorAll("#report-catalog .publication-row")];
  const empty = document.querySelector("#no-results");
  if (search && project && stage && cards.length && empty) {
    const filter = () => {
      const query = search.value.trim().toLowerCase();
      const projectId = project.value;
      const stageId = stage.value;
      let visible = 0;
      for (const card of cards) {
        const matchesText = !query || (card.dataset.search || "").includes(query);
        const matchesProject = !projectId || card.dataset.project === projectId;
        const matchesStage = !stageId || card.dataset.stage === stageId;
        const show = matchesText && matchesProject && matchesStage;
        card.hidden = !show;
        if (show) visible += 1;
      }
      empty.hidden = visible !== 0;
    };
    search.addEventListener("input", filter);
    project.addEventListener("change", filter);
    stage.addEventListener("change", filter);
  }

  const knowledgeSearch = document.querySelector("[data-knowledge-search]");
  const knowledgeDomain = document.querySelector("[data-knowledge-domain]");
  const knowledgeItems = [...document.querySelectorAll("[data-knowledge-item]")];
  const knowledgeGroups = [...document.querySelectorAll("[data-knowledge-group]")];
  const knowledgeCount = document.querySelector("[data-knowledge-count]");
  const knowledgeEmpty = document.querySelector("[data-knowledge-empty]");
  if (knowledgeItems.length && (knowledgeSearch || knowledgeDomain)) {
    const savedOpenState = new Map();
    let filteringActive = false;
    const requestedDomain = new URLSearchParams(window.location.search).get("domain") || "";
    if (knowledgeDomain && [...knowledgeDomain.options].some((option) => option.value === requestedDomain)) {
      knowledgeDomain.value = requestedDomain;
    }
    const filterKnowledge = () => {
      const query = (knowledgeSearch?.value || "").trim().toLocaleLowerCase();
      const domain = knowledgeDomain?.value || "";
      const nextFilteringActive = Boolean(query || domain);
      if (nextFilteringActive && !filteringActive) {
        for (const group of knowledgeGroups) savedOpenState.set(group, group.open);
      }
      let visible = 0;
      for (const item of knowledgeItems) {
        const haystack = (item.dataset.search || "").toLocaleLowerCase();
        const show = (!query || haystack.includes(query)) && (!domain || item.dataset.domain === domain);
        item.hidden = !show;
        if (show) visible += 1;
      }
      for (const group of knowledgeGroups) {
        const groupItems = [...group.querySelectorAll("[data-knowledge-item]")];
        const groupVisible = groupItems.filter((item) => !item.hidden).length;
        const groupCount = group.querySelector("[data-subtopic-count]");
        group.hidden = groupVisible === 0;
        if (groupCount) groupCount.textContent = String(groupVisible);
        if (nextFilteringActive && groupVisible > 0) group.open = true;
        else if (!nextFilteringActive && filteringActive) {
          group.hidden = false;
          group.open = savedOpenState.get(group) ?? group.open;
        }
      }
      filteringActive = nextFilteringActive;
      if (knowledgeCount) knowledgeCount.textContent = String(visible);
      if (knowledgeEmpty) knowledgeEmpty.hidden = visible !== 0;
    };
    knowledgeSearch?.addEventListener("input", filterKnowledge);
    knowledgeDomain?.addEventListener("change", filterKnowledge);
    filterKnowledge();
  }

  const openSubtopicHash = (hash, scroll) => {
    if (!hash.startsWith("#subtopic-")) return false;
    const target = document.getElementById(decodeURIComponent(hash.slice(1)));
    if (!(target instanceof HTMLDetailsElement)) return false;
    target.open = true;
    if (scroll) window.requestAnimationFrame(() => target.scrollIntoView({ block: "start" }));
    return true;
  };
  if (window.location.hash) openSubtopicHash(window.location.hash, true);
  window.addEventListener("hashchange", () => openSubtopicHash(window.location.hash, true));
  for (const link of document.querySelectorAll('a[href*="#subtopic-"]')) {
    link.addEventListener("click", (event) => {
      const targetUrl = new URL(link.href, window.location.href);
      if (targetUrl.pathname !== window.location.pathname || !openSubtopicHash(targetUrl.hash, true)) return;
      event.preventDefault();
      window.history.pushState(null, "", targetUrl.hash);
    });
  }
})();
