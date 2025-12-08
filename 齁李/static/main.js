
// Very small helper to GET JSON
async function apiGet(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error("API error: " + res.status);
  return await res.json();
}

// Example hooks per page (safe no-ops if elements not present)
document.addEventListener("DOMContentLoaded", async () => {
  // Role persistence (shared across pages)
  const roleSel = document.getElementById("roleSelect");
  if (roleSel) {
    const saved = localStorage.getItem("currentRole") || roleSel.value || "client";
    roleSel.value = saved;
    roleSel.addEventListener("change", () => {
      localStorage.setItem("currentRole", roleSel.value);
    });
  }

  // customer.html: generate id button already exists in page; nothing to wire here

  // parcel_tracking.html: try to show customer summary if we have ?customer= param
  const custSummary = document.getElementById("customerSummary");
  if (custSummary) {
    try {
      const url = new URL(window.location.href);
      const custId = url.searchParams.get("customer") || "SENDER001";
      const data = await apiGet(`/api/customers/${custId}`);
      custSummary.textContent = `客戶：${data.name}（${data.customer_id}），電話：${data.phone}，Email：${data.email}`;
    } catch (e) {
      custSummary.textContent = "（尚無客戶資料或讀取錯誤）";
    }
  }

  // billing.html: price calculator exists in page; we also attempt to show a sample monthly billing if inputs exist
  const priceResult = document.getElementById("priceResult");
  if (priceResult) {
    // no automatic call; user presses the page button defined inline
  }

  // If billing report form exists, wire a demo button (query monthly bills)
  const reportCust = document.getElementById("reportCustomerId");
  const reportMonth = document.getElementById("reportMonth");
  if (reportCust && reportMonth) {
    const table = document.querySelector("table");
    const btn = Array.from(document.querySelectorAll("button")).find(b => b.textContent.includes("產生月結報表"));
    if (btn && table) {
      btn.addEventListener("click", async () => {
        const cid = reportCust.value || "TEST001";
        const period = reportMonth.value || "2025-12";
        try {
          const bills = await apiGet(`/api/billing?customer=${encodeURIComponent(cid)}&period=${encodeURIComponent(period)}`);
          // replace tbody with new rows based on sample
          const tbody = table.querySelector("tbody") || table.createTBody();
          tbody.innerHTML = "";
          if (bills && bills.items) {
            for (const row of bills.items) {
              const tr = document.createElement("tr");
              tr.innerHTML = `<td>${row.tracking_number || "-"}</td>
                              <td>${row.date || "-"}</td>
                              <td>${row.service || "-"}</td>
                              <td>${row.amount ?? "-"}</td>`;
              tbody.appendChild(tr);
            }
          }
        } catch (e) {
          alert("找不到該月份的帳單資料");
        }
      });
    }
  }
});
