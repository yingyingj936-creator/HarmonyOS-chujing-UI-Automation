import fs from "node:fs/promises";
import path from "node:path";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const OUT = "C:/Users/jiangyingying/Downloads/AI辅助测试价值与落地效果.pptx";
const TMP = "D:/chujing_ui_auto/HarmonyOS-chujing-UI-Automation/tmp_ppt_ai_value";
const RENDER = path.join(TMP, "render");

const W = 1280;
const H = 720;
const C = {
  ink: "#0B0B0C",
  muted: "#5F6368",
  panel: "#F1F3F5",
  rule: "#CAD0D7",
  blue: "#2F80ED",
  blueSoft: "#DCEBFF",
  white: "#FFFFFF",
};
const FONT = "Microsoft YaHei";

async function writeBlob(filePath, blob) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, Buffer.from(await blob.arrayBuffer()));
}

function addShape(slide, geometry, x, y, w, h, fill = "none", line = "none") {
  return slide.shapes.add({
    geometry,
    position: { left: x, top: y, width: w, height: h },
    fill,
    line: { style: "solid", fill: line, width: line === "none" ? 0 : 1 },
  });
}

function addText(slide, text, x, y, w, h, opts = {}) {
  const box = addShape(slide, "textbox", x, y, w, h, "none", "none");
  box.text = text;
  box.text.style = {
    fontSize: opts.size ?? 22,
    bold: opts.bold ?? false,
    color: opts.color ?? C.ink,
    typeface: FONT,
    alignment: opts.align ?? "left",
    verticalAlignment: opts.valign ?? "top",
  };
  return box;
}

function addRule(slide, x, y, w, color = C.blue) {
  addShape(slide, "rect", x, y, w, 5, color, color);
}

function addFooter(slide, page) {
  addText(slide, String(page).padStart(2, "0"), 1184, 658, 54, 26, { size: 13, color: C.muted, align: "right" });
}

function addCard(slide, title, body, x, y, w, h, number) {
  const card = slide.shapes.add({
    geometry: "roundRect",
    position: { left: x, top: y, width: w, height: h },
    fill: C.panel,
    line: { style: "solid", fill: C.panel, width: 1 },
    borderRadius: "rounded-lg",
  });
  addText(slide, number, x + 26, y + 24, 54, 44, { size: 30, bold: true, color: C.blue });
  addText(slide, title, x + 96, y + 26, w - 126, 38, { size: 25, bold: true });
  addText(slide, body, x + 96, y + 78, w - 126, h - 92, { size: 18, color: C.muted });
  return card;
}

function addMetric(slide, value, label, x, y, w, h) {
  slide.shapes.add({
    geometry: "roundRect",
    position: { left: x, top: y, width: w, height: h },
    fill: C.panel,
    line: { style: "solid", fill: C.panel, width: 1 },
    borderRadius: "rounded-lg",
  });
  addText(slide, value, x + 28, y + 25, w - 56, 52, { size: 38, bold: true, color: C.blue });
  addText(slide, label, x + 28, y + 90, w - 56, h - 104, { size: 19, color: C.ink });
}

function setNotes(slide, text) {
  slide.speakerNotes.textFrame.setText(`[Sources]\n- ${text}\n[/Sources]`);
}

const presentation = Presentation.create({ slideSize: { width: W, height: H } });

// Slide 1: Value
{
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addText(slide, "AI 辅助测试带来的核心价值", 52, 48, 980, 66, { size: 42, bold: true });
  addRule(slide, 52, 142, 140);
  addText(slide, "不是单纯提升写脚本速度，而是把重复测试、问题排查和结果留痕转化成工程化能力。", 52, 182, 1040, 42, { size: 24, color: C.muted });

  addCard(slide, "节省重复回归人力", "首页、搜索、行程、路线、附近、我的等高频链路自动化，减少版本回归中的重复点击。", 52, 282, 560, 150, "1");
  addCard(slide, "提升质量发现效率", "批量验证页面加载、跳转、数据刷新和状态同步，更早发现回归风险。", 668, 282, 560, 150, "2");
  addCard(slide, "降低失败排查成本", "测试报告自动记录中文步骤、截图和断言圈选，失败时快速还原现场。", 52, 462, 560, 150, "3");
  addCard(slide, "形成可复用资产", "页面对象、公共等待、运行文档和 CI 配置沉淀，便于团队后续扩展。", 668, 462, 560, 150, "4");

  addFooter(slide, 1);
  setNotes(slide, "基于当前出境服务 UI 自动化项目实践总结，未使用外部资料。");
}

// Slide 2: Landing effect
{
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addText(slide, "目前已经落地的实际效果", 52, 48, 980, 66, { size: 42, bold: true });
  addRule(slide, 52, 142, 140);
  addText(slide, "项目已经从个人尝试推进到可运行、可追踪、可维护的自动化测试资产。", 52, 182, 980, 42, { size: 24, color: C.muted });

  addMetric(slide, "约69条", "已沉淀 UI 自动化用例，覆盖核心回归链路", 52, 278, 272, 152);
  addMetric(slide, "约50分钟", "当前全量自动化执行耗时，替代大量重复手工操作", 356, 278, 272, 152);
  addMetric(slide, "6+模块", "覆盖首页、搜索、路线、行程、附近、我的等模块", 660, 278, 272, 152);
  addMetric(slide, "可追溯", "报告包含中文步骤、截图、断言圈选和失败留痕", 964, 278, 264, 152);

  addText(slide, "已经具备的工程化能力", 52, 498, 390, 36, { size: 26, bold: true });
  addText(slide, "• pytest + Hypium 自动执行\n• Page Object 页面对象封装\n• Allure 可视化报告\n• 运行文档与 Jenkinsfile 基础配置", 52, 552, 520, 120, { size: 21, color: C.muted });

  addText(slide, "落地结论", 706, 500, 240, 36, { size: 26, bold: true, color: C.blue });
  addText(slide, "实际价值已经体现在测试效率提升、质量风险前置暴露、失败证据可追溯和团队资产复用上。", 706, 552, 470, 96, { size: 24, bold: true });

  addFooter(slide, 2);
  setNotes(slide, "量化信息来自当前项目实践：约69条用例、全量执行约50分钟、覆盖多个核心模块并支持Allure报告。");
}

await fs.mkdir(RENDER, { recursive: true });
for (const [index, slide] of presentation.slides.items.entries()) {
  const stem = `slide-${String(index + 1).padStart(2, "0")}`;
  await writeBlob(path.join(RENDER, `${stem}.png`), await presentation.export({ slide, format: "png", scale: 1 }));
  await fs.writeFile(path.join(RENDER, `${stem}.layout.json`), await (await slide.export({ format: "layout" })).text());
}
await writeBlob(path.join(RENDER, "montage.webp"), await presentation.export({ format: "webp", montage: true, scale: 1 }));
const pptx = await PresentationFile.exportPptx(presentation);
await pptx.save(OUT);
console.log(OUT);
