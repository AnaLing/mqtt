from paho.mqtt.client import Client
import time


def on_message(client, userdata, message):
    # Decodificar el mensaje y extraer el valor
    value = float(message.payload.decode())
    # Obtener el subtopic del mensaje
    subtopic = message.topic.split("/")[-1]
    # Actualizar los valores para el sensor correspondiente
    global data
    if subtopic not in data:
        data[subtopic] = {"max": value, "min": value, "total": value, "count": 1}
    else:
        if value > data[subtopic]["max"]:
            data[subtopic]["max"] = value
        if value < data[subtopic]["min"]:
            data[subtopic]["min"] = value
        data[subtopic]["total"] += value
        data[subtopic]["count"] += 1
    # Actualizar los valores globales
    global total_data
    if subtopic not in total_data:
        total_data[subtopic] = {"max": value, "min": value, "total": value, "count": 1}
    else:
        if value > total_data[subtopic]["max"]:
            total_data[subtopic]["max"] = value
        if value < total_data[subtopic]["min"]:
            total_data[subtopic]["min"] = value
        total_data[subtopic]["total"] += value
        total_data[subtopic]["count"] += 1

def main(broker, topic):
    client = Client()
    client.on_message = on_message

    print(f'Connecting on channels {topic} on {broker}')
    client.connect(broker)

    client.subscribe(topic)

    # Variables para almacenar los datos
    data = {}
    total_data = {}

    while True:
      client.loop_start()
      time.sleep(4)  # Tiempo de intervalo
      client.loop_stop()

      print("Valores por sensor:")
      for subtopic in data:
        avg = data[subtopic]["total"] / data[subtopic]["count"]
        print(f"{subtopic:10} - Min: {data[subtopic]['min']:.2f} | Max: {data[subtopic]['max']:.2f} | Avg: {avg:.2f}")
      print("Valores globales:")
      for subtopic in total_data:
        avg = total_data[subtopic]["total"] / total_data[subtopic]["count"]
        print(f"{subtopic:10} - Min: {total_data[subtopic]['min']:.2f} | Max: {total_data[subtopic]['max']:.2f} | Avg: {avg:.2f}")

    # Reiniciar los valores
      data = {}
      total_data = {}
 

if __name__ == "__main__":
    import sys
    if len(sys.argv)<3:
        print(f"Usage: {sys.argv[0]} broker topic")
    broker = sys.argv[1]
    topics = "temperature/#"
    main(broker, topics)