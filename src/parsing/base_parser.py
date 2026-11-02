from abc import ABC, abstractmethod
import pdfplumber
from src.domain.models import AttendanceReport


class BaseParser(ABC):
    """
    מחלקת אב אבסטרקטיבית לכל הפארסרים במערכת.
    """

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    def extract_text(self) -> str:
        """
        חילוץ טקסט גולמי מכל עמודי קובץ ה-PDF באמצעות pdfplumber.
        """
        full_text = ""
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        full_text += text + "\n"
        except Exception as e:
            print(f"Error extracting PDF text: {e}")
        return full_text

    @abstractmethod
    def parse_report(self) -> AttendanceReport:
        pass

    def parse(self) -> AttendanceReport:
        return self.parse_report()