const state = {
  preset: "双语台词本",
  exportType: "DOCX + PDF",
  paperSize: "A4",
  orientation: "纵向",
  fontSize: 12,
  lineHeight: 1.6,
  timeline: "完整时间码",
  coverTitleAuto: true,
  activePreview: "doc",
};

const presetDefinitions = {
  scriptbook: {
    name: "双语台词本",
    exportType: "both",
    paperSize: "A4",
    orientation: "portrait",
    margin: "normal",
    bodyFont: "Noto Sans SC",
    titleFont: "Inter",
    fontSize: 12,
    lineHeight: 1.7,
    paragraphSpacing: "balanced",
    accentColor: "#635bff",
    textAlign: "left",
    firstIndent: 0,
    translationScale: 0.9,
    tableRatio: "50-50",
    tableDensity: "normal",
    tableBorders: "light",
    timeline: "full",
    layout: "table",
    coverPage: true,
    toc: true,
    headerFooter: true,
    watermark: false,
    speakerLabel: true,
    bilingual: true,
    keywords: true,
    notes: false,
    pageNumber: "footer-center",
    documentName: "品牌访谈_双语台词本_表格版",
    coverTitleInput: "",
    coverSubtitleInput: "",
    coverMetaEnabled: true,
    coverAlign: "center",
    coverStyle: "brand",
    tocTitleInput: "目录",
    tocLevels: "2",
    tocLeader: true,
    tocNumbering: "decimal",
    coverTitleAuto: true,
  },
  bilingual: {
    name: "双语对照",
    exportType: "both",
    paperSize: "A4",
    orientation: "portrait",
    margin: "normal",
    bodyFont: "Noto Sans SC",
    titleFont: "Inter",
    fontSize: 12,
    lineHeight: 1.6,
    paragraphSpacing: "balanced",
    accentColor: "#635bff",
    textAlign: "left",
    firstIndent: 0,
    translationScale: 0.9,
    tableRatio: "50-50",
    tableDensity: "normal",
    tableBorders: "light",
    timeline: "full",
    layout: "dialogue",
    coverPage: true,
    toc: true,
    headerFooter: true,
    watermark: false,
    speakerLabel: true,
    bilingual: true,
    keywords: true,
    notes: false,
    pageNumber: "footer-center",
    documentName: "访谈整理_2026Q2_双语对照版",
    coverTitleInput: "",
    coverSubtitleInput: "Deliverable Draft",
    coverMetaEnabled: true,
    coverAlign: "center",
    coverStyle: "minimal",
    tocTitleInput: "目录",
    tocLevels: "2",
    tocLeader: true,
    tocNumbering: "decimal",
    coverTitleAuto: true,
  },
  meeting: {
    name: "会议纪要",
    exportType: "docx",
    paperSize: "A4",
    orientation: "portrait",
    margin: "narrow",
    bodyFont: "PingFang SC",
    titleFont: "Inter",
    fontSize: 11,
    lineHeight: 1.5,
    paragraphSpacing: "compact",
    accentColor: "#0fa37f",
    textAlign: "left",
    firstIndent: 0,
    translationScale: 0.9,
    tableRatio: "50-50",
    tableDensity: "compact",
    tableBorders: "light",
    timeline: "minute",
    layout: "paragraph",
    coverPage: false,
    toc: false,
    headerFooter: true,
    watermark: false,
    speakerLabel: true,
    bilingual: false,
    keywords: true,
    notes: true,
    pageNumber: "footer-right",
    documentName: "项目会议纪要_整理版",
    coverTitleInput: "",
    coverSubtitleInput: "",
    coverMetaEnabled: true,
    coverAlign: "left",
    coverStyle: "minimal",
    tocTitleInput: "目录",
    tocLevels: "2",
    tocLeader: true,
    tocNumbering: "decimal",
    coverTitleAuto: true,
  },
  course: {
    name: "课程讲义",
    exportType: "pdf",
    paperSize: "A4",
    orientation: "landscape",
    margin: "wide",
    bodyFont: "Noto Sans SC",
    titleFont: "Noto Sans SC",
    fontSize: 13,
    lineHeight: 1.8,
    paragraphSpacing: "airy",
    accentColor: "#1e88ff",
    textAlign: "justify",
    firstIndent: 0,
    translationScale: 0.9,
    tableRatio: "55-45",
    tableDensity: "comfortable",
    tableBorders: "none",
    timeline: "hidden",
    layout: "paragraph",
    coverPage: true,
    toc: true,
    headerFooter: true,
    watermark: true,
    speakerLabel: false,
    bilingual: false,
    keywords: true,
    notes: false,
    pageNumber: "header-right",
    documentName: "课程字幕讲义_横版",
    coverTitleInput: "",
    coverSubtitleInput: "Course Notes",
    coverMetaEnabled: true,
    coverAlign: "center",
    coverStyle: "brand",
    tocTitleInput: "目录",
    tocLevels: "3",
    tocLeader: true,
    tocNumbering: "decimal",
    coverTitleAuto: true,
  },
  review: {
    name: "审校稿",
    exportType: "both",
    paperSize: "Letter",
    orientation: "portrait",
    margin: "wide",
    bodyFont: "Microsoft YaHei",
    titleFont: "Inter",
    fontSize: 12,
    lineHeight: 1.7,
    paragraphSpacing: "balanced",
    accentColor: "#d9475c",
    textAlign: "left",
    firstIndent: 0,
    translationScale: 0.9,
    tableRatio: "50-50",
    tableDensity: "normal",
    tableBorders: "strong",
    timeline: "full",
    layout: "table",
    coverPage: true,
    toc: true,
    headerFooter: true,
    watermark: true,
    speakerLabel: true,
    bilingual: true,
    keywords: true,
    notes: true,
    pageNumber: "footer-center",
    documentName: "审校稿_带批注区",
    coverTitleInput: "",
    coverSubtitleInput: "Review Pack",
    coverMetaEnabled: true,
    coverAlign: "left",
    coverStyle: "minimal",
    tocTitleInput: "目录",
    tocLevels: "2",
    tocLeader: true,
    tocNumbering: "roman",
    coverTitleAuto: true,
  },
};

