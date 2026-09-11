# encryption

def encrypt_char(ch, shift1, shift2):
    """
    Transform a single character according to the encryption rules.
    Returns the new (encrypted) character.
    """
    if ch.islower():
        pos = ord(ch) - ord('a')
        if ch <= 'n':                      # a-n: 14 letters, stays within a-n
            new_pos = (pos + shift1 * shift2) % 14
        else:                              # o-z: 12 letters, stays within o-z
            new_pos = (pos - 14 - (shift1 + shift2)) % 12 + 14
        return chr(new_pos + ord('a'))

    elif ch.isupper():
        pos = ord(ch) - ord('A')
        if ch <= 'M':                      # A-M: 13 letters, stays within A-M
            new_pos = (pos - shift1) % 13
        else:                              # N-Z: 13 letters, stays within N-Z
            new_pos = (pos - 13 + shift2 ** 2) % 13 + 13
        return chr(new_pos + ord('A'))

    elif ch.isdigit():
        d = int(ch)
        new_d = (d + shift1 - shift2) % 10
        return str(new_d)

    else:
        return ch


def encrypt_file(shift1: int, shift2: int, input_path: str, output_path: str) -> None:
    """Reads input_path, encrypts every character, writes the result to output_path."""
    with open(input_path, 'r', encoding='utf-8') as f:
        original_text = f.read()

    encrypted_text = ''.join(encrypt_char(ch, shift1, shift2) for ch in original_text)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(encrypted_text)


# Decryption

def decrypt_char(ch, shift1, shift2):
    """
    Reverse the transformation for a single character.
    Each alphabet half shifts modulo its own size (14/12 lowercase,
    13/13 uppercase), so it never crosses into the other half - this
    keeps the mapping one-to-one and always reversible.
    """
    if ch.islower():
        pos = ord(ch) - ord('a')
        if ch <= 'n':
            new_pos = (pos - shift1 * shift2) % 14
        else:
            new_pos = (pos - 14 + (shift1 + shift2)) % 12 + 14
        return chr(new_pos + ord('a'))

    elif ch.isupper():
        pos = ord(ch) - ord('A')
        if ch <= 'M':
            new_pos = (pos + shift1) % 13
        else:
            new_pos = (pos - 13 - shift2 ** 2) % 13 + 13
        return chr(new_pos + ord('A'))

    elif ch.isdigit():
        d = int(ch)
        new_d = (d - shift1 + shift2) % 10
        return str(new_d)

    else:
        return ch


def decrypt_file(shift1: int, shift2: int, input_path: str, output_path: str) -> None:
    """Reads input_path (the encrypted file), decrypts it, writes the result to output_path."""
    with open(input_path, 'r', encoding='utf-8') as f:
        encrypted_text = f.read()

    decrypted_text = ''.join(decrypt_char(ch, shift1, shift2) for ch in encrypted_text)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(decrypted_text)


def verify_files(original_path: str, decrypted_path: str) -> bool:
    """Compares the two files and prints + returns whether they match exactly."""
    with open(original_path, 'r', encoding='utf-8') as f:
        original_text = f.read()

    with open(decrypted_path, 'r', encoding='utf-8') as f:
        decrypted_text = f.read()

    if original_text == decrypted_text:
        print("Verification: SUCCESS - decrypted file matches the original.")
        return True
    else:
        print("Verification: FAILED - decrypted file does NOT match the original.")
        return False


# main function
def main():
    shift1 = int(input("Enter shift1 (non-negative integer): "))
    shift2 = int(input("Enter shift2 (non-negative integer): "))

    encrypt_file(shift1, shift2, "raw_text.txt", "encrypted_text.txt")
    print("Encrypted raw_text.txt -> encrypted_text.txt")

    decrypt_file(shift1, shift2, "encrypted_text.txt", "decrypted_text.txt")
    print("Decrypted encrypted_text.txt -> decrypted_text.txt")

    verify_files("raw_text.txt", "decrypted_text.txt")

if __name__ == "__main__":
    main()