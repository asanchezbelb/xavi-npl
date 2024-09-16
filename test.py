# import snowflake.snowpark as snowpark
# def main(session: snowpark.Session):
#     # Configura el warehouse
#     session.sql("USE WAREHOUSE WH_MOD_DDP_DOCENCIA").collect()
    
#     # Define la consulta SQL
#     sql_query = """
#     SELECT 
#         * 
#     FROM 
#         DB_UOC_PROD.DDP_DOCENCIA.STAGE_ENQUESTES 
#     WHERE ENQUESTA_ID IN (668, 670)
#     AND TIPUS_PREGUNTA = 'PREGUNTA_OBERTA'
#     LIMIT 10;
#     """
    
#     # Ejecuta la consulta
#     df = session.sql(sql_query)
    
#     try:
#         # Recoge los resultados
#         result = df.collect()
#         for row in result:
#             # Limpia y muestra cada fila
#             clean_row = str(row).encode('ascii', errors='ignore').decode('ascii')
#             print(clean_row)
#     except UnicodeEncodeError as e:
#         print(f"Error de codificación: {e}")
#     except Exception as e:
#         print(f"Error inesperado: {e}")
    
#     return df



from snowflake.snowpark import Session
from snowflake.snowpark.exceptions import SnowparkGeneralException
import pandas as pd

# # Configura las credenciales de Snowflake
# snowflake_user = 'enietoo@uoc.edu'
# snowflake_password = 'xxxxxxx'
# snowflake_account = 'uocbi.eu-west-1'
# snowflake_warehouse = 'WH_DD_DMELINC'
# snowflake_role = 'R_DD_DMELINC'
# snowflake_database = 'DB_UOC_PROD'
# snowflake_schema = 'DD_DMELINC'
# snowflake_table = 'TU_TABLA'

# # Crea una sesión Snowpark
# session = {
#     "account": "uocbi.eu-west-1",
#     "user": "enietoo@uoc.edu",
#     "role": "R_DDP_LMS_TRAN_ELINC",  # optional
#     "warehouse": "WH_DDP_LMS_TRAN_ELINC",  # optional
#     "database": "DB_UOC_PROD",  # optional
#     "schema": "DDP_LMS_TRAN_ELINC",
#     "authenticator":"externalbrowser"}

# df = pd.DataFrame()
# #try:
# session_DataPortal = Session.builder.configs(session).create()

# print(session_DataPortal.get_current_database())
# print(session_DataPortal.get_current_schema())
# print(session_DataPortal.SessionBuilder)

# Configura las credenciales de Snowflake
# snowflake_user = 'enietoo@uoc.edu'
# snowflake_password = 'xxxxxxx'
# snowflake_account = 'uocbi.eu-west-1'
# snowflake_warehouse = 'WH_DD_DMELINC'
# snowflake_role = 'R_DD_DMELINC'
# snowflake_database = 'DB_UOC_PROD'
# snowflake_schema = 'DD_DMELINC'
# snowflake_table = 'TU_TABLA'

# # Crea una sesión Snowpark
# session = {
#     "account": "uocbi.eu-west-1",
#     "user": "asanchezbelb@uoc.edu",
#     "role": "R_DDP_DOCENCIA",  # optional
#     "warehouse": "WH_DDP_LMS_TRAN_ELINC",  # optional
#     "database": "DB_UOC_PROD",  # optional
#     "schema": "DDP_LMS_TRAN_ELINC",
#     "authenticator":"externalbrowser"}

# df = pd.DataFrame()
# #try:
# session_DataPortal = Session.builder.configs(session).create()

# print(session_DataPortal.get_current_database())
# print(session_DataPortal.get_current_schema())
# print(session_DataPortal.SessionBuilder)


import snowflake.snowpark as snowpark
import csv
import os

# Credenciales de Snowflake
snowflake_user = 'asanchezbelb@uoc.edu'
snowflake_password = 'xxxxxxx'
snowflake_account = 'uocbi.eu-west-1'
snowflake_warehouse = 'WH_MOD_DDP_DOCENCIA'
snowflake_role = 'R_DDP_DOCENCIA'
snowflake_database = 'DB_UOC_PROD'
snowflake_schema = 'DDP_DOCENCIA'
snowflake_table = 'STAGE_ENQUESTES'

# Configuración de sesión Snowflake
session_params = {
    "account": snowflake_account,
    "user": snowflake_user,
    "role": snowflake_role,  # Especifica el rol
    "warehouse": snowflake_warehouse,  # Especifica el warehouse
    "database": snowflake_database,  # Especifica el database
    "schema": snowflake_schema,  # Especifica el schema
    "authenticator": "externalbrowser"  # Usa autenticación de navegador
}

# Función principal para iniciar la sesión y realizar una consulta
def main():
    try:
        # Crear sesión en Snowflake usando Snowpark
        session = snowpark.Session.builder.configs(session_params).create()

        # Imprimir información de la sesión
        print("Base de datos actual:", session.get_current_database())
        print("Esquema actual:", session.get_current_schema())
        
        # Ejecutar una consulta SQL
        sql_query = ''' SELECT * 
        FROM 
            DB_UOC_PROD.DDP_DOCENCIA.STAGE_ENQUESTES 
        WHERE ENQUESTA_ID IN (668, 670)
        AND TIPUS_PREGUNTA = 'PREGUNTA_OBERTA'
        ;
        '''
        
        # Realizar la consulta y obtener los resultados
        df = session.sql(sql_query)
        result = df.collect()  # Recoge los resultados como una lista
        
        # Crear la carpeta 'data' si no existe
        os.makedirs('data', exist_ok=True)
        # Guardar los resultados en un archivo CSV
        with open('data/resultados_enquestes.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Escribir los nombres de las columnas
            writer.writerow([col.name for col in df.schema.fields])
            
            # Escribir cada fila en el archivo CSV
            for row in result:
                writer.writerow(row)

        print("Datos guardados en 'data/resultados_enquestes.csv'")
    
    except Exception as e:
        print(f"Error en la ejecución: {e}")
    
    finally:
        # Cerrar la sesión
        if session:
            session.close()

# Ejecutar la función principal
if __name__ == "__main__":
    main()


