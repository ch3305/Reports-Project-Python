from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class AttendanceRow:
  date: str
  day_of_week: Optional[str] = None
  entry_time: Optional[str] = None
  exit_time: Optional[str] = None
  break_time: Optional[str] = None
  total_hours: float = 0.0
  notes: Optional[str] = None
  work_place: Optional[str] = None
  hours_100: float = 0.0
  hours_125: float = 0.0
  hours_150: float = 0.0
  hours_shabbat: float = 0.0


@dataclass
class AttendanceReport:
  report_type: str  # "Type_A" או "Type_B"
  employee_name: str
  total_days: int
  total_monthly_hours: float
  rows: List[AttendanceRow] = field(default_factory=list)

  # שדות נוספים עבור סוג B
  card_number: Optional[str] = None
  month_title: Optional[str] = None
  hourly_rate: Optional[float] = None
  total_payment: Optional[float] = None

  # שדות נוספים עבור טבלת הסיכום של סוג A
  hours_100: float = 0.0
  hours_125: float = 0.0
  hours_150: float = 0.0
  hours_shabbat: float = 0.0
  bonus: float = 0.0
  travel: float = 0.0