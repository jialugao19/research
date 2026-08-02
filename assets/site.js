(() => {
  const search = document.querySelector("#report-search");
  const project = document.querySelector("#project-filter");
  const cards = [...document.querySelectorAll("#report-catalog .catalog-card")];
  const empty = document.querySelector("#no-results");
  if (!search || !project || !cards.length || !empty) return;

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
})();
