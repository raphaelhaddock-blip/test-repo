def add(a, b):
    """Add two numbers"""
    return a + b

def subtract(a, b):
    """Subtract b from a"""
    return a - b

def multiply(a, b):
    """Multiply two numbers"""
    return a * b

def divide(a, b):
    """Divide a by b"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def power(base, exponent):
    """Raise base to the power of exponent"""
    return base ** exponent

def modulo(a, b):
    """Return the remainder of a divided by b"""
    if b == 0:
        raise ValueError("Cannot perform modulo by zero")
    return a % b

def square_root(a):
    """Return the square root of a"""
    if a < 0:
        raise ValueError("Cannot take square root of a negative number")
    return a ** 0.5

if __name__ == "__main__":
    print("Simple Calculator")
    print("5 + 3 =", add(5, 3))
    print("5 - 3 =", subtract(5, 3))
    print("5 * 3 =", multiply(5, 3))
    print("5 / 3 =", divide(5, 3))
    print("2 ^ 3 =", power(2, 3))
    print("10 % 3 =", modulo(10, 3))
    print("sqrt(16) =", square_root(16))