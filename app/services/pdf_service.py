from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

def build_pdf_letter(outcome, output_dir: str, filename: str | None = None) -> str:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if filename is None:
        filename = f"{outcome.payment_id}.pdf"

    target = output_path / filename
    doc = SimpleDocTemplate(str(target), pagesize=letter)

    styles = getSampleStyleSheet()
    story = []

    header = Paragraph("Tax Payment Validation Letter", styles["Title"])
    story.append(header)
    story.append(Spacer(1, 18))

    details = [
        ["Field", "Value"],
        ["Taxpayer Name", outcome.taxpayer_name],
        ["Taxpayer Account", outcome.account_id],
        ["Payment ID", outcome.payment_id],
        ["Paid Amount", f"${outcome.paid_amount:,.2f}"],
        ["Assessed Amount", f"${outcome.assessed_amount:,.2f}"],
        ["Variance", f"${outcome.variance:,.2f}"],
        ["Validation Status", outcome.status.upper()],
        ["Decision", outcome.decision],
    ]

    table = Table(details, colWidths=[180, 300])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [(0.95, 0.95, 0.95), (1, 1, 1)]),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))
    story.append(table)
    story.append(Spacer(1, 16))

    story.append(Paragraph(f"<b>Notes:</b> {outcome.notes}", styles["BodyText"]))
    story.append(Spacer(1, 12))

    doc.build(story)
    return str(target)
