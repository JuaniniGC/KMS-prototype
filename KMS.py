# app_tkinter_des.py

import tkinter as tk
from tkinter import ttk, messagebox
from umbral import generar_partes, reconstruir_secreto
from envoltura import encrypt_with_DEK, decrypt_with_DEK, encrypt_DEK_with_KEK, decrypt_DEK_with_KEK
import random
import binascii
import pyperclip

# Variables globales para almacenar datos del umbral
partes_guardadas = []
clave_guardada = None
umbral_guardado = None
secreto_guardado = None

# Variables globales para almacenar datos de envoltura
encrypted_DEK_guardado = None
encrypted_text_guardado = None

# Función para copiar el texto al portapapeles
def copiar_al_portapapeles(texto):
    pyperclip.copy(texto)
    messagebox.showinfo("Copiado", "Texto copiado al portapapeles.")

# Función para encriptar por Umbral
def encriptar():
    global partes_guardadas, clave_guardada, umbral_guardado, secreto_guardado
    try:
        secreto = int(secreto_entrada.get())  # Obtener el secreto desde la entrada
        umbral = int(umbral_entrada.get())  # Umbral para la reconstrucción del secreto 
        num_partes = int(partes_generadas_entrada.get())  # Número total de partes a generar
        if umbral > num_partes:
            resultado_encriptacion.config(text="El umbral debe ser menor o igual al número total de partes.")
            return
        partes, coeficientes = generar_partes(secreto, num_partes, umbral)
        
        # Guardar las partes y la clave para usarlas en otras pestañas
        partes_guardadas = random.sample(partes, umbral)
        clave_guardada = coeficientes  # Guardar la clave generada para usarla en otro lado
        secreto_guardado = secreto  # Guardar el secreto
        
        # Mostrar las partes generadas en la interfaz gráfica
        partes_mostradas = "\n".join([f"Parte {x}: {y}" for x, y in partes])
        resultado_encriptacion.config(text=f"Partes generadas:\n{partes_mostradas}")
        
    except ValueError:
        resultado_encriptacion.config(text="Por favor, ingresa valores válidos.")

# Función para desencriptar el secreto
def desencriptar():
    try:
        if partes_guardadas:
            secreto_reconstruido = reconstruir_secreto(partes_guardadas)
            resultado_desencriptacion.config(text=f"Secreto reconstruido: {secreto_reconstruido}")
        else:
            resultado_desencriptacion.config(text="No se ha realizado la encriptación aún.")
    except Exception as e:
        resultado_desencriptacion.config(text=f"Error en la desencriptación: {e}")

# Función para encriptar con envoltura (Encriptar Claves)
def encriptar_envoltura():
    global encrypted_DEK_guardado, encrypted_text_guardado
    try:
        texto_claro = texto_claro_entrada.get()
        DEK_hex = DEK_entrada.get()
        KEK_hex = KEK_entrada.get()
        
        if not texto_claro or not DEK_hex or not KEK_hex:
            resultado_encriptacion_envoltura.config(text="Por favor, completa todos los campos.")
            return
        
        # Convertir DEK y KEK de hex a bytes
        try:
            DEK = binascii.unhexlify(DEK_hex)
            KEK = binascii.unhexlify(KEK_hex)
        except binascii.Error:
            resultado_encriptacion_envoltura.config(text="DEK y KEK deben estar en formato hexadecimal válido.")
            return
        
        if len(DEK) != 8:
            resultado_encriptacion_envoltura.config(text="DEK debe tener exactamente 8 bytes (16 caracteres hex).")
            return
        
        if len(KEK) != 8:
            resultado_encriptacion_envoltura.config(text="KEK debe tener exactamente 8 bytes (16 caracteres hex).")
            return
        
        # Encriptar el texto claro con DEK
        encrypted_text = encrypt_with_DEK(texto_claro, DEK)
        
        # Encriptar DEK con KEK
        encrypted_DEK = encrypt_DEK_with_KEK(DEK, KEK)
        
        # Almacenar los datos en variables globales
        encrypted_text_guardado = encrypted_text
        encrypted_DEK_guardado = encrypted_DEK
        
        # Mostrar los resultados en hexadecimal para facilitar la lectura
        encrypted_text_hex = binascii.hexlify(encrypted_text).decode()
        encrypted_DEK_hex = binascii.hexlify(encrypted_DEK).decode()
        
        resultado_encriptacion_envoltura.config(text=f"Texto Encriptado (hex):\n{encrypted_text_hex}\n\nDEK Encriptado (hex):\n{encrypted_DEK_hex}")
        
    except Exception as e:
        resultado_encriptacion_envoltura.config(text=f"Error en la encriptación: {e}")

