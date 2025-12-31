// ==================================================
// GLOBAL CLIPBOARD & STATE
// ==================================================
let clipboard = JSON.parse(sessionStorage.getItem("clipboard")) || null;
let itemsToDelete = { documents: [], folders: [] }; // Store items selected for deletion

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
  // Optional: You can replace alert with a toast notification
  alert(msg);
}

function openCreateFolderModal(parentId = null) {
  const modalEl = document.getElementById("createFolderModal");
  if (!modalEl) return showError("Create folder modal not found");

  const parentInput = modalEl.querySelector('input[name="parent_id"]');
  if (parentInput) parentInput.value = parentId || "";

  bootstrap.Modal.getOrCreateInstance(modalEl).show();
}


// ==================================================
// DOM READY (MAIN LOGIC)
// ==================================================
document.addEventListener("DOMContentLoaded", () => {

  const csrfToken =
    document.querySelector('meta[name="csrf-token"]')?.content ||
    document.querySelector('input[name="csrf_token"]')?.value ||
    "";

  // ==================================================
  // 1. CHECKBOX & BULK SELECTION LOGIC
  // ==================================================
  const selectAll = document.getElementById("selectAll");
  const bulkDeleteBtn = document.getElementById("bulkDeleteBtn");
  const checkboxes = document.querySelectorAll(".selectItem");

  function updateBulkDeleteState() {
    const checkedCount = document.querySelectorAll(".selectItem:checked").length;
    if (bulkDeleteBtn) {
      if (checkedCount > 0) {
        bulkDeleteBtn.removeAttribute("disabled");
      } else {
        bulkDeleteBtn.setAttribute("disabled", "true");
      }
    }
  }

  // Handle "Select All" click
  if (selectAll) {
    selectAll.addEventListener("change", () => {
      document.querySelectorAll(".selectItem").forEach(cb => {
        cb.checked = selectAll.checked;
      });
      updateBulkDeleteState();
    });
  }

  // Handle Individual Checkbox click
  document.body.addEventListener("change", (e) => {
    if (e.target.classList.contains("selectItem")) {
      updateBulkDeleteState();
    }
  });


  // ==================================================
  // 2. DELETE MODAL & LOGIC (The Fix)
  // ==================================================
  const deleteModal = document.getElementById("deleteModal");

  if (deleteModal) {
    // A. Detect what we are deleting when Modal Opens
    deleteModal.addEventListener("show.bs.modal", (event) => {
      const triggerBtn = event.relatedTarget;
      const type = triggerBtn.dataset.type; // 'bulk', 'document', or 'folder'
      const id = triggerBtn.dataset.id;

      // Reset array
      itemsToDelete = { documents: [], folders: [] };

      if (type === "bulk") {
        // Collect all checked items
        document.querySelectorAll(".selectItem:checked").forEach((cb) => {
          if (cb.dataset.type === "document") itemsToDelete.documents.push(cb.dataset.id);
          if (cb.dataset.type === "folder") itemsToDelete.folders.push(cb.dataset.id);
        });
      } else {
        // Collect single item (from dropdown)
        if (type === "document") itemsToDelete.documents.push(id);
        if (type === "folder") itemsToDelete.folders.push(id);
      }
      
      console.log("Items ready to delete:", itemsToDelete);
    });

    // B. Handle "Move to Recycle Bin" Click
    const recycleBtn = document.getElementById("moveToBinBtn");
    if (recycleBtn) {
      recycleBtn.onclick = () => performDelete("recycle");
    }

    // C. Handle "Permanently Delete" Click
    const permBtn = document.getElementById("permanentDeleteBtn");
    if (permBtn) {
      permBtn.onclick = () => performDelete("permanent");
    }
  }

  // D. The Actual API Call function
  async function performDelete(actionType) {
    if (itemsToDelete.documents.length === 0 && itemsToDelete.folders.length === 0) {
      alert("Nothing selected to delete!");
      return;
    }

    try {
      const response = await fetch("/documents/bulk-delete", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          // "X-CSRFToken": csrfToken // Enable if using Flask-WTF
        },
        body: JSON.stringify({
          action: actionType, // 'recycle' or 'permanent'
          documents: itemsToDelete.documents,
          folders: itemsToDelete.folders,
        }),
      });

      const data = await response.json();

      if (data.success) {
        window.location.reload();
      } else {
        showError("Error: " + data.message);
      }
    } catch (err) {
      console.error(err);
      showError("An error occurred while connecting to server.");
    }
  }


  // ==================================================
  // 3. ⭐ FAVORITE TOGGLE
  // ==================================================
  document.body.addEventListener("click", (e) => {
    const favBtn = e.target.closest(".favorite-toggle");
    if (!favBtn) return;

    e.preventDefault();
    e.stopPropagation();

    const type = favBtn.dataset.type;
    const id = favBtn.dataset.id;
    const icon = favBtn.querySelector("i");

    fetch(`/favorites/${type}/${id}/toggle`, {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken }
      })
      .then(r => r.json())
      .then(d => {
        if (!d.success) return showError(d.error);
        icon.classList.toggle("bi-star");
        icon.classList.toggle("bi-star-fill");
        icon.classList.toggle("text-warning");
      })
      .catch(() => showError());
  });


  // ==================================================
  // 4. DOCUMENT ACTIONS (Archive, Copy, etc)
  // ==================================================
  document.body.addEventListener("click", (e) => {
    const docEl = e.target.closest("[data-doc-action]");
    if (!docEl) return;

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

    // Handle Copy/Move/Paste for documents
    if (['copy', 'move', 'paste'].includes(action)) {
       handleClipboardAction('document', action, docId);
    }
  });


  // ==================================================
  // 5. FOLDER ACTIONS (Copy, Move, Rename)
  // ==================================================
  document.body.addEventListener("click", (e) => {
    const folderEl = e.target.closest("[data-folder-action]");
    if (!folderEl) return;

    e.preventDefault();

    const folderId = Number(folderEl.dataset.folderId);
    const action = folderEl.dataset.folderAction;

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
    
    // Handle Copy/Move/Paste for folders
    handleClipboardAction('folder', action, folderId);
  });

  // Helper for Clipboard (Consolidated logic)
  function handleClipboardAction(type, action, id) {
     if (action === "copy" || action === "move") {
        clipboard = { type, action, id };
        saveClipboard();
        showSuccess(`${type.charAt(0).toUpperCase() + type.slice(1)} ready to ${action}. Open target folder and click Paste.`);
        return;
      }
  
      if (action === "paste") {
        if (!clipboard) return showError("Clipboard is empty");
  
        // Construct URL based on what is in clipboard (not where we are clicking)
        const url = clipboard.type === "folder"
            ? `/documents/folders/${clipboard.id}/${clipboard.action}`
            : `/documents/${clipboard.id}/${clipboard.action}`;
  
        // Logic: 'id' here represents the DESTINATION folder ID (parent_id)
        fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
          },
          body: JSON.stringify({ parent_id: id })
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
  }


  // ==================================================
  // 6. OPEN CREATE FOLDER MODAL
  // ==================================================
  document.querySelectorAll('[data-bs-target="#createFolderModal"]').forEach(btn => {
    btn.addEventListener("click", () => {
      const params = new URLSearchParams(window.location.search);
      const parentId = params.get("folder");
      openCreateFolderModal(parentId ? Number(parentId) : null);
    });
  });

});