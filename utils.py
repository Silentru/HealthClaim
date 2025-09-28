"""
utils.py

Small helpers for mapping and for later extension to EDI parsing and rule-engine.
"""
import re
from typing import Dict

def normalize_code(code: str) -> str:
    if code is None:
        return ""
    return re.sub(r"[^A-Za-z0-9]", "", str(code)).upper().strip()

def parse_edi_835_stub(edi_text: str) -> Dict:
    """
    Placeholder: This is where you'd parse X12 835 to extract denial codes, paid amounts, dates.
    For production use an X12 parsing library or the clearinghouse API.
    """
    raise NotImplementedError("Implement EDI parsing or use clearinghouse export API.")