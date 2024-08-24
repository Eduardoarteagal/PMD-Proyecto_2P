from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import FloatType
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd

# Crear sesión de Spark
spark = SparkSession \
    .builder \
    .appName("KafkaData") \
    .master("local[*]") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0") \
    .getOrCreate()

# Definir el esquema de datos
schema = "value STRING"

# Leer datos de Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "topic-temperatura,topic-humedad") \
    .option("startingOffsets", "earliest") \
    .load() \
    .selectExpr("topic", "CAST(value AS STRING) as value")

# Filtrar y transformar los datos
df_temperature = df.filter(col("topic") == "topic-temperatura") \
    .selectExpr("CAST(value AS STRING) as temperature") \
    .withColumn("temperature", col("temperature").cast(FloatType()))

df_humidity = df.filter(col("topic") == "topic-humedad") \
    .selectExpr("CAST(value AS STRING) as humidity") \
    .withColumn("humidity", col("humidity").cast(FloatType()))

# Crear un DataFrame para la visualización
query_temperature = df_temperature.writeStream \
    .outputMode("append") \
    .format("memory") \
    .queryName("temperature") \
    .start()

query_humidity = df_humidity.writeStream \
    .outputMode("append") \
    .format("memory") \
    .queryName("humidity") \
    .start()

# Inicializar la figura para el gráfico
fig, ax = plt.subplots()

# Función para actualizar el gráfico
def animate(i):
    # Convertir los DataFrames de Spark a Pandas para graficar
    pdf_temperature = spark.sql("SELECT * FROM temperature").toPandas()
    pdf_humidity = spark.sql("SELECT * FROM humidity").toPandas()
    
    # Limpiar el gráfico
    ax.clear()
    
    # Graficar temperatura y humedad
    if not pdf_temperature.empty:
        ax.plot(pdf_temperature.index, pdf_temperature['temperature'], label='Temperatura', color='red')
    if not pdf_humidity.empty:
        ax.plot(pdf_humidity.index, pdf_humidity['humidity'], label='Humedad', color='blue')
    
    # Añadir leyenda
    ax.legend(loc='upper left')
    
    # Títulos y etiquetas
    ax.set_title('Datos de Temperatura y Humedad')
    ax.set_xlabel('Tiempo')
    ax.set_ylabel('Medida')

# Configurar la animación
ani = animation.FuncAnimation(fig, animate, interval=3000)

# Mostrar el gráfico
plt.show()

# Esperar a que se completen las consultas de streaming
query_temperature.awaitTermination()
query_humidity.awaitTermination()

