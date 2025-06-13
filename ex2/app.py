import math
import re


# Абстрактный класс
class Expression:
    def calculate(self, variables):
        raise NotImplementedError


# Класс для бинарных операций
class BinaryOperation(Expression):
    def __init__(self, num_left, operator, num_right):
        self.num_left = num_left
        self.operator = operator
        self.num_right = num_right

    def calculate(self, variables):
        l = self.num_left.calculate(variables)
        r = self.num_right.calculate(variables)
        if self.operator == "+":
            return l + r
        elif self.operator == "*":
            return l * r
        elif self.operator == "/":
            return l / r
        elif self.operator == "-":
            return l - r
        else:
            raise Exception(f"Неподдерживаемый оператор {self.op}")


# Класс для переменных
class Variable(Expression):
    def __init__(self, name):
        self.name = name

    def calculate(self, variables):
        if self.name in variables:
            return variables[self.name]
        else:
            raise Exception(f"Переменная {self.name} не определена")


# Класс для операций присваивания
class Assignment(Expression):
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

    def calculate(self, variables):
        value = self.expr.calculate(variables)
        variables[self.var.name] = value
        return value


# Класс для функций
class Function(Expression):
    def __init__(self, name, arg):
        self.name = name
        self.arg = arg

    def calculate(self, variables):
        arg_val = self.arg.calculate(variables)
        if self.name == "sin":
            return math.sin(arg_val)
        elif self.name == "log":
            return math.log(arg_val)
        elif self.name == "sqrt":
            return math.sqrt(arg_val)
        elif self.name == "abs":
            return abs(arg_val)
        elif self.name == "pow":
            if isinstance(self.arg, BinaryOperation):
                l = self.arg.num_left.calculate(variables)
                r = self.arg.num_right.calculate(variables)
                return math.pow(l, r)
            else:
                raise Exception("Для pow требуется 2 аргумента")
        else:
            raise Exception(f"Неизвестная функция {self.name}")


# Класс для числовых значений
class Number(Expression):
    def __init__(self, value):
        self.value = value

    def calculate(self, variables):
        return self.value


# Парсер выражений
def parser(expr):
    expr = expr.strip()
    if "=" in expr:
        var, val = expr.split("=", 1)
        return Assignment(Variable(var.strip()), parser(val.strip()))

    for op in ["+", "*", "/", "-"]:
        if op in expr:
            num_left, num_right = expr.split(op, 1)
            return BinaryOperation(
                parser(num_left.strip()), op, parser(num_right.strip())
            )

    if "(" in expr and expr.endswith(")"):
        fname, arg = expr.split("(", 1)
        arg = arg[:-1]
        return Function(fname.strip(), parser(arg.strip()))

    if re.match(r"^[a-zA-Z_]\w*$", expr):
        return Variable(expr)
    try:
        return Number(float(expr))
    except ValueError:
        raise Exception(f"Не удается произвести парсинг: {expr}")


def main():
    vars = {}
    try:
        inputs = input("Введите выражения: ")
        statements = inputs.split(";")
        for i in statements:
            if i.strip():
                expr = parser(i)
                expr.calculate(vars)
        print("Переменные и значения:")
        for x, y in vars.items():
            print(f"{x} = {y}")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
