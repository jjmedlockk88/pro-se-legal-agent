# Pro Se Legal Assistant Agent - NYE County, NV

**Free, fully open-source AI legal assistant for criminal defense and 42 USC §1983 Monell civil rights litigation.**

- Zero paid dependencies
- Local models (Ollama) optimized for 16GB MacBook Pro mid-2014
- MCP servers for legal research, PACER scraping, FOIA automation
- NYE County NV courts focus (District Court, Rules, Local Practice)
- Criminal + civil rights litigation workflows

## Quick Start

### 1. Install Dependencies

```bash
# Install Ollama (local LLM runtime)
curl https://ollama.ai/install.sh | sh

# Install Python 3.9+
brew install python@3.11

# Clone repo and install Python deps
git clone https://github.com/jjmedlockk88/pro-se-legal-agent.git
cd pro-se-legal-agent
pip install -r requirements.txt
```

### 2. Start Ollama with Lightweight Model

```bash
# Pull a smaller, faster model (7B params, good for 16GB)
ollama pull mistral:7b

# Start Ollama server (runs on localhost:11434)
ollama serve
```

### 3. Start MCP Servers

```bash
# In another terminal
python mcp_servers/legal_research_server.py
python mcp_servers/pacer_server.py
python mcp_servers/foia_server.py
python mcp_servers/nv_courts_server.py
```

### 4. Run Agent

```bash
python agent.py
```

## Architecture

```
pro-se-legal-agent/
├── agent.py                    # Main agent orchestrator
├── config.yaml                 # NYE County config, Ollama settings
├── requirements.txt            # Python dependencies (free/open-source)
├── mcp_servers/
│   ├── legal_research_server.py    # Google Scholar, Cornell Law scraping
│   ├── pacer_server.py             # PACER docket automation (free tier)
│   ├── foia_server.py              # FOIA request drafting & submission
│   ├── nv_courts_server.py         # NYE County District Court info
│   └── document_gen_server.py      # Motion/complaint generation
├── skills/
│   ├── criminal_defense/
│   │   ├── motion_drafting.py      # Motions to suppress, dismiss, etc.
│   │   ├── plea_negotiation.py     # Plea strategy analysis
│   │   ├── appeal_strategy.py      # Appeal research & planning
│   │   └── discovery_management.py # Brady, Giglio obligations
│   ├── civil_rights/
│   │   ├── monell_claim.py         # Monell doctrine, municipal liability
│   │   ├── section_1983.py         # §1983 complaint structure
│   │   ├── policy_discovery.py     # Police policy research
│   │   └── damages_calculation.py  # Compensatory/punitive damages
│   └── general/
│       ├── deadline_tracker.py     # Statute of limitations, filing deadlines
│       ├── legal_research.py       # Case law synthesis
│       └── document_organization.py# Evidence, exhibits, exhibits
├── knowledge_base/
│   ├── nye_county/
│   │   ├── district_court_rules.md
│   │   ├── local_practice_norms.md
│   │   ├── judges.md
│   │   └── filing_procedures.md
│   ├── criminal_procedure/
│   │   ├── nv_statutes.md
│   │   ├── search_seizure.md
│   │   ├── due_process.md
│   │   └── sentencing_guidelines.md
│   ├── civil_rights/
│   │   ├── monell_doctrine.md
│   │   ├── section_1983_framework.md
│   │   ├── municipal_immunity.md
│   │   └── qualified_immunity.md
│   ├── case_law/
│   │   ├── landmark_criminal.md
│   │   ├── landmark_1983.md
│   │   └── nye_county_precedent.md
│   └── forms/
│       ├── criminal_motions/
│       ├── 1983_complaints/
│       └── discovery_requests/
├── plugins/
│   ├── pacer_scraper.py        # Automated PACER searches
│   ├── scholar_scraper.py      # Google Scholar case law search
│   ├── foia_builder.py         # FOIA request automation
│   └── deadline_calculator.py  # Statute of limitations calculator
├── tests/
│   ├── test_agent.py
│   ├── test_mcp_servers.py
│   └── test_skills.py
└── docs/
    ├── SETUP.md
    ├── USAGE.md
    ├── CRIMINAL_WORKFLOW.md
    └── 1983_WORKFLOW.md
```

## Key Features

### MCP Servers (Model Context Protocol)
- **Legal Research Server**: Search case law, statutes, regulations (free sources)
- **PACER Server**: Query federal case dockets, download documents
- **FOIA Server**: Draft and submit FOIA requests to NYE County agencies
- **NV Courts Server**: NYE County District Court rules, judges, procedures
- **Document Generation Server**: Auto-generate motions, complaints, discovery

### Skills

#### Criminal Defense
- Motion drafting (suppress evidence, dismiss, etc.)
- Plea negotiation strategy
- Appeal research
- Discovery obligations (Brady, Giglio)

#### §1983 Monell Civil Rights
- Monell municipal liability doctrine
- Policy/custom discovery
- Complaint structure and drafting
- Damages analysis

