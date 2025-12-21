from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH


# ================= UTILS =================

def heading(doc, text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(14)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER


def para(doc, text="", bold=False):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = bold
    r.font.size = Pt(11)


def safe(d, k):
    return d.get(k) or "________"


# ================= MAIN GENERATOR =================

def generate_document(doc_type, d):
    doc = Document()

    # =================================================
    # 1️⃣ BAIL APPLICATION
    # =================================================
    if doc_type == "Bail Application":
        heading(doc, "IN THE HON'BLE COURT")

        para(doc, f"At {safe(d,'court_place')}")
        para(doc, f"Date: {safe(d,'date')}", bold=True)

        para(doc, "")
        para(doc, "To,")
        para(doc, f"The Hon'ble Judge, {safe(d,'court_name')}")

        para(doc, "")
        para(doc,
             f"Subject: Bail Application under Section 437/439 CrPC "
             f"in FIR No. {safe(d,'fir_number')} registered at "
             f"{safe(d,'police_station')} for offences under "
             f"{safe(d,'ipc_sections')}", bold=True)

        para(doc, "")
        para(doc,
             f"The Applicant, {safe(d,'applicant_name')}, "
             f"S/o / D/o / W/o {safe(d,'father_name')}, "
             f"aged about {safe(d,'age')} years, residing at "
             f"{safe(d,'address')}, humbly submits as under:")

        para(doc, "")
        para(doc, "GROUNDS FOR BAIL:", bold=True)
        para(doc, safe(d, "grounds"))

        para(doc, "")
        para(doc,
             "That the applicant undertakes to cooperate with the "
             "investigation and shall abide by all conditions imposed "
             "by this Hon’ble Court.")

        para(doc, "")
        para(doc,
             "PRAYER:\nIt is therefore most respectfully prayed that "
             "this Hon’ble Court may be pleased to grant bail to the "
             "Applicant in the interest of justice.")

        para(doc, "")
        para(doc, "Applicant", bold=True)
        para(doc, safe(d, "applicant_name"))

    # =================================================
    # 2️⃣ ANTICIPATORY BAIL
    # =================================================
    elif doc_type == "Anticipatory Bail":
        heading(doc, "APPLICATION FOR ANTICIPATORY BAIL")

        para(doc, f"Before the Hon'ble Court of {safe(d,'court_name')}")
        para(doc, f"Date: {safe(d,'date')}", bold=True)

        para(doc, "")
        para(doc,
             f"The Applicant {safe(d,'applicant_name')}, "
             f"S/o / D/o / W/o {safe(d,'father_name')}, "
             f"aged about {safe(d,'age')} years, residing at "
             f"{safe(d,'address')}, apprehends arrest in FIR No. "
             f"{safe(d,'fir_number')} registered at "
             f"{safe(d,'police_station')} for offences under "
             f"{safe(d,'ipc_sections')}.")

        para(doc, "")
        para(doc, "REASONS FOR APPREHENSION:", bold=True)
        para(doc, safe(d, "apprehension_reason"))

        para(doc, "")
        para(doc, "PREVIOUS CASES (IF ANY):", bold=True)
        para(doc, safe(d, "previous_cases"))

        para(doc, "")
        para(doc,
             "PRAYER:\nIt is prayed that this Hon’ble Court may kindly "
             "grant anticipatory bail to the Applicant under Section "
             "438 of the Code of Criminal Procedure.")

        para(doc, "")
        para(doc, "Applicant", bold=True)
        para(doc, safe(d, "applicant_name"))

    # =================================================
    # 3️⃣ FIR DRAFT
    # =================================================
    elif doc_type == "FIR Draft":
        heading(doc, "FIRST INFORMATION REPORT")

        para(doc, f"Police Station: {safe(d,'police_station')}", bold=True)
        para(doc, f"District: {safe(d,'district')}")
        para(doc, f"Date: {safe(d,'date')}")

        para(doc, "")
        para(doc,
             f"I, {safe(d,'complainant_name')}, "
             f"S/o / D/o / W/o {safe(d,'father_name')}, "
             f"residing at {safe(d,'address')}, submit the following "
             f"complaint:")

        para(doc, "")
        para(doc, "FACTS OF THE CASE:", bold=True)
        para(doc, safe(d, "facts"))

        para(doc, "")
        para(doc,
             f"The incident occurred on {safe(d,'incident_date')} at "
             f"{safe(d,'incident_time')} at "
             f"{safe(d,'incident_place')}.")

        para(doc, "")
        para(doc,
             "I request you to kindly register this complaint and "
             "take appropriate legal action.")

        para(doc, "")
        para(doc, "Complainant", bold=True)
        para(doc, safe(d, "complainant_name"))

    # =================================================
    # 4️⃣ AFFIDAVIT
    # =================================================
    elif doc_type == "Affidavit":
        heading(doc, "AFFIDAVIT")

        para(doc,
             f"I, {safe(d,'deponent_name')}, "
             f"S/o / D/o / W/o {safe(d,'father_name')}, "
             f"aged about {safe(d,'age')} years, "
             f"residing at {safe(d,'address')}, "
             f"do hereby solemnly affirm and state as follows:")

        para(doc, "")
        para(doc, safe(d, "statement"))

        para(doc, "")
        para(doc, "VERIFICATION:", bold=True)
        para(doc,
             f"I verify that the contents of this affidavit are true "
             f"and correct to the best of my knowledge.")

        para(doc, "")
        para(doc, f"Place: {safe(d,'place')}")
        para(doc, f"Date: {safe(d,'date')}")

        para(doc, "")
        para(doc, "Deponent", bold=True)
        para(doc, safe(d, "deponent_name"))

    # =================================================
    # 5️⃣ RENT AGREEMENT (DETAILED)
    # =================================================
    elif doc_type == "Rent Agreement":
        heading(doc, "RENT AGREEMENT")

        para(doc,
             f"This Rent Agreement is made on {safe(d,'start_date')} "
             f"between {safe(d,'owner_name')}, "
             f"S/o / D/o / W/o {safe(d,'owner_father')} (Landlord) "
             f"and {safe(d,'tenant_name')}, "
             f"S/o / D/o / W/o {safe(d,'tenant_father')} (Tenant).")

        para(doc, "")
        para(doc, "PROPERTY DESCRIPTION:", bold=True)
        para(doc, safe(d, "property_address"))

        para(doc, "")
        para(doc, "TERMS AND CONDITIONS:", bold=True)
        para(doc, f"1. Monthly Rent: ₹{safe(d,'rent_amount')}")
        para(doc, f"2. Security Deposit: ₹{safe(d,'security_deposit')}")
        para(doc,
             f"3. Duration: From {safe(d,'start_date')} "
             f"to {safe(d,'end_date')}")
        para(doc,
             f"4. Notice Period: {safe(d,'notice_period')} months")
        para(doc,
             f"5. Jurisdiction: Courts at {safe(d,'jurisdiction')}")

        para(doc, "")
        para(doc, "WITNESSES:", bold=True)
        para(doc, f"1. {safe(d,'witness_1')}")
        para(doc, f"2. {safe(d,'witness_2')}")

        para(doc, "")
        para(doc, "Landlord Signature: __________")
        para(doc, "Tenant Signature: __________")

    # =================================================
    # 6️⃣ WILL
    # =================================================
    elif doc_type == "Will":
        heading(doc, "LAST WILL AND TESTAMENT")

        para(doc,
             f"I, {safe(d,'testator_name')}, "
             f"S/o / D/o / W/o {safe(d,'father_name')}, "
             f"aged about {safe(d,'age')} years, "
             f"residing at {safe(d,'address')}, "
             f"declare this as my last Will.")

        para(doc, "")
        para(doc, "DETAILS OF ASSETS:", bold=True)
        para(doc, safe(d, "assets"))

        para(doc, "")
        para(doc, "BENEFICIARIES:", bold=True)
        para(doc, safe(d, "beneficiaries"))

        para(doc, "")
        para(doc, f"Executor: {safe(d,'executor')}")
        para(doc, f"Place: {safe(d,'place')}")
        para(doc, f"Date: {safe(d,'date')}")

        para(doc, "")
        para(doc, "Witnesses:")
        para(doc, f"1. {safe(d,'witness_1')}")
        para(doc, f"2. {safe(d,'witness_2')}")

    # =================================================
    # 7️⃣ POWER OF ATTORNEY
    # =================================================
    elif doc_type == "Power of Attorney":
        heading(doc, "POWER OF ATTORNEY")

        para(doc,
             f"I, {safe(d,'principal_name')}, "
             f"residing at {safe(d,'principal_address')}, "
             f"hereby appoint {safe(d,'agent_name')} "
             f"as my lawful attorney.")

        para(doc, "")
        para(doc, "POWERS GRANTED:", bold=True)
        para(doc, safe(d, "powers"))

        para(doc, "")
        para(doc, f"Duration: {safe(d,'duration')}")
        para(doc, f"Jurisdiction: {safe(d,'jurisdiction')}")
        para(doc, f"Place: {safe(d,'place')}")
        para(doc, f"Date: {safe(d,'date')}")

        para(doc, "")
        para(doc, "Witnesses:")
        para(doc, f"1. {safe(d,'witness_1')}")
        para(doc, f"2. {safe(d,'witness_2')}")

    # =================================================
    # 8️⃣ CUSTOM
    # =================================================
    elif doc_type == "Custom":
        heading(doc, safe(d, "custom_title"))
        para(doc, safe(d, "custom_text"))
        para(doc, "")
        para(doc, f"Place: {safe(d,'place')}")
        para(doc, f"Date: {safe(d,'date')}")

    return doc
