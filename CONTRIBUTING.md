# Contributing

> English version of [CONTRIBUTING_CN.md](CONTRIBUTING_CN.md). If they differ, the Chinese version wins.

The evidence list exists in two files: [`EVIDENCE_CN.md`](EVIDENCE_CN.md) (the Chinese master) and [`EVIDENCE.md`](EVIDENCE.md) (the English mirror). You may edit either one, but every change must be made in both, with identical IDs. `python tools/sync_evidence.py` checks ID parity between the two files and fails if they differ.

The easiest way to start is to open an issue with one of the GitHub issue templates in [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/):

- **New evidence**: propose a new item or a change to an existing one.
- **Field report**: describe an anonymized case from real reviewing.
- **False positive**: report a human-written paper that an item flagged wrongly.

## 1. Adding an item of evidence

1. Add a row at the end of the table for the relevant layer in both `EVIDENCE.md` and `EVIDENCE_CN.md`, continuing the numbering (e.g. `S19`). The columns are, in order: ID | Evidence | Typical form / example | Strength | Axis (S/R/P tables) | False-positive note | Sources.
2. Start with a conservative strength (★ or ★★). Raising an item to ★★★ requires at least two independent sources or two or more real cases, and at least one human counter-example checked to confirm it does not trigger; record false positives in `docs/field_reports/false_positives/`. Reserve ☠ for cases where a single occurrence shows that nobody checked the paper.
3. A false-positive note is required: at least one case in which humans also write this way.
4. Register the source key in `docs/SOURCES.md`, with its link, type, verification status and key points. For something you met while reviewing, use `[Internal-YYYYMMDD-abbrev]` and leave an anonymized record under `docs/field_reports/`.
5. Add one action row each to `skills/paper-author-pass/references/polish-actions.md` and `skills/paper-slop-screen/references/screen-actions.md`, and one English index row to `docs/evidence-index-en.md`.
6. Run `python tools/sync_evidence.py`. It reports an error if an ID is missing a corresponding action, or if the IDs in `EVIDENCE.md` and `EVIDENCE_CN.md` differ.
7. Add an entry to `CHANGELOG.md`.

## 2. Submitting a reviewing field report

Copy `TEMPLATE.md` in `docs/field_reports/` and name the file `YYYYMMDD-field-abbrev.md` (or start from the "Field report" issue template). **It must be anonymized**: no paper title, ID or authors; quote only the necessary parts of sentences; and first confirm that doing so does not breach the venue's confidentiality rules (usually this means waiting until reviewing has ended or the paper is public).

## 3. Changing the strength of an item or removing it

Write the reason in `CHANGELOG.md`, for example "calibration shows an AUC of only 0.45" or "newer models no longer have this habit". Do not make silent changes. Apply the change to both evidence files.

## 4. Changing the lint

- After changing a check, run `python tools/test_slop_lint.py`.
- If you have a corpus, rerun calibration: `python tools/calibration/run_calibration.py --scratch <dir> --write-tool`.
- Every check must correspond to an EVIDENCE ID; a new check is marked weak until there are calibration data for it.

## Principles

- Evidence must be observable and locatable. "Feels like AI" does not count.
- L-layer evidence supports only the writing axis (W), not the research axis (R).
- Social media posts count only as reader observations, not as consensus.
- We do not collect or publish accusations against specific individuals.
