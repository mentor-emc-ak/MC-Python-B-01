# We want to build a calculator with class Calculator. It should have methods for addition, subtraction, multiplication, and division.


class Calculator:

    def __init__(self):
        pass

    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod   
    def divide(a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

print("Welcome to the Calculator!")
calc = Calculator()

calc.add(5, 3)        # Output: 8
calc.subtract(5, 3)   # Output: 2
calc.multiply(5, 3)   # Output: 15
calc.divide(5, 3)     # Output: 1.666666666666


