from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import FloatType

# Crear sesión de Spark
spark = SparkSession \
    .builder \
    .appName("KafkaData") \
    .master("local[*]") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0") \
    .getOrCreate()

# Leer datos de Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "topic-temperatura,topic-humedad") \
    .option("startingOffsets", "earliest") \
    .load() \
    .selectExpr("topic", "CAST(value AS STRING) as value")

# Filtrar y transformar los datos de temperatura
df_temperature = df.filter(col("topic") == "topic-temperatura") \
    .selectExpr("CAST(value AS STRING) as temperature") \
    .withColumn("temperature", col("temperature").cast(FloatType())) \
    .repartition(1)  # Repartir los datos en 1 partición

# Filtrar y transformar los datos de humedad
df_humidity = df.filter(col("topic") == "topic-humedad") \
    .selectExpr("CAST(value AS STRING) as humidity") \
    .withColumn("humidity", col("humidity").cast(FloatType())) \
    .repartition(1)  # Repartir los datos en 1 partición

# Escribir los datos de temperatura en HDFS
temperature_query = df_temperature.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("checkpointLocation", "hdfs://localhost:9000/proyecto/checkpoint/temperature") \
    .option("path", "hdfs://localhost:9000/proyecto/temperatura") \
    .start()

# Escribir los datos de humedad en HDFS
humidity_query = df_humidity.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("checkpointLocation", "hdfs://localhost:9000/proyecto/checkpoint/humidity") \
    .option("path", "hdfs://localhost:9000/proyecto/humedad") \
    .start()

# Esperar a que se completen las consultas de streaming
temperature_query.awaitTermination()
humidity_query.awaitTermination()

