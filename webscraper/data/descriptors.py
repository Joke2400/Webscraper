from abc import ABC, abstractmethod

class BaseAttribute(ABC):

    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        value = self.validate(value)
        setattr(obj, self.private_name, value)

    def __delete__(self, obj):
        delattr(obj, self.private_name)

    @abstractmethod
    def validate(self, value):
        pass

class StringAttribute(BaseAttribute):

    def validate(self, value):
        if not isinstance(value, str):
            if value is None:
                value = "" 
            else:
                raise TypeError("String Attribute only accepts input of type: str")
        return value

class LowercaseStringAttribute(BaseAttribute):

    def validate(self, value):
        if not isinstance(value, str):
            if value is None:
                value = ""
            else:
                raise TypeError("String Attribute only accepts input of type: str")
        value = value.lower()
        return value

class DataStringAttribute(BaseAttribute):

    def validate(self, value):
        if not isinstance(value, str):
            if value is not None:
                raise TypeError("Data String Attribute can only be 'str' or 'None'")    
        else:
            value = value.lower()
        return value

class NumberAttribute(BaseAttribute):

    def validate(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Number Attribute only accepts input of type(s): int/float")
        return value

class ListAttribute(BaseAttribute):

    def validate(self, value):
        if not isinstance(value, (list, tuple)):
            raise TypeError("Iterable Attribute only accepts input of type(s): list/tuple")
        return value

class LocationAttribute(BaseAttribute):

    def validate(self, value):
        from .custom_data_classes import LocationTuple #yep
        if not isinstance(value, LocationTuple):
            raise TypeError("Location Attribute only accepts input of type: LocationTuple")
        return value