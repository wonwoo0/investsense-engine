# PRD: Kazuha Invest 2.0 - Vibe-Hunter Closed Loop Execution

## TL;DR
- Execute the full intelligence cycle: Run local scout scripts, consolidate data, generate analysis context, extract new keywords into `active_missions.yml`, and sync changes via Git to trigger the next cloud loop.

## Goal
- Complete one iteration of the "Vibe-Hunter 2.2" loop locally:
  1. **Scout**: Run `scout_hunter.py`, `scout_shield.py`, `scout_gov.py`, and `scout_social.py` to gather raw intelligence.
  2. **Consolidate**: Run `scout_dedup.py` to merge and deduplicate findings.
  3. **Context**: Run `brain_reasoning.py` to generate the analysis context and archive raw data.
  4. **Evolve**: Identify data gaps or new keywords from the findings and append them to `data/active_missions.yml`.
  5. **Sync**: Commit and push the updated `active_missions.yml` and Reports to the repository.

## Constraints
- Must use existing Python scripts in the root directory.
- `data/active_missions.yml` must only be appended to (or updated with valid YAML), never corrupted.
- Git commit message must follow the convention: "Manual Analysis: missions updated [skip ci]" (or similar to avoid infinite loop if needed, though workflow says it feeds the action).
- Ensure Python environment has necessary dependencies installed before running.

## Acceptance Criteria
- [ ] All scout scripts (`scout_*.py`) executed without fatal errors.
- [ ] `scout_dedup.py` and `brain_reasoning.py` executed successfully.
- [ ] `data/Reports/YYYYMMDD/Context_Input.md` (or similar output) is generated.
- [ ] `data/active_missions.yml` contains at least one updated/verified mission or confirmed "no change" status.
- [ ] Changes are committed to Git and pushed to remote `main` (or current) branch.
- [ ] Output: <promise>COMPLETE</promise>

## Verification
- Check terminal output for successful execution of all `.py` scripts.
- Read `data/active_missions.yml` to verify format validity.
- Run `git log -1` to verify the commit exists.
- Run `git status` to ensure working directory is clean (everything pushed).

## Notes
- If `active_missions.yml` has expired missions, they should be handled by the logic in `scout_hunter.py` or manually cleaned if required.
- The loop is self-reinforcing: findings in this run become the seeds for the next GitHub Action run.

## Progress

### Initial Run - 2026-01-16

- Summary: Starting the Vibe-Hunter Closed Loop.
- Decisions: Will run scripts sequentially to ensure data dependency integrity (Scout -> Dedup -> Reasoning -> Git).
- Assumptions: Python environment is set up. GitHub credentials are configured for push.
- Risks: Network timeouts during scraping; Git merge conflicts.
- Status: Pending
- Best guess at what comes next & why:
  - Run scout scripts to gather fresh data.