#### General
- Legal research synthesis
- Deadline tracking (statute of limitations, filing dates)
- Document organization (exhibits, evidence management)

### Knowledge Base
- NYE County District Court rules, judges, procedures
- Nevada criminal statutes and procedure
- §1983 and Monell doctrine (latest case law)
- Landmark cases (criminal + civil rights)
- Sample forms and templates

### Plugins
- **PACER Scraper**: Automate docket searches, fetch documents
- **Google Scholar Scraper**: Find case law for research
- **FOIA Builder**: Generate and submit FOIA requests
- **Deadline Calculator**: Compute statute of limitations dates

## Hardware Requirements

- **CPU**: 4+ cores (MacBook Pro mid-2014: Intel i7, 4 cores @ 2.2GHz)
- **RAM**: 16GB (tight, but works with Mistral 7B or Llama 2 7B)
- **Storage**: 20GB free (models + data)
- **Network**: Stable internet (for scraping, legal research)

## Model Selection for 16GB MacBook

### Recommended (Production)
- **Mistral 7B** (7.3B params, 4GB VRAM) - Best speed/quality ratio
- **Llama 2 7B** (7B params, 4GB VRAM) - Good legal reasoning
- **OpenHermes 2.5** (7B params, 4GB VRAM) - Instruction-tuned

### Alternative (if speed is critical)
- **Phi 2** (2.7B params, 2GB VRAM) - Surprisingly capable
- **Stable Beluga** (7B params, 4GB VRAM) - Legal-friendly

### Avoid (too slow on 16GB)
- 13B+ models (will swap to disk, become unusable)
- Llama 2 13B (requires ~10GB)
- Code-focused models (slower, not optimized for legal reasoning)

## Usage Examples

### Criminal Defense Workflow

```python
from agent import ProSeLegalAgent

agent = ProSeLegalAgent(model='mistral:7b', jurisdiction='nye_county')

# Research and draft motion to suppress
agent.task(
    "I was arrested in Pahrump. Police searched my car without a warrant."
    "Draft a motion to suppress the evidence under NV law."
)

# Agent will:
# 1. Research NV search/seizure law (§1983, Fourth Amendment)
# 2. Find relevant case law from 9th Circuit, Nevada courts
# 3. Draft motion with proper legal citations
# 4. Identify filing deadline (local rules)
# 5. Generate discovery requests for police records
```

### §1983 Monell Civil Rights Workflow

```python
# Research Monell municipal liability
agent.task(
    "I was arrested by NYE County Sheriff's Office. The arrest violated my "
    "constitutional rights. I want to sue the county under 42 USC §1983 for "
    "municipal liability (Monell claim). What's the factual pattern I need to show?"
)

# Agent will:
# 1. Explain Monell doctrine (policy/custom + causation)
# 2. Research NYE County Sheriff's Office policies
# 3. Identify prior incidents (pattern evidence)
# 4. Draft Monell complaint structure
# 5. Calculate statutory damages under §1983
# 6. Generate discovery requests for police policies
```

### Research Task

```python
# Legal research
agent.task(
    "What's the current law on qualified immunity in the 9th Circuit? "
    "Can I sue individual officers for §1983 violations?"
)

# Agent will:
# 1. Search Google Scholar for recent 9th Circuit cases
# 2. Synthesize qualified immunity doctrine
# 3. Cite leading cases (Ashcroft v. al-Kidd, etc.)
# 4. Explain application to your facts
```

## Free Legal Research Sources (No Paywall)

- **Google Scholar** (`scholar.google.com`) - Full case law access
- **CourtListener** - Federal + state case opinions, PACER aggregation
- **Cornell Law** (`law.cornell.edu`) - Statutes, rules, plain-language guides
- **Justia** - Cases, legal articles, forms
- **PACER** - Federal dockets (free tier with registration)
- **Nevada Legislature** (`leg.state.nv.us`) - NV statutes, rules
- **NYE County District Court** (`nyecourts.us`) - Local rules, procedures

## Limitations

- **Local models are slower**: Expect 5-15 second response time (vs. ChatGPT instant)
- **Hallucinations possible**: Always verify citations and legal reasoning
- **Not a replacement for a lawyer**: Use for research, drafting, strategy—review with legal professional if possible
- **PACER scraping rate-limited**: Respect PACER T/S to avoid blocking
- **No real-time docket updates**: Refresh manually or check PACER directly

## Support & Community

- **Issues/Feature Requests**: GitHub Issues
- **Legal Research Questions**: Discussion Forum
- **Local Resources (NYE County)**:
  - Pahrump Legal Aid Center
  - Nevada Legal Services
  - Law library at district court

## License

MIT License - Free to use, modify, distribute.

## Disclaimer

**This tool is NOT legal advice.** It's a research and drafting assistant. Always:
- Verify legal reasoning independently
- Check citations in Google Scholar / CourtListener
- Consult a real lawyer before filing anything critical
- Follow local court rules and procedures

---

**Built for pro se defendants with zero budget. Maximum legal firepower.**
