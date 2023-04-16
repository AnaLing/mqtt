from paho.mqtt.client import Client
import threading


def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    time_to_wait, topic_to_publish, message_to_publish = payload.split(':')
    time_to_wait = int(time_to_wait)
    threading.Timer(time_to_wait, publish_message, args=[topic_to_publish, message_to_publish]).start() # Temporizador

def publish_message(topic, message):
    client = Client()
    client.publish(topic, payload=message, qos=0, retain=False)
    
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
    topic = sys.argv[2]
    main(broker, topic)

