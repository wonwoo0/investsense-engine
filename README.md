# Kazuha Invest 2.0 (InvestSense)

**InvestSense** is the engine core of Kazuha Invest 2.0, an automated investment intelligence system designed to hunt for alpha, assess risks, and generate professional-grade briefings.

## 🚀 Key Features

- **Scout-Reasoning Loop**: A closed-loop system where automated scouts gather intelligence, and reasoning agents (or humans) analyze it to generate new search missions.
- **Multi-Agent Architecture**:
    - **Scout**: Distributed gathering of signals (Themes, Gov Contracts, Github, Social).
    - **Shield**: Defensive monitoring of portfolio holdings.
    - **Brain**: Context generation and reasoning support.
- **Quantifiable Rubric**: Rigorous scoring system for Alpha Confidence and Risk Assessment.

## 📂 Project Structure

- **`src/`**: Core python source code for Scouts (`scout_*.py`) and Brain (`brain_*.py`).
- **`data/`**: (Private) Registry for themes, active missions, and generated reports.
- **`prompts/`**: LLM prompts for various expert personas and reasoning stages.
- **`docs/`**: Documentation and manuals.
    - **`manuals/`**: Operational guides (Workflow, Reasoning Flow).
    - **`PRD/`**: Product Requirements Documents.

## 📖 Documentation

For detailed operational procedures, please refer to the manuals in `docs/manuals/`:

- **[Operational Workflow](docs/manuals/WORKFLOW.md)**: The "Vibe-Hunter" closed loop system overview and schedule.
- **[Reasoning Flow](docs/manuals/REASONING_FLOW.md)**: The "Manual Pilot" V7 protocol for analyzing context and generating the Daily Alpha Briefing.

## 🛠️ Quick Start

### Prerequisites
- Python 3.10+
- `uv` package manager (recommended)

### Installation

```bash
# Install dependencies
uv sync
```

### Usage

**Running the Scout (Hunter):**
```bash
python src/scout_hunter.py
```

**Generating Reasoning Context:**
```bash
python src/brain_reasoning.py
```

**Running the Dedup Logic:**
```bash
python src/scout_dedup.py
```

---
*Powered by Kazuha Invest Engine*