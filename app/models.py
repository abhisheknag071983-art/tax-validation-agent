from typing import Literal, Optional
from pydantic import BaseModel, Field

TaxStatus = Literal["valid", "partial", "rejected", "manual_review"]

class AgencyTaxRecord(BaseModel):
    account_id: str
    taxpayer_name: str
    taxpayer_id: str
    filing_year: int
    assessed_amount: float
    balance_due: float
    status: str = "active"
    due_date: str

class PaymentRecord(BaseModel):
    payment_id: str
    account_id: str
    taxpayer_id: str
    amount: float
    payment_date: str
    payment_method: str = "ACH"
    reference_no: str
    notes: str = ""

class ValidationOutcome(BaseModel):
    payment_id: str
    account_id: str
    taxpayer_name: str
    matched: bool
    status: TaxStatus
    assessed_amount: float
    paid_amount: float
    balance_due_before: float
    balance_due_after: float
    variance: float
    decision: str
    notes: str
    letter_path: Optional[str] = None

class LetterPayload(BaseModel):
    taxpayer_name: str
    taxpayer_id: str
    account_id: str
    decision: str
    amount: float
    status: str
    notes: str = ""
