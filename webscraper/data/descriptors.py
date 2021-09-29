from abc import ABC, abstractmethod

class BaseAttribute(ABC):

    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        pass

class StringAttribute(BaseAttribute):

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError("String Attribute only accepts input of type: str")
