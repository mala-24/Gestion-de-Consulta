import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from db_config import conectar_bd
import pandas as pd

# Importo la función para generar gráficos
from Graficos import generar_grafico

# Funciones CRUD
# Defino la función para crear un nuevo registro en la base de datos
def crear_registro():
    conn = conectar_bd()  # Intento conectar a la base de datos
    if conn:  # Si la conexión es exitosa
        cursor = conn.cursor()  # Creo un cursor para ejecutar consultas
        try:
            # Escribo la consulta SQL para insertar un nuevo registro en la tabla ENCUESTA
            query = """
            INSERT INTO ENCUESTA (idEncuesta, edad, Sexo, BebidasSemana, CervezasSemana, BebidasFinSemana, BebidasDestiladasSemana, 
            VinosSemana, PerdidasControl, DiversionDependenciaAlcohol, ProblemasDigestivos, TensionAlta, DolorCabeza)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            # Recojo los valores de las entradas de la interfaz gráfica
            valores = (
                entries["ID"].get(), entries["Edad"].get(), entries["Sexo"].get(), entries["Bebidas/Semana"].get(), 
                entries["Cervezas/Semana"].get(), entries["Bebidas Fin de Semana"].get(), 
                entries["Bebidas Destiladas/Semana"].get(), entries["Vinos/Semana"].get(), 
                entries["Pérdidas de Control"].get(), entries["Diversión/Dependencia Alcohol"].get(), 
                entries["Problemas Digestivos"].get(), entries["Tensión Alta"].get(), 
                entries["Dolor de Cabeza"].get()
            )
            cursor.execute(query, valores)  # Ejecuto la consulta con los valores
            conn.commit()  # Confirmo los cambios en la base de datos
            messagebox.showinfo("Éxito", "Registro creado con éxito")  # Muestro un mensaje de éxito
            leer_registros()  # Llamo a la función para leer y mostrar los registros actualizados
        except mysql.connector.Error as e:
            # Si ocurre un error, muestro un mensaje de error
            messagebox.showerror("Error", f"No se pudo crear el registro: {e}")
        finally:
            cursor.close()  # Cierro el cursor
            conn.close()  # Cierro la conexión a la base de datos

# Defino la función para leer los registros de la base de datos
def leer_registros(filtro=None, orden=None):
    conn = conectar_bd()  # Intento conectar a la base de datos
    if conn:  # Si la conexión es exitosa
        cursor = conn.cursor()  # Creo un cursor para ejecutar consultas
        try:
            query = "SELECT * FROM ENCUESTA"  # Escribo la consulta para seleccionar todos los registros
            condiciones = []  # Inicializo una lista para las condiciones de filtro
            valores = []  # Inicializo una lista para los valores de filtro

            # Si hay un filtro, lo aplico a la consulta
            if filtro:
                for campo, valor in filtro.items():
                    condiciones.append(f"{campo} = %s")  # Agrego la condición al filtro
                    valores.append(valor)  # Agrego el valor correspondiente
                query += " WHERE " + " AND ".join(condiciones)  # Agrego las condiciones a la consulta

            # Si hay un orden, lo aplico a la consulta
            if orden:
                if orden == "ID":
                    orden = "idEncuesta"  # Cambio a nombre de columna real
                query += f" ORDER BY {orden}"  # Agrego la cláusula ORDER BY

            print("Ejecutando consulta:", query)  # Imprimo la consulta para depuración
            print("Con valores:", valores)  # Imprimo los valores para depuración

            cursor.execute(query, valores)  # Ejecuto la consulta con los valores
            registros = cursor.fetchall()  # Obtengo todos los registros
            tabla.delete(*tabla.get_children())  # Limpio la tabla de la interfaz gráfica
            for registro in registros:
                tabla.insert("", "end", values=registro)  # Agrego cada registro a la tabla
        except mysql.connector.Error as e:
            # Si ocurre un error, muestro un mensaje de error
            messagebox.showerror("Error", f"No se pudieron leer los registros: {e}")
        finally:
            cursor.close()  # Cierro el cursor
    conn.close()  # Cierro la conexión a la base de datos

            
# Defino la función para cargar los datos seleccionados en la tabla a las entradas
def cargar_datos(event):
    seleccionado = tabla.selection()  # Obtengo el elemento seleccionado en la tabla
    if seleccionado:  # Si hay un elemento seleccionado
        item = tabla.item(seleccionado)  # Obtengo los valores del elemento
        valores = item['values']  # Extraigo los valores

        for idx, field in enumerate(fields):
            entries[field].delete(0, tk.END)  # Limpio la entrada
            entries[field].insert(0, valores[idx])  # Inserto el valor correspondiente


# Defino la función para actualizar un registro existente en la base de datos
def actualizar_registro():
    conn = conectar_bd()  # Intento conectar a la base de datos
    if conn:  # Si la conexión es exitosa
        cursor = conn.cursor()  # Creo un cursor para ejecutar consultas
        try:
            # Escribo la consulta SQL para actualizar un registro en la tabla ENCUESTA
            query = """
            UPDATE ENCUESTA SET edad=%s, Sexo=%s, BebidasSemana=%s, CervezasSemana=%s, BebidasFinSemana=%s,
            BebidasDestiladasSemana=%s, VinosSemana=%s, PerdidasControl=%s, DiversionDependenciaAlcohol=%s, 
            ProblemasDigestivos=%s, TensionAlta=%s, DolorCabeza=%s WHERE idEncuesta=%s
            """
            # Recojo los valores de las entradas de la interfaz gráfica
            valores = (
                entries["Edad"].get(), entries["Sexo"].get(), entries["Bebidas/Semana"].get(), 
                entries["Cervezas/Semana"].get(), entries["Bebidas Fin de Semana"].get(), 
                entries["Bebidas Destiladas/Semana"].get(), entries["Vinos/Semana"].get(), 
                entries["Pérdidas de Control"].get(), entries["Diversión/Dependencia Alcohol"].get(), 
                entries["Problemas Digestivos"].get(), entries["Tensión Alta"].get(), 
                entries["Dolor de Cabeza"].get(), entries["ID"].get()  # Incluyo el ID para identificar el registro
            )
            cursor.execute(query, valores)  # Ejecuto la consulta con los valores
            conn.commit()  # Confirmo los cambios en la base de datos
            messagebox.showinfo("Éxito", "Registro actualizado con éxito")  # Muestro un mensaje de éxito
            leer_registros()  # Llamo a la función para leer y mostrar los registros actualizados
        except mysql.connector.Error as e:
            # Si ocurre un error, muestro un mensaje de error
            messagebox.showerror("Error", f"No se pudo actualizar el registro: {e}")
        finally:
            cursor.close()  # Cierro el cursor
            conn.close()  # Cierro la conexión a la base de datos


# Defino la función para eliminar un registro de la base de datos
def eliminar_registro():
    conn = conectar_bd()  # Intento conectar a la base de datos
    if conn:  # Si la conexión es exitosa
        cursor = conn.cursor()  # Creo un cursor para ejecutar consultas
        try:
            # Escribo la consulta SQL para eliminar un registro de la tabla ENCUESTA
            query = "DELETE FROM ENCUESTA WHERE idEncuesta=%s"
            cursor.execute(query, (entries["ID"].get(),))  # Ejecuto la consulta con el ID del registro
            conn.commit()  # Confirmo los cambios en la base de datos
            messagebox.showinfo("Éxito", "Registro eliminado con éxito")  # Muestro un mensaje de éxito
            leer_registros()  # Llamo a la función para leer y mostrar los registros actualizados
        except mysql.connector.Error as e:
            # Si ocurre un error, muestro un mensaje de error
            messagebox.showerror("Error", f"No se pudo eliminar el registro: {e}")
        finally:
            cursor.close()  # Cierro el cursor
            conn.close()  # Cierro la conexión a la base de datos


# Defino la función para aplicar filtros a los registros
def aplicar_filtros():
    filtro = {}  # Inicializo un diccionario para los filtros
    if entries_filtro["ID"].get():  # Si hay un ID en el filtro
        try:
            filtro["idEncuesta"] = int(entries_filtro["ID"].get())  # Convierto a entero
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero.")  # Muestro un mensaje de error si la conversión falla
            return  # Salgo si hay un error en la conversión
    if entries_filtro["Edad"].get():  # Si hay una edad en el filtro
        try:
            filtro["edad"] = int(entries_filtro["Edad"].get())  # Convierto a entero
        except ValueError:
            messagebox.showerror("Error", "La edad debe ser un número entero.")  # Muestro un mensaje de error si la conversión falla
            return  # Salgo si hay un error en la conversión
    if entries_filtro["Sexo"].get():  # Si hay un sexo en el filtro
        filtro["Sexo"] = entries_filtro["Sexo"].get()  # Agrego el filtro de sexo

    orden = combo_orden.get() if combo_orden.get() else None  # Obtengo el orden seleccionado
    leer_registros(filtro, orden)  # Llamo a la función para leer los registros aplicando los filtros


# Defino la función para limpiar los filtros aplicados
def limpiar_filtros():
    for field in entries_filtro:  # Recorro todos los campos de filtro
        entries_filtro[field].delete(0, tk.END)  # Limpio cada entrada
    leer_registros()  # Llamo a la función para leer y mostrar todos los registros


# Defino la función para exportar los registros a un archivo Excel
def exportar_a_excel():
    registros = []  # Inicializo una lista para los registros
    for item in tabla.get_children():  # Recorro los elementos de la tabla
        registros.append(tabla.item(item)['values'])  # Agrego los valores de cada elemento a la lista
    
    if not registros:  # Verifico si hay registros para exportar
        messagebox.showwarning("Advertencia", "No hay registros para exportar.")  # Muestro un mensaje de advertencia
        return  # Salgo si no hay registros

    df = pd.DataFrame(registros, columns=fields)  # Creo un DataFrame de pandas con los registros

    try:
        archivo = "consultas_encuesta.xlsx"  # Defino el nombre del archivo Excel
        df.to_excel(archivo, index=False)  # Exporto el DataFrame a un archivo Excel
        messagebox.showinfo("Éxito", f"Los registros han sido exportados a {archivo} con éxito.")  # Muestro un mensaje de éxito
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo exportar a Excel: {e}")  # Muestro un mensaje de error si la exportación falla


# Aquí inicio la creación de la ventana principal de la aplicación
ventana = tk.Tk()
ventana.title("Gestión de Encuestas")  # Establezco el título de la ventana
ventana.geometry("1300x600")  # Defino el tamaño de la ventana
ventana.configure(bg="#e5bffb")  # Establezco el color de fondo

# Configuro el estilo de los widgets de ttk
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#4CAF50", foreground="white")  # Estilo para botones
style.configure("TLabel", background="#bff0fb", font=("Arial", 10))  # Estilo para etiquetas
style.configure("TEntry", font=("Arial", 10))  # Estilo para entradas
style.configure("TCombobox", font=("Arial", 10))  # Estilo para comboboxes


# Creo un frame para las entradas
frame_entradas = tk.Frame(ventana, bg="#bff0fb")
frame_entradas.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # Coloco el frame en la cuadrícula

# Defino los campos de entrada
fields = ["ID", "Edad", "Sexo", "Bebidas/Semana", "Cervezas/Semana", "Bebidas Fin de Semana", 
          "Bebidas Destiladas/Semana", "Vinos/Semana", "Pérdidas de Control", "Diversión/Dependencia Alcohol", 
          "Problemas Digestivos", "Tensión Alta", "Dolor de Cabeza"]
entries = {}  # Inicializo un diccionario para las entradas


# Ajusto el diseño de las entradas en una cuadrícula
for idx, field in enumerate(fields):
    tk.Label(frame_entradas, text=f"{field}:", anchor="e", width=25).grid(row=idx // 2, column=(idx % 2) * 2, padx=5, pady=5, sticky="e") # Creo una etiqueta para cada campo
    
    if field == "Sexo":  # Si el campo es 'Sexo'
        entry = ttk.Combobox(frame_entradas, values=["Mujer", "Hombre"], state="readonly")  # Creo un combobox
        entry.grid(row=idx // 2, column=(idx % 2) * 2 + 1, padx=5, pady=5, sticky="w")  # Coloco el combobox en la cuadrícula
    elif field in ["Bebidas/Semana", "Cervezas/Semana", "Bebidas Fin de Semana", 
                   "Bebidas Destiladas/Semana", "Vinos/Semana", "Pérdidas de Control"]:  # Si el campo es un número
        entry = tk.Spinbox(frame_entradas, from_=0, to=100, width=5)  # Creo un spinbox
        entry.grid(row=idx // 2, column=(idx % 2) * 2 + 1, padx=5, pady=5, sticky="w")  # Coloco el spinbox en la cuadrícula
    elif field in ["Diversión/Dependencia Alcohol", "Problemas Digestivos", "Tensión Alta"]:  # Si el campo es un booleano
        entry = ttk.Combobox(frame_entradas, values=["Sí", "No"], state="readonly")  # Creo un combobox
        entry.grid(row=idx // 2, column=(idx % 2) * 2 + 1, padx=5, pady=5, sticky="w")  # Coloco el combobox en la cuadrícula
    elif field == "Dolor de Cabeza":  # Si el campo es 'Dolor de Cabeza'
        entry = ttk.Combobox(frame_entradas, values=["Nunca", "A veces", "A menudo", "Muy a menudo"], state="readonly")  # Creo un combobox
        entry.grid(row=idx // 2, column=(idx % 2) * 2 + 1, padx=5, pady=5, sticky="w")  # Coloco el combobox en la cuadrícula
    else:  # Para otros campos
        entry = tk.Entry(frame_entradas, width=30)  # Creo una entrada de texto
        entry.grid(row=idx // 2, column=(idx % 2) * 2 + 1, padx=5, pady=5, sticky="w")  # Coloco la entrada en la cuadrícula
    
    entries[field] = entry# Agrego la entrada al diccionario

# Creo un frame para los filtros
frame_filtros = tk.Frame(ventana, bg="#0495b5")
frame_filtros.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")  # Coloco el frame en la cuadrícula

# Defino las entradas de filtro
entries_filtro = {}
filtro_fields = ["ID", "Edad", "Sexo"]
for idx, field in enumerate(filtro_fields):
    tk.Label(frame_filtros, text=f"{field}:", anchor="e", width=25).grid(row=idx, column=0, padx=5, pady=5, sticky="e")  # Creo una etiqueta para cada campo de filtro
    entry = tk.Entry(frame_filtros, width=30)  # Creo una entrada de texto para el filtro
    entry.grid(row=idx, column=1, padx=5, pady=5, sticky="w")  # Coloco la entrada en la cuadrícula

    entries_filtro[field] = entry  # Agrego la entrada al diccionario de filtros


# ComboBox para ordenar
tk.Label(frame_filtros, text="Ordenar por:").grid(row=len(filtro_fields), column=0, padx=5, pady=5, sticky="e")  # Etiqueta para ordenar
combo_orden = ttk.Combobox(frame_filtros, values=["ID", "Edad", "Sexo"], state="readonly")  # Creo un combobox para ordenar
combo_orden.grid(row=len(filtro_fields), column=1, padx=5, pady=5, sticky="w")  # Coloco el combobox en la cuadrícula
combo_orden.set("Selecciona el filtro")  # Establezco un valor por defecto


# Botón para aplicar filtros
boton_filtros = tk.Button(frame_filtros, text="Aplicar Filtros", command=aplicar_filtros)  # Creo un botón para aplicar filtros
boton_filtros.grid(row=len(filtro_fields) + 1, column=0, columnspan=2, padx=5, pady=5)  # Coloco el botón en la cuadrícula

# Botón para limpiar filtros
boton_limpiar = tk.Button(frame_filtros, text="Limpiar Filtros", command=limpiar_filtros)  # Creo un botón para limpiar filtros
boton_limpiar.grid(row=len(filtro_fields) + 2, column=0, columnspan=2, padx=5, pady=5)  # Coloco el botón en la cuadrícula

# Botones para CRUD
frame_botones = tk.Frame(ventana, bg="#bff0fb")  # Creo un frame para los botones de CRUD
frame_botones.grid(row=1, column=0, columnspan=2, pady=10)  # Coloco el frame en la cuadrícula

boton_crear = tk.Button(frame_botones, text="Crear Consulta", command=crear_registro)  # Creo un botón para crear un registro
boton_crear.grid(row=0, column=0, padx=5, pady=5)  # Coloco el botón en la cuadrícula

boton_leer = tk.Button(frame_botones, text="Visualizar Consultas", command=leer_registros)  # Creo un botón para visualizar registros
boton_leer.grid(row=0, column=1, padx=5, pady=5)  # Coloco el botón en la cuadrícula

boton_actualizar = tk.Button(frame_botones, text="Actualizar Consulta", command=actualizar_registro)  # Creo un botón para actualizar un registro
boton_actualizar.grid(row=0, column=2, padx=5, pady=5)  # Coloco el botón en la cuadrícula

boton_eliminar = tk.Button(frame_botones, text="Eliminar Consulta", command=eliminar_registro)  # Creo un botón para eliminar un registro
boton_eliminar.grid(row=0, column=3, padx=5, pady=5)  # Coloco el botón en la cuadrícula

# Botón para exportar a Excel
boton_exportar = tk.Button(frame_botones, text="Exportar a Excel", command=exportar_a_excel)  # Creo un botón para exportar a Excel
boton_exportar.grid(row=0, column=4, padx=5, pady=5)  # Coloco el botón en la cuadrícula

# Frame para visualizar gráficos
frame_graficos = tk.Frame(ventana, bg="#8306f9")  # Creo un frame para los gráficos
frame_graficos.grid(row=2, column=0, columnspan=2, pady=10)  # Coloco el frame en la cuadrícula

tk.Label(frame_graficos, text="Seleccionar tipo de gráfico:").grid(row=0, column=0, padx=5, pady=5)  # Etiqueta para seleccionar gráfico

tipo_grafico = ttk.Combobox(frame_graficos, values=["Barras", "Pastel", "Líneas"], state="readonly")  # Creo un combobox para seleccionar tipo de gráfico
tipo_grafico.grid(row=0, column=1, padx=5, pady=5)  # Coloco el combobox en la cuadrícula
tipo_grafico.set("Selecciona el tipo de gráfico")  # Establezco un valor por defecto

boton_grafico = tk.Button(frame_graficos, text="Generar Gráfico", command=lambda: generar_grafico(tabla, fields, tipo_grafico.get()))  # Creo un botón para generar gráficos
boton_grafico.grid(row=0, column=2, padx=5, pady=5)  # Coloco el botón en la cuadrícula


# Tabla para mostrar datos
tabla = ttk.Treeview(ventana, columns=fields, show="headings", height=10)  # Creo una tabla para mostrar los datos
tabla.grid(row=3, column=0, columnspan=2, pady=10)  # Coloco la tabla en la cuadrícula
tabla.bind("<ButtonRelease-1>", cargar_datos)  # Asocio la función cargar_datos al evento de selección

# Configurar encabezados de la tabla
for field in fields:# Recorro los campos
    tabla.heading(field, text=field)# Establezco el encabezado de cada columna
    tabla.column(field, width=100) # Defino el ancho de cada columna

ventana.mainloop()# Inicio el bucle principal de la aplicación