# 如何贡献

## 1. 补充一条证据

1. 在 `EVIDENCE_CN.md` 对应层级的表格末尾加一行，编号顺延（如 `S19`）。列依次是：ID｜证据｜典型表现 / 例句｜强度｜轴（S/R/P 表）｜误判提醒｜来源。
2. 强度先保守地标（★ 或 ★★）。至少要有两个独立来源，或者两个以上的真实案例，才能上调到 ★★★，并且至少检查过一篇人类反例，确认它不会触发；误判记入 `docs/field_reports/false_positives/`。☠ 只留给"出现一次就说明没人核查过"的情况。
3. 必须写误判提醒：至少一种人类也会这样写的情形。
4. 在 `docs/SOURCES.md` 登记来源键，写明链接、类型、核实状态和要点。自己审稿时遇到的，用 `[Internal-YYYYMMDD-缩写]`，并在 `docs/field_reports/` 下留一份匿名化记录。
5. 在 `skills/paper-author-pass/references/polish-actions.md` 和 `skills/paper-slop-screen/references/screen-actions.md` 里各加一行动作，并在 `docs/evidence-index-en.md` 里加一行英文索引。
6. 运行 `python tools/sync_evidence.py`。如果某个 ID 缺少对应动作，脚本会报错。
7. 在 `CHANGELOG.md` 里记一笔。

## 2. 提交审稿 field report

在 `docs/field_reports/` 下复制 `TEMPLATE.md`，文件名用 `YYYYMMDD-领域-缩写.md`。**必须匿名化**：不写论文标题、ID 或作者，原句只摘取必要的部分，而且要先确认这样做不违反所在会议的保密规定（通常需要等审稿结束或论文公开以后再写）。

## 3. 调整强度或删除证据

把理由写进 `CHANGELOG.md`，例如"校准显示 AUC 只有 0.45"或"新模型不再有这个习惯"。不要悄悄修改。

## 4. 修改 lint

- 修改检查项以后，运行 `python tools/test_slop_lint.py`。
- 如果有语料，重新运行校准：`python tools/calibration/run_calibration.py --scratch <dir> --write-tool`。
- 每个检查项必须对应一个 EVIDENCE ID；新加的检查项在没有校准数据之前都标为 weak。

## 原则

- 证据必须可观察、可定位。"感觉像 AI"不算。
- L 层证据只支撑写作轴（W），不支撑研究轴（R）。
- 社交帖子只算读者观察，不算共识。
- 不收录、也不发布针对具体个人的指控。