const fieldIds = [
  "exportType",
  "paperSize",
  "orientation",
  "margin",
  "bodyFont",
  "titleFont",
  "fontSize",
  "lineHeight",
  "paragraphSpacing",
  "accentColor",
  "textAlign",
  "firstIndent",
  "translationScale",
  "tableRatio",
  "tableDensity",
  "tableBorders",
  "pageNumber",
  "documentName",
  "coverPage",
  "toc",
  "coverTitleInput",
  "coverSubtitleInput",
  "coverMetaEnabled",
  "coverAlign",
  "coverStyle",
  "tocTitleInput",
  "tocLevels",
  "tocLeader",
  "tocNumbering",
  "headerFooter",
  "watermark",
  "speakerLabel",
  "bilingual",
  "keywords",
  "notes",
];

const el = (id) => document.getElementById(id);

const formatMap = {
  pdf: "PDF",
  docx: "DOCX",
  both: "DOCX + PDF",
};

const orientationMap = {
  portrait: "纵向",
  landscape: "横向",
};

const timelineMap = {
  full: "完整时间码",
  minute: "分钟摘要",
  hidden: "隐藏",
};

const layoutMap = {
  dialogue: "layout-dialogue",
  paragraph: "layout-paragraph",
  table: "layout-table",
};

const marginMap = {
  normal: "24 mm",
  narrow: "16 mm",
  wide: "32 mm",
};

