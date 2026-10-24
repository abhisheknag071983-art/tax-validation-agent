from __future__ import annotations

from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from app.config import settings
from app.models import AgencyTaxRecord, PaymentRecord, ValidationOutcome
from app.services.agency_service import AgencyDataStore, PaymentLoader
from app.services.pdf_service import build_pdf_letter
from app.services.validator import PaymentValidator

class ValidationState(TypedDict):
    agency_records: list[AgencyTaxRecord]
    payments: list[PaymentRecord]
    results: list[ValidationOutcome]

class TaxValidationAgent:
    def __init__(self, output_dir: str = settings.output_dir):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.validator = PaymentValidator()

    def load_agency_data(self, agency_path: str) -> list[AgencyTaxRecord]:
        store = AgencyDataStore(agency_path)
        return store.load_tax_records()

    def load_payments(self, payment_path: str) -> list[PaymentRecord]:
        return PaymentLoader.load_payments(payment_path)

    def _match_and_validate(self, agency_records: list[AgencyTaxRecord], payments: list[PaymentRecord]) -> list[ValidationOutcome]:
        store = AgencyDataStore("unused")
        results = []
        for payment in payments:
            match = store.find_matching_record(payment, agency_records)
            outcome = self.validator.validate_payment(payment, match)
            results.append(outcome)
        return results

    def _generate_letters(self, outcomes: list[ValidationOutcome]) -> list[ValidationOutcome]:
        for outcome in outcomes:
            filename = f"{outcome.payment_id}.pdf"
            letter_path = build_pdf_letter(outcome, str(self.output_dir), filename)
            outcome.letter_path = letter_path
        return outcomes

    def run(self, agency_path: str, payment_path: str) -> list[ValidationOutcome]:
        state = {
            "agency_records": self.load_agency_data(agency_path),
            "payments": self.load_payments(payment_path),
            "results": [],
        }

        graph = StateGraph(ValidationState)
        graph.add_node("load", lambda state: {**state, "agency_records": self.load_agency_data(agency_path)})
        graph.add_node("match_and_validate", lambda state: {
            **state,
            "results": self._match_and_validate(state["agency_records"], state["payments"]),
        })
        graph.add_node("generate_letters", lambda state: {
            **state,
            "results": self._generate_letters(state["results"]),
        })
        graph.add_edge(START, "load")
        graph.add_edge("load", "match_and_validate")
        graph.add_edge("match_and_validate", "generate_letters")
        graph.add_edge("generate_letters", END)

        app = graph.compile()
        final_state = app.invoke(state)
        return final_state["results"]

    def __call__(self, agency_path: str, payment_path: str) -> list[ValidationOutcome]:
        return self.run(agency_path, payment_path)
