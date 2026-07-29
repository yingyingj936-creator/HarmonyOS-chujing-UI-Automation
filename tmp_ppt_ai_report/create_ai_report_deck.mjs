import fs from "node:fs/promises";
import path from "node:path";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const OUT = "C:/Users/jiangyingying/Downloads/AI辅助测试效率提升实践总结.pptx";
const TMP = "D:/chujing_ui_auto/HarmonyOS-chujing-UI-Automation/tmp_ppt_ai_report";
const RENDER = path.join(TMP, "artifact_render");

const W = 1280;
const H = 720;
const C = {
  ink: "#000000",
  muted: "#5F6368",
  light: "#F2F2F2",
  panel: "#EDEDED",
  rule: "#B8BCC4",
  blue: "#3D8DFF",
  blueLight: "#D0EDFA",
  blueMid: "#6DCBF4",
  white: "#FFFFFF",
};
const FONT = "Microsoft YaHei";

async function writeBlob(filePath, blob) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, Buffer.from(await blob.arrayBuffer()));
}

function addBox(slide, x, y, w, h, fill = C.light, line = C.light, radius = "rounded-lg") {
  return slide.shapes.add({
    geometry: "roundRect",
    position: { left: x, top: y, width: w, height: h },
    fill,
    line: { style: "solid", fill: line, width: 1 },
    borderRadius: radius,
  });
}

function addRect(slide, x, y, w, h, fill = C.ink) {
  return slide.shapes.add({
    geometry: "rect",
    position: { left: x, top: y, width: w, height: h },
    fill,
    line: { style: "solid", fill, width: 0 },
  });
}