const previewTargetMap = {
  doc: {
    shellId: "docPreviewShell",
    previewPageId: "previewPage",
    previewContentId: "previewContent",
    viewerFileNameId: "viewerFileName",
    viewerModeId: "viewerMode",
    viewerPageId: "viewerPage",
    coverBlockId: "coverBlock",
    coverTitleId: "coverTitle",
    coverSubtitleId: "coverSubtitle",
    coverMetaLineId: "coverMetaLine",
    coverFileNameId: "coverFileName",
    coverMetaDateId: "coverMetaDate",
    headerId: "docHeader",
    pageNumberId: "docPageNumber",
    tocBlockId: "tocBlock",
    tocTitleId: "tocTitlePreview",
    tocListId: "tocList",
    sectionTitleId: "docSectionTitle",
    sectionDescriptionId: "docSectionDescription",
  },
  pdf: {
    shellId: "pdfPreviewShell",
    previewPageId: "previewPagePdf",
    previewContentId: "previewContentPdf",
    viewerFileNameId: "viewerFileNamePdf",
    viewerModeId: "viewerModePdf",
    viewerPageId: "viewerPagePdf",
    coverBlockId: "coverBlockPdf",
    coverTitleId: "coverTitlePdf",
    coverSubtitleId: "coverSubtitlePdf",
    coverMetaLineId: "coverMetaLinePdf",
    coverFileNameId: "coverFileNamePdf",
    coverMetaDateId: "coverMetaDatePdf",
    headerId: "pdfHeader",
    pageNumberId: "pdfPageNumber",
    tocBlockId: "tocBlockPdf",
    tocTitleId: "tocTitlePreviewPdf",
    tocListId: "tocListPdf",
    sectionTitleId: "pdfSectionTitle",
    sectionDescriptionId: "pdfSectionDescription",
  },
};

const sectionToggleLabels = {
  expand: "展开",
  collapse: "收起",
};

const presetContentMap = {
  scriptbook: {
    title: "产品访谈双语台词本",
    description: "以下预览展示字幕文本转为双栏表格文档后的结构效果，左栏保留原文台词，右栏展示译文，便于审阅与排练使用。",
  },
  bilingual: {
    title: "产品访谈内容整理",
    description: "以下预览展示字幕文本转为文档后的结构效果，包含时间码、说话人、翻译与关键词高亮。",
  },
  meeting: {
    title: "会议纪要结构预览",
    description: "该模板强调连续段落与关键信息提炼，适合快速归档会议内容和待办事项。",
  },
  course: {
    title: "课程讲义排版预览",
    description: "该模板突出阅读节奏与大段讲解内容，适合生成讲义、课件讲稿和学习资料。",
  },
  review: {
    title: "审校稿对照预览",
    description: "该模板保留时间轴、双语和批注空间，适合团队审校、修改追踪与内容复核。",
  },
};

function getCheckedValue(name) {
  const input = document.querySelector(`input[name="${name}"]:checked`);
  return input ? input.value : "";
}

function toCompactTime(timePart) {
  const segments = timePart.trim().split(":");
  return segments.length >= 2 ? segments.slice(-2).join(":") : timePart.trim();
}

function formatTimecodeValue(fullTimecode, timelineMode, isTableLayout) {
  if (!fullTimecode) return "";
  if (timelineMode === "hidden") return "";

  const [startRaw = "", endRaw = ""] = fullTimecode.split("-").map((item) => item.trim());
  const compactRange = `${toCompactTime(startRaw)} / ${toCompactTime(endRaw)}`;

  if (isTableLayout) return compactRange;
  if (timelineMode === "minute") return toCompactTime(startRaw);
  return fullTimecode;
}

function formatISODate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function setPanelEnabled(panelId, enabled) {
  const panel = el(panelId);
  if (!panel) return;

  panel.classList.toggle("is-disabled", !enabled);
  panel.setAttribute("aria-disabled", String(!enabled));

  panel.querySelectorAll("input, select, textarea, button").forEach((node) => {
    node.disabled = !enabled;
  });
}

function romanize(number) {
  const map = [
    { value: 1000, symbol: "M" },
    { value: 900, symbol: "CM" },
    { value: 500, symbol: "D" },
    { value: 400, symbol: "CD" },
    { value: 100, symbol: "C" },
    { value: 90, symbol: "XC" },
    { value: 50, symbol: "L" },
    { value: 40, symbol: "XL" },
    { value: 10, symbol: "X" },
    { value: 9, symbol: "IX" },
    { value: 5, symbol: "V" },
    { value: 4, symbol: "IV" },
    { value: 1, symbol: "I" },
  ];

  let value = number;
  let result = "";
  map.forEach((item) => {
    while (value >= item.value) {
      result += item.symbol;
      value -= item.value;
    }
  });
  return result;
}

