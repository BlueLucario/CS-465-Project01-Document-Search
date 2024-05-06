from abc import ABC, abstractmethod

class AbstractDocument(ABC):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.name

class SimpleDocument(AbstractDocument):
    def __init__(self, name: str, id: int):
        super().__init__(name)
        self.id = id

class FlexibleDocument(AbstractDocument):
    def __init__(self, name: str, id: int, **kwargs):
        super().__init__(name)
        self.id = id

        for property, value in kwargs.items():
            setattr(self, property, value)
