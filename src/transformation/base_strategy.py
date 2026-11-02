from abc import ABC, abstractmethod
import random
from src.domain.models import AttendanceReport
from src.domain.models import AttendanceReport

class TypeBStrategy:
    def transform(self, report: AttendanceReport) -> AttendanceReport:
        # בדיקה בטוחה האם השדה קיים לפני גישה אליו
        if hasattr(report, 'hourly_rate') and report.hourly_rate:
            pass
        return report
class BaseStrategy(ABC):
    """
    Abstract base class for data variation strategies using Strategy Pattern.
    """

    def __init__(self, seed: int = 42):
        # Set a fixed seed to ensure deterministic behavior across runs
        self.seed = seed
        random.seed(self.seed)

    @abstractmethod
    def transform(self, report: AttendanceReport) -> AttendanceReport:
        """
        Applies variations to the input report while maintaining logical consistency.
        """
        pass