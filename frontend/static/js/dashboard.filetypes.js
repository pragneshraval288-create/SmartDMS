/* ===========================
   DASHBOARD FILE TYPE CHART
   Horizontal % bars (image-style)
=========================== */

document.addEventListener("DOMContentLoaded", () => {

  if (typeof Chart === "undefined") {
    console.warn("Chart.js not loaded");
    return;
  }

  const canvas = document.getElementById("typeChart");
  if (!canvas) return;

  // Read data from data-* attributes (safe pattern)
  let labels = [];
  let counts = [];

  try {
    labels = JSON.parse(canvas.dataset.labels || "[]");
    counts = JSON.parse(canvas.dataset.counts || "[]");
  } catch (e) {
    console.error("Invalid file type chart data", e);
    return;
  }

  if (!labels.length || !counts.length) return;

  const total = counts.reduce((a, b) => a + b, 0);
  const percentages = counts.map(v =>
    total > 0 ? Math.round((v / total) * 100) : 0
  );

  // 🎨 Dynamic color palette (safe for any number of types)
  const COLORS = [
    "#2563eb", // blue
    "#16a34a", // green
    "#facc15", // yellow
    "#dc2626", // red
    "#9333ea", // purple
    "#0d9488", // teal
    "#ea580c", // orange
  ];

  const bgColors = labels.map(
    (_, i) => COLORS[i % COLORS.length]
  );

  new Chart(canvas, {
    type: "bar",
    data: {
      labels: labels.map((l, i) => `${percentages[i]}% ${l}`),
      datasets: [{
        data: percentages,
        backgroundColor: bgColors,
        borderRadius: 8,
        barThickness: 26
      }]
    },
    options: {
      indexAxis: "y", // 🔥 horizontal
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: ctx => ctx.raw + "%"
          }
        }
      },
      scales: {
        x: {
          beginAtZero: true,
          max: 100,
          ticks: {
            callback: v => v + "%"
          },
          grid: { display: false }
        },
        y: {
          grid: { display: false }
        }
      }
    }
  });

});
