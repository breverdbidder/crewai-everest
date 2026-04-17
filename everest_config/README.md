# Everest Config — CrewAI Tenants & Crews

Everest-specific configuration on top of CrewAI MIT core. Clean vendor boundary: do NOT modify files outside `everest_config/`.

## Files
- `tenants.yaml` — SSOT mapping of 8 Everest tenants to their Crews
- `crews/` — One Python file per Crew; `build_<tenant>_crew()` signature
- `tools/` — Custom Tool classes wrapping MOS marketingskills + ai-marketing-skills

## Adding a new tenant
1. Add entry to `tenants.yaml`
2. Create `crews/<tenant>.py` following `zonewise.py` template
3. Add test in `tests/test_crews.py`

## Why CrewAI not Suna
Suna is Elastic License 2.0 which blocks multi-tenant SaaS. CrewAI is MIT. See repo_evaluations score 92.
