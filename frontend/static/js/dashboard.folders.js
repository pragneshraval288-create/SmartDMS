// ==================================================
// GLOBAL CLIPBOARD
// ==================================================
let clipboard = JSON.parse(sessionStorage.getItem("clipboard")) || null;
let deleteModal = null;

// ==================================================
// HELPERS
// ==================================================
function saveClipboard() {
  sessionStorage.setItem("clipboard", JSON.stringify(clipboard));
}

function clearClipboard() {
  clipboard = null;
  sessionStorage.removeItem("clipboard");
}

function showError(msg) {
  alert(msg || "Server error");
}

function showSuccess(msg) {
  alert(msg);
}

// ==================================================
// CREATE FOLDER (SHARED LOGIC)
// ==================================================
function openCreateFolderModal(parentId = null) {
  const modalEl = document.getElementById("createFolderModal");
  if (!modalEl) return showError("Create folder modal not found");

  const parentInput = modalEl.querySelector('input[name="parent_id"]');
  if (parentInput) {
    parentInput.value = parentId || "";
  }

  bootstrap.Modal.getOrCreateInstance(modalEl).show();
}

// ==================================================
// DELETE MODAL HANDLER
// ==================================================
function openDeleteModal(type, id) {
  const modalEl = document.getElementById("deleteModal");
  if (!modalEl) return showError("Delete modal not found");

  modalEl.dataset.type = type;
  modalEl.dataset.id = id;

  deleteModal = bootstrap.Modal.getOrCreateInstance(modalEl);
  deleteModal.show();
}

// ==================================================
// DOM READY
// ==================================================
document.addEventListener("DOMContentLoaded", () => {

  const csrfToken =
    document.querySelector('meta[name="csrf-token"]')?.content ||
    document.querySelector('input[name="csrf_token"]')?.value ||
    "";

  // ==================================================
  // SELECT ALL CHECKBOX
  // ==================================================
  const selectAll = document.getElementById("selectAll");
  const bulkDeleteBtn = document.getElementById("bulkDeleteBtn");

  function updateBulkDeleteState() {
    const checked = document.querySelectorAll(".selectItem:checked").length;
    if (bulkDeleteBtn) bulkDeleteBtn.disabled = checked === 0;
  }

  if (selectAll) {
    selectAll.addEventListener("change", () => {
      document.querySelectorAll(".selectItem").forEach(cb => {
        cb.checked = selectAll.checked;
      });
      updateBulkDeleteState();
    });
  }

  document.body.addEventListener("change", (e) => {
    if (e.target.classList.contains("selectItem")) {
      updateBulkDeleteState();
    }
  });



  // ==================================================
  // ⭐ FAVORITE TOGGLE (DOCUMENT + FOLDER)
  // ==================================================
  document.body.addEventListener("click", (e) => {
    const favBtn = e.target.closest(".favorite-toggle");
    if (!favBtn) return;

    e.preventDefault();
    e.stopPropagation();

    const type = favBtn.dataset.type; // document | folder
    const id = favBtn.dataset.id;
    const icon = favBtn.querySelector("i");

    fetch(`/favorites/${type}/${id}/toggle`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken
      }
    })
      .then(r => r.json())
      .then(d => {
        if (!d.success) return showError(d.error);

        // toggle icon instantly
        if (icon.classList.contains("bi-star")) {
          icon.classList.remove("bi-star");
          icon.classList.add("bi-star-fill", "text-warning");
        } else {
          icon.classList.remove("bi-star-fill", "text-warning");
          icon.classList.add("bi-star");
        }
      })
      .catch(() => showError());
  });

  // ==================================================
  // SINGLE CLICK HANDLER (DOC + FOLDER ACTIONS)
  // ==================================================
  document.body.addEventListener("click", (e) => {

    // ---------- DOCUMENT ----------
    const docEl = e.target.closest("[data-doc-action]");
    if (docEl) {
      e.preventDefault();

      const docId = Number(docEl.dataset.docId);
      const action = docEl.dataset.docAction;

      if (action === "archive") {
        if (!confirm("Archive this document?")) return;

        fetch(`/documents/${docId}/archive`, {
          method: "POST",
          headers: { "X-CSRFToken": csrfToken }
        })
          .then(r => r.json())
          .then(d => d.success ? location.reload() : showError(d.error))
          .catch(() => showError());
        return;
      }

      clipboard = { type: "document", action, id: docId };
      saveClipboard();
      showSuccess(`Document ready to ${action}. Open target folder and click Paste.`);
      return;
    }

    // ---------- FOLDER ----------
    const folderEl = e.target.closest("[data-folder-action]");
    if (!folderEl) return;

    e.preventDefault();

    const folderId = Number(folderEl.dataset.folderId);
    const action = folderEl.dataset.folderAction;

    if (action === "copy" || action === "move") {
      clipboard = { type: "folder", action, id: folderId };
      saveClipboard();
      showSuccess(`Folder ready to ${action}. Open target folder and click Paste.`);
      return;
    }

    if (action === "paste") {
      if (!clipboard) return showError("Clipboard is empty");

      const url =
        clipboard.type === "folder"
          ? `/documents/folders/${clipboard.id}/${clipboard.action}`
          : `/documents/${clipboard.id}/${clipboard.action}`;

      fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({ parent_id: folderId })
      })
        .then(r => r.json())
        .then(d => {
          if (d.success) {
            clearClipboard();
            location.reload();
          } else {
            showError(d.error);
          }
        })
        .catch(() => showError());
      return;
    }

    if (action === "rename") {
      const newName = prompt("Enter new folder name:");
      if (!newName) return;

      fetch(`/documents/folders/${folderId}/rename`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({ name: newName })
      })
        .then(r => r.json())
        .then(d => d.success ? location.reload() : showError(d.error))
        .catch(() => showError());
      return;
    }

    if (action === "delete") {
      openDeleteModal("folder", folderId);
    }
  });

  // ==================================================
  // + FOLDER BUTTON
  // ==================================================
  document.querySelectorAll('[data-bs-target="#createFolderModal"]').forEach(btn => {
    btn.addEventListener("click", () => {
      const params = new URLSearchParams(window.location.search);
      const parentId = params.get("folder");
      openCreateFolderModal(parentId ? Number(parentId) : null);
    });
  });

});

// ==================================================
// DELETE MODAL BUTTONS (FOLDER)
// ==================================================
document.getElementById("moveToBinBtn")?.addEventListener("click", () => {
  const modalEl = document.getElementById("deleteModal");
  const folderId = modalEl.dataset.id;

  fetch(`/documents/folders/${folderId}/bin`, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken
    }
  })
    .then(r => r.json())
    .then(d => {
      if (d.success) {
        deleteModal.hide();
        location.reload();
      } else {
        showError(d.error);
      }
    })
    .catch(() => showError());
});

document.getElementById("permanentDeleteBtn")?.addEventListener("click", () => {
  const modalEl = document.getElementById("deleteModal");
  const folderId = modalEl.dataset.id;

  if (!confirm("This will permanently delete the folder. Continue?")) return;

  fetch(`/documents/folders/${folderId}/delete`, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken
    }
  })
    .then(r => r.json())
    .then(d => {
      if (d.success) {
        deleteModal.hide();
        location.reload();
      } else {
        showError(d.error);
      }
    })
    .catch(() => showError());
});