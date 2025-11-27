# Sample Python Code for Testing

def calculate_factorial(n):
    """Calculate factorial of a number"""
    if n == 0 or n == 1:
        return 1
    return n * calculate_factorial(n - 1)


class Calculator:
    """A simple calculator class"""
    
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


def main():
    calc = Calculator()
    print(f"5 + 3 = {calc.add(5, 3)}")
    print(f"5 - 3 = {calc.subtract(5, 3)}")
    print(f"5 * 3 = {calc.multiply(5, 3)}")
    print(f"5 / 3 = {calc.divide(5, 3)}")
    
    print(f"\nFactorial of 5 = {calculate_factorial(5)}")


if __name__ == "__main__":
    main()