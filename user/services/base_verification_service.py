from abc import ABC, abstractmethod

class BaseVerificationService(ABC):
    @abstractmethod
    def generate_code(self):
        pass

    @abstractmethod
    def send_code(self, user, code):
        pass
