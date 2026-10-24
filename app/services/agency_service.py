import csv
import json
from pathlib import Path
from typing import List

from app.models import AgencyTaxRecord, PaymentRecord

class AgencyDataStore:
    def __init__(self, data_path: str):
        self.data_path = Path(data_path)

    def load_tax_records(self) -> List[AgencyTaxRecord]:
        if not self.data_path.exists():
            raise FileNotFoundError(f"Agency data file not found: {self.data_path}")

        if self.data_path.suffix.lower() == ".json":
            raw = json.loads(self.data_path.read_text())
            return [AgencyTaxRecord(**item) for item in raw]

        if self.data_path.suffix.lower() == ".csv":
            records = []
            with self.data_path.open(newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    records.append(AgencyTaxRecord(**row))
            return records

        raise ValueError("Unsupported agency data format. Use .json or .csv")

    def find_matching_record(self, payment: PaymentRecord, records: List[AgencyTaxRecord]) -> AgencyTaxRecord | None:
        for record in records:
            if payment.account_id == record.account_id:
                return record
            if payment.taxpayer_id == record.taxpayer_id:
                return record
        return None

class PaymentLoader:
    @staticmethod
    def load_payments(file_path: str) -> List[PaymentRecord]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Payment data file not found: {path}")

        if path.suffix.lower() == ".json":
            raw = json.loads(path.read_text())
            return [PaymentRecord(**item) for item in raw]

        if path.suffix.lower() == ".csv":
            rows = []
            with path.open(newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append(PaymentRecord(**row))
            return rows

        raise ValueError("Unsupported payment data format. Use .json or .csv")
