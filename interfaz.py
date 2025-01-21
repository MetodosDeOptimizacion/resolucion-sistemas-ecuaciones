import streamlit as st
from sympy import symbols, Eq, solve, Matrix

# Función para resolver por sustitución
def metodo_sustitucion(ecuaciones, variables):
    soluciones = solve(ecuaciones, variables)
    return soluciones

# Función para resolver por Gauss-Jordan
def metodo_gauss_jordan(coeficientes, independientes):
    matriz = Matrix([fila + [ind] for fila, ind in zip(coeficientes, independientes)])
    matriz_reducida = matriz.rref()
    soluciones = [fila[-1] for fila in matriz_reducida[0].tolist()]
    return soluciones

# Función para resolver por regla de Cramer
def metodo_cramer(coeficientes, independientes):
    matriz_coeficientes = Matrix(coeficientes)
    matriz_independientes = Matrix(independientes)
    det_coeficientes = matriz_coeficientes.det()

    if det_coeficientes == 0:
        return "El sistema no tiene solución única."

    soluciones = []
    for i in range(len(coeficientes)):
        matriz_sustituida = matriz_coeficientes.copy()
        matriz_sustituida[:, i] = matriz_independientes
        soluciones.append(matriz_sustituida.det() / det_coeficientes)

    return soluciones

# Interfaz de Streamlit
st.title("Resolución de Sistemas de Ecuaciones")
st.write("Esta aplicación resuelve sistemas de ecuaciones utilizando los métodos de Sustitución, Gauss-Jordan y Regla de Cramer.")

# Entrada: Número de ecuaciones
num_ecuaciones = st.number_input("Número de ecuaciones:", min_value=2, step=1)

if num_ecuaciones:
    # Entrada: Coeficientes y términos independientes
    st.write("Ingrese los coeficientes y términos independientes:")

    coeficientes = []
    terminos_independientes = []

    for i in range(num_ecuaciones):
        st.write(f"Ecuación {i + 1}:")
        fila = [st.number_input(f"Coeficiente de x{j + 1} (Ecuación {i + 1}):", key=f"coef_{i}_{j}") for j in range(num_ecuaciones)]
        coeficientes.append(fila)
        terminos_independientes.append(st.number_input(f"Término independiente (Ecuación {i + 1}):", key=f"indep_{i}"))

    # Selección del método
    metodo = st.selectbox("Seleccione el método para resolver:", ["Sustitución", "Gauss-Jordan", "Regla de Cramer"])

    if st.button("Resolver"):
        variables = symbols(' '.join([f'x{i + 1}' for i in range(num_ecuaciones)]))

        if metodo == "Sustitución":
            ecuaciones = []
            for i in range(num_ecuaciones):
                ecuacion = Eq(sum(coeficientes[i][j] * variables[j] for j in range(num_ecuaciones)), terminos_independientes[i])
                ecuaciones.append(ecuacion)
            soluciones = metodo_sustitucion(ecuaciones, variables)

        elif metodo == "Gauss-Jordan":
            soluciones = metodo_gauss_jordan(coeficientes, terminos_independientes)

        elif metodo == "Regla de Cramer":
            soluciones = metodo_cramer(coeficientes, terminos_independientes)

        # Mostrar las soluciones
        st.write("### Soluciones:")
        if isinstance(soluciones, str):
            st.write(soluciones)
        else:
            for i, solucion in enumerate(soluciones):
                st.write(f"x{i + 1} = {solucion}")
