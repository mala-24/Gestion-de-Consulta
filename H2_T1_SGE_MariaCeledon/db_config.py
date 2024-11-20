from tkinter import messagebox
import mysql.connector

# Aquí defino una función para conectar a la base de datos MySQL
def conectar_bd():
    try:
        # Intento establecer la conexión con la base de datos utilizando los parámetros especificados
        conn = mysql.connector.connect(
            host="localhost",  # Especifico que el host es 'localhost'
            user="root",  # Indico que el usuario es 'root'
            password="Malu0224",  # Proporciono la contraseña para el usuario
            database="ENCUESTAS"  # Indico que la base de datos a la que quiero conectar es 'ENCUESTAS'
        )
        return conn  # Si la conexión es exitosa, devuelvo el objeto de conexión
    except mysql.connector.Error as e:
        # Si ocurre un error durante la conexión, muestro un mensaje de error usando un cuadro de diálogo
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
        return None  # Si hay un error, devuelvo None


