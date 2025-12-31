// ===================================
// DELETE MODAL CONTEXT SET
// ===================================
document.addEventListener("click", function (e) {

  const trigger = e.target.closest("[data-bs-target='#deleteModal']");
  if (!trigger) return;

  const type = trigger.dataset.type;
  const id = trigger.dataset.id || "";

  const ctx = document.getElementById("deleteContext");
  ctx.dataset.type = type;
  ctx.dataset.id = id;
  ctx.dataset.bulk = id ? "false" : "true";
});


// ===================================
// CSRF TOKEN
// ===================================
const csrfToken =
  document.querySelector('meta[name="csrf-token"]')?.content ||
  document.querySelector('input[name="csrf_token"]')?.value ||
  "";


// ===================================
// MOVE TO RECYCLE BIN
// ===================================
document.getElementById("moveToBinBtn")?.addEventListener("click", async () => {
  await performDelete("bin");
});


// ===================================
// PERMANENT DELETE
// ===================================
document.getElementById("permanentDeleteBtn")?.addEventListener("click", async () => {
  if (!confirm("This action cannot be undone. Continue?")) return;
  await performDelete("delete");
});


// ===================================
// CORE DELETE HANDLER (JSON SAFE 🔥)
// ===================================
async function performDelete(action) {

  const ctx = document.getElementById("deleteContext");
  const type = ctx.dataset.type;
  const id = ctx.dataset.id;
  const isBulk = ctx.dataset.bulk === "true";

  let url = "";

  if (type === "document") {
    url = isBulk
      ? `/documents/bulk/${action}`
      : `/documents/${id}/${action}`;
  }

  if (type === "folder") {
    url = isBulk
      ? `/documents/folders/bulk/${action}`
      : `/documents/folders/${id}/${action}`;
  }

  try {
    const res = await fetch(url, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken
      }
    });

    // 🔥 SAFE RESPONSE HANDLING
    const text = await res.text();

    let data;
    try {
      data = JSON.parse(text);
    } catch {
      console.error("Non-JSON response:", text);
      alert("Server returned invalid response. Check backend route.");
      return;
    }

    if (!data.success) {
      alert(data.error || "Server error");
      return;
    }

    location.reload();

  } catch (err) {
    console.error(err);
    alert("Request failed");
  }
}
