from confluent_kafka import Producer
import random
import time

# Configuración del productor de Kafka
conf = {
    'bootstrap.servers': 'localhost:9092',
}

producer = Producer(conf)

# Función para simular datos de sensores
def generate_sensor_data():
    return {
        'temperature': round(random.uniform(15.0, 30.0), 2),
        'humidity': round(random.uniform(30.0, 70.0), 2)
    }

# Función de callback para confirmar el envío
def delivery_report(err, msg):
    if err is not None:
        print(f'Error al enviar mensaje: {err}')
    else:
        print(f'Mensaje enviado a {msg.topic()} [{msg.partition()}]')

# Envío de datos simulados a Kafka
def send_sensor_data(topic_temp, topic_humid):
    while True:
        data = generate_sensor_data()
        
        # Enviar solo la temperatura al tópico de temperatura
        temperature_data = f'{data["temperature"]}'
        print(f'Enviando temperatura: {temperature_data}')
        producer.produce(topic_temp, key='temperature_data', value=temperature_data, callback=delivery_report)
        
        # Enviar solo la humedad al tópico de humedad
        humidity_data = f'{data["humidity"]}'
        print(f'Enviando humedad: {humidity_data}')
        producer.produce(topic_humid, key='humidity_data', value=humidity_data, callback=delivery_report)
        
        producer.flush()
        time.sleep(1)

if __name__ == '__main__':
    topic_temperature = 'topic-temperatura'
    topic_humidity = 'topic-humedad'
    send_sensor_data(topic_temperature, topic_humidity)

