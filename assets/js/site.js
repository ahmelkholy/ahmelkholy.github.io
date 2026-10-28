"use strict";
// Progressive enhancement only: navigation and content work without JavaScript.
for (const time of document.querySelectorAll("[data-local-date]")) {
  const date = new Date(time.dataset.localDate + "T12:00:00Z");
  if (!Number.isNaN(date.valueOf()))
    time.textContent = new Intl.DateTimeFormat(document.documentElement.lang, {
      dateStyle: "long",
      timeZone: "UTC",
    }).format(date);
}
const toc = document.querySelector("[data-toc]");
if (toc) {
  const headings = document.querySelectorAll(
    ".article-body h2, .article-body h3",
  );
  if (headings.length > 1) {
    toc.hidden = false;
    for (const heading of headings) {
      if (!heading.id) continue;
      const li = document.createElement("li");
      const a = document.createElement("a");
      a.href = "#" + encodeURIComponent(heading.id);
      a.textContent = heading.textContent;
      li.append(a);
      toc.querySelector("ul").append(li);
    }
  }
}
const filters = document.querySelector("[data-filters]");
if (filters) {
  filters.hidden = false;
  const language = document.querySelector("#language"),
    query = document.querySelector("#query");
  const items = [...document.querySelectorAll("[data-articles] > li")];
  const normalize = (s) =>
    s.normalize("NFKD").replace(/\p{M}/gu, "").toLocaleLowerCase();
  const initial =
    new URLSearchParams(location.search).get("lang") ||
    filters.dataset.defaultLang;
  if (["en", "ar", "ru"].includes(initial)) language.value = initial;
  function filter() {
    const q = normalize(query.value.trim());
    let count = 0;
    for (const item of items) {
      item.hidden = !(
        (language.value === "all" || item.dataset.lang === language.value) &&
        normalize(item.dataset.search).includes(q)
      );
      if (!item.hidden) count++;
    }
    document.querySelector("[data-filter-status]").textContent = count
      ? `${count} ${filters.dataset.countLabel}`
      : language.value === "ru" && !q
        ? filters.dataset.russianEmpty
        : filters.dataset.empty;
  }
  language.addEventListener("change", filter);
  query.addEventListener("input", filter);
  filter();
}
