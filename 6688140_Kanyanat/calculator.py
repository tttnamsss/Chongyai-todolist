"""Simple Python Calculator

A basic calculator that supports addition, subtraction, multiplication, and division.
"""


def add(a, b):
    """Add two numbers."""
    return a + b


def subtract(a, b):
    """Subtract two numbers."""
    return a - b


def multiply(a, b):
    """Multiply two numbers."""
    return a * b


def divide(a, b):
    """Divide two numbers."""
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b


def calculator():
    """Interactive calculator that accepts user input."""
    print("=" * 40)
    print("Simple Python Calculator")
    print("=" * 40)
    print("\nOperations:")
    print("  + : Add")
    print("  - : Subtract")
    print("  * : Multiply")
    print("  / : Divide")
    print("  q : Quit")
    print("=" * 40)

    while True:
        try:
            # Get user input
            operation = input("\nEnter operation (+, -, *, /, q): ").strip()

            if operation.lower() == 'q':
                print("Thank you for using the calculator. Goodbye!")
                break

            if operation not in ['+', '-', '*', '/']:
                print("Invalid operation. Please try again.")
                continue

            # Get numbers
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            # Perform calculation
            if operation == '+':
                result = add(num1, num2)
            elif operation == '-':
                result = subtract(num1, num2)
            elif operation == '*':
                result = multiply(num1, num2)
            elif operation == '/':
                result = divide(num1, num2)

            print(f"\nResult: {num1} {operation} {num2} = {result}")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    calculator()
