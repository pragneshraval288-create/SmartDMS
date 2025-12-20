/* ===========================
   BASE NOTIFICATIONS HANDLER
   (STABLE + CLEAN UX)
=========================== */

document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("notifBtn");
  const dropdown = document.getElementById("notifDropdown");
  const badge = btn ? btn.querySelector(".badge") : null;
  const csrfToken =
    document.querySelector('meta[name="csrf-token"]')?.content ||
    document.getElementById("csrfToken")?.value;

  if (!btn || !dropdown) return;

  let isOpen = false;

  /* ----------------------------------
     TOGGLE DROPDOWN
  ---------------------------------- */
  btn.addEventListener("click", (e) => {
    e.stopPropagation();

    isOpen = !isOpen;
    dropdown.classList.toggle("d-none", !isOpen);

    if (!isOpen) return;

    // MARK AS READ
    fetch("/notifications/mark-read", {
      method: "POST",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        ...(csrfToken && { "X-CSRFToken": csrfToken })
      },
      credentials: "same-origin"
    })
      .then(() => {
        if (badge) badge.remove();
      })
      .catch(() => {
        console.warn("Failed to mark notifications as read");
      });
  });

  /* ----------------------------------
     CLOSE ON OUTSIDE CLICK
  ---------------------------------- */
  document.addEventListener("click", () => {
    if (!isOpen) return;
    isOpen = false;
    dropdown.classList.add("d-none");
  });

  /* ----------------------------------
     CLOSE ON SCROLL (UX SAFETY)
  ---------------------------------- */
  window.addEventListener("scroll", () => {
    if (!isOpen) return;
    isOpen = false;
    dropdown.classList.add("d-none");
  });

  /* ----------------------------------
     DROPDOWN ACTIONS
     (DELETE SINGLE + CLEAR ALL)
  ---------------------------------- */
  dropdown.addEventListener("click", (e) => {
    e.stopPropagation();

    /* DELETE SINGLE */
    const deleteBtn = e.target.closest(".notif-delete");
    if (deleteBtn) {
      const item = deleteBtn.closest(".notif-item");
      const id = item?.dataset.id;
      if (!id) return;

      fetch(`/notifications/delete/${id}`, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          ...(csrfToken && { "X-CSRFToken": csrfToken })
        },
        credentials: "same-origin"
      })
        .then(() => {
          item.remove();
          refreshNotificationUI();
        })
        .catch(() => {
          console.warn("Failed to delete notification");
        });

      return;
    }

    /* CLEAR ALL */
    if (e.target.id === "notifClearAll") {
      fetch("/notifications/clear-all", {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          ...(csrfToken && { "X-CSRFToken": csrfToken })
        },
        credentials: "same-origin"
      })
        .then(() => {
          dropdown.innerHTML = `
            <div class="notif-empty">
              No new notifications
            </div>
          `;
        })
        .catch(() => {
          console.warn("Failed to clear notifications");
        });
    }
  });

  /* ----------------------------------
     EMPTY STATE HANDLER
  ---------------------------------- */
  function refreshNotificationUI() {
    const items = dropdown.querySelectorAll(".notif-item");
    if (items.length === 0) {
      dropdown.innerHTML = `
        <div class="notif-empty">
          No new notifications
        </div>
      `;
    }
  }
});

// ===============================
// MOBILE SIDEBAR TOGGLE
// ===============================
document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.getElementById("sidebarToggle");

  if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
      document.body.classList.toggle("sidebar-open");
    });
  }
});