function getActivePreviewLabel() {
  return state.activePreview === "pdf" ? "PDF" : "DOCX";
}

function setActivePreview(type) {
  state.activePreview = type === "pdf" ? "pdf" : "doc";
}

function updatePreviewVisibility(exportType) {
  const switcher = el("previewSwitch");
  const docShell = el(previewTargetMap.doc.shellId);
  const pdfShell = el(previewTargetMap.pdf.shellId);
  const tabDoc = el("previewTabDoc");
  const tabPdf = el("previewTabPdf");

  const normalizedExportType = exportType || "both";

  if (normalizedExportType === "docx") setActivePreview("doc");
  if (normalizedExportType === "pdf") setActivePreview("pdf");

  const showTabs = normalizedExportType === "both";
  if (switcher) switcher.hidden = !showTabs;

  const showDoc = normalizedExportType !== "pdf" && state.activePreview === "doc";
  const showPdf = normalizedExportType !== "docx" && state.activePreview === "pdf";

  if (docShell) docShell.hidden = !showDoc;
  if (pdfShell) pdfShell.hidden = !showPdf;

  if (tabDoc) {
    const isActive = state.activePreview === "doc";
    tabDoc.classList.toggle("is-active", isActive);
    tabDoc.setAttribute("aria-selected", String(isActive));
  }

  if (tabPdf) {
    const isActive = state.activePreview === "pdf";
    tabPdf.classList.toggle("is-active", isActive);
    tabPdf.setAttribute("aria-selected", String(isActive));
  }
}

function updatePreviewHeaderBadges() {
  const activeLabel = getActivePreviewLabel();
  el("previewFormat").textContent = activeLabel;
  el("previewPaper").textContent = `${state.paperSize} / ${state.orientation}`;
}

function setPreviewVars(previewPage) {
  if (!previewPage) return;
  previewPage.style.setProperty("--preview-body-font", el("bodyFont").value);
  previewPage.style.setProperty("--preview-title-font", el("titleFont").value);
  previewPage.style.setProperty("--preview-font-size", `${state.fontSize}pt`);
  previewPage.style.setProperty("--preview-line-height", `${state.lineHeight}`);
  previewPage.style.setProperty("--preview-text-align", el("textAlign")?.value || "left");
  previewPage.style.setProperty("--preview-indent", `${el("firstIndent")?.value || 0}em`);
  previewPage.style.setProperty("--translation-scale", `${el("translationScale")?.value || 0.9}`);

  const pagePaddingMap = {
    normal: { x: 34, y: 18 },
    narrow: { x: 26, y: 14 },
    wide: { x: 46, y: 22 },
  };
  const pad = pagePaddingMap[el("margin").value] || pagePaddingMap.normal;
  previewPage.style.setProperty("--page-pad-x", `${pad.x}px`);
  previewPage.style.setProperty("--page-pad-y", `${pad.y}px`);

  const ratioMap = {
    "50-50": ["50%", "50%"],
    "55-45": ["55%", "45%"],
    "60-40": ["60%", "40%"],
  };
  const ratio = ratioMap[el("tableRatio")?.value || "50-50"] || ratioMap["50-50"];
  previewPage.style.setProperty("--script-col-left", ratio[0]);
  previewPage.style.setProperty("--script-col-right", ratio[1]);

  const densityMap = {
    compact: { x: 12, y: 10 },
    normal: { x: 16, y: 14 },
    comfortable: { x: 18, y: 16 },
  };
  const density = densityMap[el("tableDensity")?.value || "normal"] || densityMap.normal;
  previewPage.style.setProperty("--script-cell-pad-x", `${density.x}px`);
  previewPage.style.setProperty("--script-cell-pad-y", `${density.y}px`);

  const borderMap = {
    none: "transparent",
    light: "rgba(137, 154, 182, 0.18)",
    strong: "rgba(99, 91, 255, 0.36)",
  };
  previewPage.style.setProperty("--table-border-color", borderMap[el("tableBorders")?.value || "light"] || borderMap.light);
}

