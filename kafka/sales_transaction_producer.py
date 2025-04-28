import json
import random
import time

from faker import Faker
from confluent_kafka import Producer #SerializingProducer
import socket, uuid
from datetime import datetime

fake = Faker()

def generate_sales_transactions():
    user = fake.simple_profile()

    return {
        "transactionId": fake.uuid4(),
        "productId": random.choice(['product1', 'product2', 'product3', 'product4', 'product5', 'product6']),
        "productName": random.choice(['laptop', 'mobile', 'tablet', 'watch', 'headphone', 'speaker']),
        'productCategory': random.choice(['electronic', 'fashion', 'grocery', 'home', 'beauty', 'sports']),
        'productPrice': round(random.uniform(10, 1000), 2),
        'productQuantity': random.randint(1, 10),
        'productBrand': random.choice(['apple', 'samsung', 'oneplus', 'mi', 'boat', 'sony']),
        'currency': random.choice(['GBP', 'AUD']),
        'customerId': user['username'],
        'transactionDate': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
        "paymentMethod": random.choice(['credit_card', 'debit_card', 'online_transfer'])
    }

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg.key())))
        

def main():
    topic = 'financial_transactions'

    conf = {'bootstrap.servers': 'localhost:9094',
                'client.id': socket.gethostname()}
    producer= Producer(conf)
    curr_time = datetime.now()

    while (datetime.now() - curr_time).seconds < 120:
        try:
            transaction = generate_sales_transactions()
            transaction['totalAmount'] = round(transaction['productPrice'] * transaction['productQuantity'], 2)
            hdrs = [('headerkey', str(uuid.uuid4()))]
            print(transaction)
            producer.produce(topic,
                                key=transaction['transactionId'],
                                value=json.dumps(transaction),
                                callback=acked,
                                headers = hdrs
                                # vpartition =  5
                                )
            #  producer.poll(1)
            producer.flush()

            #wait for 5 seconds before sending the next transaction
            time.sleep(3)
        except BufferError:
            print("Buffer full! Waiting...")
            time.sleep(1)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()