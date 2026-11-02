from dataclasses import dataclass
from typing import List, Optional

@dataclass
class AttendanceRow:
    date: str
    day_of_week: str
    entry_time: Optional[str] = None
    exit_time: Optional[str] = None
    break_time: Optional[str] = None
    total_hours: float = 0.0
    notes: Optional[str] = ""
    # Type A fields
    place: Optional[str] = None
    hours_100: float = 0.0
    hours_125: float = 0.0
    hours_150: float = 0.0
    shabbat_hours: float = 0.0

@dataclass
class AttendanceReport:
    report_type: str
    employee_name: str
    total_days: int
    total_monthly_hours: float
    rows: List[AttendanceRow]
    card_number: Optional[str] = None
    total_payment: Optional[float] = None
    hourly_rate: Optional[float] = None
    month_title: Optional[str] = None
    regular_monthly_hours: Optional[float] = None
    monthly_125_hours: Optional[float] = None
    monthly_150_hours: Optional[float] = None
    monthly_shabbat_hours: Optional[float] = None
    monthly_100_hours: Optional[float] = None