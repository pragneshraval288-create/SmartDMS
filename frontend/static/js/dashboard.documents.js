document.addEventListener("DOMContentLoaded", () => {
  // ===================================
  // 1. GLOBAL VARIABLES & SELECTORS
  // ===================================
  const deleteModal = document.getElementById("deleteModal");
  const bulkDeleteBtn = document.getElementById("bulkDeleteBtn");
  const selectAllCheckbox = document.getElementById("selectAll");
  const checkboxes = document.querySelectorAll(".selectItem");
  
  // To store what we are about to delete
  let itemsToDelete = { documents: [], folders: [] };

  // ===================================
  // 2. CHECKBOX LOGIC (Select All / Toggle)
  // ===================================
  
  // Handle "Select All"
  if (selectAllCheckbox) {
    selectAllCheckbox.addEventListener("change", function () {
      checkboxes.forEach((cb) => (cb.checked = this.checked));
      updateBulkButtonState();
    });
  }

  // Handle Individual Checkboxes
  checkboxes.forEach((cb) => {
    cb.addEventListener("change", updateBulkButtonState);
  });

  function updateBulkButtonState() {
    const anyChecked = document.querySelector(".selectItem:checked");
    if (bulkDeleteBtn) {
      if (anyChecked) {
        bulkDeleteBtn.removeAttribute("disabled");
      } else {
        bulkDeleteBtn.setAttribute("disabled", "true");
      }
    }
  }

  // ===================================
  // 3. PREPARE DELETE DATA (When Modal Opens)
  // ===================================
  
  if (deleteModal) {
    deleteModal.addEventListener("show.bs.modal", (event) => {
      const triggerBtn = event.relatedTarget;
      const type = triggerBtn.dataset.type; // 'bulk', 'document', or 'folder'
      const id = triggerBtn.dataset.id;

      // Reset storage
      itemsToDelete = { documents: [], folders: [] };

      if (type === "bulk") {
        // CASE A: BULK DELETE - Collect from checkboxes
        document.querySelectorAll(".selectItem:checked").forEach((cb) => {
          if (cb.dataset.type === "document") {
            itemsToDelete.documents.push(cb.dataset.id);
          } else if (cb.dataset.type === "folder") {
            itemsToDelete.folders.push(cb.dataset.id);
          }
        });
      } else {
        // CASE B: SINGLE DELETE - Collect from the clicked button
        if (type === "document") itemsToDelete.documents.push(id);
        if (type === "folder") itemsToDelete.folders.push(id);
      }

      // Debugging (Optional)
      console.log("Items prepared for delete:", itemsToDelete);
    });
  }

  // ===================================
  // 4. PERFORM DELETE ACTIONS
  // ===================================

  // Button: Move to Recycle Bin
  document.getElementById("moveToBinBtn")?.addEventListener("click", () => {
    performDelete("recycle");
  });

  // Button: Permanently Delete
  document.getElementById("permanentDeleteBtn")?.addEventListener("click", () => {
    performDelete("permanent");
  });

  async function performDelete(actionType) {
    if (itemsToDelete.documents.length === 0 && itemsToDelete.folders.length === 0) {
      alert("Nothing selected");
      return;
    }

    try {
      const response = await fetch("/documents/bulk-delete", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          // "X-CSRFToken": csrfToken // Uncomment if using Flask-WTF CSRF
        },
        body: JSON.stringify({
          action: actionType, // 'recycle' or 'permanent'
          documents: itemsToDelete.documents,
          folders: itemsToDelete.folders,
        }),
      });

      const result = await response.json();

      if (result.success) {
        window.location.reload();
      } else {
        alert("Error: " + result.message);
      }
    } catch (error) {
      console.error(error);
      alert("An error occurred while connecting to server.");
    }
  }
});