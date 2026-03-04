# Clara AI — Automated Voice Agent Configuration Pipeline

An automated zero-cost pipeline that converts demo and onboarding call transcripts into structured, deployment-ready AI voice agent configurations for Clara Answers.

---

## What This Does
```
Demo Call Transcript
       ↓
[Pipeline A] → Account Memo JSON (v1) + Retell Agent Spec (v1)
       ↓
Onboarding Call Transcript
       ↓
[Pipeline B] → Updated Memo (v2) + Agent Spec (v2) + Changelog
```

---

## Tech Stack (Zero Cost)

| Layer | Tool | Why |
|-------|------|-----|
| LLM | Groq API (Llama 3.3 70B) | Free tier, fast, powerful |
| Storage | Local JSON + GitHub | Zero cost, fully reproducible |
| Scripting | Python 3.12 | Batch processing, clean modules |
| Dashboard | HTML + Vanilla JS | No dependencies, runs anywhere |

---

## Project Structure
```
clara-ai-pipeline/
├── data/                        # Input transcripts (demo + onboarding)
├── outputs/
│   └── accounts/
│       └── ACC-001/
│           ├── v1/
│           │   ├── account_memo.json
│           │   └── agent_spec.json
│           └── v2/
│               ├── account_memo.json
│               ├── agent_spec.json
│               └── changelog.json
├── scripts/
│   ├── extract.py               # LLM extraction from transcript
│   ├── generate_agent.py        # Agent spec + prompt generator
│   ├── batch_pipeline_a.py      # Run Pipeline A on all demo files
│   ├── batch_pipeline_b.py      # Run Pipeline B on all onboarding files
│   └── generate_mock_data.py    # Generate mock transcripts for testing
├── prompts/
│   ├── extract_demo.txt         # Extraction prompt for demo calls
│   └── extract_onboarding.txt   # Extraction prompt for onboarding calls
├── dashboard/
│   └── index.html               # Visual dashboard with v1→v2 diff viewer
├── workflows/                   # n8n workflow export (architecture reference)
├── .env.example                 # Environment variable template
└── README.md
```

---

## Setup

### Prerequisites
- Python 3.12
- Git
- Groq API key (free at console.groq.com)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/zugzubii/clara-ai-pipeline.git
cd clara-ai-pipeline
```

2. Install dependencies:
```bash
pip install groq python-dotenv requests
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your Groq API key
```

---

## Running the Pipeline

### Step 1 — Add your transcript files to /data
Name them like: `demo_ACC-001.txt` and `onboarding_ACC-001.txt`

### Step 2 — Run Pipeline A (Demo → v1 Agent)
```bash
python scripts/batch_pipeline_a.py
```

### Step 3 — Run Pipeline B (Onboarding → v2 Agent + Changelog)
```bash
python scripts/batch_pipeline_b.py
```

### Step 4 — View the Dashboard
```bash
python -m http.server 8000
```
Open browser at: `http://localhost:8000/dashboard/`

---

## Output Format

### Account Memo JSON
Structured extraction of all business configuration from the transcript including business hours, emergency definitions, routing rules, integration constraints, and unknowns.

### Retell Agent Spec JSON
Includes a fully generated system prompt with business hours flow, after-hours flow, transfer protocol, fallback logic, and key variables — ready to paste into Retell.

### Changelog JSON
Field-level diff between v1 and v2 showing exactly what changed after the onboarding call and why.

---

## Dashboard

The dashboard at `/dashboard/index.html` provides:
- Overview stats (total accounts, v1/v2 counts, total field changes)
- Per-account cards with version badges
- Interactive v1 → v2 diff viewer (color coded)
- Full memo and agent spec viewer
- Generated system prompt viewer

---

## Architecture Decisions

**Why Groq instead of OpenAI?** Groq's free tier provides access to Llama 3.3 70B with no credit card required, meeting the zero-cost constraint while maintaining high extraction quality.

**Why local JSON instead of Supabase?** For full reproducibility without requiring database credentials. The schema is designed to be dropped into Supabase with no changes.

**Why Python scripts instead of n8n?** Simpler setup for evaluators, no Docker required. The batch scripts are idempotent and produce identical results on repeated runs.

---

## Known Limitations
- Requires transcripts as `.txt` files (audio transcription not included in this version)
- Mock data used for 4 of 5 accounts due to limited dataset provided
- Dashboard requires a local server to load JSON files (browser security restriction)

---

## What I Would Add With Production Access
- Live Retell API integration to deploy agents directly
- Whisper audio transcription for raw recordings
- Supabase backend for multi-user access
- Slack/email notifications on pipeline completion
- n8n workflow for no-code trigger support
- Automated testing with transcript edge cases

---

## Dataset
- ACC-001: Ben's Electric Solutions (real demo call provided)
- ACC-002 to ACC-005: Realistic mock accounts generated for pipeline testing

---

*Built by Kushagra Chaudhary — B.Tech CSE, VIT Vellore*