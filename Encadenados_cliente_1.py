from paho.mqtt.client import Client
import time
import math

# El primer cliente se subscribe a "numbers". Si recibe un primo, pone una alarma en "alarm"
# Función que verifica si un número es primo
def es_primo(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def on_message(client, userdata, message):
    number = int(message.payload.decode())
    if es_primo(number):
        # Publicación de mensaje en el topic "alarm"
        client.publish("alarm", "on")
        print("Alarma activada")
        
        
def main(broker, topic):
    client = Client()
    client.on_message = on_message

    print(f'Connecting on channels {topic} on {broker}')
    client.connect(broker)

    client.subscribe(topic)

    client.on_message = on_message

    client.loop_start()

    while True:
      time.sleep(1)
    
    
if __name__ == "__main__":
    import sys
    if len(sys.argv)<3:
        print(f"Usage: {sys.argv[0]} broker topic")
    broker = sys.argv[1]
    topic = "numbers"
    main(broker, topic)

