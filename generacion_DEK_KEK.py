import os

# Función para generar una clave aleatoria de 32 bytes
def generate_key():
    return os.urandom(8)  # Genera 32 bytes de clave

# Guardar las combinaciones en un archivo de texto
def generate_keys_file(filename):
    with open(filename, 'w') as f:
        for _ in range(20):
            DEK = generate_key()
            KEK = generate_key()
            f.write(f"DEK: {DEK.hex()}\nKEK: {KEK.hex()}\n\n")

# Generar el archivo con las combinaciones
generate_keys_file("dek_kek_combinations.txt")
