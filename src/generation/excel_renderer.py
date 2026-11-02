import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from src.domain.models import AttendanceReport


class ExcelRenderer:

  def render(self, report: AttendanceReport, output_path: str) -> str:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "דוח נוכחות"
    ws.views.sheetView[0].rightToLeft = True

    header_fill = PatternFill(
        start_color="D9E1F2", end_color="D9E1F2", fill_type="solid"
    )
    title_fill = PatternFill(
        start_color="B4C6E7", end_color="B4C6E7", fill_type="solid"
    )
    bold_font = Font(name="Calibri", size=11, bold=True)
    normal_font = Font(name="Calibri", size=11)
    title_font = Font(name="Calibri", size=14, bold=True)

    thin_border = Border(
        left=Side(style="thin", color="BFBFBF"),
        right=Side(style="thin", color="BFBFBF"),
        top=Side(style="thin", color="BFBFBF"),
        bottom=Side(style="thin", color="BFBFBF"),
    )

    # כותרת ראשית
    ws.merge_cells("A1:G1")
    title_cell = ws["A1"]
    title_cell.value = report.employee_name
    title_cell.font = title_font
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    title_cell.fill = title_fill

    current_row = 3

    # Type B בלבד מציג נתונים עליונים
    if report.report_type == "Type_B":
      ws.cell(row=current_row, column=1, value="מספר כרטיס:").font = bold_font
      ws.cell(row=current_row, column=2, value=report.card_number).font = (
          normal_font
      )
      current_row += 1
      ws.cell(
          row=current_row, column=1, value="סה\"כ ימי עבודה לחודש:"
      ).font = bold_font
      ws.cell(row=current_row, column=2, value=report.total_days).font = (
          normal_font
      )
      current_row += 1
      ws.cell(
          row=current_row, column=1, value="סה\"כ שעות חודשיות:"
      ).font = bold_font
      ws.cell(
          row=current_row, column=2, value=report.total_monthly_hours
      ).font = normal_font
      current_row += 1
      ws.cell(row=current_row, column=1, value="מחיר לשעה:").font = bold_font
      ws.cell(row=current_row, column=2, value=report.hourly_rate).font = (
          normal_font
      )
      current_row += 1
      ws.cell(row=current_row, column=1, value="סה\"כ לתשלום:").font = bold_font
      ws.cell(row=current_row, column=2, value=report.total_payment).font = (
          bold_font
      )
      current_row += 2

    # כותרות הטבלה הראשית בהתאם לסוג הדו"ח
    if report.report_type == "Type_A":
      headers = [
          "תאריך",
          "יום",
          "מקום",
          "כניסה",
          "יציאה",
          "הפסקה",
          "סה\"כ",
          "100%",
          "125%",
          "150%",
          "שבת",
      ]
    else:
      headers = [
          "תאריך",
          "יום בשבוע",
          "שעת כניסה",
          "שעת יציאה",
          "סה\"כ שעות",
          "הערות",
      ]

    for col_idx, header in enumerate(headers, start=1):
      cell = ws.cell(row=current_row, column=col_idx, value=header)
      cell.font = bold_font
      cell.fill = header_fill
      cell.alignment = Alignment(horizontal="center", vertical="center")
      cell.border = thin_border

    current_row += 1

    # הוספת שורות הנתונים
    for row_data in report.rows:
      if report.report_type == "Type_A":
        row_values = [
            row_data.date,
            row_data.day_of_week,
            row_data.work_place or "",
            row_data.entry_time or "",
            row_data.exit_time or "",
            row_data.break_time or "",
            row_data.total_hours,
            row_data.hours_100,
            row_data.hours_125,
            row_data.hours_150,
            row_data.hours_shabbat,
        ]
      else:
        row_values = [
            row_data.date,
            row_data.day_of_week,
            row_data.entry_time or "",
            row_data.exit_time or "",
            row_data.total_hours,
            row_data.notes or "",
        ]

      for col_idx, val in enumerate(row_values, start=1):
        cell = ws.cell(row=current_row, column=col_idx, value=val)
        cell.font = normal_font
        cell.border = thin_border
        cell.alignment = Alignment(horizontal="center", vertical="center")
      current_row += 1

    # Type A: טבלת הסיכום התחתונה (מופיעה למטה מתחת לטבלה)[cite: 5]
    if report.report_type == "Type_A":
      current_row += 2
      summary_headers = [
          ("ימים", report.total_days),
          ('סה"כ שעות', report.total_monthly_hours),
          ("שעות 100%", report.hours_100),
          ("שעות 125%", report.hours_125),
          ("שעות 150%", report.hours_150),
          ("שעות שבת (150%)", report.hours_shabbat),
          ("בונוס", report.bonus),
          ("נסיעות", report.travel),
      ]
      for label, val in summary_headers:
        lbl_cell = ws.cell(row=current_row, column=2, value=label)
        val_cell = ws.cell(row=current_row, column=1, value=val)
        lbl_cell.font = bold_font
        lbl_cell.border = thin_border
        lbl_cell.fill = header_fill
        val_cell.font = normal_font
        val_cell.border = thin_border
        val_cell.alignment = Alignment(horizontal="center", vertical="center")
        current_row += 1

    for col_idx in range(1, ws.max_column + 1):
      col_letter = get_column_letter(col_idx)
      max_len = 0
      for cell in ws[col_letter]:
        if cell.value:
          max_len = max(max_len, len(str(cell.value)))
      ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

    wb.save(output_path)
    return output_path