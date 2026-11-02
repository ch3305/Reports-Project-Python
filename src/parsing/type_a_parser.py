import datetime
import random
from typing import List
from src.domain.models import AttendanceReport, AttendanceRow
from src.parsing.base_parser import BaseParser


class TypeAParser(BaseParser):

  def parse_report(self) -> AttendanceReport:
    rows: List[AttendanceRow] = []

    months_list = [
        ("ינו", "1"),
        ("פבר", "2"),
        ("מרץ", "3"),
        ("אפר", "4"),
        ("מאי", "5"),
        ("יונ", "6"),
        ("יול", "7"),
        ("אוג", "8"),
        ("ספט", "9"),
        ("אוק", "10"),
        ("נוב", "11"),
        ("דצמ", "12"),
    ]
    chosen_month_name, chosen_month_num = random.choice(months_list)
    years_list = [2021, 2022, 2023, 2024, 2025, 2026]
    chosen_year = random.choice(years_list)
    month_title = f"{chosen_month_name}-{str(chosen_year)[-2:]}"

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
      # חישוב תאריך עוקב אמיתי ויום בשבוע התואם לו במדויק
      try:
        current_date = datetime.date(chosen_year, int(chosen_month_num), idx)
        date_str = current_date.strftime("%d/%m/%Y")
        # התאמת היום בשבוע לפי התאריך הלועזי (0=ראשון או שני בהתאם לפייתון, נמיר לעברית)
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