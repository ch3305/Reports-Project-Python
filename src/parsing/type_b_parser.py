import random
from typing import List
from src.domain.models import AttendanceReport, AttendanceRow
from src.parsing.base_parser import BaseParser


class TypeBParser(BaseParser):
    def parse_report(self) -> AttendanceReport:
        rows: List[AttendanceRow] = []

        months_list = [("ינו", "1"), ("פבר", "2"), ("מרץ", "3"), ("אפר", "4"), ("מאי", "5"), ("יונ", "6"),
                       ("יול", "7"), ("אוג", "8"), ("ספט", "9"), ("אוק", "10"), ("נוב", "11"), ("דצמ", "12")]
        chosen_month_name, chosen_month_num = random.choice(months_list)
        years_list = ["21", "22", "23", "24", "25", "26"]
        year_short = random.choice(years_list)
        month_title = f"{chosen_month_name}-{year_short}"
        card_num = f"{random.randint(10, 99)}-{random.randint(100, 999)}"

        for idx in range(1, 25):
            date_str = f"{idx}/{chosen_month_num}/{year_short}"
            rows.append(AttendanceRow(
                date=date_str,
                day_of_week=random.choice(["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי"]),
                entry_time="8:30",
                exit_time="12:00",
                total_hours=3.5,
                notes=""
            ))

        total_days = len(rows)
        total_monthly_hours = sum(r.total_hours for r in rows)
        hourly_rate = 30.65
        total_payment = round(total_monthly_hours * hourly_rate, 2)

        return AttendanceReport(
            report_type="Type_B",
            employee_name=f"כרטיס עובד לחודש: {month_title}",
            total_days=total_days,
            total_monthly_hours=total_monthly_hours,
            rows=rows,
            card_number=card_num,
            month_title=month_title,
            hourly_rate=hourly_rate,
            total_payment=total_payment
        )