function renderToc({ tocBlock, tocTitle, tocList }) {
  if (!tocBlock || !tocList) return;

  const tocEnabled = el("toc").checked;
  tocBlock.style.display = tocEnabled ? "block" : "none";
  if (!tocEnabled) return;

  const tocTitleValue = el("tocTitleInput")?.value?.trim() || "目录";
  const levels = Number(el("tocLevels")?.value || 2);
  const leader = el("tocLeader")?.checked ?? true;
  const numbering = el("tocNumbering")?.value || "decimal";

  if (tocTitle) tocTitle.textContent = tocTitleValue;
  tocBlock.classList.toggle("toc-leader-hidden", !leader);

  const items = [
    { level: 1, title: state.sectionTitle || "正文", page: 1 },
    { level: 2, title: "背景与目标", page: 2 },
    { level: 2, title: "配置项说明", page: 3 },
    { level: 3, title: "排版样式", page: 4 },
    { level: 3, title: "结构设置", page: 5 },
    { level: 1, title: "附录", page: 6 },
  ].filter((item) => item.level <= levels);

  const counters = [0, 0, 0];
  const getNumberLabel = (level) => {
    if (numbering === "none") return "";
    if (numbering === "roman" && level === 1) return `${romanize(counters[0])}.`;
    return `${counters.slice(0, level).join(".")}.`;
  };

  tocList.innerHTML = "";
  items.forEach((item) => {
    counters[item.level - 1] += 1;
    for (let i = item.level; i < counters.length; i += 1) counters[i] = 0;

    const li = document.createElement("li");
    li.className = `toc-item toc-level-${item.level}`;

    const numberLabel = getNumberLabel(item.level);
    li.innerHTML = `
      <span class="toc-label">
        ${numberLabel ? `<span class="toc-number">${numberLabel}</span>` : ""}
        <span class="toc-text">${item.title}</span>
      </span>
      <span class="toc-leader" aria-hidden="true"></span>
      <span class="toc-page">${item.page}</span>
    `;
    tocList.appendChild(li);
  });
}

function updatePreviewFor(type, documentName) {
  const target = previewTargetMap[type];
  const previewPage = el(target.previewPageId);
  const previewContent = el(target.previewContentId);

  if (el(target.viewerFileNameId)) el(target.viewerFileNameId).textContent = documentName;
  if (el(target.viewerModeId)) el(target.viewerModeId).textContent = type === "pdf" ? "PDF 预览" : "DOCX 预览";

  const coverEnabled = el("coverPage").checked;
  const coverBlock = el(target.coverBlockId);
  if (coverBlock) coverBlock.style.display = coverEnabled ? "block" : "none";

  if (el(target.coverTitleId)) el(target.coverTitleId).textContent = el("coverTitleInput")?.value?.trim() || documentName;
  if (el(target.coverFileNameId)) el(target.coverFileNameId).textContent = el("fileName").textContent;

  const coverSubtitle = el("coverSubtitleInput")?.value?.trim() || "";
  const coverSubtitleNode = el(target.coverSubtitleId);
  if (coverSubtitleNode) {
    coverSubtitleNode.textContent = coverSubtitle;
    coverSubtitleNode.hidden = !coverSubtitle;
  }

  const coverMetaEnabled = el("coverMetaEnabled")?.checked ?? true;
  const coverMetaLine = el(target.coverMetaLineId);
  if (coverMetaLine) coverMetaLine.style.display = coverMetaEnabled ? "block" : "none";
  if (el(target.coverMetaDateId)) el(target.coverMetaDateId).textContent = formatISODate(new Date());

  if (coverBlock) {
    const align = el("coverAlign")?.value || "center";
    const style = el("coverStyle")?.value || "minimal";
    coverBlock.classList.toggle("cover-align-center", align === "center");
    coverBlock.classList.toggle("cover-align-left", align === "left");
    coverBlock.classList.toggle("cover-style-brand", style === "brand");
    coverBlock.classList.toggle("cover-style-minimal", style === "minimal");
  }

  if (el(target.sectionTitleId)) el(target.sectionTitleId).textContent = state.sectionTitle || "文档预览";
  if (el(target.sectionDescriptionId)) el(target.sectionDescriptionId).textContent = state.sectionDescription || "当前配置将实时反映在这里。";

  const pageNumber = el("pageNumber").value;
  const pageNumberMap = {
    none: "未显示页码",
    "footer-center": "页脚居中",
    "footer-right": "页脚右侧",
    "header-right": "页眉右侧",
  };
  if (el(target.pageNumberId)) {
    el(target.pageNumberId).textContent = type === "pdf" ? `页码：${pageNumberMap[pageNumber]}` : pageNumberMap[pageNumber];
  }

  const headerVisible = el("headerFooter").checked;
  if (el(target.headerId)) {
    el(target.headerId).textContent = headerVisible
      ? `页眉：${state.preset} / ${state.paperSize} / 边距 ${marginMap[el("margin").value]}`
      : "未启用页眉页脚";
  }

  renderToc({
    tocBlock: el(target.tocBlockId),
    tocTitle: el(target.tocTitleId),
    tocList: el(target.tocListId),
  });

  setPreviewVars(previewPage);

  if (previewContent) {
    previewContent.className = `preview-content ${layoutMap[getCheckedValue("layout")]}`;
  }
}

