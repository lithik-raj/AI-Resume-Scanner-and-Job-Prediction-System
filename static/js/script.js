console.log("Resume Screening System Loaded");
document.querySelectorAll(".match-fill").forEach(function (bar) {
  const match = parseFloat(bar.dataset.match) || 0;

  bar.style.width = Math.min(Math.max(match, 0), 100) + "%";
});