import math
import re

class ExpressionEvaluator:
    def __init__(self):
        self.variables = {}

    def evaluate(self, expression):
        expressions = expression.split(';')
        results = []
        for expr in expressions:
            expr = expr.strip()
            if not expr:
                continue
            try:
                result = self._evaluate_expression(expr)
                results.append(result)
            except (ValueError, SyntaxError, NameError, TypeError) as e:
                return f"Error: {e}"
        return self._format_results(results)

    def _evaluate_expression(self, expression):
        # Simple variable assignment handling
        if '=' in expression:
            var_name, value_expr = expression.split('=', 1)
            var_name = var_name.strip()
            value = self._evaluate_expression(value_expr.strip())
            self.variables[var_name] = value
            return f"{var_name} = {value}"

        # Evaluate using eval() with safety checks (highly discouraged for production)
        # For real-world applications, use a safer parsing and evaluation library like ast.literal_eval or a dedicated math expression parser.
        code = compile(expression, '<string>', 'eval')
        for name in code.co_names:
            if name not in math.__dict__ and name not in self.variables:
                raise NameError(f"Undefined variable or function: {name}")
        try:
            result = eval(code, {"__builtins__": {}}, {**math.__dict__, **self.variables})
            return result
        except (ValueError, TypeError) as e:
            raise ValueError(f"Evaluation error: {e}")


    def _format_results(self, results):
      if not results:
        return "No expressions to evaluate."
      output = ""
      for result in results:
        output += str(result) + "\n"
      return output


# Example usage
calculator = ExpressionEvaluator()

expression1 = "x = 10; y = 20; z = x + y; a = pow(2,3); b = sin(x); c = sqrt(100); d = abs(-5); e = log(10)"
print(f"Evaluating: {expression1}")
result1 = calculator.evaluate(expression1)
print(result1)


expression2 = "x = 10; y = 0; z = x / y" # Example of error handling
print(f"Evaluating: {expression2}")
result2 = calculator.evaluate(expression2)
print(result2)

expression3 = "x = 5; y = x 2; z = (x + y) 3"  # Example with parenthesis
print(f"Evaluating: {expression3}")
result3 = calculator.evaluate(expression3)
print(result3)

expression4 = "x = 10; y = x + 5; invalid_var" #Example with undefined variable
print(f"Evaluating: {expression4}")
result4 = calculator.evaluate(expression4)
print(result4)

expression5 = "" #Example with empty expression
print(f"Evaluating: {expression5}")
result5 = calculator.evaluate(expression5)
print(result5)