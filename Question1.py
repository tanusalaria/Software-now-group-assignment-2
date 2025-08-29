# Encryption / Decryption Program
# ---------------------------------
rawText=""
def encrypt_char(ch, shift1, shift2):
    """Encrypt a single character based on rules"""
    if ch.islower():
        if 'a' <= ch <= 'm':
            # shift forward by shift1 * shift2
            pos=ord(ch)
            newPos=pos+(shift1*shift2)
            newChar=chr(newPos)
            return newChar
        else:
            # shift backward by shift1 + shift2
            pos=ord(ch)
            newPos= pos-(shift1+shift2)
            newChar=chr(newPos)
            return newChar
    elif ch.isupper():
        if 'A' <= ch <= 'M':
            # shift backward by shift1
            pos=ord(ch)
            newPos=pos-shift1
            newChar=chr(newPos)
            return newChar
        else:
            # shift forward by shift2²
            pos=ord(ch)
            newPos=pos+(shift2**2)
            newChar=chr(newPos)
            return newChar
    else:
        # Non-alphabet characters unchanged
        return ch
def decrypt_char(ch,rawCh, shift1, shift2):
    """Decrypt a single character (reverse rules)"""
    if rawCh.islower():
        if 'a' <= rawCh <= 'm':
            pos=ord(ch)
            newPos=pos-(shift1*shift2)
            newChar=chr(newPos)
            return newChar
            
        else:
            pos=ord(ch)
            newPos= pos+(shift1+shift2)
            newChar=chr(newPos)
            return newChar
    elif rawCh.isupper():
        if 'A' <= rawCh <= 'M':
            pos=ord(ch)
            newPos=pos+shift1
            newChar=chr(newPos)
            return newChar
        else:
            pos=ord(ch)
            newPos=pos-(shift2**2)
            newChar=chr(newPos)
            return newChar
    else:
        return ch



def encrypt_file(input_file, output_file, shift1, shift2):
    with open(input_file, "r", encoding="utf-8") as f:
        global rawText
        rawText= f.read()
    encrypted = "".join(encrypt_char(ch, shift1, shift2) for ch in rawText)
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        f.write(encrypted)


def decrypt_file(input_file, output_file, shift1, shift2):
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()
    decrypted = "".join(decrypt_char(text[ch],rawText[ch], shift1, shift2) for ch in range(len(text)))
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        f.write(decrypted)


def verify(original_file, decrypted_file):
    with open(original_file, "r", encoding="utf-8") as f1, open(decrypted_file, "r", encoding="utf-8") as f2:
        original = f1.read()
        decrypted = f2.read()

    if original == decrypted:
        print("✅ Decryption successful! Files match.")
    else:
        print("❌ Decryption failed! Files do not match.")
        # Debugging: show first mismatch
        for i, (o, d) in enumerate(zip(original, decrypted)):
            if o != d:
                print(f"Mismatch at position {i}: original='{o}' decrypted='{d}'")
                break
        if len(original) != len(decrypted):
            print(f"File lengths differ: original={len(original)}, decrypted={len(decrypted)}")


# ------------------ MAIN ------------------
if __name__ == "__main__":
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    # Step 1: Encrypt
    encrypt_file("raw_text.txt", "encrypted_text.txt", shift1, shift2)

    # Step 2: Decrypt
    decrypt_file("encrypted_text.txt", "decrypted_text.txt", shift1, shift2)

    # Step 3: Verify
    verify("raw_text.txt", "decrypted_text.txt")


