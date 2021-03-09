import random


# reading and filtering the text in the file so that it has only uppercase letters
def read_and_filter(input_file, plain_text):
    file = open(input_file, 'r')
    for character in file.read():
        if character == character.lower():
            character = character.upper()
        if 'A' <= character <= 'Z':
            plain_text += character
    file.close()
    return plain_text


# encrypting the plain_text with a given key
def encrypt_text(plain_text, encrypted_text, key, output_file, number_has_letter, letter_has_number):
    m = len(key)
    for i in range(len(plain_text)):
        encrypted_text += number_has_letter[(letter_has_number[plain_text[i]] + letter_has_number[key[i % m]]) % 26]

    output = open(output_file, "w")
    output.write(encrypted_text)
    output.close()
    return encrypted_text


# generating a random key with length of at least 7 and maximum of 26
def generate_key(alphabet):
    generated_key = ''
    for i in range(0, random.randrange(7, 25)):
        generated_key += random.choice(alphabet)
    return generated_key


# shift each letter with a given offset
def shift(shift_offset, text_to_shift):
    shifted_text = ''
    for letter in text_to_shift:
        if chr(ord(letter) + shift_offset) > 'Z':
            letter = chr(((ord(letter) + shift_offset) - ord('Z')) + ord('A') - 1)
        else:
            letter = chr(ord(letter) + shift_offset)
        shifted_text += letter
    return shifted_text


# from a string of characters, compute the frequencies of each letter of the string and then calculate the probability
# of choosing the same 2 letters in a row
def index_of_coincidence(string_of_letters):
    index = 0.0
    frequency_of_letters = {}
    for i in range(len(string_of_letters)):
        if string_of_letters[i] in frequency_of_letters:
            frequency_of_letters[string_of_letters[i]] += 1
        else:
            frequency_of_letters[string_of_letters[i]] = 1
    length = len(string_of_letters)
    for i in frequency_of_letters:
        index += float(frequency_of_letters[i] / length) * float((frequency_of_letters[i] - 1) / (length - 1))
    return index


def mutual_index_of_coincidence(string_of_letters, english_letter_frequencies):
    mutual_ic = 0.0
    length = len(string_of_letters)
    frequency_of_letters = {}
    for i in range(len(string_of_letters)):
        if string_of_letters[i] in frequency_of_letters:
            frequency_of_letters[string_of_letters[i]] += 1
        else:
            frequency_of_letters[string_of_letters[i]] = 1
    for i in frequency_of_letters:
        mutual_ic += english_letter_frequencies[i] * float(frequency_of_letters[i] / length)
    return mutual_ic


def get_key_length(encrypted_text):
    best_avg = 0
    key_length = 0
    best_key_length = 0
    best_index_of_coincidence_array = []
    for i in range(156):
        index_of_coincidence_array = []
        key_length += 1
        for j in range(key_length):
            index_of_coincidence_array.append(index_of_coincidence(encrypted_text[j::key_length]))
        avg = sum(index_of_coincidence_array) / len(index_of_coincidence_array)

        if abs(avg - 0.065) < abs(best_avg - 0.065):
            best_avg = avg
            best_index_of_coincidence_array = index_of_coincidence_array
            best_key_length = key_length
    print(f"IC Array values: {best_index_of_coincidence_array}")
    return best_key_length


def get_key(encrypted_text, key_length, english_letter_frequencies):
    key = ''
    for i in range(key_length):
        shift_offset = 0
        best_shift_offset = 0
        best_mutual_ic = 0.0
        while shift_offset < 26:
            mutual_ic = mutual_index_of_coincidence(shift(shift_offset, encrypted_text[i::key_length]),
                                                    english_letter_frequencies)
            if abs(0.065 - mutual_ic) < abs(0.065 - best_mutual_ic):
                best_mutual_ic = mutual_ic
                best_shift_offset = shift_offset
            shift_offset += 1
        letter = chr((26 - best_shift_offset) % 26 + ord('A'))
        key += letter
    return key


def actual_key(found_key):
    key = ''
    divisors = []
    for i in range(2, int((len(found_key) / 2) + 1)):
        if len(found_key) % i == 0:
            divisors.append(i)
    divisors.append(len(found_key))
    for divisor in divisors:
        if (found_key[0:divisor] * int(len(found_key) / divisor)) == found_key:
            key = found_key[0:divisor]
            break

    return key


def decrypt_text(encrypted_text, key, output_file, number_has_letter, letter_has_number):
    o_file = open(output_file, "w")
    decrypted_text = ""
    for i in range(len(encrypted_text)):
        decrypted_text += number_has_letter[(letter_has_number[encrypted_text[i]]
                                             - letter_has_number[key[i % len(key)]]) % 26]
    o_file.write(decrypted_text)
    o_file.close()
    return decrypted_text


def main():
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    plain_text = ""
    plain_text = read_and_filter("input_text.txt", plain_text)

    # key = generate_key(alphabet)
    key = "ABABBABAABABA"
    # creating dictionaries, letters have assigned a number and numbers have assigned a letter
    letter_has_number = {}
    number_has_letter = {}

    for i in range(len(alphabet)):
        letter_has_number[alphabet[i]] = i
        number_has_letter[i] = alphabet[i]

    encrypted_text = ""
    encrypted_text = encrypt_text(plain_text, encrypted_text, key, "encrypted_text.txt", number_has_letter,
                                  letter_has_number)
    print(f"Key value is: {key}")
    print(f"Plain Text: {plain_text}")
    found_key_length = get_key_length(encrypted_text)
    print(f"Best key length: {found_key_length}")

    # http://cs.wellesley.edu/~fturbak/codman/letterfreq.html?fbclid=IwAR2jBtEFQZe1jH9mZcQpGXP8TSrOfEp5cohas4C2im7C6BA2S6EE5DLUBjs
    english_letter_frequencies = {
        'A': 0.08167,
        'B': 0.01492,
        'C': 0.02782,
        'D': 0.04253,
        'E': 0.12702,
        'F': 0.02228,
        'G': 0.02015,
        'H': 0.06094,
        'I': 0.06966,
        'J': 0.00153,
        'K': 0.00772,
        'L': 0.04025,
        'M': 0.02406,
        'N': 0.06749,
        'O': 0.07507,
        'P': 0.01929,
        'Q': 0.00095,
        'R': 0.05987,
        'S': 0.06327,
        'T': 0.09056,
        'U': 0.02758,
        'V': 0.00978,
        'W': 0.02360,
        'X': 0.00150,
        'Y': 0.01975,
        'Z': 0.00074
    }
    found_key = get_key(encrypted_text, found_key_length, english_letter_frequencies)
    print(f"Found key: {found_key}")
    the_key = actual_key(found_key)
    print(f"Actual key: {the_key}")

    decrypted_text = decrypt_text(encrypted_text, the_key, "decrypted_text.txt", number_has_letter, letter_has_number)
    if plain_text == decrypted_text:
        print("Successfully decrypted!")
        print(f"Decrypted text: {decrypted_text}")


if __name__ == '__main__':
    main()
