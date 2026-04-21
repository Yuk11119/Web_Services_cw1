# GenAI Declaration Appendix

## A. Tools Used
- ChatGPT/Codex assistant (planning, debugging support, documentation drafting)

## B. Usage by Task
1. API design planning: endpoint grouping, architecture options, risk checks.
2. Implementation support: scaffolding guidance for routers/services/tests.
3. Documentation support: report structure and wording refinement.

## C. Verification Workflow
- All generated suggestions were manually reviewed before use.
- API behavior was verified through local runs and `pytest` execution.
- Inconsistent or non-applicable suggestions were rejected.

## D. Outcome and Reflection
- GenAI reduced drafting/debugging time and improved exploration breadth.
- Quality depended on strict human validation and domain judgment.
- The final implementation reflects deliberate engineering choices by the student.

## E. Evidence Index
| File | Local Date | Purpose Summary |
|---|---|---|
| `docs/genai_logs/log_2026-04-19_project_planning.md` | 2026-04-19 | Brief interpretation and execution planning evidence |
| `docs/genai_logs/log_2026-04-19_api_build_debug.md` | 2026-04-19 | API scaffolding/debug assistance evidence |
| `docs/genai_logs/log_2026-04-21_report_preparation.md` | 2026-04-21 | Report drafting/refinement assistance evidence |
| `docs/genai_logs/test_evidence_2026-04-21.txt` | 2026-04-21 | Local verification output (`pytest -q`, 6 passed) |

All evidence files are stored under `docs/genai_logs/`.
