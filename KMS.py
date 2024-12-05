import tkinter as tk
from tkinter import ttk
from umbral import generar_partes, reconstruir_secreto
import random

# Variables globales para almacenar datos
partes_guardadas = []
clave_guardada = None
umbral_guardado = None
secreto_guardado = None

# Función para encriptar el texto
def encriptar():
    global partes_guardadas, clave_guardada, umbral_guardado, secreto_guardado
    try:
        secreto = int(secreto_entrada.get())  # Obtener el secreto desde la entrada
        umbral = int(umbral_entrada.get())  # Umbral para la reconstrucción del secreto 
        num_partes = int(partes_generadas_entrada.get())  # Número total de partes a generar
        partes, coeficientes = generar_partes(secreto, num_partes, umbral)
        
        # Guardar las partes y la clave para usarlas en otras pestañas
        partes_guardadas = random.sample(partes, umbral)
        clave_guardada = coeficientes  # Guardar la clave generada para usarla en otro lado
        secreto_guardado = secreto  # Guardar el secreto
        
        # Mostrar las partes generadas en la interfaz gráfica
        partes_mostradas = "\n".join([f"Parte {x}: {y}" for x, y in partes])
        resultado_encriptacion.config(text=f"Partes generadas:\n{partes_mostradas}")
        
    except ValueError:
        resultado_encriptacion.config(text="Por favor, ingresa un secreto válido.")

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

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("KMS-prototype")
ventana.geometry("600x400")  # Ancho de 600 px y Alto de 400 px

# Crear el widget Notebook (pestañas)
notebook = ttk.Notebook(ventana)
notebook.pack(fill='both', expand=True)

# Crear las pestañas
pestana_encriptacion = tk.Frame(notebook)
pestana_desencriptacion = tk.Frame(notebook)

# Agregar las pestañas al notebook
notebook.add(pestana_encriptacion, text="Encriptar por Umbral")
notebook.add(pestana_desencriptacion, text="Desencriptación")

# **Pestaña de Encriptación**
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
etiqueta_umbral = tk.Label(pestana_encriptacion, text="Introduce el umbral (debe ser menor al total de partes generadas):")
etiqueta_umbral.pack(pady=5)
umbral_entrada = tk.Entry(pestana_encriptacion, width=30)
umbral_entrada.pack(pady=10)

# Botón para encriptar
boton_encriptar = tk.Button(pestana_encriptacion, text="Separar la clave privada", command=encriptar)
boton_encriptar.pack(pady=10)

# Etiqueta para mostrar el resultado de la encriptación
resultado_encriptacion = tk.Label(pestana_encriptacion, text="Resultado de la encriptación aparecerá aquí.")
resultado_encriptacion.pack(pady=10)

# **Pestaña de Desencriptación**
# Botón para desencriptar
boton_desencriptar = tk.Button(pestana_desencriptacion, text="Desencriptar", command=desencriptar)
boton_desencriptar.pack(pady=10)

# Etiqueta para mostrar el resultado de la desencriptación
resultado_desencriptacion = tk.Label(pestana_desencriptacion, text="Resultado de la desencriptación aparecerá aquí.")
resultado_desencriptacion.pack(pady=10)

# Ejecutar la aplicación
ventana.mainloop()
