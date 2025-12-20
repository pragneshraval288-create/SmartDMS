/* ===========================
   DASHBOARD UPLOADS TREND
   (REAL DATA ONLY)
=========================== */

document.addEventListener("DOMContentLoaded", () => {

  // Safety: Chart.js loaded or not
  if (typeof Chart === "undefined") {
    console.warn("Chart.js not loaded");
    return;
  }

  const canvas = document.getElementById("uploadsChart");
  if (!canvas) return;

  // Read data from HTML data-* attributes
  let labels = [];
  let counts = [];

  try {
    labels = JSON.parse(canvas.dataset.labels || "[]");
    counts = JSON.parse(canvas.dataset.counts || "[]");
  } catch (err) {
    console.error("Invalid uploads chart data", err);
    return;
  }

  if (labels.length === 0 || counts.length === 0) return;

  const ctx = canvas.getContext("2d");

  // Gradient for area fill
  const blueGradient = ctx.createLinearGradient(0, 0, 0, 220);
  blueGradient.addColorStop(0, "rgba(30, 58, 138, 0.45)");
  blueGradient.addColorStop(1, "rgba(30, 58, 138, 0.05)");

  // Create chart
  new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Uploads",
          data: counts,
          fill: true,
          backgroundColor: blueGradient,
          borderColor: "#1e3a8a",
          borderWidth: 3,
          tension: 0.4,
          pointRadius: 4,
          pointHoverRadius: 6,
          pointBackgroundColor: "#1e3a8a"
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => `Uploads: ${ctx.raw}`
          }
        }
      },
      scales: {
        x: {
          grid: { display: false }
        },
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0
          }
        }
      }
    }
  });

});
