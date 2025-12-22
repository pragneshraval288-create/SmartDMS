// ==================================================
// GLOBAL CLIPBOARD
// ==================================================
let clipboard = JSON.parse(sessionStorage.getItem("clipboard")) || null;
let pasteBtn = null;
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
  updatePasteButton();
}

function updatePasteButton() {
  if (!pasteBtn) return;
  pasteBtn.disabled = clipboard === null;
}

function showError(msg) {
  alert(msg || "Server error");
}

function showSuccess(msg) {
  alert(msg);
}

// ==================================================
// DELETE MODAL HANDLER
// ==================================================
function openDeleteModal(type, id) {
  const modalEl = document.getElementById("deleteModal");
  if (!modalEl) return showError("Delete modal not found");

  modalEl.dataset.type = type; // folder | document
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

  pasteBtn = document.getElementById("pasteBtn");
  updatePasteButton();

  // ==================================================
  // DELETE MODAL BUTTONS
  // ==================================================
  const moveBtn = document.getElementById("moveToBinBtn");
  const deleteBtn = document.getElementById("permanentDeleteBtn");
  const modalEl = document.getElementById("deleteModal");

  if (moveBtn && deleteBtn && modalEl) {

    // MOVE TO RECYCLE BIN (SOFT DELETE)
    moveBtn.onclick = () => {
      const { type, id } = modalEl.dataset;

      const url =
        type === "folder"
          ? `/documents/folders/${id}/bin`
          : `/documents/${id}/bin`;

      fetch(url, {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken }
      })
        .then(r => r.json())
        .then(d => d.success ? location.reload() : showError(d.error))
        .catch(() => showError());
    };

    // PERMANENT DELETE
    deleteBtn.onclick = () => {
      if (!confirm("This action cannot be undone. Continue?")) return;

      const { type, id } = modalEl.dataset;

      const url =
        type === "folder"
          ? `/documents/folders/${id}/delete`
          : `/documents/${id}/delete`;

      fetch(url, {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken }
      })
        .then(r => r.json())
        .then(d => d.success ? location.reload() : showError(d.error))
        .catch(() => showError());
    };
  }

  // ==================================================
  // PASTE REQUEST
  // ==================================================
  function sendPasteRequest(url, payload) {
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken
      },
      body: JSON.stringify(payload)
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
  }

  // ==================================================
  // SINGLE CLICK HANDLER (FOLDER + DOCUMENT)
  // ==================================================
  document.body.addEventListener("click", (e) => {

    /* ---------- DOCUMENT ACTIONS ---------- */
    const docEl = e.target.closest("[data-doc-action]");
    if (docEl) {
      e.preventDefault();
      e.stopPropagation();

      const docId = Number(docEl.dataset.docId);
      const action = docEl.dataset.docAction;

      if (action === "delete") {
        openDeleteModal("document", docId);
        return;
      }

      clipboard = { type: "document", action, id: docId };
      saveClipboard();
      updatePasteButton();
      showSuccess(`Document ready to ${action}. Open target folder and click Paste.`);
      return;
    }

    /* ---------- FOLDER ACTIONS ---------- */
    const folderEl = e.target.closest("[data-folder-action]");
    if (!folderEl) return;

    e.preventDefault();

    const folderId = Number(folderEl.dataset.folderId);
    const action = folderEl.dataset.folderAction;

    if (action === "copy" || action === "move") {
      clipboard = { type: "folder", action, id: folderId };
      saveClipboard();
      updatePasteButton();
      showSuccess(`Folder ready to ${action}. Open target folder and click Paste.`);
      return;
    }

    if (action === "paste") {
      if (!clipboard) return showError("Clipboard is empty");

      const targetParentId = folderId;

      if (clipboard.type === "folder") {
        sendPasteRequest(
          `/documents/folders/${clipboard.id}/${clipboard.action}`,
          { parent_id: targetParentId }
        );
      }

      if (clipboard.type === "document") {
        sendPasteRequest(
          `/documents/${clipboard.id}/${clipboard.action}`,
          { parent_id: targetParentId }
        );
      }
      return;
    }

    if (action === "rename") {
      const newName = prompt("Enter new folder name:");
      if (!newName) return;

      sendPasteRequest(
        `/documents/folders/${folderId}/rename`,
        { name: newName }
      );
      return;
    }

    if (action === "delete") {
      openDeleteModal("folder", folderId);
    }
  });

  // ==================================================
  // TOP PASTE BUTTON
  // ==================================================
  if (pasteBtn) {
    pasteBtn.addEventListener("click", () => {
      if (!clipboard) return;

      const urlParams = new URLSearchParams(window.location.search);
      const targetParentId = urlParams.get("folder")
        ? Number(urlParams.get("folder"))
        : null;

      if (clipboard.type === "folder") {
        sendPasteRequest(
          `/documents/folders/${clipboard.id}/${clipboard.action}`,
          { parent_id: targetParentId }
        );
      }

      if (clipboard.type === "document") {
        sendPasteRequest(
          `/documents/${clipboard.id}/${clipboard.action}`,
          { parent_id: targetParentId }
        );
      }
    });
  }
});
