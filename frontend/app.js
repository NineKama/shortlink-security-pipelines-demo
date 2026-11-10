const form = document.getElementById("form");
const input = document.getElementById("url");
const message = document.getElementById("message");
const result = document.getElementById("result");
const shortLink = document.getElementById("short");
const copyBtn = document.getElementById("copy");
const table = document.getElementById("table");
const rows = document.getElementById("rows");
const empty = document.getElementById("empty");

const shortUrl = (code) => `${location.origin}/r/${code}`;

function showMessage(text, isError) {
  message.textContent = text;
  message.className = isError ? "error" : "";
}

async function loadLinks() {
  try {
    const res = await fetch("/api/links");
    const links = await res.json();
    rows.replaceChildren();
    for (const link of links) {
      const tr = document.createElement("tr");

      const tdShort = document.createElement("td");
      const a = document.createElement("a");
      a.href = shortUrl(link.code);
      a.textContent = `/r/${link.code}`;
      a.target = "_blank";
      a.rel = "noopener noreferrer";
      tdShort.append(a);

      const tdUrl = document.createElement("td");
      tdUrl.className = "url";
      tdUrl.textContent = link.url; // textContent để tránh XSS
      tdUrl.title = link.url;

      const tdClicks = document.createElement("td");
      tdClicks.className = "num";
      tdClicks.textContent = link.clicks;

      tr.append(tdShort, tdUrl, tdClicks);
      rows.append(tr);
    }
    table.hidden = links.length === 0;
    empty.hidden = links.length !== 0;
  } catch {
    showMessage("Không tải được danh sách link. Kiểm tra backend đã chạy chưa.", true);
  }
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  showMessage("", false);
  try {
    const res = await fetch("/api/shorten", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: input.value.trim() }),
    });
    const data = await res.json();
    if (!res.ok) {
      result.hidden = true;
      showMessage(data.error || "Không rút gọn được link.", true);
      return;
    }
    shortLink.href = shortUrl(data.code);
    shortLink.textContent = shortUrl(data.code);
    result.hidden = false;
    copyBtn.textContent = "Sao chép";
    input.value = "";
    loadLinks();
  } catch {
    showMessage("Không kết nối được máy chủ. Hãy thử lại.", true);
  }
});

copyBtn.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(shortLink.textContent);
    copyBtn.textContent = "Đã sao chép";
  } catch {
    showMessage("Không sao chép được. Hãy chọn link và sao chép thủ công.", true);
  }
});

loadLinks();
