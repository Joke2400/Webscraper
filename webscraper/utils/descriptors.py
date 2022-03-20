from abc import ABC, abstractmethod

class BaseValidator(ABC):

    def __init__(self, check):
        self.check = check

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value, set_public=False):
        value = self.validate(value)
        if not set_public:
            setattr(obj, self.private_name, value)
        else:
            setattr(obj, self.public_name, value)

    def __delete__(self, obj):
        delattr(obj, self.private_name)

    @abstractmethod
    def validate(self, value):
        pass
class SpecifiedOrNoneValidator(BaseValidator):

    def validate(self, value):
        if not isinstance(value, self.check):
            if value is not None:
                raise TypeError(f"Validation failed on attribute: '{self.public_name}'.")
        return value

class SpecifiedOnlyValidator(BaseValidator):

    def validate(self, value):
        if not isinstance(value, self.check):
            raise TypeError(f"Validation failed on attribute: '{self.public_name}'.")
        return value

class ListContentValidator:

    def validate(self, value):
        if not all(isinstance(item, self.check) for item in value):
            raise TypeError(f"Validation failed on list: '{self.public_name}'.")
        return value

class StringValidator(BaseValidator):

    def validate(self, value):
        if not isinstance(value, str):
            if value is not None:
                raise TypeError(f"Attribute: '{self.public_name}' only accepts input of type: str")
        return value

class LowercaseStringValidator(BaseValidator):

    def validate(self, value):
        if not isinstance(value, str):
            if value is not None:
                raise TypeError(f"Attribute: '{self.public_name}' only accepts input of type: str")
        value = value.lower()
        return value
