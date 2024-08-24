import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pyspark.sql import SparkSession

# Crear sesión de Spark
spark = SparkSession \
    .builder \
    .appName("DataVisualization") \
    .master("local[*]") \
    .getOrCreate()

# Inicializar la figura y los ejes para el gráfico
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

# Configuración de estilo
plt.style.use('ggplot')  # Usar estilo ggplot predefinido

# Función para actualizar el gráfico
def animate(i):
    # Leer datos desde HDFS
    pdf_temperature = spark.read.parquet("hdfs://localhost:9000/proyecto/temperatura").toPandas()
    pdf_humidity = spark.read.parquet("hdfs://localhost:9000/proyecto/humedad").toPandas()
    
    # Limpiar los ejes
    ax1.clear()
    ax2.clear()
    
    # Graficar temperatura
    if not pdf_temperature.empty:
        ax1.plot(pdf_temperature.index, pdf_temperature['temperature'], color='red', linewidth=2)
        ax1.set_title('Datos de Temperatura', fontsize=14)
        ax1.set_xlabel('Tiempo', fontsize=12)
        ax1.set_ylabel('Temperatura (°C)', fontsize=12)
        ax1.legend(['Temperatura'], loc='upper left', fontsize=12)
    
    # Graficar humedad
    if not pdf_humidity.empty:
        ax2.plot(pdf_humidity.index, pdf_humidity['humidity'], color='blue', linewidth=2)
        ax2.set_title('Datos de Humedad', fontsize=14)
        ax2.set_xlabel('Tiempo', fontsize=12)
        ax2.set_ylabel('Humedad (%)', fontsize=12)
        ax2.legend(['Humedad'], loc='upper left', fontsize=12)

# Configurar la animación
ani = animation.FuncAnimation(fig, animate, interval=3000, blit=False)

# Ajustar el diseño para que las subgráficas no se superpongan
plt.tight_layout()

# Mostrar el gráfico con interactividad habilitada
plt.show()

