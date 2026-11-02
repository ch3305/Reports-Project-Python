import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from src.generation.base_renderer import BaseRenderer
from src.domain.models import AttendanceReport


class ExcelRenderer(BaseRenderer):
    def render(self, report: AttendanceReport, output_path: str) -> str:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "דו\"ח נוכחות"
        ws.views.sheetView[0].rightToLeft = True

        header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
        header_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
        title_font = Font(name="Segoe UI", size=14, bold=True, color="1F4E79")
        bold_font = Font(name="Segoe UI", size=10, bold=True)
        regular_font = Font(name="Segoe UI", size=10)

        thin_border = Border(
            left=Side(style='thin', color='D9D9D9'),
            right=Side(style='thin', color='D9D9D9'),
            top=Side(style='thin', color='D9D9D9'),
            bottom=Side(style='thin', color='D9D9D9')
        )

        # כותרת מותאמת לפי סוג הדו"ח
        if report.report_type == "Type_A":
            ws.cell(row=1, column=1, value=f"דו\"ח נוכחות - {report.report_type}").font = title_font
            ws.cell(row=2, column=1, value=f"שם העובד: {report.employee_name}").font = bold_font
            headers = ["תאריך", "יום", "מקום ע.", "כניסה", "יציאה", "הפסקה", "סה\"כ", "100%", "125%", "150%", "שבת"]
        else:
            # כותרת מותאמת לסוג B בדיוק לפי המקור
            title_text = f"כרטיס עובד לחודש: {report.month_title or 'ספט-22'} | כרטיס: {report.card_number}"
            ws.cell(row=1, column=1, value=title_text).font = title_font
            headers = ["תאריך", "יום בשבוע", "שעת כניסה", "שעת יציאה", "סה\"כ שעות", "הערות"]

        start_row = 4

        # כתיבת הכותרות
        for col_idx, header in enumerate(headers, 1):
            cell = ws.cell(row=start_row, column=col_idx, value=header)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")

        # כתיבת השורות
        current_row = start_row + 1
        for row_data in report.rows:
            if report.report_type == "Type_A":
                row_values = [
                    row_data.date, row_data.day_of_week, row_data.place or "גליון",
                    row_data.entry_time or "", row_data.exit_time or "", row_data.break_time or "",
                    row_data.total_hours, row_data.hours_100, row_data.hours_125,
                    row_data.hours_150, row_data.shabbat_hours
                ]
            else:
                row_values = [
                    row_data.date,
                    row_data.day_of_week,
                    row_data.entry_time or "",
                    row_data.exit_time or "",
                    row_data.total_hours,
                    row_data.notes or ""
                ]

            for col_idx, val in enumerate(row_values, 1):
                cell = ws.cell(row=current_row, column=col_idx, value=val)
                cell.font = regular_font
                cell.border = thin_border
                cell.alignment = Alignment(horizontal="center", vertical="center")
            current_row += 1

        # סיכומים
        current_row += 1
        ws.cell(row=current_row, column=1, value="סה\"כ ימי עבודה לחודש:").font = bold_font
        ws.cell(row=current_row, column=2, value=report.total_days).font = bold_font

        current_row += 1
        ws.cell(row=current_row, column=1, value="סה\"כ שעות חודשיות:").font = bold_font
        ws.cell(row=current_row, column=2, value=report.total_monthly_hours).font = bold_font

        if report.report_type == "Type_B":
            if report.hourly_rate:
                current_row += 1
                ws.cell(row=current_row, column=1, value="מחיר לשעה:").font = bold_font
                ws.cell(row=current_row, column=2, value=f"₪{report.hourly_rate:,.2f}").font = bold_font

            if report.total_payment:
                current_row += 1
                ws.cell(row=current_row, column=1, value="סה\"כ לתשלום:").font = bold_font
                ws.cell(row=current_row, column=2, value=f"₪{report.total_payment:,.2f}").font = bold_font

        wb.save(output_path)
        return output_path