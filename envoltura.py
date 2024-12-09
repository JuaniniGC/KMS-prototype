from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# Función para generar una clave aleatoria de 8 bytes para DES
def generate_key():
    return get_random_bytes(8)  # 8 bytes de clave

# Cifrado simétrico del mensaje usando DES
def encrypt_with_DEK(plain_text, DEK):
    cipher = DES.new(DEK, DES.MODE_CBC)  # Cifra en modo CBC
    iv = cipher.iv  # Vector de inicialización (se utiliza automáticamente en DES)
    
    # Aplicamos padding (PKCS7) al mensaje
    padded_data = pad(plain_text.encode(), DES.block_size)
    
    cipher_text = cipher.encrypt(padded_data)
    return iv + cipher_text  # Devolvemos IV + texto cifrado

# Cifrado de DEK con KEK (Key Encryption Key)
def encrypt_DEK_with_KEK(DEK, KEK):
    cipher = DES.new(KEK, DES.MODE_ECB)  # Cifra en modo ECB
    encrypted_DEK = cipher.encrypt(pad(DEK, DES.block_size))  # Pad para que tenga longitud correcta
    return encrypted_DEK

# Descifrado de DEK con KEK
def decrypt_DEK_with_KEK(encrypted_DEK, KEK):
    cipher = DES.new(KEK, DES.MODE_ECB)
    decrypted_DEK = unpad(cipher.decrypt(encrypted_DEK), DES.block_size)
    return decrypted_DEK

# Descifrado del mensaje con DEK
def decrypt_with_DEK(cipher_text, DEK):
    iv = cipher_text[:8]  # Extraemos el IV
    cipher_text = cipher_text[8:]  # Extraemos el texto cifrado
    
    cipher = DES.new(DEK, DES.MODE_CBC, iv)  # Descifra en modo CBC
    
    padded_plain_text = unpad(cipher.decrypt(cipher_text), DES.block_size)
    return padded_plain_text.decode()

# Función principal
def main():
    # Generar claves DEK (8 bytes) y KEK (8 bytes)
    DEK = generate_key()  # 8 bytes para DES
    KEK = generate_key()  # 8 bytes para DES

    # Mensaje a cifrar
    plain_text = "Este es un mensaje secreto"

    # Encriptar el mensaje con DEK
    encrypted_message = encrypt_with_DEK(plain_text, DEK)

    # Encriptar DEK con KEK
    encrypted_DEK = encrypt_DEK_with_KEK(DEK, KEK)

    # Para descifrar:
    # Desencriptamos DEK usando KEK
    decrypted_DEK = decrypt_DEK_with_KEK(encrypted_DEK, KEK)

    # Desencriptamos el mensaje usando el DEK
    decrypted_message = decrypt_with_DEK(encrypted_message, decrypted_DEK)
    
    print(f"Mensaje original: {plain_text}")
    print(f"Mensaje descifrado: {decrypted_message}")

