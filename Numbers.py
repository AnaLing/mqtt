from paho.mqtt.client import Client


def on_message(client, userdata, msg):
    number = float(msg.payload)
    print("Received number:", number)

    # Separar enteros y reales
    if number.is_integer():
        print("Entero:", int(number))
    else:
        print("Real:", number)


    # Estudiar propiedades del número entero
    if number.is_integer():
        if number < 2:
            print("No es primo")
        else:
            is_prime = True
            for divisor in range(2, int(number/2) + 1):
                if number % divisor == 0:
                    is_prime = False
                    break
            if is_prime:
                print("Es primo")
            else:
                print("No es primo")

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
    topic = "numbers"
    main(broker, topic)