import random
import string


def generate_random_password():
    # Define the pattern for the password
    pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*_=+-]).{8,}$'

    # Define character sets for each pattern requirement
    uppercase_chars = string.ascii_uppercase
    lowercase_chars = string.ascii_lowercase
    digit_chars = string.digits
    special_chars = '!@#$%^&*_=+-'

    # Create a list to store characters that meet the pattern requirements
    valid_chars = []

    # Add at least 1 character from each character set
    valid_chars.extend(random.choice(uppercase_chars))
    valid_chars.extend(random.choice(lowercase_chars))
    valid_chars.extend(random.choice(digit_chars))
    valid_chars.extend(random.choice(special_chars))

    # Fill the rest of the string with random characters
    remaining_length = max(0, random.randint(10, 20) - len(valid_chars))
    valid_chars.extend(random.choice(uppercase_chars + lowercase_chars + digit_chars + special_chars) for _ in range(remaining_length))

    # Shuffle the valid characters to randomize the order
    random.shuffle(valid_chars)

    # Convert the list of characters to a string
    password = ''.join(valid_chars)

    return password
