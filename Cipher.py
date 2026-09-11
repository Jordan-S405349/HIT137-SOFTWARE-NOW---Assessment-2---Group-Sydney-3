#encryption

def encrypt_char(ch, shift1, shift2):
    """
    Transform a single character according to the encryption rules.
    Returns the new (encrypted) character.
    """
    if ch.islower():
        pos = ord(ch) - ord('a')          # a=0, b=1, ... z=25
        if ch <= 'n':                     # first half: a-n
            new_pos = (pos + shift1 * shift2) % 26
        else:                             # second half: o-z
            new_pos = (pos - (shift1 + shift2)) % 26
        return chr(new_pos + ord('a'))

    elif ch.isupper():
        pos = ord(ch) - ord('A')          # A=0, B=1, ... Z=25
        if ch <= 'M':                     # first half: A-M
            new_pos = (pos - shift1) % 26
        else:                             # second half: N-Z
            new_pos = (pos + shift2 ** 2) % 26
        return chr(new_pos + ord('A'))

    elif ch.isdigit():
        d = int(ch)
        new_d = (d + shift1 - shift2) % 10
        return str(new_d)

    else:
        # spaces, tabs, newlines, punctuation, symbols: unchanged
        return ch


def encrypt_file(shift1: int, shift2: int, input_path: str, output_path: str) -> None:
    """Reads input_path, encrypts every character, writes the result to output_path."""
    with open(input_path, 'r', encoding='utf-8') as f:
        original_text = f.read()

    encrypted_text = ''
    for ch in original_text:
        encrypted_text += encrypt_char(ch, shift1, shift2)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(encrypted_text)


# main function 
def main():
    shift1 = int(input("Enter shift1 (non-negative integer): "))
    shift2 = int(input("Enter shift2 (non-negative integer): "))

    encrypt_file(shift1, shift2, "raw_text.txt", "encrypted_text.txt")
    print("Encrypted raw_text.txt -> encrypted_text.txt")

 


if __name__ == "__main__":
    main()