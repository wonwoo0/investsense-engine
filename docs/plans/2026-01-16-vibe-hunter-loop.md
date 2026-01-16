# Vibe-Hunter Loop Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task.

**Goal:** Execute the full intelligence cycle: Run local scout scripts, consolidate data, generate analysis context, extract new keywords, and sync changes.

**Architecture:** Sequential execution of Python scripts (`scout_*.py` -> `scout_dedup.py` -> `brain_reasoning.py`) reading/writing to `data/` directory and commiting to Git.

**Tech Stack:** Python 3.9+, Git

### Task 1: Environment Setup

**Files:**
- Modify: `pyproject.toml` (if needed, but likely just install)

**Step 1: Install Dependencies**
Run: `pip install -r requirements.txt` (if exists) or `pip install duckduckgo-search requests pyyaml python-dotenv google-generativeai python-telegram-bot feedparser sentence-transformers scikit-learn numpy` based on `pyproject.toml`.
Actually better: `pip install .` or manual install of deps.

**Step 2: Verify Import**
Run: `python -c "import duckduckgo_search; import yaml; print('Imports OK')"`
Expected: "Imports OK"

### Task 2: Execute Scout Scripts

**Files:**
- Run: `src/scout_hunter.py`
- Run: `src/scout_shield.py`
- Run: `src/scout_gov.py`
- Run: `src/scout_social.py`

**Step 1: Run Scout Hunter**
Run: `python src/scout_hunter.py`
Expected: Output "Captured X signals to data/Incoming/..."

**Step 2: Run Scout Shield**
Run: `python src/scout_shield.py`
Expected: Success output.

**Step 3: Run Scout Gov**
Run: `python src/scout_gov.py`
Expected: Success output.

**Step 4: Run Scout Social**
Run: `python src/scout_social.py`
Expected: Success output.

**Step 5: Verify Data Incoming**
Run: `ls -F data/Incoming/`
Expected: JSON files present.

### Task 3: Consolidate Findings

**Files:**
- Run: `src/scout_dedup.py`

**Step 1: Run Dedup**
Run: `python src/scout_dedup.py`
Expected: Output "Consolidated X findings..." and creation of `data/Incoming/deduped_*.json` (or similar).

### Task 4: Generate Context & Evolve

**Files:**
- Run: `src/brain_reasoning.py`

**Step 1: Run Reasoning**
Run: `python src/brain_reasoning.py`
Expected: Output "Context generated..." and update to `data/active_missions.yml`.

**Step 2: Verify Outputs**
Run: `cat data/active_missions.yml`
Expected: Valid YAML with potentially new missions.
Run: `ls -R data/Reports/`
Expected: New Report/Context file.

### Task 5: Git Sync

**Files:**
- Git commands

**Step 1: Check Status**
Run: `git status`

**Step 2: Commit and Push**
Run: `git add data/active_missions.yml data/Reports/`
Run: `git commit -m "Manual Analysis: missions updated [skip ci]"`
Run: `git push`

