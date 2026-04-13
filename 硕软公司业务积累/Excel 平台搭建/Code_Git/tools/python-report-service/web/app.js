const templateSelect = document.getElementById("templateSelect");
const loadSampleButton = document.getElementById("loadSampleButton");
const resetButton = document.getElementById("resetButton");
const formatButton = document.getElementById("formatButton");
const generateButton = document.getElementById("generateButton");
const payloadInput = document.getElementById("payloadInput");
const resultOutput = document.getElementById("resultOutput");
const curlOutput = document.getElementById("curlOutput");
const statusBadge = document.getElementById("statusBadge");
const fieldHints = document.getElementById("fieldHints");
const previewGrid = document.getElementById("previewGrid");
const previewMeta = document.getElementById("previewMeta");

const templateHints = {
  shandong_short_link_reporting: "共享字段: linkList\nentries 字段: signature, companyName\n说明: 多签名共用同一份链接列表。",
  shandong_multi_level_domain: "共享字段: linkList, businessUsage\nentries 字段: signature, companyName\n说明: 多签名共用域名列表与用途。",
  shandong_link_authorization: "共享字段: linkCompanyName, linkList, businessUsage\nentries 字段: companyName\n说明: 授权方共用，被授权方逐条生成。",
  shandong_phone_ownership_claim: "共享字段: phoneNumbers, phoneUsage\nentries 字段: signature, companyName\n说明: 多签名共用号码列表。",
  beijing_link_authorization: "共享字段: linkCompanyName, linkList, businessScope\nentries 字段: companyName\n说明: 双章模板。",
  beijing_compliance_commitment: "共享字段: businessScope, lgiItems\nentries 字段: companyName\n说明: lgiItems 会按每 10 条拆分。",
  beijing_number_ownership_claim: "共享字段: numberList\nentries 字段: signature, companyName\n说明: numberList 会被转成声明表格。"
};

function setStatus(type, text) {
  statusBadge.className = `badge ${type}`;
  statusBadge.textContent = text;
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function formatJson(value) {
  return JSON.stringify(value, null, 2);
}

async function loadTemplates() {
  const response = await fetch("/api/v1/reports/templates");
  const data = await response.json();
  templateSelect.innerHTML = data.templates
    .map((item) => `<option value="${item}">${item}</option>`)
    .join("");
  await loadSample();
}

async function loadSample() {
  const templateType = templateSelect.value;
  const response = await fetch(`/api/v1/reports/sample/${templateType}`);
  const data = await response.json();
  payloadInput.value = formatJson(data.sample);
  renderCurl(data.sample);
  fieldHints.textContent = templateHints[templateType] || "暂无字段提示";
  setStatus("idle", "样例已加载");
}

function renderCurl(payload) {
  curlOutput.textContent = [
    "curl -X POST http://127.0.0.1:8000/api/v1/reports/generate \\",
    "  -H \"Content-Type: application/json\" \\",
    `  -d '${JSON.stringify(payload)}'`
  ].join("\n");
}

function toPreviewUrl(filePath) {
  if (!filePath) {
    return "";
  }
  const normalized = String(filePath).replace(/\\/g, "/");
  const marker = "/storage/";
  const markerIndex = normalized.indexOf(marker);
  if (markerIndex >= 0) {
    return normalized.slice(markerIndex);
  }
  return filePath;
}

function renderPreviews(imageFiles = []) {
  if (!Array.isArray(imageFiles) || imageFiles.length === 0) {
    previewMeta.textContent = "生成后显示";
    previewGrid.innerHTML = '<div class="preview-empty">等待生成图片...</div>';
    return;
  }

  previewMeta.textContent = `共 ${imageFiles.length} 张`;
  const versionToken = Date.now();
  previewGrid.innerHTML = imageFiles
    .map((filePath, index) => {
      const previewUrl = `${toPreviewUrl(filePath)}?v=${versionToken}-${index}`;
      const fileName = filePath.split(/[\\/]/).pop();
      return `
        <article class="preview-card">
          <img src="${escapeHtml(previewUrl)}" alt="预览图 ${index + 1}">
          <div class="preview-card-body">
            <p class="preview-card-title">${escapeHtml(fileName || `图片${index + 1}`)}</p>
            <a class="preview-card-link" href="${escapeHtml(previewUrl)}" target="_blank" rel="noreferrer">打开原图</a>
          </div>
        </article>
      `;
    })
    .join("");
}

function parsePayload() {
  return JSON.parse(payloadInput.value);
}

async function generateReport() {
  let payload;
  try {
    payload = parsePayload();
  } catch (error) {
    setStatus("error", "JSON 错误");
    resultOutput.textContent = `请求体 JSON 解析失败:\n${error.message}`;
    return;
  }

  setStatus("loading", "生成中");
  resultOutput.textContent = "正在调用后端生成，请稍候...";
  renderCurl(payload);

  try {
    const response = await fetch("/api/v1/reports/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(formatJson(data));
    }
    setStatus("success", "生成成功");
    resultOutput.textContent = formatJson(data);
    renderPreviews(data.imageFiles);
  } catch (error) {
    setStatus("error", "生成失败");
    resultOutput.textContent = error.message;
    renderPreviews([]);
  }
}

function resetPayload() {
  payloadInput.value = "";
  resultOutput.textContent = "等待生成结果...";
  curlOutput.textContent = "";
  fieldHints.textContent = "";
  setStatus("idle", "未执行");
  renderPreviews([]);
}

function formatPayload() {
  try {
    payloadInput.value = formatJson(parsePayload());
  } catch (error) {
    setStatus("error", "JSON 错误");
    resultOutput.textContent = `格式化失败:\n${error.message}`;
  }
}

templateSelect.addEventListener("change", loadSample);
loadSampleButton.addEventListener("click", loadSample);
resetButton.addEventListener("click", resetPayload);
formatButton.addEventListener("click", formatPayload);
generateButton.addEventListener("click", generateReport);

loadTemplates().catch((error) => {
  setStatus("error", "加载失败");
  resultOutput.textContent = `初始化页面失败:\n${error.message}`;
});
