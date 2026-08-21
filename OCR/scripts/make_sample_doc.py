"""Generates a synthetic test document image (NOT a real certificate) so
the OCR pipeline can be verified end-to-end before real scanned documents
are available. Mimics the layout/field density of a GST registration
certificate for demo/testing purposes only.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "/home/abisheak/.nvm/versions/node/v22.23.1/lib/node_modules/n8n/node_modules/pdfjs-dist/standard_fonts/LiberationSans-Regular.ttf"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "sample_docs"

GST_LINES = [
    ("SAMPLE DOCUMENT — SYNTHETIC TEST FIXTURE, NOT A REAL CERTIFICATE", 22, True),
    ("", 16, False),
    ("GOODS AND SERVICES TAX REGISTRATION CERTIFICATE", 20, True),
    ("", 16, False),
    ("Registration Number (GSTIN): 33ABCDE1234F1Z5", 18, False),
    ("Legal Name of Business: Chennai Textile Works", 18, False),
    ("Trade Name: Chennai Textile Works", 18, False),
    ("Constitution of Business: Proprietorship", 18, False),
    ("Address of Principal Place of Business:", 18, False),
    ("  No. 45, Anna Salai, Chennai, Tamil Nadu, 600002", 18, False),
    ("Date of Liability: 01/04/2023", 18, False),
    ("Period of Validity: From 01/04/2023 To NA", 18, False),
    ("Type of Registration: Regular", 18, False),
    ("", 16, False),
    ("Signature: (digitally signed)", 18, False),
    ("Date of Issue: 15/04/2023", 18, False),
]

LABOUR_LINES = [
    ("SAMPLE DOCUMENT - SYNTHETIC TEST FIXTURE, NOT A REAL CERTIFICATE", 22, True),
    ("", 16, False),
    ("EPF ESTABLISHMENT REGISTRATION AND CONTRIBUTION CHALLAN", 20, True),
    ("", 16, False),
    ("Establishment Name: Chennai Textile Works", 18, False),
    ("Establishment Registration Number: TN/CHN/0045821/000", 18, False),
    ("Employer Name: R. Kumaresan", 18, False),
    ("Establishment Address: No. 45, Anna Salai, Chennai, Tamil Nadu, 600002", 18, False),
    ("Nature of Business: Garment Manufacturing", 18, False),
    ("Number of Employees: 35", 18, False),
    ("EPF UAN Details: UAN 100482913765", 18, False),
    ("EPF Contribution: Rs. 42,000 for wage month July 2026", 18, False),
    ("ESI Details: ESI Code 34-00-192837-000-1001", 18, False),
    ("ESI Contribution: Rs. 8,750 for wage month July 2026", 18, False),
    ("Applicable Labour Act: Employees Provident Fund and Miscellaneous Provisions Act, 1952", 18, False),
    ("Compliance Return Period: July 2026", 18, False),
    ("Challan Payment Details: Challan No. CHL209384, paid via net banking", 18, False),
    ("Date of Submission: 14/08/2026", 18, False),
    ("Acknowledgement Reference Number: TRRN 302948571", 18, False),
    ("Compliance Status: Filed", 18, False),
]


def make_image(lines, out_path: Path):
    width, height = 900, 850
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    y = 30
    for text, size, bold in lines:
        font = ImageFont.truetype(FONT_PATH, size)
        draw.text((40, y), text, fill="black", font=font)
        y += size + 14

    draw.rectangle([10, 10, width - 10, height - 10], outline="black", width=2)
    img.save(out_path)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    make_image(GST_LINES, OUTPUT_DIR / "sample_gst_certificate.png")
    make_image(LABOUR_LINES, OUTPUT_DIR / "sample_epf_challan.png")