# Función para desencriptar con envoltura (Desencriptar Claves)
def desencriptar_envoltura():
    try:
        encrypted_text_hex = encrypted_text_entrada.get()
        encrypted_DEK_hex = encrypted_DEK_entrada.get()
        KEK_hex = KEK_desencriptar_entrada.get()
        
        if not encrypted_text_hex or not encrypted_DEK_hex or not KEK_hex:
            resultado_desencriptacion_envoltura.config(text="Por favor, completa todos los campos.")
            return
        
        # Convertir los datos de hex a bytes
        try:
            encrypted_text = binascii.unhexlify(encrypted_text_hex)
            encrypted_DEK = binascii.unhexlify(encrypted_DEK_hex)
            KEK = binascii.unhexlify(KEK_hex)
        except binascii.Error:
            resultado_desencriptacion_envoltura.config(text="Los datos deben estar en formato hexadecimal válido.")
            return
        
        if len(KEK) != 8:
            resultado_desencriptacion_envoltura.config(text="KEK debe tener exactamente 8 bytes (16 caracteres hex).")
            return
        
        # Desencriptar DEK con KEK
        DEK = decrypt_DEK_with_KEK(encrypted_DEK, KEK)
        
        # Desencriptar el texto con DEK
        texto_desencriptado = decrypt_with_DEK(encrypted_text, DEK)
        
        resultado_desencriptacion_envoltura.config(text=f"Texto Desencriptado:\n{texto_desencriptado}")
        
    except Exception as e:
        resultado_desencriptacion_envoltura.config(text=f"Error en la desencriptación: {e}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("KMS-prototype con DES")
ventana.geometry("800x600")  # Ancho de 800 px y Alto de 600 px

# Crear el widget Notebook (pestañas)
notebook = ttk.Notebook(ventana)
notebook.pack(fill='both', expand=True)

# Crear las pestañas
pestana_encriptacion = tk.Frame(notebook)
pestana_desencriptacion = tk.Frame(notebook)
pestana_envoltura_encriptacion = tk.Frame(notebook)
pestana_envoltura_desencriptacion = tk.Frame(notebook) 

# Agregar las pestañas al notebook
notebook.add(pestana_encriptacion, text="Encriptar por Umbral")
notebook.add(pestana_desencriptacion, text="Desencriptación del Umbral")
notebook.add(pestana_envoltura_encriptacion, text="Envoltura de Encriptación")
notebook.add(pestana_envoltura_desencriptacion, text="Envoltura de Desencriptación")

# **Pestaña de Encriptación por Umbral**
# Etiqueta para la entrada del texto
etiqueta_secreto = tk.Label(pestana_encriptacion, text="Introduce el secreto (número):")
etiqueta_secreto.pack(pady=5)
secreto_entrada = tk.Entry(pestana_encriptacion, width=30)
secreto_entrada.pack(pady=10)

# Etiqueta para la entrada de las partes generadas
etiqueta_partes_generadas = tk.Label(pestana_encriptacion, text="Introduce el número total de partes a generar:")
etiqueta_partes_generadas.pack(pady=5)
partes_generadas_entrada = tk.Entry(pestana_encriptacion, width=30)
partes_generadas_entrada.pack(pady=10)

# Etiqueta para la entrada del umbral
etiqueta_umbral = tk.Label(pestana_encriptacion, text="Introduce el umbral (debe ser menor o igual al total de partes generadas):")
etiqueta_umbral.pack(pady=5)
umbral_entrada = tk.Entry(pestana_encriptacion, width=30)
umbral_entrada.pack(pady=10)

# Botón para encriptar
boton_encriptar = tk.Button(pestana_encriptacion, text="Separar la clave privada", command=encriptar)
boton_encriptar.pack(pady=10)

# Etiqueta para mostrar el resultado de la encriptación
resultado_encriptacion = tk.Label(pestana_encriptacion, text="Resultado de la separación de la clave privada aparecerá aquí.", justify=tk.LEFT)
resultado_encriptacion.pack(pady=10)

# **Pestaña de Desencriptación del Umbral**
# Botón para desencriptar
boton_desencriptar = tk.Button(pestana_desencriptacion, text="Desencriptar", command=desencriptar)
boton_desencriptar.pack(pady=10)

# Etiqueta para mostrar el resultado de la desencriptación
resultado_desencriptacion = tk.Label(pestana_desencriptacion, text="Resultado de la desencriptación aparecerá aquí.", justify=tk.LEFT)
resultado_desencriptacion.pack(pady=10)

# **Pestaña de Envoltura de Encriptación**
# Etiqueta para el texto en claro
etiqueta_texto_claro_envoltura = tk.Label(pestana_envoltura_encriptacion, text="Introduce el texto en claro:")
etiqueta_texto_claro_envoltura.pack(pady=5)
texto_claro_entrada = tk.Entry(pestana_envoltura_encriptacion, width=50)
texto_claro_entrada.pack(pady=10)

# Etiqueta para la DEK
etiqueta_DEK = tk.Label(pestana_envoltura_encriptacion, text="Introduce la DEK (hexadecimal, 8 bytes = 16 hex):")
etiqueta_DEK.pack(pady=5)
DEK_entrada = tk.Entry(pestana_envoltura_encriptacion, width=50)
DEK_entrada.pack(pady=10)

# Etiqueta para la KEK  
etiqueta_KEK = tk.Label(pestana_envoltura_encriptacion, text="Introduce la KEK (hexadecimal, 8 bytes = 16 hex):")
etiqueta_KEK.pack(pady=5)
KEK_entrada = tk.Entry(pestana_envoltura_encriptacion, width=50)
KEK_entrada.pack(pady=10)

# Botón para encriptar
boton_encriptar_envoltura = tk.Button(pestana_envoltura_encriptacion, text="Encriptar", command=encriptar_envoltura)
boton_encriptar_envoltura.pack(pady=10)

# Etiqueta para mostrar el resultado de la encriptación
resultado_encriptacion_envoltura = tk.Label(pestana_envoltura_encriptacion, text="Resultado de la encriptación aparecerá aquí.", justify=tk.LEFT)
resultado_encriptacion_envoltura.pack(pady=10)

# Botón para copiar el texto cifrado al portapapeles
boton_copiar_texto_encriptado = tk.Button(pestana_envoltura_encriptacion, text="Copiar Texto Encriptado", command=lambda: copiar_al_portapapeles(binascii.hexlify(encrypted_text_guardado).decode() if encrypted_text_guardado else ""))
boton_copiar_texto_encriptado.pack(pady=10)

# Botón para copiar la DEK cifrada al portapapeles
boton_copiar_DEK_encriptado = tk.Button(pestana_envoltura_encriptacion, text="Copiar DEK Encriptada", command=lambda: copiar_al_portapapeles(binascii.hexlify(encrypted_DEK_guardado).decode() if encrypted_DEK_guardado else ""))
boton_copiar_DEK_encriptado.pack(pady=10)


# **Pestaña de Envoltura de Desencriptación**
# Etiqueta para la entrada del texto encriptado
etiqueta_encrypted_text = tk.Label(pestana_envoltura_desencriptacion, text="Introduce el texto encriptado (hexadecimal):")
etiqueta_encrypted_text.pack(pady=5)
encrypted_text_entrada = tk.Entry(pestana_envoltura_desencriptacion, width=50)
encrypted_text_entrada.pack(pady=10)

# Etiqueta para la entrada de DEK encriptada
etiqueta_encrypted_DEK = tk.Label(pestana_envoltura_desencriptacion, text="Introduce la DEK encriptada (hexadecimal, 8 bytes = 16 hex):")
etiqueta_encrypted_DEK.pack(pady=5)
encrypted_DEK_entrada = tk.Entry(pestana_envoltura_desencriptacion, width=50)
encrypted_DEK_entrada.pack(pady=10)

# Etiqueta para la KEK
etiqueta_KEK_desencriptar = tk.Label(pestana_envoltura_desencriptacion, text="Introduce la KEK (hexadecimal, 8 bytes = 16 hex):")
etiqueta_KEK_desencriptar.pack(pady=5)
KEK_desencriptar_entrada = tk.Entry(pestana_envoltura_desencriptacion, width=50)
KEK_desencriptar_entrada.pack(pady=10)

# Botón para desencriptar
boton_desencriptar_envoltura = tk.Button(pestana_envoltura_desencriptacion, text="Desencriptar", command=desencriptar_envoltura)
boton_desencriptar_envoltura.pack(pady=10)

# Etiqueta para mostrar el resultado de la desencriptación
resultado_desencriptacion_envoltura = tk.Label(pestana_envoltura_desencriptacion, text="Resultado de la desencriptación aparecerá aquí.", justify=tk.LEFT)
resultado_desencriptacion_envoltura.pack(pady=10)

if __name__ == "__main__":
    ventana.mainloop()
