import tkinter as tk
from umbral import generar_partes, reconstruir_secreto
import random

# Función para encriptar el texto
def encriptar():
    try:
        secreto = int(secreto_entrada.get())  # Obtener el secreto desde la entrada
        umbral = int(umbral_entrada.get())  # Umbral para la reconstrucción del secreto 
        num_partes = int(partes_generadas_entrada.get())  # Número total de partes a generar
        partes, coeficientes = generar_partes(secreto, num_partes, umbral)
        
        # Mostrar las partes generadas en la interfaz gráfica
        partes_mostradas = "\n".join([f"Parte {x}: {y}" for x, y in partes])
        resultado_encriptacion.config(text=f"Partes generadas:\n{partes_mostradas}")
        
        # Guardar partes para desencriptación
        global partes_guardadas
        partes_guardadas = random.sample(partes, umbral)
        
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

etiqueta_secreto = tk.Label(ventana, text="Introduce el secreto (número):")
etiqueta_secreto.pack(pady=5)
secreto_entrada = tk.Entry(ventana, width=30)
secreto_entrada.pack(pady=10)

etiqueta_partes_generadas = tk.Label(ventana, text="Introduce el numero total de partes a generar:")
etiqueta_partes_generadas.pack(pady=5)
partes_generadas_entrada = tk.Entry(ventana, width=30)
partes_generadas_entrada.pack(pady=10)

etiqueta_umbral = tk.Label(ventana, text="Introduce el umbral (debe ser menor al total de partes generadas):")
etiqueta_umbral.pack(pady=5)
umbral_entrada = tk.Entry(ventana, width=30)
umbral_entrada.pack(pady=10)


boton_ = tk.Button(ventana, text="Encriptar", command=encriptar)
boton_encriptar.pack(pady=10)

boton_desencriptar = tk.Button(ventana, text="Desencriptar", command=desencriptar)
boton_desencriptar.pack(pady=10)

# Etiqueta para mostrar el resultado de la encriptación
resultado_encriptacion = tk.Label(ventana, text="Resultado de la encriptación aparecerá aquí.")
resultado_encriptacion.pack(pady=10)

# Etiqueta para mostrar el resultado de la desencriptación
resultado_desencriptacion = tk.Label(ventana, text="Resultado de la desencriptación aparecerá aquí.")
resultado_desencriptacion.pack(pady=10)

# Variable global para almacenar las partes generadas
partes_guardadas = []

# Ejecutar la aplicación
ventana.mainloop()
