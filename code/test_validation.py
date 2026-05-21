"""Unit tests for the validation module."""
from datetime import date

import validation as v


GOOD = {
    "vendor_name": "ACME SUPPLIES LTD",
    "invoice_date": "2026-04-15",
    "subtotal": 135.00,
    "tax": 25.65,
    "total": 160.65,
    "line_items": [
        {"description": "Printer paper A4", "amount": 45.00},
        {"description": "Ink cartridge", "amount": 54.00},
        {"description": "USB-C cable 2m", "amount": 36.00},
    ],
}


def test_clean_document_has_no_anomalies():
    assert v.validate(GOOD, today=date(2026, 5, 1)) == []
    assert v.status_for([]) == "validated"


def test_line_items_sum_mismatch_is_caught():
    bad = {**GOOD, "subtotal": 200.00}
    anomalies = v.check_line_items_sum(bad)
    assert len(anomalies) == 1
    assert anomalies[0]["kind"] == "line_items_sum_mismatch"


def test_total_mismatch_is_caught():
    bad = {**GOOD, "total": 999.00}
    anomalies = v.check_total(bad)
    assert len(anomalies) == 1
    assert anomalies[0]["kind"] == "total_mismatch"


def test_total_within_tolerance_passes():
    ok = {**GOOD, "total": 160.66}  # 0.01 off, within tolerance
    assert v.check_total(ok) == []


def test_missing_vendor_and_total():
    bad = {"line_items": [{"amount": 1}]}
    anomalies = v.check_required_fields(bad)
    kinds = [a["detail"] for a in anomalies]
    assert any("vendor_name" in k for k in kinds)
    assert any("total" in k for k in kinds)


def test_invalid_date():
    bad = {**GOOD, "invoice_date": "15/04/2026"}
    anomalies = v.check_date(bad, today=date(2026, 5, 1))
    assert anomalies[0]["kind"] == "invalid_date"


def test_future_date():
    bad = {**GOOD, "invoice_date": "2027-01-01"}
    anomalies = v.check_date(bad, today=date(2026, 5, 1))
    assert anomalies[0]["kind"] == "future_date"


def test_status_for_error_is_needs_review():
    anomalies = [{"kind": "total_mismatch", "severity": "error"}]
    assert v.status_for(anomalies) == "needs_review"
