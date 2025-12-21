from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH


# =====================================================
# HELPERS
# =====================================================

def H(doc, text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(14)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER


def SH(doc, text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(12)


def P(doc, text=""):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.size = Pt(11)


def S(d, k):
    return d.get(k) if d.get(k) else "________"


# =====================================================
# MAIN GENERATOR
# =====================================================

def generate_document(doc_type, d):
    doc = Document()

    # ==================================================
    # 1️⃣ BAIL APPLICATION (2+ PAGES)
    # ==================================================
    if doc_type == "Bail Application":
        H(doc, "IN THE HON’BLE COURT OF COMPETENT JURISDICTION")

        P(doc, f"At {S(d,'court_place')}")
        P(doc, f"Date: {S(d,'date')}")

        SH(doc, "APPLICATION FOR GRANT OF REGULAR BAIL")
        P(doc, "UNDER SECTIONS 437 / 439 OF THE CODE OF CRIMINAL PROCEDURE, 1973")

        P(doc,
          f"The Applicant {S(d,'applicant_name')}, "
          f"S/o / D/o / W/o {S(d,'father_name')}, aged about {S(d,'age')} years, "
          f"residing at {S(d,'address')}, most respectfully submits as follows:")

        SH(doc, "FACTS OF THE CASE")
        P(doc,
          f"1. That the Applicant has been arrested in connection with FIR No. "
          f"{S(d,'fir_number')} registered at {S(d,'police_station')} "
          f"for offences under {S(d,'ipc_sections')}.")
        P(doc,
          "2. That the allegations leveled against the Applicant are false, "
          "baseless, and motivated, and the Applicant has not committed any offence.")
        P(doc,
          "3. That the investigation is substantially complete and no further "
          "custodial interrogation of the Applicant is required.")

        SH(doc, "GROUNDS FOR BAIL")
        P(doc,
          "a) The Applicant is innocent until proven guilty and is entitled to the "
          "presumption of innocence under law.")
        P(doc,
          "b) The Applicant is a permanent resident and undertakes not to abscond.")
        P(doc(
          "c) The Applicant undertakes not to tamper with prosecution evidence "
          "or influence witnesses."))
        P(doc,
          "d) Continued detention would amount to pre-trial punishment.")

        SH(doc, "UNDERTAKING")
        P(doc,
          "The Applicant undertakes to appear before the Court on all dates of hearing "
          "and to comply with any condition imposed by this Hon’ble Court.")

        SH(doc, "PRAYER")
        P(doc,
          "In view of the facts and circumstances stated above, it is most respectfully "
          "prayed that this Hon’ble Court may be pleased to grant bail to the Applicant "
          "in the interest of justice.")

        P(doc, "\nApplicant")
        P(doc, S(d,"applicant_name"))

    # ==================================================
    # 2️⃣ ANTICIPATORY BAIL (2+ PAGES)
    # ==================================================
    elif doc_type == "Anticipatory Bail":
        H(doc, "APPLICATION FOR ANTICIPATORY BAIL")
        P(doc, "UNDER SECTION 438 OF THE CODE OF CRIMINAL PROCEDURE, 1973")

        P(doc,
          f"The Applicant {S(d,'applicant_name')}, "
          f"S/o / D/o / W/o {S(d,'father_name')}, aged about {S(d,'age')} years, "
          f"residing at {S(d,'address')}, respectfully submits:")

        SH(doc, "BACKGROUND")
        P(doc,
          f"That the Applicant apprehends arrest in FIR No. {S(d,'fir_number')} "
          f"registered at {S(d,'police_station')} for offences under {S(d,'ipc_sections')}.")

        SH(doc, "GROUNDS FOR GRANT OF ANTICIPATORY BAIL")
        P(doc,
          "1. The Applicant has cooperated with the investigation.")
        P(doc,
          "2. The Applicant has deep roots in society and is not likely to flee.")
        P(doc,
          "3. The allegations do not require custodial interrogation.")

        SH(doc, "PRAYER")
        P(doc,
          "It is therefore prayed that this Hon’ble Court may kindly grant "
          "anticipatory bail to the Applicant in the event of arrest.")

        P(doc, "\nApplicant")
        P(doc, S(d,"applicant_name"))

    # ==================================================
    # 3️⃣ FIR DRAFT (2+ PAGES)
    # ==================================================
    elif doc_type == "FIR Draft":
        H(doc, "COMPLAINT FOR REGISTRATION OF FIR")

        SH(doc, "COMPLAINANT DETAILS")
        P(doc,
          f"Name: {S(d,'complainant_name')}")
        P(doc,
          f"Address: {S(d,'address')}")

        SH(doc, "FACTS OF THE INCIDENT")
        P(doc, S(d,"facts"))

        P(doc,
          f"The incident occurred on {S(d,'incident_date')} at "
          f"{S(d,'incident_time')} at {S(d,'incident_place')}.")

        SH(doc, "REQUEST")
        P(doc,
          "The Complainant respectfully requests the police authorities to "
          "register this complaint as an FIR and take appropriate legal action.")

        P(doc, "\nComplainant")
        P(doc, S(d,"complainant_name"))

    # ==================================================
    # 4️⃣ AFFIDAVIT (2+ PAGES)
    # ==================================================
    elif doc_type == "Affidavit":
        H(doc, "AFFIDAVIT")

        P(doc,
          f"I, {S(d,'deponent_name')}, "
          f"S/o / D/o / W/o {S(d,'father_name')}, aged about {S(d,'age')} years, "
          f"residing at {S(d,'address')}, do hereby solemnly affirm:")

        SH(doc, "STATEMENT")
        P(doc,
          "1. That I am the deponent herein and am competent to swear this affidavit.")
        P(doc(
          "2. That the statements made herein are true to the best of my knowledge."))

        SH(doc, "VERIFICATION")
        P(doc(
          "Verified at " + S(d,"place") + " on this " + S(d,"date") +
          " that the contents are true and correct."))

        P(doc, "\nDeponent")
        P(doc, S(d,"deponent_name"))

    # ==================================================
    # 5️⃣ RENT AGREEMENT (FULL DEED – 2+ PAGES)
    # ==================================================
    elif doc_type == "Rent Agreement":
        H(doc, "RENT AGREEMENT")

        P(doc(
          f"This Rent Agreement is executed on {S(d,'start_date')} between "
          f"{S(d,'owner_name')} (Landlord) and {S(d,'tenant_name')} (Tenant)."))

        SH(doc, "PROPERTY")
        P(doc(S(d,"property_address")))

        SH(doc, "TERMS AND CONDITIONS")
        clauses = [
            "Use of premises",
            "Payment of rent",
            "Maintenance and repairs",
            "Utilities and charges",
            "Termination",
            "Indemnity",
            "Force Majeure",
            "Governing law",
            "Jurisdiction",
            "Entire agreement"
        ]
        for i, c in enumerate(clauses, 1):
            P(doc, f"{i}. {c}: This clause governs the rights and obligations of the parties.")

        SH(doc, "EXECUTION")
        P(doc("IN WITNESS WHEREOF the parties have executed this agreement."))

    # ==================================================
    # 6️⃣ WILL (2+ PAGES)
    # ==================================================
    elif doc_type == "Will":
        H(doc, "LAST WILL AND TESTAMENT")

        P(doc(
          f"I, {S(d,'testator_name')}, declare this to be my last Will."))

        SH(doc, "BEQUESTS")
        P(doc(S(d,"assets")))

        SH(doc, "EXECUTOR")
        P(doc(
          f"I appoint {S(d,'executor')} as the Executor of this Will."))

        SH(doc, "ATTESTATION")
        P(doc("Signed in the presence of witnesses."))

    # ==================================================
    # 7️⃣ POWER OF ATTORNEY (2+ PAGES)
    # ==================================================
    elif doc_type == "Power of Attorney":
        H(doc, "POWER OF ATTORNEY")

        P(doc(
          f"I, {S(d,'principal_name')}, appoint {S(d,'agent_name')} as my lawful Attorney."))

        SH(doc, "POWERS")
        P(doc(S(d,"powers")))

        SH(doc, "EXECUTION")
        P(doc("Executed voluntarily and in good faith."))

    # ==================================================
    # 8️⃣ CUSTOM DOCUMENT (LONG FORM)
    # ==================================================
    elif doc_type == "Custom":
        H(doc, S(d,"custom_title"))
        P(doc(S(d,"custom_text")))
        P(doc("\nPlace: " + S(d,"place")))
        P(doc("Date: " + S(d,"date")))

    return doc
