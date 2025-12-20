// ==================================================
// GLOBAL CLIPBOARD
// ==================================================
let clipboard = JSON.parse(sessionStorage.getItem("clipboard")) || null;
let pasteBtn = null;

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
// DOM READY
// ==================================================
document.addEventListener("DOMContentLoaded", () => {

  const csrfToken =
    document.querySelector('meta[name="csrf-token"]')?.content ||
    document.querySelector('input[name="csrf_token"]')?.value ||
    "";

  pasteBtn = document.getElementById("pasteBtn");
  updatePasteButton();

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
  // 🔥 SINGLE CLICK HANDLER (FOLDER + DOCUMENT)
  // ==================================================
  document.body.addEventListener("click", (e) => {

    /* ---------------- DOCUMENT ACTIONS ---------------- */
    const docEl = e.target.closest("[data-doc-action]");
    if (docEl) {
      e.preventDefault();
      e.stopPropagation();

      const docId = Number(docEl.dataset.docId);
      const action = docEl.dataset.docAction;

      clipboard = {
        type: "document",
        action,
        id: docId
      };

      saveClipboard();
      updatePasteButton();

      alert(`Document ready to ${action}. Open target folder and click Paste.`);
      return;
    }

    /* ---------------- FOLDER ACTIONS ---------------- */
    const folderEl = e.target.closest("[data-folder-action]");
    if (!folderEl) return;

    e.preventDefault();

    const folderId = Number(folderEl.dataset.folderId);
    const action = folderEl.dataset.folderAction;

    // COPY / MOVE
    if (action === "copy" || action === "move") {
      clipboard = {
        type: "folder",
        action,
        id: folderId
      };
      saveClipboard();
      updatePasteButton();
      showSuccess(`Folder ready to ${action}. Open target folder and click Paste.`);
      return;
    }

    // PASTE
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

    // RENAME
    if (action === "rename") {
      const newName = prompt("Enter new folder name:");
      if (!newName) return;

      sendPasteRequest(
        `/documents/folders/${folderId}/rename`,
        { name: newName }
      );
    }

    // DELETE
    if (action === "delete") {
      if (!confirm("Delete this folder and all its contents?")) return;

      fetch(`/documents/folders/${folderId}/delete`, {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken }
      })
        .then(r => r.json())
        .then(d => d.success ? location.reload() : showError(d.error))
        .catch(() => showError());
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
