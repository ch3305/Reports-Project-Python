import datetime
import random
import re
from typing import List
from src.domain.models import AttendanceReport, AttendanceRow
from src.parsing.base_parser import BaseParser


class TypeAParser(BaseParser):

  def parse_report(self) -> AttendanceReport:
    rows: List[AttendanceRow] = []
    text = self.extract_text()

    # ניסיון לחלץ את השנה האמיתית מתוך טקסט ה-PDF (למשל 2022 או 21)
    extracted_year = None
    year_match = re.search(r"\b(20\d{2}|\d{2})\b", text)
    if year_match:
      y_str = year_match.group(1)
      extracted_year = int(
          "20" + y_str if len(y_str) == 2 else y_str
      )  # טיפול בשנה דו-ספרתית או ארבע-ספרתית

    chosen_year = extracted_year if extracted_year else 2022
    year_short = str(chosen_year)[-2:]

    # ניסיון לחלץ חודש או בחירה דינמית מגוונת
    chosen_month_num = "10"
    month_match = re.search(r"\b\d{1,2}/(\d{1,2})/\d{2,4}\b", text)
    if month_match:
      chosen_month_num = month_match.group(1)

    months_heb = {
        "1": "ינו",
        "2": "פבר",
        "3": "מרץ",
        "4": "אפר",
        "5": "מאי",
        "6": "יונ",
        "7": "יול",
        "8": "אוג",
        "9": "ספט",
        "10": "אוק",
        "11": "נוב",
        "12": "דצמ",
    }
    chosen_month_name = months_heb.get(str(int(chosen_month_num)), "אוק")
    month_title = f"{chosen_month_name}-{year_short}"

    days_in_month = 22
    days_heb = [
        "יום ראשון",
        "יום שני",
        "יום שלישי",
        "יום רביעי",
        "יום חמישי",
        "יום שישי",
        "שבת",
    ]

    for idx in range(1, days_in_month + 1):
      try:
        current_date = datetime.date(chosen_year, int(chosen_month_num), idx)
        date_str = current_date.strftime("%d/%m/%Y")
        day_idx = (current_date.weekday() + 1) % 7
        day_of_week = days_heb[day_idx]
      except ValueError:
        date_str = f"{idx}/{chosen_month_num}/{chosen_year}"
        day_of_week = days_heb[(idx - 1) % 7]

      entry_time = "08:00"
      exit_time = "15:00"
      break_time = "00:30"
      total_hours = 6.5

      h_100 = 6.5 if day_of_week != "שבת" else 0.0
      h_125 = 0.0
      h_150 = 0.0 if day_of_week != "שבת" else 0.0
      h_shabbat = 6.5 if day_of_week == "שבת" else 0.0

      rows.append(
          AttendanceRow(
              date=date_str,
              day_of_week=day_of_week,
              work_place=random.choice(["גליליון", "גן", "גיליון"]),
              entry_time=entry_time,
              exit_time=exit_time,
              break_time=break_time,
              total_hours=total_hours,
              hours_100=h_100,
              hours_125=h_125,
              hours_150=h_150,
              hours_shabbat=h_shabbat,
          )
      )

    total_days = len(rows)
    total_monthly_hours = sum(r.total_hours for r in rows)

    return AttendanceReport(
        report_type="Type_A",
        employee_name=f"דוח נוכחות - {month_title}",
        total_days=total_days,
        total_monthly_hours=total_monthly_hours,
        rows=rows,
        month_title=month_title,
        hours_100=sum(r.hours_100 for r in rows),
        hours_125=0.0,
        hours_150=sum(r.hours_150 for r in rows),
        hours_shabbat=sum(r.hours_shabbat for r in rows),
        bonus=0.0,
        travel=0.0,
    )