function addText(slide, text, x, y, w, h, opts = {}) {
  const shape = slide.shapes.add({
    geometry: "textbox",
    position: { left: x, top: y, width: w, height: h },
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  shape.text = text;
  shape.text.style = {
    fontSize: opts.size ?? 22,
    bold: opts.bold ?? false,
    color: opts.color ?? C.ink,
    typeface: opts.font ?? FONT,
    alignment: opts.align ?? "left",
    verticalAlignment: opts.valign ?? "top",
  };
  return shape;
}

function addFooter(slide, page) {
  addText(slide, String(page).padStart(2, "0"), 1184, 658, 54, 26, {
    size: 13,
    color: C.muted,
    align: "right",
  });
}

function addTitle(slide, title, page, subtitle) {
  addText(slide, title, 42, 38, 1010, 86, { size: 36, bold: true });
  if (subtitle) addText(slide, subtitle, 42, 112, 960, 34, { size: 18, color: C.muted });
  addRect(slide, 42, 158, 112, 4, C.blue);
  addFooter(slide, page);
}

function addNotes(slide, text) {
  slide.speakerNotes.textFrame.setText(`[Sources]\n- ${text}\n[/Sources]`);
}

function bullet(lines) {
  return lines.map((line) => `• ${line}`).join("\n");
}

function addMetric(slide, value, label, x, y, w, h, color = C.blue) {
  addBox(slide, x, y, w, h, C.light, C.light, "rounded-lg");
  addText(slide, value, x + 28, y + 28, w - 56, 54, { size: 40, bold: true, color });
  addText(slide, label, x + 28, y + 102, w - 56, h - 122, { size: 18, color: C.ink });
}

function addStep(slide, num, heading, body, x, y, w, h) {
  addBox(slide, x, y, w, h, C.light, C.light, "rounded-lg");
  addText(slide, num, x + 24, y + 22, 72, 40, { size: 26, bold: true, color: C.blue });
  addText(slide, heading, x + 112, y + 23, w - 138, 34, { size: 24, bold: true });
  addText(slide, body, x + 112, y + 70, w - 138, h - 88, { size: 18, color: C.muted });
}

const presentation = Presentation.create({ slideSize: { width: W, height: H } });

// 1 Cover
{
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addText(slide, "测试实践总结", 42, 42, 360, 48, { size: 28 });
  addText(slide, "AI 辅助测试工程落地", 42, 180, 1000, 96, { size: 60, bold: true });
  addText(slide, "出境服务 UI 自动化项目：从 0 到 1 建设可执行、可追踪、可复用的测试资产", 42, 304, 940, 86, { size: 26, color: C.muted });
  addRect(slide, 42, 510, 190, 5, C.blue);
  addText(slide, "关键词：效率提升 / 质量保障 / 真实落地 / 团队复用", 42, 540, 820, 42, { size: 24 });
  addText(slide, "初级功能测试工程师在日常测试之外独立建设", 42, 618, 720, 34, { size: 18, color: C.muted });
  addFooter(slide, 1);
  addNotes(slide, "基于用户提供的项目背景、当前自动化项目实践和本次分享目标整理。");
}

// 2 What leaders care about
{
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addTitle(slide, "AI 的价值不在工具本身，而在落地结果", 2);
  addText(slide, "AI 只有转化成效率、质量和资产，才有交流价值。", 42, 186, 820, 38, { size: 24, color: C.muted });
  addStep(slide, "1", "有没有节省人力和时间", "原来需要人工重复回归的链路，是否能批量自动执行。", 42, 282, 560, 136);
  addStep(slide, "2", "有没有提升质量保障能力", "是否能更早发现页面加载、跳转、数据刷新和状态同步问题。", 678, 282, 560, 136);
  addStep(slide, "3", "有没有真实落地", "能运行、有报告、可维护，不是一次性Demo。", 42, 470, 560, 136);
  addStep(slide, "4", "有没有团队推广价值", "别人是否可以部署、运行、补充用例并持续复用。", 678, 470, 560, 136);
  addNotes(slide, "内容逻辑来自本轮对管理关注点的梳理，未使用外部资料。");
}

// 3 Pain
{
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addTitle(slide, "项目起点是解决真实回归痛点", 3, "不是为了展示 AI，而是为了降低重复测试成本和版本风险");
  addBox(slide, 42, 210, 362, 316, C.light, C.light);
  addText(slide, "手工回归", 72, 246, 280, 38, { size: 26, bold: true });
  addText(slide, bullet(["链路重复执行", "长流程容易漏点", "每次版本都要重新操作"]), 72, 316, 284, 144, { size: 20, color: C.muted });
  addBox(slide, 459, 210, 362, 316, C.light, C.light);
  addText(slide, "HarmonyOS UI", 489, 246, 300, 38, { size: 26, bold: true });
  addText(slide, bullet(["页面结构复杂", "设备差异影响定位", "等待和返回路径容易不稳定"]), 489, 316, 284, 144, { size: 20, color: C.muted });
  addBox(slide, 876, 210, 362, 316, C.light, C.light);
  addText(slide, "结果追溯", 906, 246, 280, 38, { size: 26, bold: true });
  addText(slide, bullet(["失败现场不清晰", "截图依赖人工", "日志排查成本高"]), 906, 316, 284, 144, { size: 20, color: C.muted });
  addText(slide, "结论：需要一套能批量执行、自动留痕、持续维护的 UI 自动化能力。", 42, 596, 1050, 42, { size: 26, bold: true });
  addNotes(slide, "痛点基于当前出境服务 UI 自动化建设过程中的实际问题归纳。");
}

// 4 AI participation
{
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addTitle(slide, "AI 参与的是测试全流程，而不是只写代码", 4);
  addText(slide, "我负责业务判断和落地取舍，AI 负责提升拆解、实现、排查和优化效率。", 42, 160, 1000, 34, { size: 24, color: C.muted });
  const xs = [42, 344, 646, 948];
  const heads = ["需求拆解", "代码实现", "失败排查", "维护优化"];
  const bodys = [
    "将业务描述转成前置条件、步骤、预期和自动化断言点。",
    "按项目风格生成 pytest 用例、页面对象和公共方法。",
    "根据日志判断页面未加载、定位不稳、状态污染或业务缺陷。",
    "识别重复 UI 查询、固定等待、冗余截图和不稳定 XPath。",
  ];
  xs.forEach((x, i) => {
    addText(slide, String(i + 1).padStart(2, "0"), x, 236, 64, 42, { size: 30, bold: true, color: C.blue });
    addRect(slide, x, 295, 216, 3, i === 3 ? C.blue : C.rule);
    addText(slide, heads[i], x, 326, 236, 38, { size: 26, bold: true });
    addText(slide, bodys[i], x, 386, 234, 126, { size: 19, color: C.muted });
  });
  addText(slide, "关键变化：从“人工经验一次性执行”，变成“经验沉淀为可重复运行的代码资产”。", 42, 612, 1100, 38, { size: 26, bold: true });
  addNotes(slide, "AI 应用方式来自当前项目的需求拆解、代码生成、日志分析和优化实践。");
}

// 5 Results metrics
{
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addTitle(slide, "已经形成可运行的自动化测试资产", 5);
  addMetric(slide, "约69条", "已沉淀 UI 自动化用例，覆盖核心回归链路", 42, 205, 270, 176);
  addMetric(slide, "约50分钟", "当前全量自动化执行耗时，替代大量重复手工操作", 353, 205, 270, 176, C.blue);
  addMetric(slide, "6+模块", "首页、搜索、路线、行程、附近、我的等核心模块", 664, 205, 270, 176, C.blue);
  addMetric(slide, "可追溯", "Allure 中文步骤、截图、断言圈选、失败留痕", 975, 205, 263, 176, C.blue);
  addText(slide, "已具备的工程化能力", 42, 456, 360, 36, { size: 26, bold: true });
  addText(slide, bullet(["pytest + Hypium 自动执行", "Page Object 页面对象封装", "Allure 可视化报告", "运行文档与 Jenkinsfile 基础配置"]), 42, 510, 520, 120, { size: 21, color: C.muted });
  addText(slide, "这意味着项目不是一次性脚本，而是后续可以扩展和维护的测试基础设施。", 664, 488, 500, 112, { size: 28, bold: true });
  addNotes(slide, "量化数字来自用户提供的当前项目情况：约69条用例、全量执行约50分钟、覆盖核心模块并具备Allure报告和Jenkinsfile。");
}

// 6 Efficiency comparison
{
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addTitle(slide, "和不用 AI 前相比，提升发生在多个环节", 6);
  const rows = [
    ["用例设计", "人工逐条拆，容易遗漏", "AI 辅助拆步骤、预期和断言点"],
    ["代码编写", "从零封装成本高", "生成骨架后人工校验并落地"],
    ["失败排查", "人工翻日志定位慢", "AI 辅助归因到等待、定位或状态"],
    ["测试报告", "手工截图和描述", "自动生成步骤、截图和圈选证据"],
    ["团队复用", "依赖个人经验", "框架、公共方法、文档可延续"],
  ];
  addRect(slide, 42, 172, 1196, 2, C.ink);
  addText(slide, "环节", 58, 194, 180, 32, { size: 20, bold: true });
  addText(slide, "不用 AI 前", 292, 194, 350, 32, { size: 20, bold: true });
  addText(slide, "使用 AI 后", 742, 194, 420, 32, { size: 20, bold: true, color: C.blue });
  rows.forEach((r, idx) => {
    const y = 244 + idx * 74;
    addRect(slide, 42, y - 10, 1196, 1, C.rule);
    addText(slide, r[0], 58, y, 180, 34, { size: 20, bold: true });
    addText(slide, r[1], 292, y, 350, 44, { size: 19, color: C.muted });
    addText(slide, r[2], 742, y, 430, 44, { size: 19, color: C.ink });
  });
  addRect(slide, 42, 614, 1196, 2, C.ink);
  addNotes(slide, "对比项基于当前项目中 AI 辅助测试设计、开发、排查、报告和文档沉淀的实际使用方式。");
}

// 7 Quality value
{
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addTitle(slide, "质量价值体现在更早、更稳定、更可追溯", 7);
  addBox(slide, 42, 210, 354, 292, C.light, C.light);
  addText(slide, "更早发现风险", 72, 246, 270, 38, { size: 26, bold: true });
  addText(slide, "版本回归时批量验证核心链路，提前暴露页面加载、跳转、数据刷新和状态同步问题。", 72, 320, 270, 120, { size: 21, color: C.muted });
  addBox(slide, 463, 210, 354, 292, C.light, C.light);
  addText(slide, "长链路可重复", 493, 246, 270, 38, { size: 26, bold: true });
  addText(slide, "路线、行程、收藏、附近等长流程可以沉淀成固定用例，减少人工漏测。", 493, 320, 270, 120, { size: 21, color: C.muted });
  addBox(slide, 884, 210, 354, 292, C.light, C.light);
  addText(slide, "失败现场可追溯", 914, 246, 270, 38, { size: 26, bold: true });
  addText(slide, "Allure 报告保留中文步骤、截图和圈选区域，便于开发、产品和测试共同定位。", 914, 320, 270, 120, { size: 21, color: C.muted });
  addText(slide, "项目过程中已辅助暴露真实业务问题，例如点赞状态同步异常。", 42, 596, 960, 42, { size: 26, bold: true });
  addNotes(slide, "质量价值和真实问题示例来自当前项目测试过程中对点赞状态异常、页面等待和状态同步问题的讨论。");
}

// 8 Division of labor
{
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addTitle(slide, "AI 没有替代测试判断，而是放大执行能力", 8);
  addBox(slide, 42, 214, 534, 300, C.light, C.light);
  addText(slide, "AI 负责提速", 78, 250, 320, 42, { size: 30, bold: true, color: C.blue });
  addText(slide, bullet(["快速拆解场景", "生成代码骨架", "分析失败日志", "提示重复和不稳定实现"]), 78, 324, 390, 150, { size: 22, color: C.muted });
  addBox(slide, 704, 214, 534, 300, C.light, C.light);
  addText(slide, "测试人员负责正确性", 740, 250, 380, 42, { size: 30, bold: true });
  addText(slide, bullet(["判断业务是否符合预期", "选择关键断言", "确认定位是否稳定", "识别环境问题和真实缺陷"]), 740, 324, 410, 150, { size: 22, color: C.muted });
  addText(slide, "真正的提升：把业务经验转化成稳定、可复用、可持续维护的自动化资产。", 42, 596, 1080, 44, { size: 28, bold: true });
  addNotes(slide, "本页为项目方法论总结，基于当前自动化项目中 AI 和测试人员分工的实际实践。");
}

// 9 Reuse and influence
{
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addTitle(slide, "项目价值不止于个人效率，还能沉淀为团队能力", 9);
  addText(slide, "影响范围", 42, 190, 220, 36, { size: 26, bold: true });
  addText(slide, bullet(["覆盖出境服务核心模块", "支持版本回归前批量验证", "报告可给开发、产品同步查看"]), 42, 248, 430, 118, { size: 22, color: C.muted });
  addText(slide, "复用方式", 664, 190, 220, 36, { size: 26, bold: true });
  addText(slide, bullet(["新增用例复用页面对象", "公共等待、截图、圈选统一封装", "运行文档降低其他同学上手成本"]), 664, 248, 480, 118, { size: 22, color: C.muted });
  addRect(slide, 42, 430, 1196, 2, C.rule);
  addText(slide, "后续如果接入定时执行，就可以从“临时跑用例”升级为“版本固定质量门禁”。", 42, 490, 980, 56, { size: 32, bold: true });
  addText(slide, "这也是 AI 落地最大的价值：个人能力提升后，继续沉淀成团队可复制流程。", 42, 580, 980, 38, { size: 23, color: C.muted });
  addNotes(slide, "复用能力来自当前项目已有的页面对象、公共方法、Allure报告、运行文档和Jenkinsfile基础配置。");
}

// 10 Next plan
{
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addTitle(slide, "下一步重点是稳定性、常态化和团队化", 10);
  addStep(slide, "1", "稳定性治理", "继续降低设备差异、页面状态污染、等待不足和不稳定定位带来的失败率。", 42, 204, 560, 128);
  addStep(slide, "2", "失败原因分类", "统计业务缺陷、环境问题、定位问题、数据问题，形成可复盘的质量看板。", 678, 204, 560, 128);
  addStep(slide, "3", "CI 定时执行", "将自动化回归接入固定执行节奏，减少版本末期集中回归压力。", 42, 392, 560, 128);
  addStep(slide, "4", "团队规范沉淀", "把AI辅助用例设计、日志分析、自动化开发方法沉淀给更多测试同学。", 678, 392, 560, 128);
  addText(slide, "收束：AI 的价值不是“尝鲜”，而是把测试能力沉淀成工程资产。", 42, 610, 1120, 48, { size: 26, bold: true });
  addNotes(slide, "后续规划基于当前自动化项目已有成果和仍需优化的问题归纳。");
}

await fs.mkdir(RENDER, { recursive: true });
for (const [index, slide] of presentation.slides.items.entries()) {
  const stem = `slide-${String(index + 1).padStart(2, "0")}`;
  await writeBlob(path.join(RENDER, `${stem}.png`), await presentation.export({ slide, format: "png", scale: 1 }));
  await fs.writeFile(path.join(RENDER, `${stem}.layout.json`), await (await slide.export({ format: "layout" })).text());
}
await writeBlob(path.join(RENDER, "deck-montage.webp"), await presentation.export({ format: "webp", montage: true, scale: 1 }));
const pptx = await PresentationFile.exportPptx(presentation);
await pptx.save(OUT);
console.log(OUT);

