import pdfplumber


class ReportClassifier:
    """
    Responsible for classifying the type of an attendance report from raw PDF text or filename.
    """

    @staticmethod
    def classify(pdf_path: str) -> str:
        # זיהוי לפי שם הקובץ במידה והטקסט סרוק ולא חולץ
        if "n_r_" in pdf_path or "Type_B" in pdf_path:
            return "Type_B"

        full_text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        full_text += text + "\n"
        except Exception as e:
            pass

        # Identify unique markers for Type B reports
        if "כרטיס עובד לחודש" in full_text or "סה:\"כ ימי עבודה לחודש" in full_text or "מחיר לשעה" in full_text:
            return "Type_B"

        return "Type_A"