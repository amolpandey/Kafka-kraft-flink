from confluent_kafka import Producer
import socket


def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))

if __name__ == "__main__":
    conf = {'bootstrap.servers': 'localhost:9096',
            'client.id': socket.gethostname()}

    print(socket.gethostname())
    producer = Producer(conf)
    print('---------')
    print(type(producer))

    # producer.produce('demo-topic', key="Name", value="Amol Pandey", callback=acked)

    # producer.produce('demo-topic', key="Name", value="Amol Pandey")
    producer.produce('sample-2', key="Name", value="Amol Pandey V1")

    producer.flush()
    # Wait up to 1 second for events. Callbacks will be invoked during
    # this method call if the message is acknowledged.
    # producer.poll(5)

    print('Process completed.')