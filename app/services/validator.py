from app.models import AgencyTaxRecord, PaymentRecord, ValidationOutcome

class PaymentValidator:
    def __init__(self, tolerance_cents: float = 1.0):
        self.tolerance_cents = tolerance_cents

    def validate_payment(self, payment: PaymentRecord, agency_record: AgencyTaxRecord | None) -> ValidationOutcome:
        if agency_record is None:
            return ValidationOutcome(
                payment_id=payment.payment_id,
                account_id=payment.account_id,
                taxpayer_name="Unknown",
                matched=False,
                status="manual_review",
                assessed_amount=0.0,
                paid_amount=payment.amount,
                balance_due_before=0.0,
                balance_due_after=0.0,
                variance=payment.amount,
                decision="No matching agency record",
                notes="The payment could not be matched to a taxpayer account in the agency dataset.",
            )

        assessed_amount = agency_record.balance_due
        balance_before = agency_record.balance_due
        variance = payment.amount - assessed_amount

        if abs(variance) <= self.tolerance_cents:
            status = "valid"
            decision = "Payment matches the assessed balance"
            notes = "The payment amount aligns with the balance due and is ready for confirmation."
            balance_after = 0.0
        elif payment.amount < assessed_amount:
            status = "partial"
            decision = "Partial payment accepted"
            notes = "The payment is less than the amount due. The balance remains outstanding."
            balance_after = assessed_amount - payment.amount
        elif payment.amount > assessed_amount:
            status = "manual_review"
            decision = "Overpayment requires review"
            notes = "The payment exceeds the expected balance. Manual review is required before approval."
            balance_after = payment.amount - assessed_amount
        else:
            status = "rejected"
            decision = "Payment rejected"
            notes = "The payment did not validate against the agency record."
            balance_after = assessed_amount

        return ValidationOutcome(
            payment_id=payment.payment_id,
            account_id=agency_record.account_id,
            taxpayer_name=agency_record.taxpayer_name,
            matched=True,
            status=status,
            assessed_amount=assessed_amount,
            paid_amount=payment.amount,
            balance_due_before=balance_before,
            balance_due_after=balance_after,
            variance=variance,
            decision=decision,
            notes=notes,
        )
