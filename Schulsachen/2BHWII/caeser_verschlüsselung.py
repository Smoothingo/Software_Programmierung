def caesar_encrypt(text, key):
    result = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) + key
            if char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
                elif shifted < ord('A'):
                    shifted += 26
            else:
                if shifted > ord('z'):
                    shifted -= 26
                elif shifted < ord('a'):
                    shifted += 26
            result += chr(shifted)
        else:
            result += char
    return result

def caesar_decrypt(text, key):
    return caesar_encrypt(text, -key)


action = input("Möchten Sie eine Nachricht verschlüsseln oder entschlüsseln? (v/e): ")

if action.lower() == 'v':
    message = input("Geben Sie eine Nachricht ein: ")
    key = int(input("Geben Sie eine Verschiebungszahl ein: "))

    encrypted = caesar_encrypt(message, key)
    print("Verschlüsselte Nachricht:", encrypted)

elif action.lower() == 'e':
    message = input("Geben Sie eine verschlüsselte Nachricht ein: ")
    key = int(input("Geben Sie eine Verschiebungszahl ein: "))

    decrypted = caesar_decrypt(message, key)
    print("Entschlüsselte Nachricht:", decrypted)

else:
    print("Ungültige Aktion. Bitte 'v' für Verschlüsselung oder 'e' für Entschlüsselung eingeben.")
