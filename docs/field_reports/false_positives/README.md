# 误判登记 / False-positive registry

记录筛查结论出错的案例（匿名化）：用了哪条证据、为什么是误判、清单需要怎么改。
Cases where the list or the lint was wrong, what fired, why it was wrong, and what we changed.

| ID | 报告 Report | 触发 What fired | 原因 Why it was a false positive | 处理 Fix |
|---|---|---|---|---|
| FP-001 | [#1](https://github.com/THUROI0787/absent-author/issues/1) | L01 `spaced_double_hyphen`, S03 `published_draft` | CRediT role names ("Writing -- original draft", "Writing -- review & editing") are a publisher-mandated taxonomy. Three human economics manuscripts got S03 `high` from their contribution statement alone. | lint 0.2.1 drops matches inside CRediT role names for L01 and S03; S03 false-positive note updated. |
| FP-002 | [#2](https://github.com/THUROI0787/absent-author/issues/2) | P02-todo `undefined_ref_labels` | Labels set inside a user macro (`\label{#3}` in a `\newcommand` body) resolve in LaTeX, but the lint only saw literal `\label{...}`. | lint 0.2.1 expands label macros (`\newcommand`, `\def`); if a label macro cannot be expanded, unresolved refs become an info note pointing to the compile log. |
| FP-003 | [#3](https://github.com/THUROI0787/absent-author/issues/3) | S01 `this_does_not_mean` | In theory writing, "Assumption 2 … does not imply …" states a logical relation between mathematical objects, the kind of scope condition authors should keep. | lint 0.2.1 skips "does not imply" when a mathematical object or inline math precedes it in the same sentence; S01 false-positive note updated. |

Thanks to the reporters. Every entry here came with a minimal reproduction, which made the fix straightforward.
