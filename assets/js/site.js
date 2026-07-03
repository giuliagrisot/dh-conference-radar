const searchBox = document.querySelector("#searchBox");
const regionFilter = document.querySelector("#regionFilter");
const statusFilter = document.querySelector("#statusFilter");
const cards = Array.from(document.querySelectorAll(".conference-card"));
const emptyState = document.querySelector("#emptyState");

function applyFilters() {
  const query = searchBox.value.trim().toLowerCase();
  const region = regionFilter.value;
  const status = statusFilter.value;
  let visible = 0;

  cards.forEach((card) => {
    const matchesQuery = !query || card.dataset.search.includes(query);
    const matchesRegion = !region || card.dataset.region === region;
    const matchesStatus = !status || card.dataset.status === status;
    const show = matchesQuery && matchesRegion && matchesStatus;
    card.hidden = !show;
    if (show) visible += 1;
  });

  emptyState.hidden = visible !== 0;
}

[searchBox, regionFilter, statusFilter].forEach((control) => {
  control.addEventListener("input", applyFilters);
});
