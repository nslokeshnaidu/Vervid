from pydantic import BaseModel, Field
from typing import List, Optional


class AnalysisResult(BaseModel):
    """
    Stores the complete output of the VeriVid pipeline.
    """

    transcript: str

    language: Optional[str] = None

    translated_text: Optional[str] = None

    claims: List[str] = Field(default_factory=list)

    evidence: Optional[list] = None

    verification: Optional[list] = None

    report: Optional[dict] = None