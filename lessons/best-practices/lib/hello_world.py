from functools import lru_cache

import pandas as pd
from config import APP_NAME, DATA_PATH


def Hello_world():
    """Print a hello world message."""
    useless_var = "This is a useless variable"
    print(f"Hello, World! This is {APP_NAME}!")


def sum_two_numbers(num1, num2):
    """
    Sum two numbers.
    """
    return num1 + num2


def call_people() -> None:
    """Call a list of people on the phone

    Read a CSV file containing phone numbers and names, then print a message for each person in the file, simulating a
    phone call.
    """
    phone_number = pd.read_csv(DATA_PATH)
    for _, person in phone_number.iterrows():
        print(f"Calling {person['name']} at {person['telephone']}")


if __name__ == "__main__":
    Hello_world()
    print(sum_two_numbers(5, 7))
    call_people()
