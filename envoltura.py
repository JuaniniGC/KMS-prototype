from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
from cryptography.hazmat.primitives import padding

# Función para generar una clave aleatoria de longitud 'size' en bytes
def generate_key(size):
    return os.urandom(size)

# Cifrado simétrico del mensaje usando DEK (Data Encryption Key)
def encrypt_with_DEK(plain_text, DEK):
    # Usamos el modo de cifrado AES en CBC
    iv = os.urandom(16)  # Vector de inicialización aleatorio
    cipher = Cipher(algorithms.AES(DEK), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Aplicamos padding usando PKCS7
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plain_text.encode()) + padder.finalize()
    
    cipher_text = encryptor.update(padded_data) + encryptor.finalize()
    return iv + cipher_text  # Devolvemos IV + texto cifrado

# Cifrado de DEK con KEK (Key Encryption Key)
def encrypt_DEK_with_KEK(DEK, KEK):
    # Usamos el modo GCM de AES para cifrar el DEK
    iv = os.urandom(12)  # IV de 12 bytes para GCM
    cipher = Cipher(algorithms.AES(KEK), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Ciframos el DEK
    encrypted_DEK = encryptor.update(DEK) + encryptor.finalize()
    
    # Retornamos el IV, el texto cifrado y el tag de autenticación
    return iv + encryptor.tag + encrypted_DEK

# Descifrado de DEK con KEK
def decrypt_DEK_with_KEK(encrypted_DEK, KEK):
    iv = encrypted_DEK[:12]  # Extraemos el IV
    tag = encrypted_DEK[12:28]  # Extraemos el tag (16 bytes)
    cipher_text = encrypted_DEK[28:]  # Extraemos el texto cifrado

    cipher = Cipher(algorithms.AES(KEK), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    
    DEK = decryptor.update(cipher_text) + decryptor.finalize()
    return DEK

# Descifrado del mensaje con DEK
def decrypt_with_DEK(cipher_text, DEK):
    iv = cipher_text[:16]  # Extraemos el IV
    cipher_text = cipher_text[16:]  # Extraemos el texto cifrado
    
    cipher = Cipher(algorithms.AES(DEK), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    padded_plain_text = decryptor.update(cipher_text) + decryptor.finalize()
    
    # Eliminamos el padding usando PKCS7
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plain_text = unpadder.update(padded_plain_text) + unpadder.finalize()
    
    return plain_text.decode()

# Función principal
def main():
    # Generar claves DEK (32 bytes) y KEK (32 bytes)
    DEK = generate_key(32)  # 256 bits
    KEK = generate_key(32)  # 256 bits

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

if __name__ == "__main__":
    main()
