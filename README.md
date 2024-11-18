# Gestion de Consulta
Este proyecto es una aplicación de escritorio para la gestión de encuestas utilizando Python, Tkinter y MySQL. 
Permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre los registros de encuestas y visualizar gráficos

# 🎬Preview
![]

# 💻Usage


1. Instalar Paquetes de Python: Abre la terminal o el símbolo del sistema y ejecuta los siguientes comandos:

	```
   pip install mysql-connector-python pandas openpyxl
	```

   **Conectar la Aplicación con MySQL**
   
   Crea una base de datos llamada encuestas:
   ```
     CREATE DATABASE encuestas;
     USE encuestas;

      CREATE TABLE ENCUESTA (
          idEncuesta INT AUTO_INCREMENT PRIMARY KEY,
          edad INT,
          Sexo VARCHAR(10),
          BebidasSemana INT,
          CervezasSemana INT,
          BebidasFinSemana INT,
          BebidasDestiladasSemana INT,
          VinosSemana INT,
          PerdidasControl VARCHAR(3),
          DiversionDependenciaAlcohol VARCHAR(3),
          ProblemasDigestivos VARCHAR(3),
          TensionAlta VARCHAR(3),
          DolorCabeza VARCHAR(20)
      );
    ```
