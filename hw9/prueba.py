def format_to_six_digits(number):
    # Convert the number to a string and use zfill to add leading zeros
    formatted_number = str(number).zfill(6)
    print(type(formatted_number))
    return formatted_number

# Example usage:
number1 = 12345
formatted_number1 = format_to_six_digits(number1)
print(formatted_number1)  # Output: 012345

number2 = 987654
formatted_number2 = format_to_six_digits(number2)
print(formatted_number2)  # Output: 987654