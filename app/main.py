from fastapi import FastAPI
from pydantic import BaseModel

from app.agents.tax_validation_agent import TaxValidationAgent
from app.config import settings

app = FastAPI(title="Tax Payment Validation Agent")

agent = TaxValidationAgent(output_dir=settings.output_dir)

class ValidationRequest(BaseModel):
    agency_path: str = settings.agency_data_path
    payment_path: str = settings.payment_data_path

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/validate")
async def validate_payments(payload: ValidationRequest):
    results = agent.run(payload.agency_path, payload.payment_path)
    return {
        "count": len(results),
        "results": [
            {
                "payment_id": item.payment_id,
                "account_id": item.account_id,
                "taxpayer_name": item.taxpayer_name,
                "matched": item.matched,
                "status": item.status,
                "decision": item.decision,
                "letter_path": item.letter_path,
            }
            for item in results
        ],
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
