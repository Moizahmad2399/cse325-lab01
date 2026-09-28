# CSE325-2026-L01-K7QX
def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a Celsius temperature to Fahrenheit."""
    return celsius * 9 / 5 + 32

if __name__ == "__main__":
    try:
        c = float(input("Celsius: "))
        print(f"{c}C = {celsius_to_fahrenheit(c)}F")
    except ValueError:
        print("Please enter a numeric value.")