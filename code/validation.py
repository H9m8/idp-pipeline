"""Validation checks for extracted document data.

Pure functions, no I/O, so they're easy to unit test and to reuse
inside the n8n Code node. Each check returns a list of anomaly dicts;
an empty list means the check passed.
"""
from datetime import date, datetime


# how many currency units two amounts may differ by and still be "equal"
TOLERANCE = 0.02


def _to_float(value):
    """Best-effort numeric coercion. Returns None if not parseable."""
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def check_line_items_sum(data):
    """Line item amounts should sum to the subtotal."""
    subtotal = _to_float(data.get("subtotal"))
    items = data.get("line_items") or []
    if subtotal is None or not items:
        return []
    total = 0.0
    for item in items:
        amount = _to_float(item.get("amount"))
        if amount is not None:
            total += amount
    if abs(total - subtotal) > TOLERANCE:
        return [{
            "kind": "line_items_sum_mismatch",
            "detail": f"line items sum to {total:.2f} but subtotal is {subtotal:.2f}",
            "severity": "error",
        }]
    return []


def check_total(data):
    """subtotal + tax should equal total."""
    subtotal = _to_float(data.get("subtotal"))
    tax = _to_float(data.get("tax")) or 0.0
    total = _to_float(data.get("total"))
    if subtotal is None or total is None:
        return []
    expected = subtotal + tax
    if abs(expected - total) > TOLERANCE:
        return [{
            "kind": "total_mismatch",
            "detail": f"subtotal {subtotal:.2f} + tax {tax:.2f} = {expected:.2f}, but total is {total:.2f}",
            "severity": "error",
        }]
    return []


def check_required_fields(data):
    """Vendor, total, and at least one line item must be present."""
    anomalies = []
    if not data.get("vendor_name"):
        anomalies.append({
            "kind": "missing_field",
            "detail": "vendor_name is missing",
            "severity": "warning",
        })
    if _to_float(data.get("total")) is None:
        anomalies.append({
            "kind": "missing_field",
            "detail": "total is missing or not a number",
            "severity": "error",
        })
    if not (data.get("line_items") or []):
        anomalies.append({
            "kind": "missing_field",
            "detail": "no line items found",
            "severity": "warning",
        })
    return anomalies


def check_date(data, today=None):
    """invoice_date must parse as YYYY-MM-DD and not be in the future."""
    raw = data.get("invoice_date")
    if not raw:
        return []
    today = today or date.today()
    try:
        parsed = datetime.strptime(str(raw), "%Y-%m-%d").date()
    except ValueError:
        return [{
            "kind": "invalid_date",
            "detail": f"invoice_date '{raw}' is not a valid YYYY-MM-DD date",
            "severity": "warning",
        }]
    if parsed > today:
        return [{
            "kind": "future_date",
            "detail": f"invoice_date '{raw}' is in the future",
            "severity": "warning",
        }]
    return []


def validate(data, today=None):
    """Run all checks and return a combined list of anomalies."""
    anomalies = []
    anomalies += check_required_fields(data)
    anomalies += check_line_items_sum(data)
    anomalies += check_total(data)
    anomalies += check_date(data, today=today)
    return anomalies


def status_for(anomalies):
    """Decide the document status from the anomalies found."""
    if any(a["severity"] == "error" for a in anomalies):
        return "needs_review"
    if anomalies:
        return "needs_review"
    return "validated"