function updateOutputs() {
  el("fontSizeOutput").textContent = `${el("fontSize").value} pt`;
  el("lineHeightOutput").textContent = el("lineHeight").value;
  if (el("firstIndentOutput")) el("firstIndentOutput").textContent = `${el("firstIndent").value} em`;
  if (el("translationScaleOutput")) el("translationScaleOutput").textContent = `${Math.round(Number(el("translationScale").value) * 100)}%`;
}

function updateSectionSummaries() {
  const fileName = el("fileName")?.textContent || "未上传文件";
  const activePreset = document.querySelector(".preset-chip.is-active")?.textContent?.trim() || state.preset;
  const layoutLabels = {
    dialogue: "对话分栏",
    paragraph: "连续段落",
    table: "双栏表格",
  };

  const uploadSummary = `${fileName} · 18:25 · 142 段`;
  const presetSummary = `${activePreset} · ${layoutLabels[getCheckedValue("layout")] || "双栏表格"} · ${el("bilingual").checked ? "双语输出" : "单语输出"}`;
  const formatSummary = `${formatMap[el("exportType").value]} · ${el("paperSize").value} ${orientationMap[el("orientation").value]} · ${marginMap[el("margin").value]}`;
  const styleSummary = `${el("bodyFont").value} / ${el("fontSize").value} pt / ${el("lineHeight").value} / ${layoutLabels[getCheckedValue("layout")] || "双栏表格"}`;

  if (el("uploadSummary")) el("uploadSummary").textContent = uploadSummary;
  if (el("presetSummary")) el("presetSummary").textContent = presetSummary;
  if (el("formatSummary")) el("formatSummary").textContent = formatSummary;
  if (el("styleSummary")) el("styleSummary").textContent = styleSummary;
}

function setControlsCollapsed(collapsed) {
  const workspace = document.querySelector(".workspace");
  const controlsPanel = el("controlsPanel");
  const toggleButton = el("toggleControls");
  const toggleText = toggleButton?.querySelector(".controls-rail__text");

  workspace?.classList.toggle("controls-collapsed", collapsed);
  controlsPanel?.classList.toggle("is-collapsed", collapsed);

  if (toggleButton) {
    toggleButton.setAttribute("aria-expanded", String(!collapsed));
    toggleButton.setAttribute("aria-label", collapsed ? "展开配置中心" : "收起配置中心");
  }

  if (toggleText) {
    toggleText.textContent = collapsed ? sectionToggleLabels.expand : sectionToggleLabels.collapse;
  }
}

