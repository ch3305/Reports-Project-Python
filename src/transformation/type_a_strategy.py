import random
from datetime import datetime, timedelta
from copy import deepcopy
from src.transformation.base_strategy import BaseStrategy
from src.domain.models import AttendanceReport, AttendanceRow


class TypeAStrategy(BaseStrategy):
    """
    Data variation strategy for Type A reports.
    Adjusts start/end times within a realistic range and recalculates total hours.
    """

    def transform(self, report: AttendanceReport) -> AttendanceReport:
        new_report = deepcopy(report)
        new_rows: list[AttendanceRow] = []

        for row in new_report.rows:
            if row.entry_time and row.exit_time:
                # Add random variation of +/- 15 minutes to entry and exit times
                entry_dt = datetime.strptime(row.entry_time, "%H:%M")
                exit_dt = datetime.strptime(row.exit_time, "%H:%M")

                shift_entry = random.randint(-15, 15)
                shift_exit = random.randint(-15, 15)

                new_entry_dt = entry_dt + timedelta(minutes=shift_entry)
                new_exit_dt = exit_dt + timedelta(minutes=shift_exit)

                # Ensure exit is strictly after entry
                if new_exit_dt <= new_entry_dt:
                    new_exit_dt = new_entry_dt + timedelta(hours=8)

                # Calculate new total hours (assuming 30 min break)
                duration = (new_exit_dt - new_entry_dt).total_seconds() / 3600.0
                break_hours = 0.5 if duration > 5.0 else 0.0
                total_hours = round(max(0.0, duration - break_hours), 2)

                row.entry_time = new_entry_dt.strftime("%H:%M")
                row.exit_time = new_exit_dt.strftime("%H:%M")
                row.total_hours = total_hours

            new_rows.append(row)

        new_report.rows = new_rows
        new_report.total_days = len(new_rows)
        new_report.total_monthly_hours = round(sum(r.total_hours for r in new_rows), 2)
        return new_report