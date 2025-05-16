# Aquí voy a explicar las dificultades y pasos clave a seguir al realizar el proyecto.


## Script 
· Para la realización del script me he apoyado en la documentación oficial de Microsoft ->[Microsoft Learn Datalake Service Client](https://learn.microsoft.com/en-us/python/api/overview/azure/storage-file-datalake-readme?view=azure-python).
## Dar acceso a mi app para interactuar con el DataLake

1. Accede al [portal de Azure](https://portal.azure.com/).
2. Navega al **Storage Account** deseado.
3. En el menú lateral, selecciona **Control de acceso (IAM)**.
4. Haz clic en **Agregar** > **Agregar asignación de rol**.
5. Elige el rol adecuado (por ejemplo, *Storage Blob Data Contributor*).
6. En **Asignar acceso a**, selecciona **Usuario, grupo o entidad de servicio**.
7. Busca y selecciona la **App Registration** correspondiente.
8. Haz clic en **Revisar y asignar** para finalizar.

Esto otorga a la App Registration los permisos necesarios sobre el Storage Account.

# Trabajar con Databricks
He decidido trabajar con Databricks, desde mi repositorio, para esto desde añado la carpeta git 
a databricks, pudiendo trabajar desde la UI de Databricks en mi repo.
![alt text](img/image.png)
## Permisos en DataBricks
### Para manejar el acceso de Databricks al DataLake he seguido los siguientes pasos:

1. Crear un service principal
2. Añadir al grupo de acceso a DataLake con rol de Storage Blob Data Contributor
3. Crear secreto en key vault
4. Añadir a un secret-scope de databricks el secreto.
5. Conectar desde el nootebook usando el método de conexión de service-principal 
![alt text](img/image-sp-con.png)