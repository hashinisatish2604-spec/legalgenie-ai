from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH


def add_heading(doc, text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(14)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER


def add_para(doc, text, bold=False):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(11)


def generate_document(doc_type, d, language="en"):
    doc = Document()

    # ================= BAIL APPLICATION =================
    if doc_type == "Bail Application":
        add_heading(doc, "IN THE HON'BLE COURT")

        add_para(doc, f"Date: {d.get('date')}", bold=True)
        add_para(doc, "")

        add_para(doc, "To,")
        add_para(doc, "The Hon'ble Judge,")
        add_para(doc, d.get("court"))
        add_para(doc, "")

        add_para(
            doc,
            f"Subject: Bail Application for {d.get('accused')} (Case No: {d.get('case_no')})",
            bold=True
        )

        add_para(doc, "")
        add_para(
            doc,
            f"I, {d.get('petitioner')}, respectfully submit this bail application on behalf of "
            f"{d.get('accused')}. The grounds for seeking bail are as follows:"
        )

        add_para(doc, "")
        add_para(doc, d.get("reason"))

        add_para(doc, "")
        add_para(doc, "Hence, it is humbly prayed that this Hon'ble Court may be pleased to grant bail.")

        add_para(doc, "")
        add_para(doc, "Yours faithfully,")
        add_para(doc, d.get("petitioner"), bold=True)

        return doc

    # ================= FIR DRAFT =================
    if doc_type == "FIR Draft":
        add_heading(doc, "FIRST INFORMATION REPORT (FIR)")

        add_para(doc, f"Police Station: {d.get('fir_police')}", bold=True)
        add_para(doc, f"Date of Occurrence: {d.get('fir_date')}")
        add_para(doc, f"Place of Occurrence: {d.get('fir_place')}")

        add_para(doc, "")
        add_para(doc, f"Complainant Name: {d.get('fir_name')}", bold=True)

        add_para(doc, "")
        add_para(doc, "Facts of the Case:", bold=True)
        add_para(doc, d.get("fir_facts"))

        add_para(doc, "")
        add_para(doc, "I hereby request the concerned authorities to take appropriate legal action.")

        add_para(doc, "")
        add_para(doc, "Signature of Complainant")
        add_para(doc, d.get("fir_name"), bold=True)

        return doc

    # ================= RENT AGREEMENT =================
    if doc_type == "Rent Agreement":
        add_heading(doc, "RENT AGREEMENT")

        add_para(
            doc,
            f"This Rent Agreement is made on {d.get('rent_date')} between "
            f"{d.get('landlord')} (Landlord) and {d.get('tenant')} (Tenant)."
        )

        add_para(doc, "")
        add_para(doc, "Property Details:", bold=True)
        add_para(doc, d.get("property"))

        add_para(doc, "")
        add_para(doc, f"Monthly Rent: ₹{d.get('rent')}")
        add_para(doc, f"Security Deposit: ₹{d.get('deposit')}")
        add_para(doc, f"Lease Period: {d.get('lease_period')}")

        add_para(doc, "")
        add_para(doc, "Both parties hereby agree to the above terms and conditions.")

        add_para(doc, "")
        add_para(doc, "Landlord Signature: ________")
        add_para(doc, "Tenant Signature: ________")

        return doc

    # ================= WILL =================
    if doc_type == "Will":
        add_heading(doc, "LAST WILL AND TESTAMENT")

        add_para(
            doc,
            f"I, {d.get('testator')}, residing at {d.get('testator_address')}, "
            "being of sound mind, declare this to be my Last Will."
        )

        add_para(doc, "")
        add_para(doc, "Details of Assets:", bold=True)
        add_para(doc, d.get("assets"))

        add_para(doc, "")
        add_para(doc, "Beneficiary Details:", bold=True)
        add_para(doc, d.get("beneficiary"))

        add_para(doc, "")
        add_para(doc, f"Executor: {d.get('executor')}")

        add_para(doc, "")
        add_para(doc, f"Date: {d.get('will_date')}")
        add_para(doc, "Signature of Testator")

        return doc

    # ================= POWER OF ATTORNEY =================
    if doc_type == "Power of Attorney":
        add_heading(doc, "POWER OF ATTORNEY")

        add_para(
            doc,
            f"I, {d.get('principal')}, hereby appoint {d.get('agent')} as my lawful attorney."
        )

        add_para(doc, "")
        add_para(doc, "Powers Granted:", bold=True)
        add_para(doc, d.get("authority"))

        add_para(doc, "")
        add_para(doc, f"Date: {d.get('poa_date')}")
        add_para(doc, "Signature of Principal")

        return doc

    # ================= CUSTOM =================
    if doc_type == "Custom":
        add_heading(doc, "LEGAL DOCUMENT")
        add_para(doc, d.get("custom_text"))
        return doc

    return doc