function setSectionExpanded(section, expanded) {
  if (!section) return;

  const toggle = section.querySelector(".config-section__toggle");
  const controlsScroller = el("controlsPanelBody");

  const setAria = (value) => {
    if (toggle) toggle.setAttribute("aria-expanded", String(value));
  };

  const closeSection = (targetSection) => {
    const targetToggle = targetSection.querySelector(".config-section__toggle");
    if (targetToggle) targetToggle.setAttribute("aria-expanded", "false");
    targetSection.classList.remove("is-open");
  };

  if (expanded && section.classList.contains("is-collapsible")) {
    document.querySelectorAll(".config-section.is-collapsible").forEach((item) => {
      if (item !== section) closeSection(item);
    });
  }

  if (expanded) {
    section.classList.add("is-open");
    setAria(true);

    requestAnimationFrame(() => {
      if (!controlsScroller) return;
      const sectionRect = section.getBoundingClientRect();
      const scrollerRect = controlsScroller.getBoundingClientRect();
      const extraOffset = 10;
      const deltaTop = sectionRect.top - scrollerRect.top - extraOffset;
      controlsScroller.scrollTo({
        top: controlsScroller.scrollTop + deltaTop,
        behavior: "smooth",
      });
    });
    return;
  }

  closeSection(section);
}

function updatePreview() {
  const exportTypeValue = el("exportType").value;
  state.exportType = formatMap[exportTypeValue];
  state.paperSize = el("paperSize").value;
  state.orientation = orientationMap[el("orientation").value];
  state.fontSize = Number(el("fontSize").value);
  state.lineHeight = Number(el("lineHeight").value);
  state.timeline = timelineMap[getCheckedValue("timeline")];

  updatePreviewVisibility(exportTypeValue);

  const coverEnabled = el("coverPage").checked;
  const tocEnabled = el("toc").checked;
  setPanelEnabled("coverSettingsPanel", coverEnabled);
  setPanelEnabled("tocSettingsPanel", tocEnabled);

  const accentColor = el("accentColor").value;
  document.documentElement.style.setProperty("--primary", accentColor);
  document.documentElement.style.setProperty("--primary-strong", accentColor);

  updatePreviewHeaderBadges();
  el("summaryPreset").textContent = state.preset;
  el("summaryTypography").textContent = `${state.fontSize} pt / ${state.lineHeight.toFixed(1)}`;
  el("summaryTimeline").textContent = state.timeline;

  const documentName = el("documentName").value || "未命名文档";
  if (state.coverTitleAuto && el("coverTitleInput")) {
    el("coverTitleInput").value = documentName;
  }

  updatePreviewFor("doc", documentName);
  updatePreviewFor("pdf", documentName);
  updateSectionSummaries();

  const enhancements = [];
  if (el("speakerLabel").checked) enhancements.push("说话人");
  if (el("bilingual").checked) enhancements.push("双语");
  if (el("keywords").checked) enhancements.push("高亮");
  if (el("notes").checked) enhancements.push("批注区");
  el("summaryEnhancements").textContent = enhancements.length ? enhancements.join(" / ") : "无";

  const isTableLayout = getCheckedValue("layout") === "table";

  document.querySelectorAll(".translation").forEach((node) => {
    node.style.display = el("bilingual").checked ? "block" : "none";
  });

  document.querySelectorAll(".speaker").forEach((node) => {
    node.style.display = el("speakerLabel").checked ? "inline-flex" : "none";
  });

  document.querySelectorAll(".timecode").forEach((node) => {
    const timelineMode = getCheckedValue("timeline");
    const fullTimecode = node.dataset.fullTimecode;
    const formattedTime = formatTimecodeValue(fullTimecode, timelineMode, isTableLayout);

    node.style.display = formattedTime ? "inline-flex" : "none";
    if (formattedTime) node.textContent = formattedTime;
  });

  document.querySelectorAll("mark").forEach((node) => {
    node.style.display = "inline";
    node.style.background = el("keywords").checked ? "rgba(255, 214, 102, 0.44)" : "transparent";
    node.style.padding = el("keywords").checked ? "0 3px" : "0";
  });

  document.body.classList.toggle("show-notes", el("notes").checked);
  document.body.classList.toggle("show-watermark", el("watermark").checked);
}

