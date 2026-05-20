from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

os.makedirs("sample_docs", exist_ok=True)

def make_invoice(path):
    c = canvas.Canvas(path, pagesize=letter)
    t = c.beginText(50, 750)
    for line in [
        "ACME SUPPLIES LTD",
        "Tax ID: GB123456789",
        "",
        "INVOICE  #INV-2026-0042",
        "Date: 2026-04-15",
        "Currency: EUR",
        "",
        "Description                Qty    Unit     Amount",
        "Printer paper A4            10    4.50     45.00",
        "Ink cartridge (black)        3   18.00     54.00",
        "USB-C cable 2m               5    7.20     36.00",
        "",
        "Subtotal:   135.00",
        "Tax (19%):   25.65",
        "Total:      160.65",
    ]:
        t.textLine(line)
    c.drawText(t)
    c.save()
    print("wrote", path)

make_invoice("sample_docs/invoice_acme.pdf")
