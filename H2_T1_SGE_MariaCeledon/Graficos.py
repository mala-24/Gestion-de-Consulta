from tkinter import messagebox
import matplotlib.pyplot as plt
import pandas as pd

# Defino la función generar_grafico que se encargará de crear gráficos a partir de los datos en la tabla
def generar_grafico(tabla, fields, tipo):
    registros = []  # Inicializo una lista vacía para almacenar los registros
    
    # Recorro cada elemento (fila) de la tabla y extraigo los valores
    for item in tabla.get_children():
        registros.append(tabla.item(item)['values'])
    
    # Verifico si hay registros; si no, muestro un mensaje de advertencia
    if not registros:
        messagebox.showwarning("Advertencia", "No hay registros para graficar.")
        return # Salgo de la función si no hay datos

# Creo un DataFrame de pandas a partir de los registros y los campos especificados
    df = pd.DataFrame(registros, columns=fields)

    if tipo == "Barras":
        graficar_barras(df)
    elif tipo == "Pastel":
        graficar_pastel(df)
    elif tipo == "Líneas":
        graficar_lineas(df)
    else:
        # Si el tipo de gráfico no es reconocido, muestro un mensaje de error.
        messagebox.showerror("Error", "Tipo de gráfico no reconocido.")


# Defino la función graficar_barras para crear un gráfico de barras.
def graficar_barras(df):
    # Agrupo los datos por 'Edad' y calculo el consumo promedio de bebidas por semana.
    consumo_promedio = df.groupby('Edad')['Bebidas/Semana'].mean().reset_index()
    
    # Configuro el tamaño de la figura y creo el gráfico de barras.
    plt.figure(figsize=(10, 6))
    plt.bar(consumo_promedio['Edad'], consumo_promedio['Bebidas/Semana'], color='skyblue')
    plt.title('Consumo Promedio de Bebidas por Grupo de Edad')  # Título del gráfico.
    plt.xlabel('Edad')  # Etiqueta del eje X.
    plt.ylabel('Consumo Promedio de Bebidas/Semana')  # Etiqueta del eje Y.
    plt.xticks(rotation=45)  # Roto las etiquetas del eje X para mejor legibilidad.
    plt.tight_layout()  # Ajusto el diseño para que no se solapen los elementos.
    plt.show()  # Muestro el gráfico.

# Defino la función graficar_pastel para crear un gráfico de pastel.
def graficar_pastel(df):
    # Agrupo los datos por 'Sexo' y sumo el consumo total de bebidas por semana.
    consumo_total = df.groupby('Sexo')['Bebidas/Semana'].sum()
    
    # Configuro el tamaño de la figura y creo el gráfico de pastel.
    plt.figure(figsize=(8, 8))
    plt.pie(consumo_total, labels=consumo_total.index, autopct='%1.1f%%', startangle=140)
    plt.title('Consumo Total de Bebidas por Sexo')  # Título del gráfico.
    plt.axis('equal')  # Aseguro que el gráfico de pastel tenga una relación de aspecto igual.
    plt.show()  # Muestro el gráfico.

# Defino la función graficar_lineas para crear un gráfico de líneas.
def graficar_lineas(df):
    # Agrupo los datos por 'Edad' y calculo el consumo promedio de bebidas por semana.
    consumo_por_edad = df.groupby('Edad')['Bebidas/Semana'].mean().reset_index()
    
    # Configuro el tamaño de la figura y creo el gráfico de líneas.
    plt.figure(figsize=(10, 6))
    plt.plot(consumo_por_edad['Edad'], consumo_por_edad['Bebidas/Semana'], marker='o')
    plt.title('Consumo Promedio de Bebidas por Edad')  # Título del gráfico.
    plt.xlabel('Edad')  # Etiqueta del eje X.
    plt.ylabel('Consumo Promedio de Bebidas/Semana')  # Etiqueta del eje Y.
    plt.xticks(rotation=45)  # Roto las etiquetas del eje X para mejor legibilidad.
    plt.tight_layout()  # Ajusto el diseño para que no se solapen los elementos.
    plt.show()  # Muestro el gráfico.