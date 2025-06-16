# cheaper/utils/base_validator.py
from abc import ABC, abstractmethod

class BaseValidator(ABC):
    @abstractmethod
    def validate(self, value: str) -> bool:
        """Validate the input value."""
        pass