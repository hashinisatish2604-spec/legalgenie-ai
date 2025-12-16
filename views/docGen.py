from dotenv import load_dotenv
load_dotenv()

from utils.groq_client import call_llm

# =====================================================
# LANGUAGE MAP
# =====================================================
LANGUAGE_MAP = {
    "en": "Respond in English.",
    "hi": "Respond in Hindi using Devanagari script.",
    "kn": "Respond in Kannada script."
}

# =====================================================
# DOCUMENT TEMPLATES
# =====================================================
TEMPLATES = {

    "bail": """
IN THE HON'BLE COURT OF {court_name}

Case Number: {case_number}
Police Station: {police_station}

Applicant:
{applicant_name}
{applicant_address}

Age of Accused: {accused_age}

Offence:
{offence}

Sections:
{sections}

Date of Arrest:
{arrest_date}

FACTS OF THE CASE:
{facts}

GROUNDS FOR BAIL:
{grounds_for_bail}

Previous Bail Orders:
{previous_bail_orders}

PRAYER:
The applicant humbly prays that this Hon’ble Court may be pleased to grant bail in the interest of justice.

Place:
Date:
""",

    "anticipatory": """
ANTICIPATORY BAIL APPLICATION

Court Name:
{court_name}

Applicant Name:
{applicant_name}

FIR Number:
{fir_number}

Police Station:
{police_station}

Offence:
{offence}

Sections:
{sections}

Grounds:
{grounds}

Reason for Apprehension:
{reason_for_apprehension}
""",

    "fir": """
FIRST INFORMATION REPORT (FIR)

Police Station:
{police_station}

FIR Number:
{fir_number}

Complainant Name:
{complainant_name}

Complainant Address:
{complainant_address}

Accused Name:
{accused_name}

Incident Description:
{incident_description}

Date of Incident:
{date_of_incident}

Time of Incident:
{time_of_incident}

Place of Incident:
{place_of_incident}
""",

    "affidavit": """
AFFIDAVIT

I, {deponent_name}, aged {age}, S/o or D/o {father_mother_name},
residing at {address}, occupation {occupation},
do hereby solemnly affirm as follows:

{statement}

Place: {place}
Date: {date}
""",

    "rent": """
RENT AGREEMENT

This Rent Agreement is made between:

Landlord:
{landlord_name}

Tenant:
{tenant_name}

Property Address:
{property_address}

Purpose of Rent:
{purpose_of_rent}

Monthly Rent:
{monthly_rent}

Security Deposit:
{deposit}

Rent Start Date:
{rent_start_date}

Duration:
{duration}

Maintenance Charges:
{maintenance_charges}
""",

    "will": """
LAST WILL AND TESTAMENT

I, {testator_name}, aged {age}, residing at {address},
hereby declare this to be my last Will.

Executor:
{executor_name}

Beneficiaries:
{beneficiaries}

Assets Description:
{assets_description}

Witness 1:
{witness_1}

Witness 2:
{witness_2}
""",

    "poa": """
POWER OF ATTORNEY

Grantor:
{grantor_name}

Grantee:
{grantee_name}

Relationship:
{relationship}

Powers Granted:
{powers_granted}

Property Details:
{property_details}

Duration:
{duration}

Place:
{place}
""",

    "custom": """
{document_title}

{document_description}

Additional Notes:
{additional_notes}

Place: {place}
Date: {date}
"""
}

# =====================================================
# SAFE DOCUMENT GENERATOR
# =====================================================
def generate_document(doc_type, form_data, language="en"):
    """
    Generates a legal document in the selected language.
    Safely fills missing fields and calls the LLM.
    """

    template = TEMPLATES.get(doc_type)
    if not template:
        return "Invalid document type."

    # ---------- SAFE FORMAT (prevents KeyError) ----------
    class SafeDict(dict):
        def __missing__(self, key):
            return ""

    prompt_body = template.format_map(SafeDict(form_data))

    final_prompt = f"""
You are an expert Indian legal document drafter.

{LANGUAGE_MAP.get(language, "Respond in English.")}

Draft the following legal document professionally:

{prompt_body}
"""

    return call_llm(final_prompt)
