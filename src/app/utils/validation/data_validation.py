"""Base data validator class"""
from abc import ABC, abstractmethod

class BaseDataValidation(ABC):
    
    @abstractmethod
    def data_validator_create(self, data) -> bool:
        pass
    
    @abstractmethod
    def data_validator_update(self, data) -> bool:
        pass
