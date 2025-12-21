from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from io import BytesIO


def add_heading(doc, text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(14)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER


def add_para(doc, text, bold=False):
    p = doc.add_paragraph()
    run = p.add_run(text or "")
    run.bold = bold
    run.font.size = Pt(11)


def safe(d, key):
    return d.get(key) or "________"


def generate_document(doc_type, d):
    doc = Document()

    # ================= BAIL APPLICATION =================
    if doc_type == "Bail Application":
        add_heading(doc, "IN THE HON'BLE COURT")

        add_para(doc, f"Date: {safe(d,'date')}", bold=True)
        add_para(doc, "")

        add_para(doc, "To,")
        add_para(doc, "The Hon'ble Judge,")
        add_para(doc, safe(d, "court_name"))

        add_para(doc, "")
        add_para(
            doc,
            f"Subject: Bail Application for {safe(d,'applicant_name')} "
            f"(Case No: {safe(d,'case_number')})",
            bold=True
        )

        add_para(doc, "")
        add_para(
            doc,
            f"I, {safe(d,'applicant_name')}, aged {safe(d,'age')}, "
            f"residing at {safe(d,'address')}, respectfully submit this bail application."
        )

        add_para(doc, "")
        add_para(doc, "Grounds for Bail:", bold=True)
        add_para(doc, safe(d, "reason_for_bail"))

        add_para(doc, "")
        add_para(doc, "Yours faithfully,")
        add_para(doc, safe(d, "applicant_name"), bold=True)

    # ================= FIR DRAFT =================
    elif doc_type == "FIR Draft":
        add_heading(doc, "FIRST INFORMATION REPORT")

        add_para(doc, f"Police Station: {safe(d,'police_station')}", bold=True)
        add_para(doc, f"District: {safe(d,'district')}")
        add_para(doc, f"Date of Incident: {safe(d,'incident_date')}")
        add_para(doc, f"Time of Incident: {safe(d,'incident_time')}")
        add_para(doc, f"Place of Incident: {safe(d,'incident_place')}")

        add_para(doc, "")
        add_para(doc, "Facts of the Case:", bold=True)
        add_para(doc, safe(d, "incident_details"))

        add_para(doc, "")
        add_para(doc, "Signature of Complainant")
        add_para(doc, safe(d, "complainant_name"), bold=True)

    # ================= RENT AGREEMENT =================
    elif doc_type == "Rent Agreement":
        add_heading(doc, "RENT AGREEMENT")

        add_para(
            doc,
            f"This agreement is made between {safe(d,'owner_name')} (Owner) "
            f"and {safe(d,'tenant_name')} (Tenant)."
        )

        add_para(doc, "")
        add_para(doc, "Property Address:", bold=True)
        add_para(doc, safe(d, "property_address"))

        add_para(doc, "")
        add_para(doc, f"Monthly Rent: ₹{safe(d,'rent_amount')}")
        add_para(doc, f"Security Deposit: ₹{safe(d,'security_deposit')}")

        add_para(doc, "")
        add_para(doc, "Owner Signature: __________")
        add_para(doc, "Tenant Signature: __________")

    # ================= WILL =================
    elif doc_type == "Will":
        add_heading(doc, "LAST WILL AND TESTAMENT")

        add_para(
            doc,
            f"I, {safe(d,'testator_name')}, aged {safe(d,'age')}, "
            f"residing at {safe(d,'address')}, declare this as my Will."
        )

        add_para(doc, "")
        add_para(doc, "Beneficiary Details:", bold=True)
        add_para(doc, safe(d, "beneficiary_details"))

        add_para(doc, "")
        add_para(doc, "Signature of Testator")

    # ================= POWER OF ATTORNEY =================
    elif doc_type == "Power of Attorney":
        add_heading(doc, "POWER OF ATTORNEY")

        add_para(
            doc,
            f"I, {safe(d,'principal_name')}, appoint {safe(d,'agent_name')} "
            "as my lawful attorney."
        )

        add_para(doc, "")
        add_para(doc, "Powers Granted:", bold=True)
        add_para(doc, safe(d, "powers_granted"))

        add_para(doc, "")
        add_para(doc, "Signature of Principal")

    # ================= CUSTOM =================
    elif doc_type == "Custom":
        add_heading(doc, safe(d, "custom_title"))
        add_para(doc, safe(d, "custom_text"))

    return doc
