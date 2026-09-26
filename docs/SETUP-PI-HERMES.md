# Local setup for Hermes/OpenCode/Pi

This stack is intentionally provider-agnostic. Configure Pi to use Hermes or the model/provider already working in OpenCode. Do not add API keys to this repository.

## First run

```bash
mkdir -p case_workspace private_sources drafts
chmod 700 case_workspace private_sources drafts
cp -n case_workspace/README.md case_workspace/README.private.md
```

Install only what you need. Python's standard library is enough for the ledger/hash utilities; use a virtual environment for optional OCR/PDF packages.

## Privacy

- Keep case material outside the Git repository or in an encrypted local directory.
- Add private paths to `.git/info/exclude`, not merely `.gitignore`.
- Back up encrypted copies offline.
- Remove names, addresses, birth dates, booking numbers, and unredacted discovery before sharing prompts.
- Review the model provider's retention policy before sending any confidential material.

## Operating loop

1. Ask the agent to summarize the current record and list unknowns.
2. Add primary documents and source links.
3. Run a narrow research task.
4. Ask for an adverse-authority/red-team pass.
5. Generate a draft with record citations and a filing-quality gate.
6. Human review, then file only through the court-approved process.
