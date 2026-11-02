import pdfplumber
from src.domain.models import AttendanceReport
from src.parsing.ocr import OCRProcessor


class BaseParser:

  def __init__(self, pdf_path: str):
    self.pdf_path = pdf_path
    self.ocr_processor = OCRProcessor()

  def extract_text(self) -> str:
    """שלב ראשון: מנסה לחלץ טקסט דיגיטלי ישירות דרך pdfplumber.

    אם הקובץ סרוק והתוצאה ריקה, מפעיל OCR מלא (תחנה 1).
    """
    text = ""
    try:
      with pdfplumber.open(self.pdf_path) as pdf:
        for page in pdf.pages:
          page_text = page.extract_text()
          if page_text:
            text += page_text + "\n"
    except Exception:
      pass

    # אם לא נמצא טקסט דיגיטלי (PDF סרוק / תמונה), נפעיל את תחנת ה-OCR
    if not text.strip():
      text = self.ocr_processor.extract_text(self.pdf_path)

    return text

  def parse(self) -> AttendanceReport:
    """מתודת מעטפת אחידה (Interface) המאפשרת ל-Main לקרוא ל-parse()

    מבלי לדעת באיזה סוג דוח מדובר, ומפעילה את הניתוח של המחלקה הספציפית.
    """
    return self.parse_report()

  def parse_report(self) -> AttendanceReport:
    """מתודה שאותה מממש כל פרסר ספציפי (TypeA / TypeB)."""
    raise NotImplementedError("יש לממש מתודה זו במחלקה היורשת")