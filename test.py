


import snowflake.snowpark as snowpark
import csv
import os
from dotenv import load_dotenv

load_dotenv()

# Credenciales de Snowflake
snowflake_user = os.getenv('SNOWFLAKE_USER')
snowflake_password = os.getenv('SNOWFLAKE_PASSWORD')
snowflake_account = os.getenv('SNOWFLAKE_ACCOUNT')
snowflake_warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
snowflake_role = os.getenv('SNOWFLAKE_ROLE')
snowflake_database = os.getenv('SNOWFLAKE_DATABASE')
snowflake_schema = os.getenv('SNOWFLAKE_SCHEMA')
snowflake_table = os.getenv('SNOWFLAKE_TABLE')

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


