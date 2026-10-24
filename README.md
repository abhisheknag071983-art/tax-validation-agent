# Tax Payment Validation Agent

This project builds an agentic workflow for validating taxpayer payments against agency tax records and producing PDF submission letters.

## Features
- Loads agency tax ledger data from JSON or CSV
- Matches payments to taxpayer accounts
- Validates balance due with tolerance checks
- Flags partial, overpayment, and unmatched payments
- Produces PDF letters for submission or audit
- Exposes a FastAPI endpoint to process batches

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
python app/main.py
```

Then call the API:
```bash
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -d '{
    "agency_path": "data/agency_records.json",
    "payment_path": "data/payments.json"
  }'
```

The generated PDFs will appear in the `output/` folder.
