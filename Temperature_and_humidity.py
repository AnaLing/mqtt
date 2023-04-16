from paho.mqtt.client import Client

# Constantes de temperatura y humedad límite
K0 = 20
K1 = 50


def on_message(client, userdata, message):
    if message.topic == "temperature/temp1":
        # Obtenemos el valor de temperatura del mensaje y lo convertimos a float
        temperatura = float(message.payload.decode())
        if temperatura > K0:
            # Si la temperatura supera K0, nos suscribimos al topic de humedad
            client.subscribe("humidity/temp1")
        else:
            # Si la temperatura vuelve a bajar de K0, dejamos de suscribirnos al topic de humedad y mostramos un mensaje
            client.unsubscribe("humidity/temp1")
            print("Dejando de escuchar topic humidity")

    elif message.topic == "humidity/temp1":
        # Obtenemos el valor de humedad del mensaje y lo convertimos a float
        humedad = float(message.payload.decode())
        if humedad > K1:
            # Si la humedad supera K1, dejamos de suscribirnos al topic de humedad y mostramos un mensaje
            client.unsubscribe("humidity/temp1")
            print("Dejando de escuchar topic humidity")


def main(broker, topic):
    client = Client()
    client.on_message = on_message

    print(f'Connecting on channels {topic} on {broker}')
    client.connect(broker)

    client.subscribe(topic)

    client.loop_forever()

if __name__ == "__main__":
    import sys
    if len(sys.argv)<3:
        print(f"Usage: {sys.argv[0]} broker topic")
    broker = sys.argv[1]
    topic = "temperature/temp1" # Elegimos este termometro
    main(broker, topic)
