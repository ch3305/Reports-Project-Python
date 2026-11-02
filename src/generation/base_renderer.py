from abc import ABC, abstractmethod
from src.domain.models import AttendanceReport

class BaseRenderer(ABC):
    """
    Abstract renderer defining the interface for document generation.
    """

    @abstractmethod
    def render(self, report: AttendanceReport, output_path: str) -> str:
        """
        Renders the given report object to a file at output_path.
        Returns the path of the created file.
        """
        pass