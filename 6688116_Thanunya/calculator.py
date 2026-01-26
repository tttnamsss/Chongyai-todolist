"""
Simple Calculator Module
Supports basic arithmetic operations: add, subtract, multiply, and divide
"""


class Calculator:
    """A simple calculator class for basic arithmetic operations."""

    def add(self, a, b):
        """Add two numbers."""
        return a + b

    def subtract(self, a, b):
        """Subtract b from a."""
        return a - b

    def multiply(self, a, b):
        """Multiply two numbers."""
        return a * b

    def divide(self, a, b):
        """Divide a by b."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def calculate_velocity(self, distance, time):
        """Calculate velocity given distance and time.
        
        Args:
            distance: Distance traveled (in any unit)
            time: Time taken (in any unit)
            
        Returns:
            Velocity as distance/time
            
        Raises:
            ValueError: If time is zero
        """
        if time == 0:
            raise ValueError("Time cannot be zero")
        return distance / time


def main():
    """Interactive calculator main function."""
    calc = Calculator()

    print("=" * 40)
    print("Welcome to Simple Calculator")
    print("=" * 40)

    while True:
        print("\nChoose an operation:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Calculate Velocity")
        print("6. Exit")

        choice = input("\nEnter choice (1/2/3/4/5/6): ").strip()

        if choice == "6":
            print("Thank you for using the calculator. Goodbye!")
            break

        if choice not in ["1", "2", "3", "4", "5"]:
            print("Invalid choice. Please try again.")
            continue

        try:
            if choice == "5":
                distance = float(input("Enter distance: "))
                time = float(input("Enter time: "))
                result = calc.calculate_velocity(distance, time)
                print(f"\nVelocity = {distance} / {time} = {result} units/time")
            else:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))

                if choice == "1":
                    result = calc.add(num1, num2)
                    operation = "+"
                elif choice == "2":
                    result = calc.subtract(num1, num2)
                    operation = "-"
                elif choice == "3":
                    result = calc.multiply(num1, num2)
                    operation = "*"
                elif choice == "4":
                    result = calc.divide(num1, num2)
                    operation = "/"

                print(f"\n{num1} {operation} {num2} = {result}")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Invalid input: {e}. Please enter valid numbers.")


if __name__ == "__main__":
    main()
