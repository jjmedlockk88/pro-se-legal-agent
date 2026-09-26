# Case Workspace Schema

Keep this directory private and out of Git. Use copies; preserve originals separately.

## Files

- `case_profile.yml` — jurisdiction, case numbers, parties, counsel, custody, hearings.
- `timeline.csv` — `date,time,event,source,confidence,deadline,notes`.
- `evidence_index.csv` — `id,description,source,date,hash,location,authenticity,issues`.
- `contradictions.csv` — `issue,source_a,quote_a,source_b,quote_b,materiality,next_step`.
- `deadlines.csv` — `matter,trigger,deadline,source,confidence,reminder,status`.
- `claims_matrix.csv` — `defendant,capacity,right,act,policy_or_custom,causation,injury,remedy,proof,gaps,defenses`.
- `research_log.csv` — `query,source,accessed,proposition,pinpoint,adverse_authority,status`.
- `filings.csv` — `title,filed_or_due,source,served,order,result,next_action`.

## Evidence hygiene

Hash original files with SHA-256, retain metadata, log every transfer, and never edit originals. Redact working copies. Do not upload sensitive files to a public repository or an untrusted service.
