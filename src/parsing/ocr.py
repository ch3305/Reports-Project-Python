import os
from pdf2image import convert_from_path
import pytesseract


class OCRProcessor:
  """תחנה 1 בצינור: המרת קובץ PDF סרוק או רגיל לתמונות וחילוף טקסט באמצעות OCR."""

  def __init__(self, tesseract_path: str = None):
    # במידה ו-Tesseract אינו מותקן בנתיב ברירת המחדל של המערכת, ניתן להגדיר את הנתיב כאן
    if tesseract_path:
      pytesseract.pytesseract.tesseract_cmd = tesseract_path

  def extract_text(self, pdf_path: str) -> str:
    """מקבל נתיב לקובץ PDF, ממיר את העמודים לתמונות ומחלץ טקסט בעברית ובאנגלית."""
    if not os.path.exists(pdf_path):
      raise FileNotFoundError(f"קובץ ה-PDF לא נמצא בנתיב: {pdf_path}")

    full_text = ""
    try:
      # המרת עמודי ה-PDF לרשימת תמונות
      images = convert_from_path(pdf_path)

      for page_num, image in enumerate(images, start=1):
        # זיהוי אותיות ומספרים באמצעות Tesseract (שפות: עברית heb ואנגלית eng)
        page_text = pytesseract.image_to_string(image, lang="heb+eng")
        full_text += f"\n--- עמוד {page_num} ---\n" + page_text

    except Exception as e:
      print(
          f"אזהרה: שגיאה בהפעלת ה-OCR עבור הקובץ {pdf_path}. פירוט: {e}"
      )
      # מחחזיר מחרוזת ריקה כדי שהמערכת תעבור בצורה חלקה למנגנון הגיבוי (Fallback)
      return ""

    return full_text