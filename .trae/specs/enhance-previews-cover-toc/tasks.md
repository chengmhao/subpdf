# Tasks

- [x] Task 1: 梳理现状并建立预览目标结构
  - [x] 确认现有导出格式选择（DOCX/PDF/BOTH）与预览 DOM 结构
  - [x] 定义 DOC 预览与 PDF 预览的容器结构与切换规则（含 BOTH Tab）

- [x] Task 2: 增加封面页/目录页独立配置面板（条件显示）
  - [x] 在“文档规格/结构”区域新增“封面页设置”面板（仅 coverPage 启用时可编辑）
  - [x] 在“文档规格/结构”区域新增“目录页设置”面板（仅 toc 启用时可编辑）
  - [x] 为上述面板补齐最小字段（见 spec.md），并接入状态/默认值

- [x] Task 3: 实现 DOC/PDF 双预览与切换
  - [x] 新增 DOC 预览容器（Word/Office 风格外壳 + 纸张画布）
  - [x] 新增 PDF 预览容器（PDF 阅读器风格外壳 + 纸张画布）
  - [x] 根据导出格式显示对应预览：docx=>DOC、pdf=>PDF、both=>Tab
  - [x] 预览信息条（格式、纸张、方向）与当前预览类型同步

- [x] Task 4: 将封面/目录配置映射到两个预览
  - [x] DOC 预览：渲染封面页与目录页（可见差异与样式）
  - [x] PDF 预览：渲染封面页与目录页（可见差异与样式）
  - [x] 切换 coverPage/toc 开关时实时更新两种预览

- [x] Task 5: 预览“更真实”的视觉增强（不引入新依赖）
  - [x] DOC 预览：增加 Word 类工具条/状态栏、页边距提示、标题层级样式
  - [x] PDF 预览：增加 PDF 工具条、固定布局感、渲染差异（字体/抗锯齿/字距模拟）

- [x] Task 6: 验证与回归
  - [x] 验证折叠配置中心与滚动不受影响
  - [x] 验证导出格式切换时预览切换正确且无布局溢出
  - [x] 更新 checklist.md 勾选通过项

# Task Dependencies
- Task 3 depends on Task 1
- Task 4 depends on Task 2 and Task 3
- Task 5 depends on Task 3
- Task 6 depends on Task 2, Task 3, Task 4, Task 5
