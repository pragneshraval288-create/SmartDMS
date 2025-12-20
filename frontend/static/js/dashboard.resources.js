/* ===========================
   DASHBOARD SYSTEM RESOURCES
   (STABLE + FUTURE READY)
=========================== */

function meterChart(id, value, color) {
  const el = document.getElementById(id);
  if (!el || typeof Chart === "undefined") return;

  // Destroy existing chart if reloaded (safety)
  if (el._chartInstance) {
    el._chartInstance.destroy();
  }

  const chart = new Chart(el, {
    type: "doughnut",
    data: {
      datasets: [
        {
          data: [value, Math.max(0, 100 - value)],
          backgroundColor: [color, "#e5e7eb"],
          borderWidth: 0,
          hoverOffset: 0
        }
      ]
    },
    options: {
      responsive: true,
      cutout: "75%",
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => `${ctx.raw}%`
          }
        }
      },
      animation: {
        duration: 900,
        easing: "easeOutCubic"
      }
    }
  });

  // store instance for safety
  el._chartInstance = chart;
}

document.addEventListener("DOMContentLoaded", () => {
  /*
    NOTE:
    These are INDICATIVE / DEMO values.
    Backend live monitoring can be plugged later.
  */
  meterChart("cpuChart", 8, "#0ea5e9");     // CPU %
  meterChart("memoryChart", 38, "#22c55e"); // Memory %
  meterChart("diskChart", 5, "#facc15");    // Disk %
});
