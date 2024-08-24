from pyspark.sql import SparkSession
import os

# Crear sesión de Spark
spark = SparkSession \
    .builder \
    .appName("LeerParquetLocalHDFS") \
    .master("local[*]") \
    .getOrCreate()

# Leer los archivos Parquet desde HDFS local
df_humedad = spark.read.parquet("hdfs://localhost:9000/proyecto/humedad/")
df_temperatura = spark.read.parquet("hdfs://localhost:9000/proyecto/temperatura/")

# Mostrar los datos de Humedad
print("Datos de Humedad:")
df_humedad.show(truncate=False)

# Mostrar los datos de Temperatura
print("Datos de Temperatura:")
df_temperatura.show(truncate=False)

# Ruta para guardar los datos en archivos CSV
output_dir = "output_data"

# Crear la carpeta si no existe
os.makedirs(output_dir, exist_ok=True)

# Guardar los datos en archivos CSV en la carpeta local
df_humedad.write.csv(os.path.join(output_dir, "humedad_data.csv"), header=True, mode="overwrite")
df_temperatura.write.csv(os.path.join(output_dir, "temperatura_data.csv"), header=True, mode="overwrite")

# Parar la sesión de Spark
spark.stop()

