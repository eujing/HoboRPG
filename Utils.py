import inspect
import _ast
import types


def autoslot(cls):
    """
    A decorator to optimize the memory footprint of classes.
    Automatically generates a modified class with '__slots__' based on the __init__ definition.

    Args:
        cls: Class to optimize

    Returns:
        A modified version of the class that does not use a dict internally
    """
    name = cls.__name__
    bases = cls.__bases__

    body = {funcName: func for funcName, func in inspect.getmembers(cls)
            if isinstance(func, types.FunctionType)}

    slots = []
    for base in bases:
        if hasattr(base, "__slots__"):
            slots.extend(base.__slots__)

    # Parse ast of target class to look for assignments to attributes
    source = inspect.getsource(cls)
    ast = compile(source, "dummyFile", "exec", _ast.PyCF_ONLY_AST)

    classdef = ast.body[0]
    for declaration in classdef.body:
        if isinstance(declaration, _ast.FunctionDef):
            if declaration.name == "__init__":
                for statement in declaration.body:
                    if isinstance(statement, _ast.Assign):
                        for target in statement.targets:
                            if target.attr not in slots:
                                slots.append(target.attr)

    body["__slots__"] = slots

    return type(name, bases, body)


class Vector2D(object):
    """
    A convenient class for doing 2D operations
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector2D(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vector2D(x, y)

    def __mul__(self, other):
        if isinstance(other, Vector2D):
            x = self.x * other.x
            y = self.y * other.y
        else:
            x = other * self.x
            y = other * self.y
        return Vector2D(x, y)

    def __div__(self, other):
        if isinstance(other, Vector2D):
            x = self.x / other.x
            y = self.y / other.y
        else:
            x = self.x / other
            y = self.y / other
        return Vector2D(x, y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self, other):
        if isinstance(other, Vector2D):
            self.x *= other.x
            self.y *= other.y
        else:
            self.x *= other
            self.y *= other
        return self

    def __idiv__(self, other):
        if isinstance(other, Vector2D):
            self.x /= other.x
            self.y /= other.y
        else:
            self.x /= other
            self.y /= other
        return self

    def limit(self, topLeft, bottomRight):
        if not isinstance(topLeft, Vector2D):
            raise TypeError
        if not isinstance(bottomRight, Vector2D):
            raise TypeError
        self.x = limit(self.x, topLeft.x, bottomRight.x)
        self.y = limit(self.y, topLeft.y, bottomRight.y)

    def within(self, topLeft, bottomRight):
        if not isinstance(topLeft, Vector2D):
            raise TypeError
        if not isinstance(bottomRight, Vector2D):
            raise TypeError
        if self.x < topLeft.x or self.x > bottomRight.x:
            return False
        if self.y < topLeft.y or self.y > bottomRight.y:
            return False
        else:
            return True


def limit(var, lower, higher):
    if var < lower:
        return lower
    elif var >= higher:
        return higher
    else:
        return var
