import random
from datetime import datetime, timedelta
from copy import deepcopy
from src.transformation.base_strategy import BaseStrategy
from src.domain.models import AttendanceReport


class TypeBStrategy(BaseStrategy):
    """
    Data variation strategy for Type B reports.
    Adjusts times, recalculates hours, and updates financial totals.
    """

    def transform(self, report: AttendanceReport) -> AttendanceReport:
        new_report = deepcopy(report)
        new_rows = []

        for row in new_report.rows:
            if row.entry_time and row.exit_time:
                entry_dt = datetime.strptime(row.entry_time, "%H:%M")
                exit_dt = datetime.strptime(row.exit_time, "%H:%M")

                # Slight variation of +/- 10 minutes
                new_entry_dt = entry_dt + timedelta(minutes=random.randint(-10, 10))
                new_exit_dt = exit_dt + timedelta(minutes=random.randint(-10, 10))

                if new_exit_dt <= new_entry_dt:
                    new_exit_dt = new_entry_dt + timedelta(hours=4)

                total_hours = round((new_exit_dt - new_entry_dt).total_seconds() / 3600.0, 2)

                row.entry_time = new_entry_dt.strftime("%H:%M")
                row.exit_time = new_exit_dt.strftime("%H:%M")
                row.total_hours = total_hours

            new_rows.append(row)

        new_report.rows = new_rows
        new_report.total_days = len(new_rows)
        new_report.total_monthly_hours = round(sum(r.total_hours for r in new_rows), 2)

        # Recalculate financial totals if hourly rate exists
        if new_report.hourly_rate:
            new_report.total_payment = round(new_report.total_monthly_hours * new_report.hourly_rate, 2)

        return new_report