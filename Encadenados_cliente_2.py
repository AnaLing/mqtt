from paho.mqtt.client import Client
import time

# El segundo cliente, si está la alarma puesta, se subscribe a "humidity" y calcula la media


# Variables para el cálculo del valor medio
humidity_values = []
total_humidity = 0
num_humidity_values = 0


def on_message(client, userdata, message):
    if message.topic == "alarm" and message.payload.decode() == "on":
        # Inicio del temporizador
        print("Temporizador iniciado")
        time.sleep(3)
      
        # Cálculo del valor medio de la humedad
        media = total_humidity / num_humidity_values
      
        # Publicación del valor medio en el topic "result"
        client.publish("result", str(media))
        print("Valor medio de humedad calculado y enviado:", media)

# Función que se ejecuta al recibir un mensaje en el topic "humidity"
def on_humidity(client, userdata, message):
    global total_humidity, num_humidity_values
    humidity = float(message.payload.decode())
    total_humidity += humidity
    num_humidity_values += 1
    
def main(broker, topic):
    client = Client()
    client.on_message = on_message

    print(f'Connecting on channels {topic} on {broker}')
    client.connect(broker)

    client.subscribe(topic)
        
    client.subscribe("humidity")
    client.message_callback_add("humidity", on_humidity)

    client.on_message = on_message
    
    client.loop_forever()

if __name__ == "__main__":
    import sys
    if len(sys.argv)<3:
        print(f"Usage: {sys.argv[0]} broker topic")
    broker = sys.argv[1]
    topic = "alarm"
    main(broker, topic)
