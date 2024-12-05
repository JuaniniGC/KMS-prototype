import random
from sympy import Symbol, expand

def generar_polinomio(secret, grado):
    """Genera un polinomio de grado especificado con el secreto como término constante."""
    coeficientes = [secret] + [random.randint(1, 100) for _ in range(grado)]
    return coeficientes

def evaluar_polinomio(coeficientes, x):
    """Evalúa un polinomio dado en un punto x."""
    resultado = 0
    for i, coef in enumerate(coeficientes):
        resultado += coef * (x ** i)
    return resultado

def generar_partes(secret, num_partes, umbral):
    """Genera las partes necesarias para reconstruir el secreto."""
    coeficientes = generar_polinomio(secret, umbral - 1)
    partes = [(x, evaluar_polinomio(coeficientes, x)) for x in range(1, num_partes + 1)]
    return partes, coeficientes

def reconstruir_secreto(partes):
    """Reconstruye el secreto utilizando interpolación de Lagrange."""
    x = Symbol('x')
    secreto = 0
    for i, (xi, yi) in enumerate(partes):
        li = 1
        for j, (xj, _) in enumerate(partes):
            if i != j:
                li *= (x - xj) / (xi - xj)
        secreto += expand(yi * li).subs(x, 0)  # Evaluar el polinomio en x=0 para obtener el término constante
    return int(secreto)

# Ejemplo de uso
secreto_original = 543  # El secreto a compartir
num_partes = 10          # Número de partes a generar
umbral = 6             # Número mínimo de partes necesarias para reconstruir el secreto

# Generar partes
partes, coeficientes = generar_partes(secreto_original, num_partes, umbral)
print("Partes generadas:", partes)
print("Coeficientes del polinomio:", coeficientes)

# Seleccionar 3 partes (umbral) para reconstruir el secreto
partes_seleccionadas = random.sample(partes, umbral)
print("Partes seleccionadas:", partes_seleccionadas)

# Reconstruir el secreto
secreto_reconstruido = reconstruir_secreto(partes_seleccionadas)
print("Secreto reconstruido:", secreto_reconstruido)
