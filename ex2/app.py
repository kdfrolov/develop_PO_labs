import abc
import math

class Expression(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def evaluate(self):
        pass

class ArithmeticExpression(Expression):
    def __init__(self, expression_str):
        self.expression_str = expression_str

    def evaluate(self):
        try:
            parts = self.expression_str.split()

            num_left = float(parts[0])
            operator = parts[1]
            num_right = float(parts[2])

            if operator == '+':
                res = num_left + num_right
            elif operator == '-':
                res = num_left - num_right
            elif operator == '*':
                res = num_left * num_right
            elif operator == '/':
                if num_right == 0:
                    raise ZeroDivisionError("Деление на ноль")
                res = num_left / num_right
            elif operator == '<':
                res = num_left < num_right
            elif operator == '>':
                res = num_left > num_right
            elif operator == '<=':
                res = num_left <= num_right
            elif operator == '>=':
                res = num_left >= num_right
            elif operator == '!=':
                res = num_left != num_right
            elif operator == '==':
                res = num_left == num_right
            else:
                raise ValueError("Неизвестный оператор. Допустимы: +, -, *, /, <, >, <=, >=, !=, ==")

            return res
            except ValueError as e:
                return f"Ошибка: {e}"
            except ZeroDivisionError as e:
                return f"Ошибка: {e}"
            except Exception as e:
                return f"Непредвиденная ошибка: {e}"
        
        # Здесь можно использовать более безопасный способ вычисления, чем eval()
        # Например, библиотеку ast.literal_eval или специализированный парсер
        code = compile(self.expression_str, '<string>', 'eval')
        try:
            result = eval(code, {"__builtins__": {}}, {**math.__dict__})
            return result
        except (ValueError, TypeError, NameError) as e:
            raise ValueError(f"Evaluation error: {e}")


class AssignmentExpression(Expression):
    def __init__(self, var_name, expression):
        self.var_name = var_name
        self.expression = expression

    def evaluate(self):
        value = self.expression.evaluate()
        # Здесь можно добавить обработку ошибок присваивания
        return f"{self.var_name} = {value}"


class ExpressionEvaluator:
    def __init__(self):
        self.variables = {}

    def evaluate(self, expression_str):
        expressions = expression_str.split(';')
        results = []
        for expr_str in expressions:
            expr_str = expr_str.strip()
            if not expr_str:
                continue
            try:
                expression = self._parse_expression(expr_str)
                result = expression.evaluate()
                results.append(result)
            except (ValueError, SyntaxError) as e:
                return f"Error: {e}"
        return "\n".join(map(str, results))


    def _parse_expression(self, expression_str):
        """Разбирает строку и создает соответствующий объект выражения."""
        if '=' in expression_str:
            var_name, value_expr = expression_str.split('=', 1)
            var_name = var_name.strip()
            value_expression = self._parse_expression(value_expr.strip())
            return AssignmentExpression(var_name, value_expression)
        else:
            return ArithmeticExpression(expression_str)



# Пример использования
evaluator = ExpressionEvaluator()
expression = "x = 10; y = 20; z = x + y; a = pow(2, 3)"
result = evaluator.evaluate(expression)
print(result)

# expression2 = "x = 10; y = x + 5; z = (x + y) 3"
# result2 = evaluator.evaluate(expression2)
# print(result2)

# expression3 = "x = 10; y = 0; z = x / y"  #Ошибка
# result3 = evaluator.evaluate(expression3)
# print(result3)