function applyPreset(presetKey) {
  const preset = presetDefinitions[presetKey];
  if (!preset) return;

  state.preset = preset.name;
  state.sectionTitle = presetContentMap[presetKey]?.title;
  state.sectionDescription = presetContentMap[presetKey]?.description;
  state.coverTitleAuto = preset.coverTitleAuto ?? true;

  fieldIds.forEach((id) => {
    const target = el(id);
    if (!target) return;

    if (target.type === "checkbox") {
      target.checked = Boolean(preset[id]);
      return;
    }

    target.value = preset[id];
  });

  if (state.coverTitleAuto && el("coverTitleInput")) {
    el("coverTitleInput").value = el("documentName").value || "";
  }

  const timelineInput = document.querySelector(`input[name="timeline"][value="${preset.timeline}"]`);
  const layoutInput = document.querySelector(`input[name="layout"][value="${preset.layout}"]`);
  if (timelineInput) timelineInput.checked = true;
  if (layoutInput) layoutInput.checked = true;

  document.querySelectorAll(".preset-chip").forEach((chip) => {
    chip.classList.toggle("is-active", chip.dataset.preset === presetKey);
  });

  updateOutputs();
  updatePreview();
}

function bindEvents() {
  fieldIds.forEach((id) => {
    const target = el(id);
    if (!target) return;

    if (id === "coverTitleInput") {
      target.addEventListener("input", () => {
        const value = el("coverTitleInput")?.value?.trim() || "";
        state.coverTitleAuto = value.length === 0;
        updateOutputs();
        updatePreview();
      });
    } else {
      target.addEventListener("input", () => {
        updateOutputs();
        updatePreview();
      });
    }
    target.addEventListener("change", updatePreview);
  });

  document.querySelectorAll('input[name="timeline"], input[name="layout"]').forEach((input) => {
    input.addEventListener("change", updatePreview);
  });

  document.querySelectorAll(".timecode").forEach((node) => {
    node.dataset.fullTimecode = node.textContent;
  });

  el("previewTabDoc")?.addEventListener("click", () => {
    setActivePreview("doc");
    updatePreview();
  });

  el("previewTabPdf")?.addEventListener("click", () => {
    setActivePreview("pdf");
    updatePreview();
  });

  document.querySelectorAll(".preset-chip").forEach((chip) => {
    chip.addEventListener("click", () => applyPreset(chip.dataset.preset));
  });

  document.querySelectorAll(".config-section.is-collapsible").forEach((section) => {
    const toggle = section.querySelector(".config-section__toggle");
    if (!toggle) return;

    toggle.addEventListener("click", () => {
      const expanded = toggle.getAttribute("aria-expanded") === "true";
      if (expanded) {
        const openSections = document.querySelectorAll(".config-section.is-collapsible.is-open");
        if (openSections.length === 1) return;
        setSectionExpanded(section, false);
        return;
      }

      setSectionExpanded(section, true);
    });
  });

  el("toggleControls")?.addEventListener("click", () => {
    const controlsPanel = el("controlsPanel");
    const isCollapsed = controlsPanel?.classList.contains("is-collapsed");
    setControlsCollapsed(!isCollapsed);
  });

  el("loadPreset").addEventListener("click", () => applyPreset("scriptbook"));

  el("subtitleFile").addEventListener("change", (event) => {
    const input = event.target;
    if (!(input instanceof HTMLInputElement) || !input.files || !input.files.length) return;
    el("fileName").textContent = input.files[0].name;
    updatePreview();
  });
}

bindEvents();
setControlsCollapsed(false);
setSectionExpanded(document.querySelector('.config-section[data-section="upload"]'), true);
applyPreset("scriptbook");
