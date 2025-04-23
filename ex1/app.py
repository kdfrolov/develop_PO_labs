def calc(expr):
    """Вычисляет результат арифметического или логического выражения."""
    try:
        parts = expr.split()
        if len(parts) != 3:
            raise ValueError("Некорректный формат выражения. Требуется 'число оператор число'")

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


while True:
    expr = input("Введите арифметическое или логическое выражение (например, 10 + 5) или 'quit' для выхода: ")
    if expr.lower() == 'q':
        break
    res = calc(expr)
    print(f"Результат: {res}")
